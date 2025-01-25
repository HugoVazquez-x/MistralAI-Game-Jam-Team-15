using System;
using System.Collections;
using System.IO;
using System.Text;
using System.Text.Json;
using Unity.VisualScripting.Antlr3.Runtime;
using UnityEngine;
using UnityEngine.Networking;

public class CustomClientStartRequest
{
    public string candidate_1_name { get; set; }
    public string candidate_2_name { get; set; }
}

public class CustomClientChatRequest
{
    public string previous_character_text { get; set; }

    public string previous_speaker { get; set; } // "trump" | "kamala" | "player"
    public string current_speaker { get; set; } // "trump" | "kamala"
}

public class CustomClientChatRawResponse
{
    public string generated_text { get; set; }
    public string audio { get; set; }

    public float anger { get; set; } // 0 - 1
}

public class CustomClientChatResponse : CustomClientChatRawResponse
{
    public AudioClip audioClip { get; set; }
}

public class CustomClientPlayerCardRequest
{
    public string previous_character_text { get; set; }
    public string previous_speaker { get; set; } // "trump" | "kamala" | "player"
    public int card_id { get; set; }
}

public class CustomClientPlayerCardResponseRaw
{
    public string presenter_question { get; set; }
    public string audio { get; set; } // "trump" | "kamala" | "player"
}

public class CustomClientPlayerCardResponse : CustomClientPlayerCardResponseRaw
{
    public AudioClip audioClip { get; set; }
}

public class CustomClientCardsResponse
{
    public DebateCardData[] cards { get; set; }
}

public class CustomClient
{
    public static int requestCount = 0;

    private IEnumerator GetApiCall(string endpoint, Action<string> successCallback)
    {
        using (
            UnityWebRequest www = UnityWebRequest.Get(GameManager.singleton.customApiUrl + endpoint)
        )
        {
            yield return www.SendWebRequest();

            Debug.Log("GET RESPONSE: " + www.downloadHandler.text);

            if (www.result != UnityWebRequest.Result.Success)
            {
                GameManager.singleton.HandleError(www.error + "\n(GET " + endpoint + ")");
            }
            else
            {
                string response = www.downloadHandler.text;
                successCallback(response);
            }
        }
    }

    private IEnumerator PostApiCall(string endpoint, string body, Action<string> successCallback)
    {
        using (
            UnityWebRequest www = UnityWebRequest.Post(
                GameManager.singleton.customApiUrl + endpoint,
                body,
                "application/json"
            )
        )
        {
            yield return www.SendWebRequest();
            requestCount++;

            if (www.result != UnityWebRequest.Result.Success)
            {
                GameManager.singleton.HandleError(www.error + "\n(POST " + endpoint + ")");
            }
            else
            {
                string response = www.downloadHandler.text;
                successCallback(response);
            }
        }
    }

    public IEnumerator Start(string candidate_1_name, string candidate_2_name)
    {
        string body = JsonSerializer.Serialize(
            new CustomClientStartRequest
            {
                candidate_1_name = candidate_1_name,
                candidate_2_name = candidate_2_name,
            }
        );

        Debug.Log("CustomClient body: " + body);

        yield return PostApiCall("/start", body, (string res) => { });
    }

    public IEnumerator Chat(
        string previous_character_text,
        string character,
        string previous_speaker,
        Action<CustomClientChatResponse> successCallback
    )
    {
        string body = JsonSerializer.Serialize(
            new CustomClientChatRequest
            {
                previous_character_text = previous_character_text,
                previous_speaker = previous_speaker,
                current_speaker = character,
            }
        );

        Debug.Log("CustomClient body: " + body);

        CustomClientChatRawResponse response = null;

        yield return PostApiCall(
            "/infer",
            body,
            (string res) =>
            {
                response = JsonSerializer.Deserialize<CustomClientChatRawResponse>(res);
            }
        );

        Debug.Log("CustomClient response: " + response.generated_text + " " + response.audio);

        yield return PostProcessAudio(
            response.audio,
            character,
            (AudioClip clip) =>
            {
                successCallback(
                    new CustomClientChatResponse
                    {
                        generated_text = response.generated_text,
                        audio = response.audio,
                        anger = response.anger,
                        audioClip = clip,
                    }
                );
            }
        );
    }

    public IEnumerator GetDebateCards(Action<DebateCardData[]> successCallback)
    {
        yield return GetApiCall(
            "/cards_request",
            (string res) =>
            {
                // string rr = "{\"cards\":" + res.Replace("\\", "") + "}";
                DebateCardData[] cards = JsonSerializer.Deserialize<DebateCardData[]>(res);
                successCallback(cards);
            }
        );
    }

    public IEnumerator PlayerPlayCard(
        CustomClientPlayerCardRequest request,
        Action<CustomClientPlayerCardResponse> successCallback
    )
    {
        CustomClientPlayerCardResponseRaw res = null;
        yield return PostApiCall(
            "/card-voice",
            JsonSerializer.Serialize(request),
            (string r) =>
            {
                res = JsonSerializer.Deserialize<CustomClientPlayerCardResponseRaw>(r);
            }
        );

        yield return PostProcessAudio(
            res.audio,
            res.presenter_question,
            (AudioClip clip) =>
            {
                successCallback(
                    new CustomClientPlayerCardResponse
                    {
                        presenter_question = res.presenter_question,
                        audio = res.audio,
                        audioClip = clip,
                    }
                );
            }
        );
    }

    IEnumerator PostProcessAudio(
        string audioString,
        string character,
        Action<AudioClip> successCallback
    )
    {
        var audioBytes = Convert.FromBase64String(audioString);

        string fileName = character + "_" + requestCount + ".mp3";

        string filePath = Path.Join(Application.persistentDataPath, fileName);
        Debug.Log("CustomClient audioBytes: " + audioBytes.Length + " path " + filePath);

        File.WriteAllBytes(filePath, audioBytes);

        var uri = new Uri(filePath);

        UnityWebRequest request = UnityWebRequestMultimedia.GetAudioClip(
            uri.AbsoluteUri,
            AudioType.MPEG
        );

        yield return request.SendWebRequest();
        if (request.result.Equals(UnityWebRequest.Result.ConnectionError))
            GameManager.singleton.HandleError(request.error + "\n(getting the file " + uri + ")");
        else
        {
            AudioClip clip = DownloadHandlerAudioClip.GetContent(request);
            successCallback(clip);
        }
    }
}

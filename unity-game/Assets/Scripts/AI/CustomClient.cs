using System;
using System.Collections;
using System.IO;
using System.Text.Json;
using UnityEngine;
using UnityEngine.Networking;

public class CustomClient
{
    public static int requestCount = 0;

    private IEnumerator GetApiCall(string endpoint, Action<string> successCallback)
    {
        using (
            UnityWebRequest www = UnityWebRequest.Get(GameManager.singleton.customApiUrl + endpoint)
        )
        {
            // www.SetRequestHeader("game-id", GameManager.singleton.gameId);
            yield return www.SendWebRequest();
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
            // www.SetRequestHeader("game-id", GameManager.singleton.gameId);
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

        yield return PostApiCall(
            "/start",
            body,
            (string res) =>
            {
                Debug.Log("Started game succesfully!");
            }
        );
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

        CustomClientChatRawResponse response = null;

        yield return PostApiCall(
            "/infer",
            body,
            (string res) =>
            {
                response = JsonSerializer.Deserialize<CustomClientChatRawResponse>(res);
            }
        );

        yield return Helpers.PostProcessAudio(
            response.audio,
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

        yield return Helpers.PostProcessAudio(
            res.audio,
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
}

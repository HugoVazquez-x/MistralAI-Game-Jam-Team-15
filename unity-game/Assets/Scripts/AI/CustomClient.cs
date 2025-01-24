using System;
using System.Collections;
using System.Text;
using System.Text.Json;
using UnityEngine;
using UnityEngine.Networking;

public class CustomClientRequest
{
    public string previous_character_text { get; set; }
    public string previous_speaker { get; set; }
    public string current_speaker { get; set; }
}

public class CustomClientResponse
{
    public string generated_text { get; set; }
}

public class CustomClient
{
    string apiUrl = "http://192.168.80.211:8000";

    private IEnumerator GetApiCall(string endpoint, Action<string> successCallback)
    {
        using (UnityWebRequest www = UnityWebRequest.Get(apiUrl + endpoint))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
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
            UnityWebRequest www = UnityWebRequest.Post(apiUrl + endpoint, body, "application/json")
        )
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                string response = www.downloadHandler.text;
                successCallback(response);
            }
        }
    }

    public IEnumerator Chat(
        string previous_character_text,
        string character,
        string previous_speaker,
        Action<string> successCallback
    )
    {
        string body = JsonSerializer.Serialize(
            new CustomClientRequest
            {
                previous_character_text = previous_character_text,
                previous_speaker = previous_speaker,
                current_speaker = character,
            }
        );

        Debug.Log("CustomClient body: " + body);

        yield return PostApiCall("/chat", body, successCallback);
    }

    public IEnumerator GetDebateCards(Action<string> successCallback)
    {
        yield return GetApiCall("/debate-cards", successCallback);
    }
}

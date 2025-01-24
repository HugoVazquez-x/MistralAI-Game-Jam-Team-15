using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.Json;
using UnityEngine;
using UnityEngine.Networking;

public interface APIClient<Request, Response>
{
    public string apiUrl { get; }

    // public IEnumerator CompleteChat(Request request, Action<Response> successCallback);
    // {


    //     string body = JsonSerializer.Serialize<Request>(request);

    //     using (
    //         UnityWebRequest www = UnityWebRequest.Post(
    //             apiUrl + "/v1/chat/completions",
    //             body,
    //             "application/json"
    //         )
    //     )
    //     {
    //         www.SetRequestHeader("Authorization", "Bearer gpjBOBGS9R02yN607sQV9PV7qb1yidy0");
    //         yield return www.SendWebRequest();

    //         if (www.result != UnityWebRequest.Result.Success)
    //         {
    //             Debug.LogError(www.error);
    //         }
    //         else
    //         {
    //             string response = www.downloadHandler.text;
    //             Debug.Log("Text Response: " + response);

    //             var jsonResponse = JsonSerializer.Deserialize<Response>(response);

    //             ChatChoice[] choices = jsonResponse.choices;
    //             Debug.Log("Text choices: " + choices);

    //             successCallback.Invoke(choices[0].message.content);
    //         }
    //     }
    // }
}

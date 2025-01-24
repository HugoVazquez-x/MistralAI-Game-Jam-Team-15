using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using UnityEngine;
using UnityEngine.Networking;

public class MSG
{
    public string content { get; set; }

    public string role { get; set; }
}

public class ChatResponse
{
    public ChatChoice[] choices { get; set; }
}

public class ChatChoice
{
    public MSG message { get; set; }
}

public class ChatRequest
{
    public string model { get; set; }
    public int max_tokens { get; set; }
    public MSG[] messages { get; set; }
}

public class MistralAPIClient
{
    public string apiUrl = "https://api.mistral.ai/";

    private List<MSG> SwitchAssistantAndUser(List<MSG> messages)
    {
        List<MSG> newMessages = new();

        foreach (var message in messages)
        {
            switch (message.role)
            {
                case "user":
                    newMessages.Add(new MSG { role = "assistant", content = message.content });
                    break;
                case "assistant":
                    newMessages.Add(new MSG { role = "user", content = message.content });
                    break;
                default:
                    newMessages.Add(message);
                    break;
            }
        }

        return newMessages;
    }

    public IEnumerator CompleteChat(List<MSG> messages, Action<string> successCallback)
    {
        Debug.Log("CompleteChat: " + messages.Count);

        if (messages.Last().role == "assistant")
        {
            messages = SwitchAssistantAndUser(messages);
        }

        string body = JsonSerializer.Serialize(
            new ChatRequest
            {
                model = "mistral-small-latest",
                max_tokens = 100,
                messages = messages.ToArray(),
            }
        );

        Debug.Log("MistralAPIClient body: " + body);

        using (
            UnityWebRequest www = UnityWebRequest.Post(
                apiUrl + "/v1/chat/completions",
                body,
                "application/json"
            )
        )
        {
            www.SetRequestHeader("Authorization", "Bearer gpjBOBGS9R02yN607sQV9PV7qb1yidy0");
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                string response = www.downloadHandler.text;
                Debug.Log("Text Response: " + response);

                var jsonResponse = JsonSerializer.Deserialize<ChatResponse>(response);

                ChatChoice[] choices = jsonResponse.choices;
                Debug.Log("Text choices: " + choices);

                successCallback.Invoke(choices[0].message.content);
            }
        }
    }
}

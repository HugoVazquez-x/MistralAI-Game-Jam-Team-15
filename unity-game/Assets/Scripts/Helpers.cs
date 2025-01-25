using System;
using System.Collections;
using System.IO;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;

public static class Helpers
{
    public static float[] ConvertByteToFloat(byte[] array)
    {
        float[] floatArr = new float[array.Length / 4];
        for (int i = 0; i < floatArr.Length; i++)
        {
            if (BitConverter.IsLittleEndian)
                Array.Reverse(array, i * 4, 4);
            floatArr[i] = BitConverter.ToSingle(array, i * 4) / 0x80000000;
        }
        return floatArr;
    }

    public static IEnumerator AnimateText(
        TextMeshProUGUI textComponent,
        string text,
        float delayBetweenCharacters = 0.2f
    )
    {
        textComponent.text = "";
        foreach (char letter in text.ToCharArray())
        {
            textComponent.text += letter;
            yield return new WaitForSeconds(delayBetweenCharacters);
        }

        textComponent.text = text;
    }

    public static IEnumerator PostProcessAudio(
        string audioString,
        Action<AudioClip> successCallback
    )
    {
        var audioBytes = Convert.FromBase64String(audioString);

        string fileName = Guid.NewGuid().ToString() + ".mp3";

        string filePath = Path.Join(Application.persistentDataPath, fileName);

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

using System;
using System.Collections;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using JetBrains.Annotations;
using NLayer; // Décodage MP3
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

    public static AudioClip ConvertMp3StreamToAudioClip(byte[] mp3Bytes)
    {
        try
        {
            // Lire le flux MP3 à partir d'un MemoryStream
            using (var mp3Stream = new MemoryStream(mp3Bytes))
            using (var mp3Reader = new MpegFile(mp3Stream)) // Créez un lecteur MP3
            {
                // Obtenez les propriétés du flux audio
                int sampleRate = 44100; // mp3Reader.SampleRate; // Fréquence d'échantillonnage
                int channels = mp3Reader.Channels; // Nombre de canaux (stéréo/mono)

                Debug.Log(
                    $"Sample rate: {sampleRate}, Channels: {channels}, Length: {mp3Reader.Length}"
                );

                // Décoder les échantillons PCM
                float[] audioSamples = new float[mp3Reader.Length / 4]; // Float = 4 octets 32
                int samplesRead = mp3Reader.ReadSamples(audioSamples, 0, audioSamples.Length);

                float maxAmplitude = 0f;
                for (int i = 0; i < samplesRead; i++)
                {
                    if (Math.Abs(audioSamples[i]) > maxAmplitude)
                        maxAmplitude = Math.Abs(audioSamples[i]);
                }

                if (maxAmplitude > 1.0f)
                {
                    for (int i = 0; i < samplesRead; i++)
                    {
                        audioSamples[i] /= maxAmplitude;
                    }
                }

                if (samplesRead % channels != 0)
                {
                    Debug.LogError("Le nombre d'échantillons lus ne correspond pas aux canaux.");
                }

                // Créer un AudioClip Unity à partir des échantillons PCM
                AudioClip audioClip = AudioClip.Create(
                    "DecodedMp3",
                    samplesRead / channels,
                    channels,
                    sampleRate,
                    false
                );
                audioClip.SetData(audioSamples, 0);

                return audioClip;
            }
        }
        catch (Exception ex)
        {
            Debug.LogError($"Erreur lors du décodage du flux MP3 : {ex.Message}");
            return null;
        }
    }

    public static IEnumerator PostProcessAudio(
        string audioString,
        Action<AudioClip> successCallback
    )
    {
        Debug.Log("Playing audio....");

        var audioBytes = Convert.FromBase64String(audioString);

        AudioClip clip = ConvertMp3StreamToAudioClip(audioBytes);

        successCallback(clip);

        // var samples = ConvertByteToFloat(audioBytes);

        // Debug.Log($"Audio bytes: {audioBytes.Length}, Samples: {samples.Length}");

        // // int channels = GameManager.singleton.sampleAudio.channels;
        // // int frequency = GameManager.singleton.sampleAudio.frequency;
        // // Debug.Log($"Channels: {channels}, Frequency: {frequency}");
        // // float[] samples = new float[GameManager.singleton.sampleAudio.samples * GameManager.singleton.sampleAudio.channels];
        // // GameManager.singleton.sampleAudio.GetData(samples, 0);

        // var clip = AudioClip.Create("ClipName", samples.Length, 1, 44100, false);
        // clip.SetData(samples, 0);
        // successCallback(clip);

        yield break;
    }
}

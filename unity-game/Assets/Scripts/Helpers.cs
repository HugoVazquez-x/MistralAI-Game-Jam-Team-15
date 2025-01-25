using System;
using System.Collections;
using TMPro;
using UnityEngine;

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
}

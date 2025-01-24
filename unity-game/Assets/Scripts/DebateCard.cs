using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class DebateCard : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI cardText;

    public string CardText => cardText.text;

    public void SetText(string text)
    {
        cardText.text = text;
    }
}

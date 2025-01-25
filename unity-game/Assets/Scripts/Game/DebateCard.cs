using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class DebateCard : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI cardText;

    [SerializeField]
    private SideCompass sideCompass;

    public DebateCardData cardData;

    public string CardText => cardText.text;

    public void SetCard(DebateCardData data)
    {
        cardData = data;
        cardText.text = data.title;
        sideCompass.Value = data.side;
    }
}

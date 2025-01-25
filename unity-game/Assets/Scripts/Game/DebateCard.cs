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

    [SerializeField]
    private GameObject loader;

    [SerializeField]
    private GameObject instructions;

    void Start()
    {
        loader.SetActive(false);
    }

    public bool played = false;

    public void SetCard(DebateCardData data)
    {
        cardData = data;
        cardText.text = data.title;
        sideCompass.Value = data.side;
        sideCompass.gameObject.SetActive(true);
        loader.SetActive(false);
    }

    public void OnPlayCard()
    {
        loader.SetActive(true);
        played = true;
    }
}

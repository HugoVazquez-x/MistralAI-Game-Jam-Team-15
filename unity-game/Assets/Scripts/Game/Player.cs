using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

[Serializable]
public class DebateCardData
{
    public int? id { get; set; }
    public string title { get; set; }
    public string description { get; set; }
    public string source { get; set; }
    public int side { get; set; }
    public string game_context { get; set; }
    public bool change_personal_context { get; set; }

    public int information_intensity { get; set; }
}

public class Player : MonoBehaviour
{
    [SerializeField]
    public List<DebateCardData> cards;

    [SerializeField]
    public DebateCard currentCard;

    [SerializeField]
    private DebateCard nextDebateCard;

    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    private bool isDrawingCard = false;

    private bool hasPlayerCard = false;

    public void DrawCard()
    {
        if (isDrawingCard)
            return;
        isDrawingCard = true;

        if (cards.Count == 0)
            cards = new List<DebateCardData>(GameManager.singleton.cards);

        animator.SetTrigger("DrawCard");
        GameManager.singleton.soundManager.PlayPageFlip();
        DebateCardData randomCard = cards[UnityEngine.Random.Range(0, cards.Count)];
        nextDebateCard.SetCard(randomCard);
    }

    public void OnDrawCardEnd()
    {
        currentCard.SetCard(nextDebateCard.cardData);
        isDrawingCard = false;
    }

    public void OnPlayCard()
    {
        if (!hasPlayerCard)
        {
            GameManager.singleton.OnPlayerSendQuestion(currentCard.cardData);
            currentCard.OnPlayCard();
            hasPlayerCard = true;
        }
        else
        {
            MainCanvas.singleton.ShowBossCallUI(
                "Bolloré",
                "Wait for the people to stop talking before playing your card",
                2f
            );
        }
    }

    public void OnPlayedCard(DebateCardData debateCardData)
    {
        cards.Remove(debateCardData);
        DrawCard();
        hasPlayerCard = false;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.RightArrow) && !GameManager.singleton.IsPlayerTurn)
        {
            DrawCard();
        }
        if (Input.GetKeyDown(KeyCode.Space))
        {
            OnPlayCard();
        }
    }
}

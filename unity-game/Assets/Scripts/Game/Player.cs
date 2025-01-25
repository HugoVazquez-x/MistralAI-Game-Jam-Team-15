using System;
using System.Collections;
using System.Collections.Generic;
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
    private DebateCardData[] cards;

    private DebateCardData currentCardData;

    [SerializeField]
    private DebateCard currentCard;

    [SerializeField]
    private DebateCard nextCard;

    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    private bool isDrawingCard = false;

    public void DrawCard()
    {
        if (isDrawingCard)
            return;
        isDrawingCard = true;
        if (cards.Length == 0)
        {
            cards = GameManager.singleton.cards.ToArray();
            return;
        }

        animator.SetTrigger("DrawCard");

        nextCard.SetCard(cards[UnityEngine.Random.Range(0, cards.Length)]);
    }

    public void OnDrawCardEnd()
    {
        currentCard.SetCard(nextCard.cardData);
        currentCardData = nextCard.cardData;
        isDrawingCard = false;
    }

    public void OnPlayCard()
    {
        if (GameManager.singleton.nextCard == null)
        {
            GameManager.singleton.OnPlayerSendQuestion(currentCard.cardData);
        }
    }

    void Update()
    {
        if (GameManager.singleton.isGameOver)
            return;

        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            DrawCard();
        }
        if (Input.GetKeyDown(KeyCode.Space))
        {
            OnPlayCard();
        }
    }
}

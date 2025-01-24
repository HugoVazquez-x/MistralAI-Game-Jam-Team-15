using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    [SerializeField]
    private string[] cards;

    [SerializeField]
    private DebateCard currentCard;

    [SerializeField]
    private DebateCard nextCard;

    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    public void DrawCard()
    {
        animator.SetTrigger("DrawCard");

        string newCardText = cards[Random.Range(0, cards.Length)];

        nextCard.SetText(newCardText);
    }

    public void OnDrawCardEnd()
    {
        currentCard.SetText(nextCard.CardText);
    }

    public void OnPlayCard()
    {
        GameManager.singleton.OnPlayerSendQuestion(currentCard.CardText);
    }

    void Update()
    {
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

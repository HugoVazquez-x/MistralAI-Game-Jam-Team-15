using System;
using System.Collections.Generic;
using System.Linq;
using Unity.Profiling.LowLevel.Unsafe;
using UnityEngine;

[Serializable]
public class Head
{
    public Sprite head;
    public float threshold;
}

public class AICharacter : MonoBehaviour
{
    public string characterName;

    [SerializeField]
    private string context;

    [SerializeField]
    private List<Head> heads;

    public string Context => context;

    public float anger = 0; // from 0 to 10

    [SerializeField]
    private AnimationCurve rednessByAnger;

    private Animator animator;

    private SpriteRenderer headRenderer;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    public void StartTalking()
    {
        animator.SetBool("isTalking", true);
    }

    public void StopTalking()
    {
        animator.SetBool("isTalking", false);
    }

    public void SetAnger(float newAnger)
    {
        anger = newAnger;
        foreach (var head in heads)
        {
            if (anger >= head.threshold)
            {
                headRenderer.sprite = head.head;
            }
        }
        headRenderer.color = Color.Lerp(
            Color.white,
            Color.red,
            rednessByAnger.Evaluate(anger / 10)
        );
    }
}

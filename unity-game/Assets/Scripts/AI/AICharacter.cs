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

    [SerializeField]
    private float anger = 0; // from 0 to 10

    public float Anger // from 0 to 10
    {
        get => anger;
        set => SetAnger(value);
    }

    [SerializeField]
    private AnimationCurve rednessByAnger;

    [SerializeField]
    private AnimationCurve jitterByAnger;

    [SerializeField]
    private Thermometer angerMeter;

    private Animator animator;

    [SerializeField]
    private SpriteRenderer headRenderer;

    [SerializeField]
    private Jitter jitter;

    void Start()
    {
        animator = GetComponent<Animator>();
        SetAnger(anger);
    }

    public void StartTalking()
    {
        animator.SetBool("isTalking", true);
    }

    public void StopTalking()
    {
        animator.SetBool("isTalking", false);
    }

    private void SetAnger(float newAnger)
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

        angerMeter.Value = anger / 10;

        jitter.Amplitude = jitterByAnger.Evaluate(anger / 10);

        if (anger >= 10)
        {
            GameManager.singleton.OnCharacterLeft(this);
        }
    }
}

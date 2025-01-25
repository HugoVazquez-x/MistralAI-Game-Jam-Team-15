using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Thermometer : MonoBehaviour
{
    [SerializeField]
    private Color color;

    private float targetValue;

    private float value; // from 0 to 1

    [SerializeField]
    private float minValue = 1;

    [SerializeField]
    private float maxValue = 3.5f;

    [SerializeField]
    private float lerpSpeed = 5;

    public float Value
    {
        get => value;
        set { targetValue = value; }
    }

    [SerializeField]
    private SpriteRenderer mercurySprite;

    void Start()
    {
        mercurySprite.color = color;
    }

    void UpdateThermometer()
    {
        mercurySprite.size = new Vector2(
            mercurySprite.size.x,
            Mathf.Lerp(minValue, maxValue, value)
        );
    }

    void Update()
    {
        value = Mathf.Lerp(value, targetValue, Time.deltaTime * lerpSpeed);
        UpdateThermometer();
    }
}

using System;
using UnityEngine;

public class SideCompass : MonoBehaviour
{
    [SerializeField]
    private Gradient gradient;

    private float value; // from -1 to 1

    [SerializeField]
    private Transform arrow;

    [SerializeField]
    private SpriteRenderer bgSprite;

    public float Value // from -1 to 1
    {
        get => value;
        set
        {
            this.value = value;
            UpdateCompass();
        }
    }

    void Start()
    {
        bgSprite.color = gradient.Evaluate(0.5f);
    }

    void UpdateCompass()
    {
        float t = (value + 1) / 2;
        bgSprite.color = gradient.Evaluate(t);

        arrow.localEulerAngles = new Vector3(0, 0, Math.Clamp(Value, -1, 1) * 88);
    }
}

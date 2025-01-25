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

    public float Value
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
        arrow.localEulerAngles = new Vector3(0, 0, value * 88);
    }
}

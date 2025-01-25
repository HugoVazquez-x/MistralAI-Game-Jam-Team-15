using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class CheeringPeople : MonoBehaviour
{
    [SerializeField]
    private Sprite[] sprites;

    [SerializeField]
    private float timeBetweenSprites = 0.1f;

    [SerializeField]
    private float timeBetweenSpritesMultiplier = 1.0f;

    private SpriteRenderer spriteRenderer;

    private Vector3 initialPosition;

    void Start()
    {
        timeBetweenSprites = Random.Range(0.1f, 0.5f);
        spriteRenderer = GetComponent<SpriteRenderer>();
        spriteRenderer.sprite = sprites[Random.Range(0, sprites.Length)];
        initialPosition = transform.position;
    }

    void Update()
    {
        transform.position = new Vector3(
            initialPosition.x,
            initialPosition.y
                + Mathf.Sin(
                    Time.time * 2
                        + (transform.position.x + transform.position.y + transform.position.z)
                            * 0.1f
                ) * 0.1f,
            initialPosition.z
        );
    }
}

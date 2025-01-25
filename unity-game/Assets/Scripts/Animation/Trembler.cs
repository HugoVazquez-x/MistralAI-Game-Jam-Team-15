using System.Collections;
using UnityEngine;

class Trembler : MonoBehaviour
{
    [SerializeField]
    private float speed = 1;

    [SerializeField]
    private float amplitude = 0.1f;

    [SerializeField]
    private AnimationCurve zRotationCurve;

    [SerializeField]
    private float duration = 1;

    private Vector3 initialPosition;
    private Quaternion initialRotation;

    void Start()
    {
        initialPosition = transform.position;
        initialRotation = transform.rotation;
    }

    public void Tremble()
    {
        StartCoroutine(TrembleCoroutine());
    }

    IEnumerator TrembleCoroutine()
    {
        float t = 0;
        while (t < duration)
        {
            t += Time.deltaTime * speed;
            transform.position = initialPosition + Random.insideUnitSphere * amplitude;
            transform.rotation =
                initialRotation * Quaternion.Euler(0, 0, zRotationCurve.Evaluate(t));
            yield return null;
        }
        transform.position = initialPosition;
        transform.rotation = initialRotation;
    }
}

using UnityEngine;

class Jitter : MonoBehaviour
{
    [SerializeField]
    private float amplitude = 0.1f; // Maximum displacement in each axis

    public float Amplitude
    {
        get => amplitude;
        set => amplitude = value;
    }

    [SerializeField]
    private float frequency = 10f; // How fast the jittering occurs

    private Vector3 initialPosition;

    void Start()
    {
        initialPosition = transform.position;
    }

    void Update()
    {
        // Generate random offsets within the amplitude range
        float offsetX = Mathf.PerlinNoise(Time.time * frequency, 0f) * 2f - 1f;
        float offsetY = Mathf.PerlinNoise(0f, Time.time * frequency) * 2f - 1f;
        float offsetZ = Mathf.PerlinNoise(Time.time * frequency, Time.time * frequency) * 2f - 1f;

        // Apply jitter with amplitude scaling
        Vector3 jitter = new Vector3(offsetX, offsetY, offsetZ) * amplitude;
        transform.position = initialPosition + jitter;
    }
}

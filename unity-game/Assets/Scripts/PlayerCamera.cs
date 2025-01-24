using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerCamera : MonoBehaviour
{
    [SerializeField]
    private float maxXRotaion = 10;

    [SerializeField]
    private float maxYRotaion = 10;

    [SerializeField]
    private Transform cameraTransform;

    float ClampRotation(float rotation, float maxRotation)
    {
        if (rotation > 180)
        {
            rotation -= 360;
        }
        rotation = Mathf.Clamp(rotation, -maxRotation, maxRotation);
        return rotation;
    }

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update()
    {
        float mouseX = Input.GetAxis("Mouse X");
        float mouseY = Input.GetAxis("Mouse Y");

        cameraTransform.Rotate(Vector3.up, mouseX);
        cameraTransform.Rotate(Vector3.right, -mouseY);

        Vector3 currentRotation = cameraTransform.localEulerAngles;
        currentRotation.x = ClampRotation(currentRotation.x, maxXRotaion);
        currentRotation.y = ClampRotation(currentRotation.y, maxYRotaion);
        currentRotation.z = 0;
        cameraTransform.localEulerAngles = currentRotation;
    }
}

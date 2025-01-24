using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestCustomClient : MonoBehaviour
{
    public CustomClient customClient = new CustomClient();

    void Start()
    {
        // StartCoroutine(
        //     customClient.Complete(
        //         "Hello, Mistral!",
        //         (response) =>
        //         {
        //             Debug.Log("Response: " + response);
        //         },
        //         "mistral"
        //     )
        // );
    }

    // Update is called once per frame
    void Update() { }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DebugManager : MonoBehaviour
{
    // Start is called before the first frame update
    void Start() { }

    // Update is called once per frame
    void Update()
    {
        if (GameManager.singleton.isGameOver)
            return;
        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            Debug.Log("Up Arrow Pressed");
            GameManager.singleton.leftCharacter.Anger++;
            GameManager.singleton.rightCharacter.Anger++;
        }
        else if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            Debug.Log("Down Arrow Pressed");
            GameManager.singleton.leftCharacter.Anger--;
            GameManager.singleton.rightCharacter.Anger--;
        }
    }
}

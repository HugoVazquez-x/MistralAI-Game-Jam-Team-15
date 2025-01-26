using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class MainMenu : MonoBehaviour
{

    [SerializeField] private TMP_InputField apiUrlInput;

    void Start() 
    {
        apiUrlInput.text = GameManager.singleton.customApiUrl;
    }
    public void OnPressPlay()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene("MainScene");
        GameManager.singleton.StartGame();
    }

    public void OnPressQuit()
    {
        Application.Quit();
    }

    public void OnEditApiUrl(string newUrl)
    {
        GameManager.singleton.customApiUrl = newUrl;
    }
}

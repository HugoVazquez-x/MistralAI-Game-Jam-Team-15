using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class MainCanvas : MonoBehaviour
{
    #region Singleton
    public static MainCanvas singleton;

    void Awake()
    {
        if (singleton == null)
        {
            singleton = this;
            DontDestroyOnLoad(gameObject);
        }
        else if (singleton != this)
        {
            Destroy(gameObject);
        }
    }

    #endregion

    public DialogManager dialogManager;

    public Fader fader;

    public GameOverScreen gameOverScreen;

    public TimerUI timerUI;

    public GameObject errorPanel;
    public TextMeshProUGUI errorText;

    public GameObject loadingPanel;

    void Start()
    {
        errorPanel.SetActive(false);
        gameOverScreen.gameObject.SetActive(false);
    }

    private bool isInCall = false;

    public void ShowBossCallUI(string bossName, string bossDescription, float speed = 1f)
    {
        if (isInCall)
            return;
        isInCall = true;

        BossCallUI bossCallUI = Instantiate(GameManager.singleton.bossCallUIPrefab, transform);
        bossCallUI.TriggerPhoneCall(bossName, bossDescription, () => isInCall = false, speed);
    }

    public void ShowGameOverScreen(string hint)
    {
        gameOverScreen.gameObject.SetActive(true);
        gameOverScreen.gameOverHintText.text = hint;
    }

    public void ReloadGame()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene("MainMenu");
    }
}

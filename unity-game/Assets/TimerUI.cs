using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TimerUI : MonoBehaviour
{
    [SerializeField]
    private TextMeshProUGUI timerText;

    // Start is called before the first frame update
    void Start() { }

    string GetTimeRemaining()
    {
        float timeRemaining = GameManager.singleton.timer.TimeRemaining;

        int minutes = Mathf.FloorToInt(timeRemaining / 60);

        int seconds = Mathf.FloorToInt(timeRemaining % 60);

        return string.Format("{0:00}:{1:00}", minutes, seconds);
    }

    void Update()
    {
        timerText.text = GetTimeRemaining();
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class MainTimer : MonoBehaviour
{
    [SerializeField]
    private float totalTime = 300;

    public float TotalTime => totalTime;

    private float timeRemaining = 300;

    public float TimeRemaining => timeRemaining;

    private bool timerRunning = false;

    [SerializeField]
    private AnimationCurve speedMultiplierByGameProgress;

    void Start()
    {
        timeRemaining = totalTime;
    }

    public void StartTimer()
    {
        timerRunning = true;
    }

    void Update()
    {
        if (!timerRunning || GameManager.singleton.isGameOver)
            return;
        if (timeRemaining > 0)
            timeRemaining -= Time.deltaTime;
        else
        {
            timeRemaining = 0;
            GameManager.singleton.OnTimerEnd();
        }

        if (Mathf.FloorToInt(timeRemaining) != Mathf.FloorToInt(timeRemaining + Time.deltaTime))
        {
            GameManager.singleton.globalSpeedMultiplier = speedMultiplierByGameProgress.Evaluate(
                1 - timeRemaining / totalTime
            );
        }
    }
}

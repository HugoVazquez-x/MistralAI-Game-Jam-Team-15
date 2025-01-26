using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScoreManager : MonoBehaviour
{
    public int score = 0;

    public int engagement = 0; // from -100 to 100 (0 is neutral)

    public int targetEngagement = 100;

    [SerializeField]
    private SideCompass publicCompass;

    public int callNumber = 4;

    public string[] bigBossNames = new string[]
    {
        "Bolloré",
        "Drahi",
        "Xavier Niel",
        "Bernard Arnault",
    };

    public string[] bigBossCalls = new string[]
    {
        "Just had a call! {TARGET} needs to win",
        "My wife wants that {TARGET} wins, you better do it, or else!...",
        "I just got a call from {TARGET}, they want to win",
        "IF {TARGET} DOESN'T WIN, YOU'RE FIRED!",
    };

    private float[] callPositions;

    void Start()
    {
        callPositions = new float[callNumber];
        for (int i = 0; i < callNumber; i++)
        {
            StartCoroutine(
                SwitchAfterDelay(
                    GameManager.singleton.timer.TotalTime * UnityEngine.Random.Range(0.2f, 0.9f)
                )
            );
        }
    }

    public void FirstCall()
    {
        MainCanvas.singleton.ShowBossCallUI(
            "Bolloré",
            "You have to make sure TRUMP wins the debate! Otherwise, you're fired!"
        );
    }

    IEnumerator SwitchAfterDelay(float waitDuration)
    {
        yield return new WaitForSeconds(waitDuration);
        SwitchTargetChar();
    }

    public void UpdateEngagement()
    {
        float angerDiff =
            GameManager.singleton.rightCharacter.Anger - GameManager.singleton.leftCharacter.Anger;

        engagement = (int)(angerDiff * 100);
        publicCompass.Value = angerDiff / 15f;
    }

    public void UpdateScore()
    {
        score += 100 / (Mathf.Abs(targetEngagement - engagement) + 1);
        UpdateEngagement();
    }

    public AICharacter CharThatShouldWin =>
        targetEngagement > 0
            ? GameManager.singleton.leftCharacter
            : GameManager.singleton.rightCharacter;

    public void SwitchTargetChar()
    {
        targetEngagement = -targetEngagement;
        MainCanvas.singleton.ShowBossCallUI(
            bigBossNames[UnityEngine.Random.Range(0, bigBossNames.Length)],
            bigBossCalls[UnityEngine.Random.Range(0, bigBossCalls.Length)]
                .Replace("{TARGET}", CharThatShouldWin.characterName.ToUpper())
        );
    }

    public void TriggerEverySecond()
    {
        UpdateScore();
    }

    void Update()
    {
        if (
            Mathf.FloorToInt(Time.time) != Mathf.FloorToInt(Time.time + Time.deltaTime)
            && !GameManager.singleton.isGameOver
        )
        {
            TriggerEverySecond();
        }
    }

    public bool Winning => engagement * targetEngagement > 0;
}

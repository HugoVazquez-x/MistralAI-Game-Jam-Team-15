#nullable enable
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public enum Turn
{
    Left,
    Right,
    Player,
}

public class GameManager : MonoBehaviour
{
    #region Singleton
    public static GameManager singleton;

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

    public SoundManager soundManager;

    public string gameId;

    public string customApiUrl = "http://192.168.80.144:8000";

    [SerializeField]
    private bool useCustomApi = false;

    [SerializeField]
    private List<MSG> messages = new();

    [SerializeField]
    public AICharacter leftCharacter;

    [SerializeField]
    public AICharacter rightCharacter;

    public BossCallUI bossCallUIPrefab;

    public CustomClient customClient = new CustomClient();

    public DebateCard debateCardPrefab;

    private AICharacter currentCharacter;
    private AICharacter? previousCharacter;

    public MainTimer timer;

    public bool isGameOver = false;

    private ScoreManager scoreManager;

    public List<DebateCardData> cards = new List<DebateCardData>();

    public DebateCardData? nextCard = null;

    public float globalSpeedMultiplier = 1;

    public Player player;

    void Start()
    {
        player = FindObjectOfType<Player>();

        InitGameId();
        currentCharacter = leftCharacter; // start with trump speaking

        StartCoroutine(StartGame());

        timer = GetComponent<MainTimer>();
        scoreManager = GetComponent<ScoreManager>();
        soundManager = GetComponent<SoundManager>();
    }

    IEnumerator StartGame()
    {
        Fader.instance.SetFullBlack();

        yield return customClient.Start(leftCharacter.characterName, rightCharacter.characterName);

        if (isGameOver)
            yield break;

        yield return customClient.GetDebateCards(
            (cards) => this.cards = new List<DebateCardData>(cards)
        );

        if (cards.Count == 0)
        {
            HandleError("No cards returned by the API");
            yield break;
        }

        for (int i = 0; i < cards.Count; i++)
            cards[i].id = i;

        if (isGameOver)
            yield break;

        yield return Fader.FadeIn();
        Debug.Log("Game started ! " + nextCard == null);

        timer.StartTimer();
        scoreManager.FirstCall();

        nextCard = null;

        // Add a first message, otherwise the AI will not start
        messages.Add(new MSG { role = "system", content = "You are at a debate" });

        while (true)
        {
            // Only blocking is API calls, the rest (talking) is async
            if (nextCard?.id != null) // needing the ?.id because of phantom undefined nextCard :shrug:
                yield return PlayerPlay(nextCard);
            else
                yield return PlayAITurn();

            NextTurn();
        }
    }

    public IEnumerator PlayAITurn()
    {
        CustomClientChatResponse? response = null;

        Debug.Log("Playing AI turn");

        yield return customClient.Chat(
            messages.Last().content,
            currentCharacter?.characterName,
            previousCharacter?.characterName ?? "player",
            (r) => response = r
        );

        // Wait for the character to finish talking
        while (MainCanvas.singleton.dialogManager.IsTalking)
            yield return null;

        messages.Add(new MSG { role = "assistant", content = response.generated_text });

        if (currentCharacter != null)
            currentCharacter.Anger = response.anger * 10;

        StartCoroutine(
            MainCanvas.singleton.dialogManager.CharacterSay(
                currentCharacter,
                response.generated_text,
                response.audioClip
            )
        );
    }

    public void NextTurn()
    {
        previousCharacter = currentCharacter;
        currentCharacter = currentCharacter == leftCharacter ? rightCharacter : leftCharacter;
    }

    #region  Player


    private bool playerTurn = false;

    public bool IsPlayerTurn => playerTurn;

    public void OnPlayerSendQuestion(DebateCardData debateCardData)
    {
        Debug.Log("Player send question " + debateCardData.title);
        nextCard = debateCardData;
    }

    IEnumerator PlayerPlay(DebateCardData debateCardData)
    {
        if (nextCard == null || playerTurn)
            yield break;

        nextCard = null; // Set here to allow AI to respond in main loop
        playerTurn = true;

        Debug.Log("Playing Player with card " + debateCardData.title);

        CustomClientPlayerCardResponse? response = null;
        yield return customClient.PlayerPlayCard(
            new CustomClientPlayerCardRequest
            {
                card_id = debateCardData.id ?? -1,
                previous_character_text = messages.Last().content,
                previous_speaker = previousCharacter?.characterName ?? "player",
            },
            (r) => response = r
        );

        messages.Add(new MSG { role = "user", content = response?.presenter_question });

        previousCharacter = null;

        // Wait for the character to finish talking
        while (MainCanvas.singleton.dialogManager.IsTalking)
            yield return null;

        // Async play the player talking not to block the main loop
        StartCoroutine(
            PlayerTalking(response.presenter_question, response.audioClip, debateCardData)
        );
    }

    IEnumerator PlayerTalking(string text, AudioClip audioClip, DebateCardData debateCardData)
    {
        yield return MainCanvas.singleton.dialogManager.CharacterSay(null, text, audioClip);

        player.OnPlayedCard(debateCardData);
        playerTurn = false;
    }

    #endregion

    public void OnTimerEnd()
    {
        if (isGameOver)
            return;
        MainCanvas.singleton.timerUI.gameObject.SetActive(false);

        isGameOver = true;
        Fader.Fade(() =>
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("EndScene");

            if (scoreManager.Winning)
            {
                EndScreen.singleton.ShowWinningEndScreen(scoreManager.score < 0);
            }
            else
            {
                MainCanvas.singleton.ShowGameOverScreen("You didn't follow orders...");

                MainCanvas.singleton.ShowBossCallUI(
                    "Bolloré",
                    "I told you "
                        + scoreManager.CharThatShouldWin.characterName
                        + " should win! You're fired!"
                );
            }
        });
    }

    public void OnCharacterLeft(AICharacter character)
    {
        if (isGameOver)
            return;
        isGameOver = true;

        MainCanvas.singleton.timerUI.gameObject.SetActive(false);

        Fader.Fade(() =>
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("EndScene");

            MainCanvas.singleton.ShowGameOverScreen(
                character.characterName + " has left the debate before the end!"
            );

            MainCanvas.singleton.ShowBossCallUI(
                "Bolloré",
                "What have you done!! I told you to go easy on them... You're fired!"
            );
        });
    }

    #region Error Handling

    public void HandleError(string error)
    {
        Debug.LogError(error);
        MainCanvas.singleton.errorText.text = error;
        MainCanvas.singleton.errorPanel.SetActive(true);
        isGameOver = true;
        Cursor.lockState = CursorLockMode.None;
    }

    #endregion

    #region Misc

    void InitGameId()
    {
        Guid myuuid = Guid.NewGuid();
        string myuuidAsString = myuuid.ToString();
        gameId = myuuidAsString;
    }

    #endregion
}

#nullable enable
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

    public void HandleError(string error)
    {
        Debug.LogError(error);
        MainCanvas.singleton.errorText.text = error;
        MainCanvas.singleton.errorPanel.SetActive(true);
        isGameOver = true;
        Cursor.lockState = CursorLockMode.None;
    }

    void Start()
    {
        currentCharacter = leftCharacter;
        StartCoroutine(StartGame());
        timer = GetComponent<MainTimer>();
        scoreManager = GetComponent<ScoreManager>();
    }

    IEnumerator StartGame()
    {
        Fader.instance.SetFullBlack();

        yield return customClient.Start(leftCharacter.characterName, rightCharacter.characterName);

        if (isGameOver)
            yield break;

        FetchCards();

        if (isGameOver)
            yield break;

        yield return Fader.FadeIn();
        timer.StartTimer();

        MainCanvas.singleton.ShowBossCallUI(
            "Bolloré",
            "You have to make sure TRUMP wins the debate! Otherwise, you're fired!"
        );

        for (int i = 0; i < 10; i++)
        {
            if (nextCard != null)
                yield return PlayerPlay(nextCard);
            else
                yield return PlayTurnCustomApi();
            yield return new WaitForSeconds(0.5f);

            NextTurn();
        }
    }

    private void FetchCards()
    {
        StartCoroutine(
            customClient.GetDebateCards(
                (cards) =>
                {
                    this.cards = new List<DebateCardData>(cards);
                    for (int i = 0; i < this.cards.Count; i++)
                    {
                        this.cards[i].id = i;
                    }
                }
            )
        );
    }

    public IEnumerator PlayTurnCustomApi()
    {
        CustomClientChatResponse? response = null;

        yield return customClient.Chat(
            messages.Last().content,
            currentCharacter?.characterName,
            previousCharacter?.characterName ?? "player",
            (r) => response = r
        );

        messages.Add(new MSG { role = "assistant", content = response.generated_text });

        if (currentCharacter != null)
            currentCharacter.Anger = response.anger * 10;

        yield return MainCanvas.singleton.dialogManager.CharacterSay(
            currentCharacter,
            response.generated_text,
            response.audioClip
        );
    }

    public void NextTurn()
    {
        previousCharacter = currentCharacter;
        currentCharacter = currentCharacter == leftCharacter ? rightCharacter : leftCharacter;
    }

    public void OnPlayerSendQuestion(DebateCardData debateCardData)
    {
        nextCard = debateCardData;
    }

    IEnumerator PlayerPlay(DebateCardData debateCardData)
    {
        nextCard = null;

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

        yield return MainCanvas.singleton.dialogManager.CharacterSay(
            null,
            response.presenter_question,
            response.audioClip
        );
    }

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
}

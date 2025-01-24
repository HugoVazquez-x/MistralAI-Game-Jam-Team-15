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


    [SerializeField]
    private bool useCustomApi = false;

    [SerializeField]
    private List<MSG> messages = new();

    [SerializeField]
    private AICharacter leftCharacter;

    [SerializeField]
    private AICharacter rightCharacter;

    [SerializeField]
    private string firstPrompt;

    private MistralAPIClient mistralAPIClient = new MistralAPIClient();
    private CustomClient customClient = new CustomClient();

    public DebateCard debateCardPrefab;

    private AICharacter currentCharacter;
    private AICharacter? previousCharacter;

    [SerializeField]
    private float score;

    void Start()
    {
        currentCharacter = leftCharacter;
        StartCoroutine(StartGame());
    }

    IEnumerator StartGame()
    {
        messages.Add(new MSG { role = "user", content = firstPrompt });

        for (int i = 0; i < 10; i++)
        {
            if (useCustomApi)
                yield return PlayTurnCustomApi();
            else
                yield return PlayTurnMistralApi();

            yield return new WaitForSeconds(0.5f);

            NextTurn();
        }
    }

    public void PlayCard(string content)
    {
        messages.Add(new MSG { role = "player", content = content });
    }

    public IEnumerator PlayTurnMistralApi()
    {
        if (!currentCharacter)
        {
            Debug.LogError("No character");
            yield break;
        }

        List<MSG> messagesToSend = new List<MSG>(messages);
        messagesToSend.Insert(
            0,
            new MSG
            {
                role = "system",
                content = currentCharacter?.Context + ".\n Only output a single sentence",
            }
        );

        yield return mistralAPIClient.CompleteChat(
            messagesToSend,
            (response) =>
            {
                messages.Add(new MSG { role = "assistant", content = response });

                MainCanvas.singleton.dialogManager.CharacterSay(currentCharacter, response);
            }
        );
    }

    public IEnumerator PlayTurnCustomApi()
    {
        yield return customClient.Chat(
            messages.Last().content,
            currentCharacter?.characterName,
            previousCharacter?.characterName ?? "player",
            (response) =>
            {
                messages.Add(new MSG { role = "assistant", content = response });

                MainCanvas.singleton.dialogManager.CharacterSay(currentCharacter, response);
            }
        );
    }

    public void NextTurn()
    {
        previousCharacter = currentCharacter;
        currentCharacter = currentCharacter == leftCharacter ? rightCharacter : leftCharacter;
    }

    public void OnPlayerSendQuestion(string question)
    {
        messages.Add(new MSG { role = "player", content = question });
        previousCharacter = null;
        currentCharacter = currentCharacter == leftCharacter ? rightCharacter : leftCharacter;
        StartCoroutine(PlayTurnCustomApi());
    }
}

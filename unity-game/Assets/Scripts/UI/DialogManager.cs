#nullable enable
using System.Collections;
using UnityEngine;

public class DialogManager : MonoBehaviour
{
    [SerializeField]
    private GameObject dialogPanel;

    [SerializeField]
    private TMPro.TextMeshProUGUI dialogText;

    [SerializeField]
    private TMPro.TextMeshProUGUI charNameText;

    private AICharacter? currentTalkingCharacter;

    [SerializeField]
    public GameObject clickForNextHint;

    [SerializeField]
    private GameObject playerQuestionPanel;

    void Start()
    {
        dialogPanel.SetActive(false);
    }

    public void CharacterSay(AICharacter? c, string dialog)
    {
        if (c != null)
        {
            currentTalkingCharacter = c;
            currentTalkingCharacter.StartTalking();
            charNameText.text = c.characterName;
        }
        else
        {
            charNameText.text = "Debate Host";
        }
        dialogPanel.SetActive(true);
        StartCoroutine(AnimateText(dialog));
    }

    IEnumerator AnimateText(string text)
    {
        dialogText.text = "";
        foreach (char letter in text.ToCharArray())
        {
            dialogText.text += letter;
            yield return new WaitForSeconds(0.02f);
        }

        dialogText.text = text;
        currentTalkingCharacter?.StopTalking();
    }

    public void OnPlayerSendQuestion(string question)
    {
        dialogPanel.SetActive(false);
        GameManager.singleton.OnPlayerSendQuestion(question);
    }
}

#nullable enable
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class DialogManager : MonoBehaviour
{
    [SerializeField]
    private GameObject dialogPanel;

    [SerializeField]
    private TMPro.TextMeshProUGUI dialogText;

    [SerializeField]
    private TMPro.TextMeshProUGUI charNameText;

    private AICharacter? currentTalkingCharacter;

    private AudioSource audioSource;

    [SerializeField]
    private float textSpeed = 0.05f;

    void Start()
    {
        dialogPanel.SetActive(false);
        audioSource = GetComponent<AudioSource>();
    }

    private bool isTalking = false;
    public bool IsTalking => isTalking;

    public IEnumerator CharacterSay(AICharacter? c, string dialog, AudioClip audioClip)
    {
        isTalking = true;

        currentTalkingCharacter?.StopTalking();
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
        yield return AnimateText(dialog, audioClip);
        currentTalkingCharacter?.StopTalking();

        while (audioSource.isPlaying)
            yield return null;

        GameManager.singleton.soundManager.PlayCheer();

        isTalking = false;
    }

    IEnumerator AnimateText(string text, AudioClip audioClip)
    {
        audioSource.clip = audioClip;
        audioSource.Play();
        audioSource.pitch = GameManager.singleton.globalSpeedMultiplier;
        yield return Helpers.AnimateText(
            dialogText,
            text,
            textSpeed / GameManager.singleton.globalSpeedMultiplier
        );
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class BossCallUI : MonoBehaviour
{
    private Animator animator;

    [SerializeField]
    private TextMeshProUGUI bossCallText;

    [SerializeField]
    private TextMeshProUGUI bossName;

    [SerializeField]
    private float showForSeconds = 2;

    [SerializeField]
    private float textSpeed = 0.1f;

    private CanvasGroup canvasGroup;

    private string bossNameText;
    private string bossCallTextText;

    private Action onBossCallEnd;

    public static BossCallUI currentBossCallUI = null;

    private float speed = 1f;

    public void TriggerPhoneCall(
        string bossName,
        string content,
        Action onBossCallEnd,
        float speed = 1f
    )
    {
        if (currentBossCallUI != null)
        {
            Destroy(currentBossCallUI.gameObject);
        }
        animator = GetComponent<Animator>();
        Debug.Log("TriggerPhoneCall : " + bossName + " : " + content);
        canvasGroup = GetComponent<CanvasGroup>();

        this.speed = speed;
        this.onBossCallEnd = onBossCallEnd;

        animator.speed = speed;

        currentBossCallUI = this;

        canvasGroup.alpha = 1;
        animator.SetTrigger("BossCall");

        bossNameText = bossName;
        bossCallTextText = content;

        this.bossName.text = "";
        this.bossCallText.text = "";
    }

    public void TriggerShowBossText()
    {
        GameManager.singleton.soundManager.PlayDing();
        StartCoroutine(ShowBossText());
    }

    private IEnumerator ShowBossText()
    {
        // yield return Helpers.AnimateText(bossName, bossNameText, textSpeed);
        bossName.text = bossNameText;
        yield return Helpers.AnimateText(bossCallText, bossCallTextText, textSpeed / speed);

        speed = 1f; // reset speed

        yield return new WaitForSeconds(showForSeconds);

        for (float i = 1; i >= 0; i -= Time.deltaTime)
        {
            canvasGroup.alpha = i;
            yield return null;
        }
        onBossCallEnd?.Invoke();
        Destroy(gameObject);
    }
}

using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class Fader : MonoBehaviour
{
    private CanvasGroup canvasGroup;

    [SerializeField]
    private float fadeDuration = 1f;

    [SerializeField]
    private bool isFullBlack = false;

    private bool isFading = false;

    public static Fader instance => MainCanvas.singleton.fader;

    private CanvasGroup CanvasGroup => canvasGroup ??= GetComponent<CanvasGroup>();

    void Start()
    {
        canvasGroup = GetComponent<CanvasGroup>();
        // StartCoroutine(FadeIn());
        if (isFullBlack)
            SetFullBlack();
        else
            SetTransparent();
    }

    public void SetFullBlack()
    {
        isFullBlack = true;
        CanvasGroup.alpha = 1;
    }

    public void SetTransparent()
    {
        isFullBlack = false;
        CanvasGroup.alpha = 0;
    }

    // from black to transparent
    public static IEnumerator FadeIn()
    {
        instance.isFading = true;
        instance.SetFullBlack();
        float t = 0;
        while (t < instance.fadeDuration)
        {
            t += Time.deltaTime;
            instance.CanvasGroup.alpha = 1 - t / instance.fadeDuration;
            yield return null;
        }
        instance.isFading = false;
        instance.SetTransparent();
    }

    // from transparent to black
    public static IEnumerator FadeOut()
    {
        instance.isFading = true;
        instance.SetTransparent();
        float t = 0;
        while (t < instance.fadeDuration)
        {
            t += Time.deltaTime;
            instance.CanvasGroup.alpha = t / instance.fadeDuration;
            yield return null;
        }
        instance.isFading = false;
        instance.SetFullBlack();
    }

    public static void Fade(
        Action fullBlackCallBack,
        Action endFadeOutCallBack = null,
        bool fadeOut = true
    )
    {
        instance.StartCoroutine(FadeCoroutine(fullBlackCallBack, endFadeOutCallBack, fadeOut));
    }

    private static IEnumerator FadeCoroutine(
        Action fullBlackCallBack,
        Action endFadeOutCallBack = null,
        bool fadeOut = true
    )
    {
        yield return FadeOut();
        fullBlackCallBack.Invoke();
        if (fadeOut)
        {
            yield return FadeIn();
            endFadeOutCallBack?.Invoke();
        }
    }
}

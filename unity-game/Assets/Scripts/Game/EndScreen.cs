using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class EndScreen : MonoBehaviour
{
    #region Singleton
    public static EndScreen singleton;

    void Awake()
    {
        if (singleton == null)
        {
            singleton = this;
        }
        else if (singleton != this)
        {
            Destroy(gameObject);
        }
    }

    #endregion



    [SerializeField]
    private GameObject trumpArticle,
        harrisArticle;

    [SerializeField]
    private Animator newsPaperAnimation;

    public void ShowWinningEndScreen(bool isTrumpWinner)
    {
        newsPaperAnimation.gameObject.SetActive(true);
        newsPaperAnimation.SetTrigger("win");
        trumpArticle.SetActive(isTrumpWinner);
        harrisArticle.SetActive(!isTrumpWinner);
    }

    public void onAnimationEnd()
    {
        MainCanvas.singleton.ShowGameOverScreen("Game Over");
    }
}

using System.Collections;
using UnityEngine;

public class SoundManager : MonoBehaviour
{
    public AudioSource sfxSource;
    public AudioSource sfxSourceDing;
    public AudioSource sfxSourcePageFlip;

    public AudioClip[] cheersClips;

    public AudioClip ding;
    public AudioClip pageFlip;

    public void PlayCheer()
    {
        sfxSource.clip = cheersClips[Random.Range(0, cheersClips.Length)];
        sfxSource.Play();
        StartCoroutine(FadeOff(sfxSource, 2f + Random.Range(0f, 0.5f)));
    }

    public void PlayDing()
    {
        sfxSourceDing.clip = ding;
        sfxSourceDing.Play();
    }

    public void PlayPageFlip()
    {
        sfxSourcePageFlip.clip = pageFlip;
        sfxSourcePageFlip.Play();
    }

    IEnumerator FadeOff(AudioSource audioSource, float duration)
    {
        float startVolume = audioSource.volume;

        while (audioSource.volume > 0)
        {
            audioSource.volume -= startVolume * Time.deltaTime / duration;

            yield return null;
        }

        audioSource.Stop();
        audioSource.volume = startVolume;
    }
}

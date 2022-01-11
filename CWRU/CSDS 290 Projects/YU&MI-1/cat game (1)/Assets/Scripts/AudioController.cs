using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class AudioController{

    public static IEnumerator Fade(AudioSource audioSource1, AudioSource audioSource2)
    {
        // while (audioSource1.volume > 0.1f) {
        //     audioSource1.volume = Mathf.Lerp(audioSource1.volume, 0f, 1f * Time.deltaTime);
        //     yield return null;
        // }
        audioSource1.Stop();
        audioSource2.Play();
        yield return null;
        // audioSource2.volume = 0;
        // while (audioSource2.volume < 0.9) {
        //     audioSource2.volume = Mathf.Lerp(audioSource2.volume, 1f, 0.5f * Time.deltaTime);
        //     yield return null;
        // }
    }
}
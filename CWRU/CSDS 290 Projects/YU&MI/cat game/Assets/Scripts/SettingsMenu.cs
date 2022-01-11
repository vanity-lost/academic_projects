using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;

public class SettingsMenu : MonoBehaviour
{

    public AudioMixer am;

    public void SetFullScreen(bool isFull)
    {
        if (isFull)
        {
            Debug.Log("FullScreen");
            Screen.fullScreenMode = FullScreenMode.ExclusiveFullScreen;
        }
        else
        {
            Debug.Log("Windowed");
            Screen.fullScreenMode = FullScreenMode.Windowed;
        }
    }

   public void SetVolume(float volume)
    {
        Debug.Log(volume);
        am.SetFloat("volume", volume);
    }
}

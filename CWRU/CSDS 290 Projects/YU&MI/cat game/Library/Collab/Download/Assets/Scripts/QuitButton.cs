using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuitButton : MonoBehaviour
{
    public void Quit() {
        Debug.Log("Quitting");
        Application.Quit();
    }
}

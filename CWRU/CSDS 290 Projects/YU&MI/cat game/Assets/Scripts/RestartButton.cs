using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class RestartButton : MonoBehaviour
{
    public GameObject GameOver;

    public void Restart() {
        SceneManager.LoadScene("main");
        GameOver.SetActive(false);
    }
}

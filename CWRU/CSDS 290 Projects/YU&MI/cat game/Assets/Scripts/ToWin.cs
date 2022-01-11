using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ToWin : MonoBehaviour
{

    public int breakCount = 0;
    public int winCount;

    // Update is called once per frame
    void Update()
    {
        if (breakCount >= winCount) {
            SceneManager.LoadScene("UI End");
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameOverController : MonoBehaviour
{
    public GameObject i;

    void Start()
    {
        Time.timeScale = 0f;
        i.SetActive(false);
    }
}

﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneTransition : MonoBehaviour
{
    public string sceneName;

    void OnTriggerEnter2D(Collider2D other) {
        if (other.CompareTag("Cat")) {
            SceneManager.LoadScene(sceneName);
        }
    }
}

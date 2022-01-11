using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class AngryBar : MonoBehaviour
{
    public float annoyance = 0f;
    public GameObject enemy;
    bool trigger = false;

    public AudioSource backgroundSource;
    public AudioSource chasingSource;

    public SimpleHealthBar annoyanceBar;

    float time = 0;
   
    void Start()
    {
        // angry.text = System.Math.Round(annoyance, 2).ToString();
        enemy.GetComponent<EnemyAI>().enabled = false;
        enemy.GetComponent<NewBehaviourScript>().enabled = true;
        annoyanceBar.UpdateBar( annoyance, 100 );
    }

    void Update() {
        if (annoyance > 0) {
            // reduce by time
            time += Time.deltaTime;
            annoyance -= 0.01f * Mathf.Pow(3, 0.1f * time);
            // angry.text = System.Math.Round(annoyance, 2).ToString();
        } else {
            time = 0;
        }

        if (annoyance < 30 && trigger) {
            trigger = false;
            StartCoroutine(AudioController.Fade(chasingSource, backgroundSource));
            // chasingSource.Stop();
            // backgroundSource.Play();
            enemy.GetComponent<EnemyAI>().enabled = false;
            enemy.GetComponent<NewBehaviourScript>().enabled = true;
        }

        if (annoyance >= 30 && !trigger) {
            trigger = true;
            StartCoroutine(AudioController.Fade(backgroundSource, chasingSource));
            // backgroundSource.Stop();
            // chasingSource.Play();
            enemy.GetComponent<EnemyAI>().enabled = true;
            enemy.GetComponent<NewBehaviourScript>().enabled = false;
        }

        enemy.GetComponent<EnemyAI>().changeSpeed(annoyance);
        enemy.GetComponent<NewBehaviourScript>().changeSpeed(annoyance);

		annoyanceBar.UpdateBar( annoyance, 100 );
    }

    public void addCount() {
        time = 0;

        if (annoyance > 80f) {
            annoyance = 100f;
        } else {
            annoyance += 20f;
        }
        // angry.text = System.Math.Round(annoyance, 2).ToString();
        annoyanceBar.UpdateBar( annoyance, 100 );
    }
}

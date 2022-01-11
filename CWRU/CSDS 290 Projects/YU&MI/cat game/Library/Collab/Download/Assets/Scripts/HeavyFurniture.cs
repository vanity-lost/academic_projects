using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HeavyFurniture : MonoBehaviour
{
    
    public GameObject cat;
    float health = 4f;
    public GameObject communication;
    float checktime = 0f;
    bool trigger = false;
    public GameObject gameOver;

    void Update()
    {
        if (Input.GetKey(KeyCode.J)) {
            // pop a text
            if (!trigger) {
                communication.SetActive(true);
                trigger = true;
            }

            // change speed
            health -= 1;
            if (health <= 0f) {
                gameOver.SetActive(true);
            }
        }

        checktime += Time.deltaTime;

        if (trigger && (checktime >= 4f)) {
            communication.SetActive(false);
        }
    }

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TextSwitch : MonoBehaviour
{

    float time = 0f;
    public GameObject credits;

    void Update()
    {
        time += Time.deltaTime;
        if (time >= 2) {
            credits.SetActive(true);
            Destroy(gameObject);
        }
    }
}

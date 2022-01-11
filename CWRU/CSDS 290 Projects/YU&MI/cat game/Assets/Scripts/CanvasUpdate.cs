using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CanvasUpdate : MonoBehaviour
{
    int count = 0;
    public GameObject canvas;
    public GameObject text1;
    public GameObject text2;
    public GameObject text3;
    public GameObject text4;

    void Update()
    {
        if (Input.GetKeyDown("space")) {
            if (count == 0) {
                count ++;
                text1.SetActive(false);
                text4.SetActive(true);
            } else if (count == 1) {
                count ++;
                text4.SetActive(false);
                text2.SetActive(true);
            } else if (count == 2) {
                count ++;
                text2.SetActive(false);
                text3.SetActive(true);
                canvas.SetActive(false);
            } 
            else {
                canvas.SetActive(false);
            }
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class dialogueUpdate : MonoBehaviour
{
    int count = 0;
    public GameObject canvas;
    public GameObject text1;
    public GameObject text2;
    public GameObject text3;
    public GameObject text4;
    public GameObject text5;
    public GameObject text6;
    public GameObject text7;
    public GameObject text8;
    public GameObject text9;
    public GameObject text10;
    //interact with space button
    void Update()
    {
        if (Input.GetKeyDown("space")) {
            if (count == 0) {
                count ++;
                text1.SetActive(false);
                text2.SetActive(true);
            } else if (count == 1) {
                count ++;
                text2.SetActive(false);
                text3.SetActive(true);
            } else if (count == 2){
                count ++;
                text3.SetActive(false);
                text4.SetActive(true);
            } else if (count == 3){
                count ++;
                text4.SetActive(false);
                text5.SetActive(true);
            } else if (count == 4){
                count ++;
                text5.SetActive(false);
                text6.SetActive(true);
            } else if (count == 5){
                count ++;
                text6.SetActive(false);
                text7.SetActive(true);
            } else if (count == 6){
                count ++;
                text7.SetActive(false);
                text8.SetActive(true);
            } else if (count == 7){
                count ++;
                text8.SetActive(false);
                text9.SetActive(true);
            } else if (count == 8){
                count ++;
                text9.SetActive(false);
                text10.SetActive(true);
            } else {
                canvas.SetActive(false);
            }
        }
    }
}

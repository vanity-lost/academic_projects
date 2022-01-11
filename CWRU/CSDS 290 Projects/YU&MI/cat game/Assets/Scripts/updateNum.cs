using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class updateNum : MonoBehaviour
{
    public int number = 0;
    public Text text;

    // Update is called once per frame
    void Update()
    {
        text.text = "Objects to be broken: " + number + "/26";
    }
}

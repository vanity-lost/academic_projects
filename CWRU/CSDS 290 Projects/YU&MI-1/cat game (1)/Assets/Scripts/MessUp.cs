using System.Collections;
using System.Collections.Generic;
using UnityEngine;
// using TMPro;

public class MessUp : MonoBehaviour
{
    public float turnSpeed = 50f;
    private float degrees = 0;
    public GameObject value;
    bool isBroken = false;

    // Update is called once per frame
    void Update()
    {
        
        if(Input.GetKey(KeyCode.J))
        {
            while (degrees < 90){
			    degrees += Time.deltaTime * turnSpeed;
			    transform.Rotate(new Vector3(0 , Time.deltaTime * turnSpeed ,0));
                }
            if (degrees >= 90) {
                if (!isBroken) {
                    isBroken = true;
                    value.GetComponent<AngryBar>().addCount();
                }
            }
            // transform.Rotate(Vector3.up,turnSpeed * Time.deltaTime);
            
        }
    }
    // void onCollisionEnter2D(Collision col)
    // {
    //     if(col.gameObject.name == "Cat")
    //     {
    //         if(Input.GetKey(KeyCode.J))
    //             transform.Rotate(Vector3.up,turnSpeed * Time.deltaTime);
    //     }            
    // }
}

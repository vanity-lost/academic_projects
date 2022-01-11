using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class objectDetection : MonoBehaviour
{

    public Transform player;
    Transform obj;

    // Update is called once per frame
    void Update()
    {
        player = GetComponent<Transform>();
        Vector2 playerPos = player.position;
        obj = this.GetComponent<Transform>();
        Vector2 objPos = obj.position;
    }
}

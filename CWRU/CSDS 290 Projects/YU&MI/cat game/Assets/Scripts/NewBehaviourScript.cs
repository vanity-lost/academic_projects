using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Pathfinding;
using System.Threading;

public class NewBehaviourScript : MonoBehaviour
{
    public Transform owner;
    public float speed;
    public Transform[] moveSpots;
    public float nextWayPointDistance = 3;
    private int ctr = 0;
    Path path;
    int currentWayPoint;
    bool reachedEndOfPath = false;

    Seeker seeker;
    Rigidbody2D rb;

    public bool isMove2 = false;

    public void changeSpeed(float annoyance) {
        speed = 1000 + annoyance * 10f;
    }

    // Start is called before the first frame update
    void Start()
    {
        //randomSpot = Random.Range(0, moveSpots.Length);
        speed = 1000f;
        seeker = GetComponent<Seeker>();
        rb = GetComponent<Rigidbody2D>();

        InvokeRepeating("UpdatePath", 0f, 10f);
    }

    void UpdatePath()
    {
        if (seeker.IsDone())
        {
            seeker.StartPath(rb.position, moveSpots[Random.Range(0, 82)].position, OnPathComplete);
        }
    }

    void OnPathComplete(Path p)
    {
        if (!p.error)
        {
            // randomSpot = Random.Range(0, 82);
            path = p;
            currentWayPoint = 0;
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (path == null)
        {
            isMove2 = false;
            return;
        }

        if (currentWayPoint >= path.vectorPath.Count)
        {
            reachedEndOfPath = true;
            isMove2 = false;
            return;
        }
        else
        {
            reachedEndOfPath = false;
        }

        Vector2 direction = ((Vector2)path.vectorPath[currentWayPoint] - rb.position).normalized;
        Vector2 force = direction * speed * Time.fixedDeltaTime;

        float distance = Vector2.Distance(rb.position, path.vectorPath[currentWayPoint]);
        isMove2 = true;
        rb.AddForce(force);

        if (distance < nextWayPointDistance)
        {
            currentWayPoint++;
        }
    }
}

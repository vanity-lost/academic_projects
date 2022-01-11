using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Pathfinding;

public class EnemyAI : MonoBehaviour
{

    public Transform target;
    public float speed = 100f;
    public float nextWayPointDistance = 3;

    Path path = null;
    int currentWayPoint = 0;
    bool reachedEndOfPath = false;

    Seeker seeker;
    Rigidbody2D rb;

    public bool isMove1 = false;

    public void changeSpeed(float annoyance) {
        speed = 900 + annoyance * 10f;
    }

    // Start is called before the first frame update
    void Start()
    {
        seeker = GetComponent<Seeker>();
        rb = GetComponent<Rigidbody2D>();

        InvokeRepeating("UpdatePath", 0f, 0.5f);
    }

    void UpdatePath()
    {
        if (seeker.IsDone())
        {
            seeker.StartPath(rb.position, target.position, OnPathComplete);
        }
    }

    void OnPathComplete(Path p)
    {
        if (!p.error)
        {
            path = p;
            currentWayPoint = 0;
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (path == null) {
            reachedEndOfPath = true;
            isMove1 = false;
            return;
        }
        if (currentWayPoint >= path.vectorPath.Count) {
            reachedEndOfPath = true;
            isMove1 = false;
            return;
        } else
        {
            reachedEndOfPath = false;
        }

        Vector2 direction = ((Vector2) path.vectorPath[currentWayPoint] - rb.position).normalized;
        Vector2 force = direction * speed * Time.deltaTime;

        float distance = Vector2.Distance(rb.position, path.vectorPath[currentWayPoint]);
        isMove1 = true;
        rb.AddForce(force);

        if (distance < nextWayPointDistance)
        {
            currentWayPoint++;
        }
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;
using UnityEngine.SceneManagement;

public class PlayerMovement : MonoBehaviour
{
    public float speed = 5f;
    Vector2 movement;
    public Rigidbody2D rigid;
    public Animator animate;
    private int brokenItems = 0;
    private int caught = 0;
    public GameObject value;
    public GameObject gameOver;
    public GameObject NumberOfObjects;
    public GameObject transi;
    public GameObject inter;
    public GameObject dialogueUpdate;

    public GameObject Step1;
    public GameObject Step2;

    public int t_items = 0;

    private bool set1 = false;
    private bool set2 = false;

    private void Start()
    {
        Time.timeScale = 1f;
        rigid = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        movement.x = Input.GetAxisRaw("Horizontal");
        movement.y = Input.GetAxisRaw("Vertical");

        animate.SetFloat("Horizontal", movement.x);
        animate.SetFloat("Vertical", movement.y);
        animate.SetFloat("Speed", movement.sqrMagnitude);

        Vector3 pos3 = rigid.position;
        if (Input.GetMouseButtonDown(0) && charHit)
        {
            Scene scene = SceneManager.GetActiveScene();
            if (scene.name == "Outside")
            {
                charHit = false;
                Destroy(to_be_destroyed);
                t_items++;
                if (t_items >= 13)
                {
                    inter.SetActive(true);
                    transi.SetActive(true);
                }
            }
            else if (scene.name == "main")
            {
                value.GetComponent<AngryBar>().addCount();
                brokenItems++;
                NumberOfObjects.GetComponent<updateNum>().number = brokenItems;
                charHit = false;
                Destroy(to_be_destroyed);
            }
        }
        if (brokenItems == 3 && !set1)
        {
            Time.timeScale = 0f;
            Step1.SetActive(true);
            if (Input.GetKeyDown(KeyCode.Space))
            {
                Step1.SetActive(false);
                set1 = true;
                Time.timeScale = 1f;
            }
        }
        if (brokenItems == 10 && !set2)
        {
            Time.timeScale = 0f;
            Step2.SetActive(true);
            if (Input.GetKeyDown(KeyCode.Space))
            {
                Step2.SetActive(false);
                set2 = true;
                Time.timeScale = 1f;
            }
        }
        if (brokenItems >= 26)
        {
            SceneManager.LoadScene("UI End");
        }
    }

    void FixedUpdate()
    {
        rigid.MovePosition(rigid.position + movement * speed * Time.fixedDeltaTime);
    }

    private bool charHit;
    private GameObject to_be_destroyed;
    private Collider2D collider;

    private void OnTriggerEnter2D(Collider2D other)
    {
        collider = other;
        Debug.Log("FIRST HIT");
        if (other.gameObject.CompareTag("prefabs"))
        {
            to_be_destroyed = other.gameObject;
            charHit = true;
            //debug purpose
            Debug.Log("Hit: " + other.gameObject.name);
            Debug.Log("Cat: " + rigid.position);

        }
        if (other.gameObject.CompareTag("Owner") && value.GetComponent<AngryBar>().annoyance > 35)
        {
            caught ++;
            if (caught == 4)
            {
                gameOver.SetActive(true);
            }
        }
        if (other.gameObject.CompareTag("NPC"))
        {
            talk();
        }
    }

    void talk()
    {
        dialogueUpdate.SetActive(true);
    }
}

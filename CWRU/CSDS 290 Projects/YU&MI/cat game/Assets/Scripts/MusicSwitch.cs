 using UnityEngine;
 using System.Collections;
 
 public class MusicSwitch : MonoBehaviour 
 {
     
     public AudioSource _AudioSource;
 
     public AudioClip _AudioClip1;
     public AudioClip _AudioClip2;
     bool isMove1, isMove2;
     public GameObject enemy;
     bool trigger = false;
 
     void Start() 
     {
         _AudioSource.clip = _AudioClip1;
 
         _AudioSource.Play();     
     }
 
     void Update () 
     {
         isMove1 = enemy.GetComponent<EnemyAI>().isMove1;
         isMove2 = enemy.GetComponent<NewBehaviourScript>().isMove2;
 
        if ((isMove1 || isMove2) && !trigger)
        {
            trigger = true;

            _AudioSource.clip = _AudioClip2;
 
            _AudioSource.Play();
        } else if (!(isMove1 || isMove2) && trigger) {
            trigger = false;
            
            _AudioSource.clip = _AudioClip1;
 
            _AudioSource.Play();
        }
     
     }
 
 }
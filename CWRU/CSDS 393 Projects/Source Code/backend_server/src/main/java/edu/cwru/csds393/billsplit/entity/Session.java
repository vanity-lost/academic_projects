package edu.cwru.csds393.billsplit.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import javax.persistence.*;
import java.util.Date;

@Entity
public class Session {
    @Id
    @GeneratedValue
    @JsonIgnore
    private Long id;

    @Column(unique = true)
    private String token;

    @ManyToOne
    @JoinColumn(nullable = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    private Account account;

    @LastModifiedDate
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastActive;

    @CreatedDate
    @Temporal(TemporalType.TIMESTAMP)
    private Date created;

    public Session() {
    }

    public Session(String token, Account account) {
        this.token = token;
        this.account = account;
        this.created = new Date();
        this.lastActive = new Date();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public Account getAccount() {
        return account;
    }

    public void setAccount(Account account) {
        this.account = account;
    }

    public Date getLastActive() {
        return lastActive;
    }

    public void setLastActive(Date lastActive) {
        this.lastActive = lastActive;
    }

    public Date getCreated() {
        return created;
    }

    public void setCreated(Date created) {
        this.created = created;
    }
}

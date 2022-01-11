package edu.cwru.csds393.billsplit.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;

@Entity
public class ResetToken {
    @Id
    @GeneratedValue
    @JsonIgnore
    private Long id;

    private String token;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(unique = true, nullable = false)
    private Account account;

    public ResetToken(String token, Account account) {
        this.token = token;
        this.account = account;
    }

    public ResetToken() { }

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
}

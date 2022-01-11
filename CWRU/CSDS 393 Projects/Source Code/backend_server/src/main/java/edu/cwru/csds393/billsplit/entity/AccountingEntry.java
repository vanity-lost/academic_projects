package edu.cwru.csds393.billsplit.entity;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

@Entity
public class AccountingEntry {
    @Id
    @GeneratedValue
    private Long id;

    private double amount;

    private String description;

    @Temporal(TemporalType.TIMESTAMP)
    private Date date;

    @ManyToOne
    @JoinColumn
    private Category category;

    @ManyToOne
    @JoinColumn
    private Account author;

    @ManyToMany
    @JoinTable
    private List<Account> participants;

    @ManyToOne
    @JoinColumn
    @OnDelete(action = OnDeleteAction.CASCADE)
    private AccountingBook accountingBook;

    public AccountingEntry() {}

    public AccountingEntry(double amount, String description, Category category, Date date, Account author, List<Account> participants, AccountingBook accountingBook) {
        this.amount = amount;
        this.description = description;
        this.category = category;
        this.author = author;
        this.participants = participants;
        this.accountingBook = accountingBook;
        this.date = date;
    }

    public Long getId() {
        return id;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Category getCategory() {
        return category;
    }

    public void setCategory(Category category) {
        this.category = category;
    }

    public Account getAuthor() {
        return author;
    }

    public void setAuthor(Account author) {
        this.author = author;
    }

    public List<Account> getParticipants() {
        return participants;
    }

    public void setParticipants(List<Account> participants) {
        this.participants = participants;
    }

    public AccountingBook getAccountingBook() {
        return accountingBook;
    }

    public void setAccountingBook(AccountingBook accountingBook) {
        this.accountingBook = accountingBook;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }
}

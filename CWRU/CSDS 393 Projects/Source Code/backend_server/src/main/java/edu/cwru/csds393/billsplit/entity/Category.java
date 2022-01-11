package edu.cwru.csds393.billsplit.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.ManyToOne;

@Entity
public class Category {
    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToOne
    @JsonIgnore
    private AccountingBook belongsTo;

    public Category() {}

    public Category(String name, AccountingBook belongsTo) {
        this.name = name;
        this.belongsTo = belongsTo;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public AccountingBook getBelongsTo() {
        return belongsTo;
    }

    public void setBelongsTo(AccountingBook belongsTo) {
        this.belongsTo = belongsTo;
    }
}

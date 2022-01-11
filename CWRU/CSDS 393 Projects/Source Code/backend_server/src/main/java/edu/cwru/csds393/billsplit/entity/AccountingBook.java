package edu.cwru.csds393.billsplit.entity;

import com.fasterxml.jackson.annotation.JsonIdentityReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import org.hibernate.annotations.Fetch;

import javax.persistence.*;
import java.util.List;
import java.util.Objects;

@Entity
public class AccountingBook {

    @Id
    @GeneratedValue
    private Long id;

    private String name;

    @ManyToOne
    @JoinColumn
    @JsonIdentityReference(alwaysAsId=true)
    private Account owner;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable
    @JsonIdentityReference(alwaysAsId=true)
    private List<Account> members;

    @OneToMany(mappedBy = "accountingBook")
    @JsonIgnore
    private List<AccountingEntry> entries;

    public void setId(Long id) {
        this.id = id;
    }

    public List<AccountingEntry> getEntries() {
        return entries;
    }

    public void setEntries(List<AccountingEntry> entries) {
        this.entries = entries;
    }

    public AccountingBook(String name, Account owner, List<Account> members) {
        this.name = name;
        this.owner = owner;
        this.members = members;
    }

    public AccountingBook() {
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

    public Account getOwner() {
        return owner;
    }

    public void setOwner(Account owner) {
        this.owner = owner;
    }

    public List<Account> getMembers() {
        return members;
    }

    public void setMembers(List<Account> viewer) {
        this.members = viewer;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AccountingBook that = (AccountingBook) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

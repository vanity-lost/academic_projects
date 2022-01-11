package edu.cwru.csds393.billsplit.model;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.AccountingBook;
import edu.cwru.csds393.billsplit.entity.Category;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class EditEntryRequest {
    @Positive
    @NotNull
    private double amount;

    @NotEmpty
    @NotNull
    private String description;

    @NotNull
    private Date date;

    @NotNull
    private Long categoryId;

    @NotEmpty
    @NotNull
    private String author;

    @NotNull
    private List<String> participants = new ArrayList<>();

    @NotNull
    private Long accountingBookId;

    private Long entryId;

    public double getAmount() {
        return amount;
    }

    public String getDescription() {
        return description;
    }

    public Long getEntryId() {
        return entryId;
    }

    public Long getCategoryId() {
        return categoryId;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getAuthor() {
        return author;
    }

    public List<String> getParticipants() {
        return participants;
    }

    public Long getAccountingBookId() {
        return accountingBookId;
    }
}

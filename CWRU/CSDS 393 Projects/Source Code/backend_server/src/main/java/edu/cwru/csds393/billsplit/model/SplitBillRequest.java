package edu.cwru.csds393.billsplit.model;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

public class SplitBillRequest {
    @NotNull
    Long accountingBookId;

    @NotEmpty
    String username;

    public Long getAccountingBookId() {
        return accountingBookId;
    }

    public String getUsername() {
        return username;
    }
}

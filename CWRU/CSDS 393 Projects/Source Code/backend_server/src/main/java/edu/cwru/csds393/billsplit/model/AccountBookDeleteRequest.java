package edu.cwru.csds393.billsplit.model;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;

public class AccountBookDeleteRequest {
    @Positive
    @NotNull
    private Long bookId;

    public Long getBookId() {
        return bookId;
    }
}

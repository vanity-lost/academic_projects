package edu.cwru.csds393.billsplit.model;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;
import java.util.ArrayList;
import java.util.List;

public class AccountingBookMemberEditRequest {
    @NotNull
    @Positive
    private Long bookId;

    @NotNull
    private List<String> members = new ArrayList<>();

    public Long getBookId() {
        return bookId;
    }

    public List<String> getMembers() {
        return members;
    }

    public void setMembers(List<String> members) {
        this.members = members;
    }
}

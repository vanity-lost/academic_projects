package edu.cwru.csds393.billsplit.model;

public class EditCategoryRequest {
    private String name;
    private Long accountingBookId;

    private Long categoryId;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Long getAccountingBookId() {
        return accountingBookId;
    }

    public Long getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Long categoryId) {
        this.categoryId = categoryId;
    }
}

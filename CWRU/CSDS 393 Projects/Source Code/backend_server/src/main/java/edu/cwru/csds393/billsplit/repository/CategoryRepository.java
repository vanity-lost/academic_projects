package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.AccountingBook;
import edu.cwru.csds393.billsplit.entity.Category;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface CategoryRepository extends CrudRepository<Category, Long> {
    List<Category> findByBelongsTo(AccountingBook book);
}

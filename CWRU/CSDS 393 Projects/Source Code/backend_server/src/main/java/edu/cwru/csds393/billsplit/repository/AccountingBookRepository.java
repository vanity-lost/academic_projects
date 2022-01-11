package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.AccountingBook;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface AccountingBookRepository extends CrudRepository<AccountingBook, Long> {
    List<AccountingBook> findByOwnerOrMembersContainsOrderById(Account owner, Account viewer);
}

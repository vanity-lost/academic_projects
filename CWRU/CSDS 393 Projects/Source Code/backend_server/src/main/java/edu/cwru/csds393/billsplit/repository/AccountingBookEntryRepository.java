package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.AccountingEntry;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface AccountingBookEntryRepository extends CrudRepository<AccountingEntry, Long> {
    List<AccountingEntry> findByAccountingBookId(Long accountingBookId);
}

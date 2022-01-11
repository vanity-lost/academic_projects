package edu.cwru.csds393.billsplit.service;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.AccountingBook;
import edu.cwru.csds393.billsplit.entity.AccountingEntry;
import edu.cwru.csds393.billsplit.entity.Category;
import edu.cwru.csds393.billsplit.exception.InvalidRequestException;
import edu.cwru.csds393.billsplit.model.AccountBookCreateRequest;
import edu.cwru.csds393.billsplit.repository.AccountRepository;
import edu.cwru.csds393.billsplit.repository.AccountingBookEntryRepository;
import edu.cwru.csds393.billsplit.repository.AccountingBookRepository;
import edu.cwru.csds393.billsplit.repository.CategoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

@Service
public class AccountingService {
    private final AccountRepository accountRepo;
    private final AccountingBookRepository accountingBookRepo;
    private final CategoryRepository categoryRepo;
    private final AccountingBookEntryRepository entryRepo;

    public AccountingService(@Autowired AccountRepository accountRepo,
                             @Autowired AccountingBookRepository accountingBookRepo,
                             @Autowired CategoryRepository categoryRepo,
                             @Autowired AccountingBookEntryRepository entryRepo) {
        this.accountRepo = accountRepo;
        this.accountingBookRepo = accountingBookRepo;
        this.categoryRepo = categoryRepo;
        this.entryRepo = entryRepo;
    }

    public AccountingBook createAccountingBook(Account owner, AccountBookCreateRequest r) {
        List<String> viewer = r.getMembers();
        List<Account> accounts = new ArrayList<>();
        for (String s : viewer) {
            Optional<Account> acc = accountRepo.findByUsernameOrEmailOrPhone(s, s, s);
            if (!acc.isPresent()) {
                throw new InvalidRequestException("invalid username");
            }
            accounts.add(acc.get());
        }
        AccountingBook accountingBook = new AccountingBook(r.getName(), owner, accounts);
        accountingBook = accountingBookRepo.save(accountingBook);
        return accountingBook;
    }

    public void deleteAccountingBook(AccountingBook book) {
        accountingBookRepo.delete(book);
    }

    @Transactional
    public List<AccountingBook> listAccountingBookByAccount(Account acnt) {
        return accountingBookRepo.findByOwnerOrMembersContainsOrderById(acnt, acnt);
    }

    public Optional<AccountingBook> getAccountingBookCheckOwnerPerm(Long id, Account acnt) {
        Optional<AccountingBook> bookFind = accountingBookRepo.findById(id);
        if (bookFind.isPresent()) {
            AccountingBook book = bookFind.get();
            if (book.getOwner().getId().equals(acnt.getId())) {
                return Optional.of(book);
            }
        }
        return Optional.empty();
    }

    public Optional<AccountingBook> getAccountingBookCheckMemberPerm(Long id, Account acnt) {
        Optional<AccountingBook> bookFind = accountingBookRepo.findById(id);
        if (bookFind.isPresent()) {
            AccountingBook book = bookFind.get();
            if (book.getOwner().equals(acnt) || book.getMembers().contains(acnt)) {
                return Optional.of(book);
            }
        }
        return Optional.empty();
    }

    public Category addCategory(String name, AccountingBook book) {
        Category c = new Category(name, book);
        c = categoryRepo.save(c);
        return c;
    }

    public Category editCategoryName(Category c, String name) {
        c.setName(name);
        return categoryRepo.save(c);
    }

    public void deleteCategory(Category c) {
        categoryRepo.delete(c);
    }

    public AccountingEntry createAccountingEntry(double amount, String description, Category category, Date date,
                                                 Account author, List<Account> participants,
                                                 AccountingBook accountingBook) {
        AccountingEntry e = new AccountingEntry(amount, description, category, date, author, participants, accountingBook);
        return entryRepo.save(e);
    }

    public AccountingEntry editAccountingEntry(AccountingEntry entry, double amount, String description,
                                               Category category, Date date, Account author,
                                               List<Account> participants) {
        entry.setAmount(amount);
        entry.setDescription(description);
        entry.setCategory(category);
        entry.setDate(date);
        entry.setAuthor(author);
        entry.setParticipants(participants);
        return entryRepo.save(entry);
    }

    public void deleteAccountingEntry(AccountingEntry entry) {
        entryRepo.delete(entry);
    }
}

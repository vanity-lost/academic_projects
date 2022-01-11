package edu.cwru.csds393.billsplit.controller;

import edu.cwru.csds393.billsplit.annotation.Require;
import edu.cwru.csds393.billsplit.authentication.AuthContext;
import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.AccountingBook;
import edu.cwru.csds393.billsplit.entity.AccountingEntry;
import edu.cwru.csds393.billsplit.entity.Category;
import edu.cwru.csds393.billsplit.exception.InvalidRequestException;
import edu.cwru.csds393.billsplit.model.*;
import edu.cwru.csds393.billsplit.repository.AccountRepository;
import edu.cwru.csds393.billsplit.repository.AccountingBookEntryRepository;
import edu.cwru.csds393.billsplit.repository.AccountingBookRepository;
import edu.cwru.csds393.billsplit.repository.CategoryRepository;
import edu.cwru.csds393.billsplit.service.AccountingService;
import edu.cwru.csds393.billsplit.service.AuthService;
import org.hibernate.Hibernate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.persistence.EntityManager;
import javax.persistence.EntityNotFoundException;
import javax.persistence.PersistenceContext;
import javax.transaction.Transactional;
import javax.validation.Valid;
import java.util.*;

@RequestMapping("/book")
@RestController
public class AccountingController {
    final AccountingService accountingService;
    private final AuthService authService;
    private final CategoryRepository categoryRepo;
    private final AccountRepository accountRepo;
    private final AccountingBookEntryRepository entryRepo;
    private final AccountingBookRepository accountingBookRepo;

    @PersistenceContext
    private EntityManager em;

    public AccountingController(@Autowired AccountingService accountingService,
                                @Autowired AuthService authService,
                                @Autowired CategoryRepository categoryRepo,
                                @Autowired AccountRepository accountRepo,
                                @Autowired AccountingBookEntryRepository entryRepo,
                                @Autowired AccountingBookRepository accountingBookRepo) {
        this.accountingService = accountingService;
        this.authService = authService;
        this.categoryRepo = categoryRepo;
        this.accountRepo = accountRepo;
        this.entryRepo = entryRepo;
        this.accountingBookRepo = accountingBookRepo;
    }

    @Require
    @RequestMapping(value = "/create", method = RequestMethod.POST)
    @ResponseBody
    public ResponseObject<AccountingBook> handleCreateBookRequest(AuthContext ctx, @RequestBody @Valid AccountBookCreateRequest r) {
        if (r.getMembers() == null) {
            r.setMembers(new ArrayList<>(0));
        }
        return new ResponseObject<AccountingBook>(accountingService.createAccountingBook(ctx.getSession().getAccount(), r));
    }

    @Require
    @RequestMapping(value = "/delete", method = RequestMethod.DELETE)
    @ResponseBody
    public ResponseObject<Void> handleDeleteBookRequest(AuthContext ctx, @RequestBody @Valid AccountBookDeleteRequest r) {
        Optional<AccountingBook> find = accountingService.getAccountingBookCheckMemberPerm(r.getBookId(), ctx.getSession().getAccount());
        if (!find.isPresent()) {
            throw new InvalidRequestException("Either no such book is found or you have no permission to edit it.");
        }
        accountingService.deleteAccountingBook(find.get());
        return ResponseObject.Success(null);
    }

    @Require
    @RequestMapping(value = "/list", method = RequestMethod.GET)
    @ResponseBody
    @Transactional
    public ResponseObject<List<AccountingBook>> handleListAccountingBook(AuthContext ctx) {
        return ResponseObject.Success(accountingService.listAccountingBookByAccount(ctx.getSession().getAccount()));
    }

    @Require
    @RequestMapping(value = "/member", method = RequestMethod.POST)
    @Transactional
    @ResponseBody
    public ResponseObject<AccountingBook> handleSetMemberRequest(@RequestBody @Valid AccountingBookMemberEditRequest r, AuthContext ctx) {
        Optional<AccountingBook> acntBook = accountingService.getAccountingBookCheckOwnerPerm(r.getBookId(), ctx.getSession().getAccount());

        if (!acntBook.isPresent())
            throw new InvalidRequestException("Either no such book is found or you have no permission to edit it.");

        AccountingBook book = acntBook.get();

        try {
            book.getMembers().clear();
            book.getMembers().addAll(authService.locateAccounts(r.getMembers()));
            book = this.accountingBookRepo.save(book);
        } catch (EntityNotFoundException e) {
            throw new InvalidRequestException(e.getMessage());
        }
        // Check perm
        return ResponseObject.Success(book);
    }

    @Require
    @RequestMapping(value = "/category/add", method = RequestMethod.POST)
    @ResponseBody
    // name, accounting book id
    public ResponseObject<Category> handleAddCategoryRequest(@RequestBody EditCategoryRequest r, AuthContext ctx) {
        if (r.getName() == null || r.getName().isEmpty()) {
            throw new InvalidRequestException("Category name is empty.");
        }
        Optional<AccountingBook> find = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        if (!find.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }
        //Account acc = ctx.getSession().getAccount();

        Category c = accountingService.addCategory(r.getName(), find.get());
        return ResponseObject.Success(c);
    }

    @Require
    @RequestMapping(value = "/category/edit", method = RequestMethod.POST)
    @ResponseBody
    // name, category id
    public ResponseObject<Category> handleEditCategoryRequest(@RequestBody EditCategoryRequest r, AuthContext ctx) {
        if (r.getName() == null || r.getName().isEmpty()) {
            throw new InvalidRequestException("Category new name is empty.");
        }
        if (r.getCategoryId() == null) {
            throw new InvalidRequestException("Need category id.");
        }

        Category c = categoryRepo.findById(r.getCategoryId()).get();

        Account acc = ctx.getSession().getAccount();
        if (!c.getBelongsTo().getOwner().equals(acc) && !c.getBelongsTo().getMembers().contains(acc)) {
            throw new InvalidRequestException("You have no permission to edit the accounting book");
        }

        return ResponseObject.Success(accountingService.editCategoryName(c, r.getName()));
    }

    @Require
    @RequestMapping(value = "/category/delete", method = RequestMethod.DELETE)
    @ResponseBody
    // category id
    public ResponseObject<Void> handleDeleteCategoryRequest(@RequestBody EditCategoryRequest r, AuthContext ctx) {
        if (r.getCategoryId() == null) {
            throw new InvalidRequestException("Need category id.");
        }
        Optional<Category> findCategory = categoryRepo.findById(r.getCategoryId());
        if (!findCategory.isPresent()) {
            throw new InvalidRequestException("Category does not exit.");
        }
        Category c = findCategory.get();

        Account acc = ctx.getSession().getAccount();
        if (!c.getBelongsTo().getOwner().equals(acc) && !c.getBelongsTo().getMembers().contains(acc)) {
            throw new InvalidRequestException("You have no permission to edit the accounting book");
        }
        accountingService.deleteCategory(c);
        return ResponseObject.Success(null);
    }

    @Require
    @RequestMapping(value = "/category/list", method = RequestMethod.POST)
    @ResponseBody
    // accounting book id
    public ResponseObject<List<Category>> handleListCategoryRequest(AuthContext ctx, @RequestBody EditCategoryRequest r) {
        Optional<AccountingBook> bookFind = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        if (!bookFind.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }

        return ResponseObject.Success(categoryRepo.findByBelongsTo(bookFind.get()));
    }

    @Require
    @RequestMapping(value = "/entry/add", method = RequestMethod.POST)
    @ResponseBody
    // individual: amount, (description), (category), date, (author), (participants), accounting book id
    // group: amount, (description), (category), date, author, participants, accounting book id
    public ResponseObject<AccountingEntry> handleAddEntryRequest(AuthContext ctx, @RequestBody @Valid EditEntryRequest r) {

        // 1. Check if book is valid & has perm
        Optional<AccountingBook> findBook = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        if (!findBook.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }
        AccountingBook book = findBook.get();

        // 2. Check category is valid.
        Optional<Category> findCategory = categoryRepo.findById(r.getCategoryId());
        if (findCategory.isPresent()) {
            if (!findCategory.get().getBelongsTo().equals(findBook.get())) {
                throw new InvalidRequestException("Illegal category.");
            }
        } else {
            throw new InvalidRequestException("Invalid category.");
        }

        // check account info
        Optional<Account> authorAccount = accountRepo.findByUsername(r.getAuthor());
        if (!authorAccount.isPresent()) {
            throw new InvalidRequestException("Account does not exist.");
        }

        List<Account> pp = null;
        try {
            pp = authService.locateAccounts(r.getParticipants());
        } catch (EntityNotFoundException e) {
            throw new InvalidRequestException(e.getMessage());
        }
        assert pp != null;

        boolean allAccountsInBook = pp.stream()
                .allMatch(account -> book.getMembers().contains(account) || book.getOwner().equals(account));
        if (!allAccountsInBook) {
            throw new InvalidRequestException("Participants must all be members of this book.");
        }

        AccountingEntry e = accountingService.createAccountingEntry(r.getAmount(), r.getDescription(),
                findCategory.get(), r.getDate(), authorAccount.get(), pp, book);
        return ResponseObject.Success(e);
    }

    @Require
    @RequestMapping(value = "/entry/edit", method = RequestMethod.POST)
    @ResponseBody
    @Transactional
    public ResponseObject<AccountingEntry> handleEditEntryRequest(AuthContext ctx, @RequestBody @Valid EditEntryRequest r) {

        // 1. Check
        Optional<AccountingEntry> findEntry = entryRepo.findById(r.getEntryId());
        if (!findEntry.isPresent()) {
            throw new InvalidRequestException("Invalid entry.");
        }
        Optional<AccountingBook> findBook = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        Optional<Category> findCategory = categoryRepo.findById(r.getCategoryId());
        Optional<Account> authorAccount = accountRepo.findByUsername(r.getAuthor());
        List<String> participants = r.getParticipants();
        List<Account> participantsAccounts = new ArrayList<>(participants.size());
        // This method throws exceptions on error
        checkAccountingEntryRequestCommon(findBook, findCategory, authorAccount, participants, participantsAccounts);
        AccountingEntry e = findEntry.get();
        e = accountingService.editAccountingEntry(e, r.getAmount(), r.getDescription(), findCategory.get(), r.getDate(), authorAccount.get(),
                participantsAccounts);
        return ResponseObject.Success(e);
    }

    @Require
    @RequestMapping(value = "/entry/delete", method = RequestMethod.DELETE)
    @ResponseBody
    // entry id
    public ResponseObject<Void> handleDeleteEntryRequest(AuthContext ctx, @RequestBody EditEntryRequest r) {
        // 1. Check
        Optional<AccountingEntry> findEntry = entryRepo.findById(r.getEntryId());
        if (!findEntry.isPresent()) {
            throw new InvalidRequestException("Invalid entry.");
        }
        AccountingEntry e = findEntry.get();
        AccountingBook book = e.getAccountingBook();
        Optional<AccountingBook> findBook = accountingService.getAccountingBookCheckMemberPerm(book.getId(), ctx.getSession().getAccount());
        if (!findBook.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }

        accountingService.deleteAccountingEntry(e);
        return ResponseObject.Success(null);
    }

    @Require
    @RequestMapping(value = "/entry/list", method = RequestMethod.POST)
    @ResponseBody
    @Transactional
    // accounting book id
    public ResponseObject<List<AccountingEntry>> handleListEntryRequest(AuthContext ctx, @RequestBody EditEntryRequest r) {
        // 1. Check
        Optional<AccountingBook> findBook = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        if (!findBook.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }
        List<AccountingEntry> entries = entryRepo.findByAccountingBookId(r.getAccountingBookId());
        for (AccountingEntry e : entries) {
            Hibernate.initialize(e.getParticipants());
        }
        return ResponseObject.Success(entries);
    }

    public void checkAccountingEntryRequestCommon(Optional<AccountingBook> findBook, Optional<Category> findCategory, Optional<Account> authorAccount,
                                                     List<String> participants, List<Account> participantsReturn) {
        // 1. Check if book is valid & has perm
        if (!findBook.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }
        AccountingBook book = findBook.get();

        // 2. Check category is valid.
        if (findCategory.isPresent()) {
            if (!findCategory.get().getBelongsTo().equals(findBook.get())) {
                throw new InvalidRequestException("Illegal category.");
            }
        } else {
            throw new InvalidRequestException("Invalid category.");
        }

        // check account info
        if (!authorAccount.isPresent()) {
            throw new InvalidRequestException("Account does not exist.");
        }

        try {
            participantsReturn.addAll(authService.locateAccounts(participants));
        } catch (EntityNotFoundException e) {
            throw new InvalidRequestException(e.getMessage());
        }

        boolean allAccountsInBook = participantsReturn.stream()
                .allMatch(account -> book.getMembers().contains(account) || book.getOwner().equals(account));
        if (!allAccountsInBook) {
            throw new InvalidRequestException("Participants must all be members of this book.");
        }
    }

    @Require
    @RequestMapping(value = "/split", method = RequestMethod.POST)
    @Transactional
    @ResponseBody
    // accounting book id, username
    public ResponseObject<Map<String, Double>> handleSplitBillRequest(AuthContext ctx, @RequestBody SplitBillRequest r) {
        // 1. Check if book is valid & has perm
        Optional<AccountingBook> findBook = accountingService.getAccountingBookCheckMemberPerm(r.getAccountingBookId(), ctx.getSession().getAccount());
        if (!findBook.isPresent()) {
            throw new InvalidRequestException("The accounting book does not exist or you have no permission to edit it.");
        }

        // 2. Check if the user belongs to the accounting book (username)
        Optional<Account> findAccount = accountRepo.findByUsername(r.getUsername());
        if (!findAccount.isPresent()) {
            throw new InvalidRequestException("Account does not exist.");
        }
        Account acc = findAccount.get();
        AccountingBook book = findBook.get();
        if(!book.getOwner().equals(acc) && !book.getMembers().contains(acc)) {
            throw new InvalidRequestException("This user is not a member of this accounting book");
        }

        List<AccountingEntry> entries = book.getEntries();
        double amount = 0;
        for (int i = 0; i < entries.size(); i++) {
            if (entries.get(i).getParticipants().contains(acc)) {
                int countParticipants = entries.get(i).getParticipants().size();
                double splitAmount = entries.get(i).getAmount() / countParticipants;
                amount += splitAmount;
            }
        }

        Map<String, Double> accountMoneySplit = new HashMap<>();
        accountMoneySplit.put(r.getUsername(), amount);

        return ResponseObject.Success(accountMoneySplit);
    }
}

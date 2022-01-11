package edu.cwru.csds393.billsplit.service;

import edu.cwru.csds393.billsplit.BillSplitTestConfiguration;
import edu.cwru.csds393.billsplit.BillsplitBackendApplication;
import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.AccountingBook;
import edu.cwru.csds393.billsplit.model.AccountBookCreateRequest;
import edu.cwru.csds393.billsplit.util.TestingUtil;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;

import javax.transaction.Transactional;
import java.util.List;

import static org.junit.Assert.*;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {BillsplitBackendApplication.class})
@Import(BillSplitTestConfiguration.class)
@Transactional
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
public class AccountingServiceTest {

    @Autowired
    private AuthService authService;

    @Autowired
    private AccountingService accountingService;

    /**
     * Test description:
     * Creates 2 accounts, and 2 accounting books.
     * All books are created under account 1.
     * Book1 should be owned by 1 and viewable by 2.
     * Book2 should be owned by 1 and no one else.
     * 1 should see both books when listing.
     * 2 should see only book 1.
     */
    @Test
    public void testBookVisibility() {
        Account account1 = TestingUtil.createAccount(authService);
        Account account2 = TestingUtil.createAccount(authService);
        Account account3 = TestingUtil.createAccount(authService);

        AccountBookCreateRequest request = new AccountBookCreateRequest();

        request.setName("Test Book 1");
        request.getMembers().add(account2.getUsername());
        AccountingBook book1 = accountingService.createAccountingBook(account1, request);
        assertNotNull("Test Book 1 creation failed", book1);

        request.setName("Test Book 2");
        request.getMembers().clear();
        assertNotNull("Test Book 2 creation failed", accountingService.createAccountingBook(account1, request));

        List<AccountingBook> account1View = accountingService.listAccountingBookByAccount(account1);
        assertNotNull("Account 1 view is null", account1View);
        assertEquals(2, account1View.size());

        List<AccountingBook> account2View = accountingService.listAccountingBookByAccount(account2);
        assertNotNull("Account 2 view is null", account2View);
        assertEquals(1, account2View.size());
        List<AccountingBook> account3View = accountingService.listAccountingBookByAccount(account3);
        assertNotNull("Account 3 view is null", account3View);
        assertEquals("Account 3 has invalid count of books", 0, account3View.size());

        long book1Id = book1.getId();
        assertTrue("Account1 should have member perm for book1",
                accountingService.getAccountingBookCheckMemberPerm(book1Id, account1).isPresent());
        assertTrue("Account1 should have owner perm for book1",
                accountingService.getAccountingBookCheckOwnerPerm(book1Id, account1).isPresent());
        assertTrue("Account2 should have member perm for book1",
                accountingService.getAccountingBookCheckMemberPerm(book1Id, account2).isPresent());
        assertFalse("Account2 should not have owner perm for book1",
                accountingService.getAccountingBookCheckOwnerPerm(book1Id, account2).isPresent());
        assertFalse("Account3 should not have member perm for book1",
                accountingService.getAccountingBookCheckMemberPerm(book1Id, account3).isPresent());
        assertFalse("Account3 should not have owner perm for book1",
                accountingService.getAccountingBookCheckOwnerPerm(book1Id, account3).isPresent());

        assertFalse("Shouldn't be able to find a non-existing book",
                accountingService.getAccountingBookCheckOwnerPerm(-1L, account1).isPresent());
        assertFalse("Shouldn't be able to find a non-existing book",
                accountingService.getAccountingBookCheckMemberPerm(-1L, account1).isPresent());
    }
}

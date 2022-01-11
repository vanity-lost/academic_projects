package edu.cwru.csds393.billsplit.util;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.model.RegisterRequest;
import edu.cwru.csds393.billsplit.service.AuthService;

public class TestingUtil {

    private static long ID = 0;

    public static Account createAccount(AuthService authService) {
        ID++;
        RegisterRequest r = new RegisterRequest();
        r.setUsername("testAccount" + ID);
        r.setPassword("12345678");
        r.setEmail("test_" + ID + "@test.com");
        r.setPhone(null);
        return authService.registerUser(r);
    }
}

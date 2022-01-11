package edu.cwru.csds393.billsplit.exception;

import org.springframework.http.HttpStatus;

public class AuthenticationException extends RequestException {
    public AuthenticationException(String code, String message) {
        super(HttpStatus.UNAUTHORIZED, code, message);
    }
}

package edu.cwru.csds393.billsplit.exception;

import edu.cwru.csds393.billsplit.model.ResponseObject;
import org.springframework.http.HttpStatus;

public class AuthorizationException extends RequestException {
    public AuthorizationException(String message) {
        super(HttpStatus.FORBIDDEN, ResponseObject.CODE_INVALID_TOKEN, message);
    }
}

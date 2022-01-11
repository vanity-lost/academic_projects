package edu.cwru.csds393.billsplit.exception;

import edu.cwru.csds393.billsplit.model.ResponseObject;
import org.springframework.http.HttpStatus;

public class InvalidRequestException extends RequestException {
    public InvalidRequestException(String message) {
        super(HttpStatus.BAD_REQUEST, ResponseObject.CODE_INVALID_REQUEST, message);
    }
}

package edu.cwru.csds393.billsplit.exception;

import org.springframework.http.HttpStatus;

public class RequestException extends RuntimeException {
    private String code;
    private HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;

    public RequestException(String code, String message) {
        super(message);
        this.code = code;
    }

    public RequestException(HttpStatus status, String code, String message) {
        super(message);
        this.code = code;
        this.status = status;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public HttpStatus getStatus() {
        return status;
    }

    public void setStatus(HttpStatus status) {
        this.status = status;
    }
}

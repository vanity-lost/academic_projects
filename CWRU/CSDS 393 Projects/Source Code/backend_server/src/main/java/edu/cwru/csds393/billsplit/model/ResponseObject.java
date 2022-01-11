package edu.cwru.csds393.billsplit.model;

public class ResponseObject<T> {
    public static final String CODE_SUCCESS = "SUCCESS";
    public static final String CODE_INVALID_REQUEST = "INVALID_REQUEST_PARAM";
    public static final String CODE_INVALID_CREDENTIALS = "INVALID_CREDENTIALS";
    public static final String CODE_INVALID_TOKEN = "INVALID_TOKEN";
    public static final String CODE_UNKNOWN_ERROR = "UNKNOWN_ERROR";


    private String code;
    private String message;
    private T data;

    public ResponseObject(T data) {
        this.code = CODE_SUCCESS;
        this.message = "";
        this.data = data;
    }

    public ResponseObject(String code, String message) {
        this.code = code;
        this.message = message;
        this.data = null;
    }

    public ResponseObject(String code, T data) {
        this.code = code;
        this.message = "";
        this.data = data;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public static <T> ResponseObject<T> Success(T data) {
        return new ResponseObject<T>(data);
    }
}

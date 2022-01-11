package edu.cwru.csds393.billsplit.exception;

import edu.cwru.csds393.billsplit.model.ResponseObject;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import javax.servlet.http.HttpServletRequest;

@ControllerAdvice
@Order(Ordered.HIGHEST_PRECEDENCE)
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    @ExceptionHandler(RequestException.class)
    @ResponseBody
    public ResponseEntity<ResponseObject<Object>> handleRequestException(
            HttpServletRequest req,
            RequestException e
    ) {
        if (e == null) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ResponseObject<>(ResponseObject.CODE_UNKNOWN_ERROR,
                            "Unexpected Exception Occurred"));
        }
        return ResponseEntity.status(e.getStatus()).body(
                new ResponseObject<>(e.getCode(), e.getMessage())
        );
    }

    @Override
    protected ResponseEntity<Object> handleExceptionInternal(Exception ex, Object body, HttpHeaders headers, HttpStatus status, WebRequest request) {
        ex.printStackTrace();
        return super.handleExceptionInternal(ex, body, headers, status, request);
    }

    @Override
    protected ResponseEntity<Object> handleHttpMessageNotReadable(HttpMessageNotReadableException ex, HttpHeaders headers, HttpStatus status, WebRequest request) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ResponseObject<>(ResponseObject.CODE_INVALID_REQUEST, ex.getMessage())
        );
    }

    @ExceptionHandler(Exception.class)
    @ResponseBody
    public ResponseEntity<ResponseObject<Object>> handleGeneralException(
            HttpServletRequest req,
            Exception e
    ) {
        if (e == null) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ResponseObject<>(ResponseObject.CODE_UNKNOWN_ERROR,
                            "Unexpected Exception Occurred"));
        }
        e.printStackTrace();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
                new ResponseObject<>(ResponseObject.CODE_UNKNOWN_ERROR, e.getMessage())
        );
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex, HttpHeaders headers, HttpStatus status, WebRequest request) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                new ResponseObject<>(ResponseObject.CODE_INVALID_REQUEST, ex.getMessage()));
    }
}

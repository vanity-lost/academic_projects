package edu.cwru.csds393.billsplit.controller;

import edu.cwru.csds393.billsplit.annotation.Require;
import edu.cwru.csds393.billsplit.authentication.AuthContext;
import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.ResetToken;
import edu.cwru.csds393.billsplit.entity.Session;
import edu.cwru.csds393.billsplit.exception.InvalidRequestException;
import edu.cwru.csds393.billsplit.exception.RequestException;
import edu.cwru.csds393.billsplit.mail.MailTemplate;
import edu.cwru.csds393.billsplit.model.AuthenticationRequest;
import edu.cwru.csds393.billsplit.model.PwdResetRequest;
import edu.cwru.csds393.billsplit.model.RegisterRequest;
import edu.cwru.csds393.billsplit.model.ResponseObject;
import edu.cwru.csds393.billsplit.service.AuthService;
import edu.cwru.csds393.billsplit.service.MailService;
import org.springframework.data.util.Pair;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.io.IOException;

@RestController
@RequestMapping("/auth")
public class AuthController {
    final AuthService authService;
    final MailService mailService;

    public AuthController(AuthService authService, MailService mailService) {
        this.authService = authService;
        this.mailService = mailService;
    }

    @RequestMapping(value = "/test_delete", method = RequestMethod.DELETE)
    @ResponseBody
    public ResponseObject<Boolean> deleteUser(@RequestBody @Valid PwdResetRequest r) {
        authService.deleteAccount(r.getUsername());
        return new ResponseObject<>(true);
    }

    @RequestMapping(value = "/register", method = RequestMethod.POST)
    @ResponseBody
    public ResponseObject<Account> handleRegisterRequest(@RequestBody @Valid RegisterRequest r) {
        if (r.getPhone() != null && r.getPhone().isEmpty()) {
            r.setPhone(null);
        }

        return new ResponseObject<>(authService.registerUser(r));
    }

    @RequestMapping(value = "/auth", method = RequestMethod.POST)
    @ResponseBody
    public ResponseObject<Session> handleAuthentication(@RequestBody AuthenticationRequest r, AuthContext auth) {
        if (auth.isAuthenticated()) {
            return new ResponseObject<>(auth.getSession());
        }
        return new ResponseObject<>(authService.authenticate(r));
    }

    @RequestMapping(value = "/me", method = RequestMethod.GET)
    @ResponseBody
    @Require // Annotate this to Require authentication
    public ResponseObject<Session> meRequest(AuthContext ctx) {
        return new ResponseObject<>(ctx.getSession());
    }

    @RequestMapping(value = "/reset", method = RequestMethod.POST)
    @ResponseBody
    public ResponseObject<String> resetPassword(@RequestBody @Valid PwdResetRequest r) {
        if (r.getCode() == null || r.getCode().isEmpty()) {
            // Request Code
            Pair<ResetToken, Account> pair = this.authService.generateResetToken(r.getUsername());
            if (pair == null) {
                throw new InvalidRequestException("Account not found");
            }
            try {
                MailTemplate template = MailTemplate.createFromResourceName("reset");
                template.receiverAddr = pair.getSecond().getEmail();
                template.setStringValue("account", pair.getSecond().getUsername());
                template.setStringValue("code", pair.getFirst().getToken());
                mailService.sendMail(template, "Password Reset Token");
                return new ResponseObject<>("Mail Sent");
            } catch (IOException e) {
                throw new RequestException(ResponseObject.CODE_UNKNOWN_ERROR, "Error while sending mail");
            }
        }
        if (r.getPassword() == null || r.getPassword().length() < 8) {
            throw new RequestException(ResponseObject.CODE_INVALID_REQUEST, "Password must be 8 or longer");
        }
        if (authService.resetPasswordWithToken(r.getUsername(), r.getPassword(), r.getCode())) {
            return new ResponseObject<>("Success");
        } else {
            throw new InvalidRequestException("Incorrect Code");
        }
    }
}

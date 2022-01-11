package edu.cwru.csds393.billsplit.service;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.ResetToken;
import edu.cwru.csds393.billsplit.entity.Session;
import edu.cwru.csds393.billsplit.exception.AuthenticationException;
import edu.cwru.csds393.billsplit.exception.InvalidRequestException;
import edu.cwru.csds393.billsplit.model.AuthenticationRequest;
import edu.cwru.csds393.billsplit.model.RegisterRequest;
import edu.cwru.csds393.billsplit.model.ResponseObject;
import edu.cwru.csds393.billsplit.repository.AccountRepository;
import edu.cwru.csds393.billsplit.repository.ResetTokenRepository;
import edu.cwru.csds393.billsplit.repository.SessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.data.util.Pair;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import javax.persistence.EntityNotFoundException;
import javax.transaction.Transactional;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class AuthService {
    private final AccountRepository accountRepo;
    private final SessionRepository sessionRepo;
    private final ResetTokenRepository tokenRepo;

    BCryptPasswordEncoder bCrypt;

    public AuthService(@Autowired AccountRepository accountRepo,
                       @Autowired SessionRepository sessionRepo,
                       @Autowired ResetTokenRepository tokenRepo) {
        this.accountRepo = accountRepo;
        this.sessionRepo = sessionRepo;
        this.tokenRepo = tokenRepo;
    }

    @PostConstruct
    private void postConstruct() {
        bCrypt = new BCryptPasswordEncoder();
    }

    public Account registerUser(RegisterRequest request) {
        // TODO: Actually validate request lmao
        String encodedPasswd = this.bCrypt.encode(request.getPassword());
        Account acnt = new Account(request.getUsername(), encodedPasswd);
        acnt.setEmail(request.getEmail());
        acnt.setNickname(request.getNickname());
        acnt.setPhone(request.getPhone());
        try {
            acnt = this.accountRepo.save(acnt);
        } catch (DataIntegrityViolationException e) {
            throw new InvalidRequestException("Failed to register: " + e.getRootCause().getLocalizedMessage());
        }
        return acnt;
    }

    public Session generateSession(Account accnt) {
        String token = UUID.randomUUID().toString();
        Session session = new Session(token, accnt);
        return sessionRepo.save(session);
    }

    public Session authenticate(AuthenticationRequest r) {
        if (r.getUsername() == null || r.getUsername().isEmpty()) {
            throw new AuthenticationException(ResponseObject.CODE_INVALID_CREDENTIALS, "Username can not be empty");
        }
        Optional<Account> find = accountRepo.findByUsernameOrEmailOrPhone(r.getUsername(), r.getUsername(), r.getUsername());
        if (find.isPresent()) {
            Account acc = find.get();
            // Validate password
            if (this.bCrypt.matches(r.getPassword(), acc.getPasswordHash())) {
                // Make a token
                return generateSession(acc);
            }
        }
        throw new AuthenticationException(ResponseObject.CODE_INVALID_CREDENTIALS, "Wrong username or password");
    }

    public Optional<Session> authWithToken(String token) {
        Optional<Session> s = sessionRepo.findByToken(token);
        if (s.isPresent()) {
            Session ss = s.get();
            ss.setLastActive(new Date());
            return Optional.of(sessionRepo.save(ss));
        }
        return Optional.empty();
    }

    /**
     *
     * @param username - username / email / phone. (Any)
     * @return null if no account matching found.
     */
    public Pair<ResetToken, Account> generateResetToken(String username) {
        Optional<Account> find = accountRepo.findByUsernameOrEmailOrPhone(username, username, username);
        if (find.isPresent()) {
            Account acc = find.get();
            String token = String.format("%08d", new Random().nextInt(100000000));
            // Delete existing token if there is one.
            Optional<ResetToken> tokenFind = tokenRepo.findByAccount(acc);
            tokenFind.ifPresent(tokenRepo::delete);
            return Pair.of(tokenRepo.save(new ResetToken(token, acc)), acc);
        }
        return null;
    }

    @Transactional
    public boolean resetPasswordWithToken(String username, String password, String token) {
        Optional<Account> find = accountRepo.findByUsernameOrEmailOrPhone(username, username, username);
        if(find.isPresent()) {
            Account acc = find.get();
            Optional<ResetToken> findToken = tokenRepo.findByAccount(acc);
            if(findToken.isPresent()) {
                ResetToken t = findToken.get();
                if(token.equals(t.getToken())) {
                    acc.setPasswordHash(bCrypt.encode(password));
                    sessionRepo.deleteAllByAccount(acc);
                    accountRepo.save(acc);
                    tokenRepo.delete(t);
                    return true;
                }
            }
        }
        return false;
    }

    @Transactional
    public void deleteAccount(String username) {
        accountRepo.deleteAccountByUsernameOrEmailOrPhone(username, username, username);
    }

    /**
     * Translates a list of usernames to a list of accounts
     *
     * @param usernames - list of usernames
     * @return list of account entities
     */
    public List<Account> locateAccounts(List<String> usernames) {
        return usernames.stream().map((username) -> {
            Optional<Account> acntFind = accountRepo.findByUsername(username);
            if (acntFind.isPresent())
                return acntFind.get();
            throw new EntityNotFoundException("Account with username " + username + " not found.");
        }).collect(Collectors.toList());
    }

}

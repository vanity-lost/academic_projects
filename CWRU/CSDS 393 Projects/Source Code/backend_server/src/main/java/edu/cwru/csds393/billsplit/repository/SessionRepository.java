package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.Session;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface SessionRepository extends CrudRepository<Session, Long> {
    Optional<Session> findByToken(String token);
    void deleteAllByAccount(Account account);
}

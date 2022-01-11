package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.ResetToken;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface ResetTokenRepository extends CrudRepository<ResetToken, Long> {
    Optional<ResetToken> findByAccount(Account account);
}

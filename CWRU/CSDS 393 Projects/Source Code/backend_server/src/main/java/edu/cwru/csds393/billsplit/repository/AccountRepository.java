package edu.cwru.csds393.billsplit.repository;

import edu.cwru.csds393.billsplit.entity.Account;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.Optional;

public interface AccountRepository extends CrudRepository<Account, Long> {
    Optional<Account> findByUsernameOrEmailOrPhone(String username, String email, String phone);
    void deleteAccountByUsernameOrEmailOrPhone(String username, String email, String phone);

    Optional<Account> findByUsername(String username);
}

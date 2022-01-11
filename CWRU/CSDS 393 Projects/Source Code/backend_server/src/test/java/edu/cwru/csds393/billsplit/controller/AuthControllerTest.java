package edu.cwru.csds393.billsplit.controller;

import edu.cwru.csds393.billsplit.BillSplitTestConfiguration;
import edu.cwru.csds393.billsplit.BillsplitBackendApplication;
import edu.cwru.csds393.billsplit.entity.Account;
import edu.cwru.csds393.billsplit.entity.ResetToken;
import edu.cwru.csds393.billsplit.entity.Session;
import edu.cwru.csds393.billsplit.model.RegisterRequest;
import edu.cwru.csds393.billsplit.repository.AccountRepository;
import edu.cwru.csds393.billsplit.repository.ResetTokenRepository;
import edu.cwru.csds393.billsplit.repository.SessionRepository;
import edu.cwru.csds393.billsplit.service.AuthService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.junit.Assert.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {BillsplitBackendApplication.class})
@Import(BillSplitTestConfiguration.class)
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
public class AuthControllerTest {
    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private AuthService authService;
    @Autowired
    private AccountRepository accountRepository;
    @Autowired
    private SessionRepository sessionRepository;
    @Autowired
    private ResetTokenRepository resetRepo;

    @Autowired
    private JavaMailSender sender;

    private Account createAccount() {
        RegisterRequest r = new RegisterRequest();
        r.setUsername("test");
        r.setPassword("12345678");
        r.setEmail("test@test.com");
        r.setPhone("");
        return authService.registerUser(r);
    }

    private Session getSession(Account a) {
        return authService.generateSession(a);
    }

    @Test
    public void testMockMvcInit() {
        assertNotNull(mockMvc);
    }

    @Test
    public void testAuthMeAuthenticationFailure() throws Exception {
        assertEquals("Failed to block an invalid authentication",
                HttpStatus.FORBIDDEN.value(), mockMvc.perform(get("/auth/me")).andReturn().getResponse().getStatus());
    }

    @Test
    public void testAuthMeAuthenticationSuccess() throws Exception {
        Account a = createAccount();
        Session s = getSession(a);
        assertEquals("Failed to authenticate with a valid token", HttpStatus.OK.value(), mockMvc.perform(
                get("/auth/me").header("Authorization", s.getToken())
        ).andReturn().getResponse().getStatus());
    }

    @Test
    public void testHandleAuthentication() throws Exception {
        Account a = createAccount();
        assertNotNull(a);
        String req = "{\n" +
                "    \"username\": \"test\",\n" +
                "    \"password\": \"12345678\"\n" +
                "}";

        MockHttpServletResponse authresponse = mockMvc.perform(post("/auth/auth").content(req).contentType(MediaType.APPLICATION_JSON)).andReturn().getResponse();
        assertEquals("Authentication did not return success",
                HttpStatus.OK.value(),
                authresponse.getStatus());

        Session s = sessionRepository.findAll().iterator().next();
        assertNotNull(s.getToken());
        assertEquals("Session Based auth failed", HttpStatus.OK.value(),
                mockMvc.perform(post("/auth/auth").content(req).contentType(MediaType.APPLICATION_JSON).header("Authorization", s.getToken())).andReturn().getResponse().getStatus());

    }

    @Test
    public void testRegisterAccount() throws Exception {
        String req = "{\n" +
                "    \"username\": \"violetaa\",\n" +
                "    \"email\": \"abc@gmail.com\",\n" +
                "    \"password\": \"12345678\",\n" +
                "    \"nickname\": \"viola\",\n" +
                "    \"phone\": \"\"\n" +
                "}";
        assertFalse("Account existed before creating", accountRepository.findByUsernameOrEmailOrPhone("violetaa", "", "").isPresent());

        assertEquals("Register did not return success",
                HttpStatus.OK.value(),
                mockMvc.perform(post("/auth/register").content(req).contentType(MediaType.APPLICATION_JSON)).andReturn().getResponse().getStatus());

        assertTrue("Account does not exist after creation success",
                accountRepository.findByUsernameOrEmailOrPhone("violetaa", "", "").isPresent());

    }

    @Test
    public void testPasswordChange() throws Exception {
        Account a = createAccount();
        assertNotNull(a);
        String req = "{\n" +
                "    \"username\": \"test\"\n" +
                "}";

        assertEquals(HttpStatus.OK.value(),
                mockMvc.perform(post("/auth/reset").content(req).contentType(MediaType.APPLICATION_JSON)).andReturn().getResponse().getStatus());

        ResetToken t = resetRepo.findByAccount(a).get();
        assertNotNull(t);

        String req2 = "{\n" +
                "    \"username\": \"test\",\n" +
                "    \"code\": \"" + t.getToken() + "\",\n" +
                "    \"password\": \"12345678\"\n" +
                "}";
        assertEquals(HttpStatus.OK.value(),
                mockMvc.perform(post("/auth/reset").content(req2).contentType(MediaType.APPLICATION_JSON)).andReturn().getResponse().getStatus());
    }
}

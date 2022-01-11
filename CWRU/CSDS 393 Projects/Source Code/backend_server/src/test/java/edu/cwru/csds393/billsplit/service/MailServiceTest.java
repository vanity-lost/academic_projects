package edu.cwru.csds393.billsplit.service;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.mail.javamail.JavaMailSender;

import javax.mail.Session;
import javax.mail.internet.MimeMessage;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@Configuration
public class MailServiceTest {
    @Bean
    @Primary
    public JavaMailSender javaMailSender() {
        JavaMailSender sender = mock(JavaMailSender.class);
        when(sender.createMimeMessage()).thenReturn(new MimeMessage((Session) null));
        return sender;
    }
}

package edu.cwru.csds393.billsplit.service;

import edu.cwru.csds393.billsplit.mail.MailTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

@Service
public class MailService {
    @Value("${spring.mail.from}")
    private String fromAddress;

    private final JavaMailSender mailSender;

    public MailService(@Autowired JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendMail(MailTemplate template, String subject) {
        MimeMessage msg = mailSender.createMimeMessage();
        try {
            msg.setFrom(fromAddress);
            msg.setSubject(subject);
            msg.setText(template.encode(), "utf-8", "html");
            msg.addRecipients(Message.RecipientType.TO, template.receiverAddr);
            mailSender.send(msg);
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }
}

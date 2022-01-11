package edu.cwru.csds393.billsplit;

import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.autoconfigure.mail.MailSenderAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

import javax.transaction.Transactional;

@Configuration
@ComponentScan("edu.cwru.csds393.billsplit")
@ImportAutoConfiguration(classes = {MailSenderAutoConfiguration.class})
@EnableWebMvc
public class BillSplitTestConfiguration {
}

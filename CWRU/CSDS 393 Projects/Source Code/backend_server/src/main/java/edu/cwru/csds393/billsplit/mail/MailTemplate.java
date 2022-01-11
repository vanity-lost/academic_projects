package edu.cwru.csds393.billsplit.mail;

import com.google.common.io.Resources;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

public class MailTemplate {
    private String content;
    public String receiverAddr;

    MailTemplate(String content) {
        this.content = content;
    }

    public void setStringValue(String templateKey, String value) {
        this.content = this.content.replace("{{" + templateKey + "}}", value);
    }

    public String encode() {
        return this.content;
    }

    public static MailTemplate createFromResourceName(String filename) throws IOException {
        return new MailTemplate(Resources.toString(MailTemplate.class.getResource("/templates/"+filename+".tpl"), StandardCharsets.UTF_8));
    }
}

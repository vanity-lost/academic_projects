package edu.cwru.csds393.billsplit.mail;

import static org.junit.Assert.*;

import org.junit.Assert;
import org.junit.Test;

import java.io.IOException;

public class MailTemplateTest {
    @Test
    public void testSetStringValue() {
        String testTemplate = "abc {{thing}} def";
        String replaceContent = "zzz";
        String expectedResult = "abc zzz def";
        MailTemplate template = new MailTemplate(testTemplate);

        assertEquals(testTemplate, template.encode());
        template.setStringValue("thing", replaceContent);
        assertEquals(expectedResult, template.encode());
    }

    @Test
    public void testLoadTemplate() {
        String templateName = "test";
        String templateContent = "abcdefg";

        try {
            MailTemplate t = MailTemplate.createFromResourceName(templateName);
            assertEquals(templateContent, t.encode());
        } catch (IOException e) {
            e.printStackTrace();
            Assert.fail();
        }
    }
}

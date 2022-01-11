package edu.cwru.csds393.billsplit.configuration.serde;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;

import java.io.IOException;
import java.util.Date;
import java.util.concurrent.TimeUnit;

public class JacksonDateDeserializer extends JsonDeserializer<Date> {
    @Override
    public Date deserialize(JsonParser p, DeserializationContext ctxt) throws IOException, JsonProcessingException {
        return new Date(TimeUnit.SECONDS.toMillis(Long.parseLong(p.getText().trim())));
    }
}

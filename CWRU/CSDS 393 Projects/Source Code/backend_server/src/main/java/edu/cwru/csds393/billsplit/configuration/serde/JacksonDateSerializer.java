package edu.cwru.csds393.billsplit.configuration.serde;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;
import java.util.Date;
import java.util.concurrent.TimeUnit;

public class JacksonDateSerializer extends JsonSerializer<Date> {
    @Override
    public void serialize(Date value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
        gen.writeNumber(TimeUnit.MILLISECONDS.toSeconds(value.getTime()));
    }
}

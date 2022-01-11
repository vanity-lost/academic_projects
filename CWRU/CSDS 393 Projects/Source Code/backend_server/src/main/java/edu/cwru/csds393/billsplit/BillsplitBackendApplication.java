package edu.cwru.csds393.billsplit;

import com.fasterxml.jackson.databind.Module;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.fasterxml.jackson.datatype.hibernate5.Hibernate5Module;
import edu.cwru.csds393.billsplit.configuration.serde.JacksonDateDeserializer;
import edu.cwru.csds393.billsplit.configuration.serde.JacksonDateSerializer;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;

import java.util.Date;

@SpringBootApplication
public class BillsplitBackendApplication {

    @Bean
    public HttpMessageConverter<Object> constructJacksonConverter() {
        MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
        ObjectMapper mapper = new ObjectMapper();
        SimpleModule m = new SimpleModule();

        m.addDeserializer(Date.class, new JacksonDateDeserializer());
        m.addSerializer(Date.class, new JacksonDateSerializer());

        mapper.registerModule(m);

        Hibernate5Module hm5 = new Hibernate5Module();
        mapper.registerModule(hm5);

        converter.setObjectMapper(mapper);
        return converter;
    }

    public static void main(String[] args) {
        SpringApplication.run(BillsplitBackendApplication.class, args);
    }
}

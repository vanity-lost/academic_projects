package edu.cwru.csds393.billsplit.authentication;

import edu.cwru.csds393.billsplit.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.List;

@Configuration
public class AuthenticationConfiguration implements WebMvcConfigurer {
    @Autowired
    @Lazy
    private AuthContextHandlerInterceptor authInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor);
    }

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        resolvers.add(new AuthContextArgumentResolver());
    }

    @Bean
    public AuthContextHandlerInterceptor authContextHandlerInterceptor(AuthService authService) {
        return new AuthContextHandlerInterceptor(authService);
    }
}

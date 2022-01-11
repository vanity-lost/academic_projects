package edu.cwru.csds393.billsplit.authentication;

import edu.cwru.csds393.billsplit.annotation.Require;
import edu.cwru.csds393.billsplit.entity.Session;
import edu.cwru.csds393.billsplit.exception.AuthorizationException;
import edu.cwru.csds393.billsplit.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Optional;

public class AuthContextHandlerInterceptor implements HandlerInterceptor {
    public AuthContextHandlerInterceptor(@Autowired AuthService authService) {
        this.authService = authService;
    }

    private AuthService authService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // Get header
        String authToken = request.getHeader("Authorization");
        AuthContext.remove();
        if (authToken != null && !authToken.isEmpty()) {
            Optional<Session> optSession = authService.authWithToken(authToken);
            optSession.ifPresent(session -> AuthContext.set(new AuthContext(session)));
        }

        // Current Context
        AuthContext ctx = AuthContext.currentContext();

        if (handler instanceof HandlerMethod) {
            if (
                    ((HandlerMethod) handler).hasMethodAnnotation(Require.class)
                    || ((HandlerMethod) handler).getMethod().getDeclaringClass().isAnnotationPresent(Require.class)
            ) {
                if (!ctx.isAuthenticated()) {
                    throw new AuthorizationException("Login Required");
                }
            }
        }

        // Authenticate
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        AuthContext.remove();
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        AuthContext.remove();
    }
}

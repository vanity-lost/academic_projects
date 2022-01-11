package edu.cwru.csds393.billsplit.authentication;

import edu.cwru.csds393.billsplit.entity.Session;

public class AuthContext {
    private Session session;

    private static ThreadLocal<AuthContext> threadLocalContext = new ThreadLocal<>();

    public static void remove() {
        threadLocalContext.remove();
    }

    public static void set(AuthContext ctx) {
        threadLocalContext.set(ctx);
    }

    public static AuthContext currentContext() {
        if (threadLocalContext.get() == null) {
            threadLocalContext.set(new AuthContext(null));
        }
        return threadLocalContext.get();
    }

    public boolean isAuthenticated() {
        return this.session != null;
    }

    public AuthContext(Session session) {
        this.session = session;
    }

    public Session getSession() {
        return session;
    }

    public void setSession(Session session) {
        this.session = session;
    }
}

'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authUtils } from '@/src/lib/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  userId: string | null;
  loading: boolean;
  login: (token: string) => void;
  logout: () => void;
  checkAuthStatus: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuthStatus = () => {
    const authenticated = authUtils.isAuthenticated();
    const currentUserId = authUtils.getUserIdFromToken();

    setIsAuthenticated(authenticated);
    setUserId(currentUserId);
    setLoading(false);
  };

  const login = (token: string) => {
    authUtils.setToken(token);
    const authenticated = authUtils.isAuthenticated();
    const currentUserId = authUtils.getUserIdFromToken();

    setIsAuthenticated(authenticated);
    setUserId(currentUserId);
    setLoading(false);
  };

  const logout = () => {
    authUtils.removeToken();
    setIsAuthenticated(false);
    setUserId(null);
  };

  useEffect(() => {
    // Check auth status on mount
    checkAuthStatus();

    // Listen for storage changes (e.g., login/logout from another tab)
    const handleStorageChange = () => {
      checkAuthStatus();
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        userId,
        loading,
        login,
        logout,
        checkAuthStatus,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
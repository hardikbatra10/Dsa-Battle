import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { login as loginRequest, registerUser as registerRequest, getProfile } from '../api/auth';
import { setTokens, clearTokens, getAccessToken } from '../utils/token';

const AuthContext = createContext(null);

// AuthContext owns the "who is logged in" state for the whole app.
// user shape (from GET /api/users/profile/):
// { username, email, rooms_created, problems_solved, total_submissions }
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadProfile = useCallback(async () => {
    const { data } = await getProfile();
    setUser(data);
    return data;
  }, []);

  // On first load, if we already have a token in localStorage, fetch the
  // profile so refreshing the page doesn't log the user out.
  useEffect(() => {
    async function init() {
      if (getAccessToken()) {
        try {
          await loadProfile();
        } catch {
          clearTokens();
          setUser(null);
        }
      }
      setIsLoading(false);
    }
    init();
  }, [loadProfile]);

  // The axios interceptor fires this event when a token refresh fails,
  // meaning the session is dead and we should drop back to "logged out".
  useEffect(() => {
    function handleForcedLogout() {
      setUser(null);
    }
    window.addEventListener('auth:logout', handleForcedLogout);
    return () => window.removeEventListener('auth:logout', handleForcedLogout);
  }, []);

  async function login({ username, password }) {
    const { data } = await loginRequest({ username, password });
    setTokens({ access: data.access, refresh: data.refresh });
    await loadProfile();
  }

  async function register({ username, email, password }) {
    await registerRequest({ username, email, password });
  }

  function logout() {
    clearTokens();
    setUser(null);
  }

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser: loadProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used inside an AuthProvider');
  }
  return ctx;
}

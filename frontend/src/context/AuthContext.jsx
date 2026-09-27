import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  login as loginRequest,
  registerUser as registerRequest,
  getProfile,
  googleLogin as googleLoginRequest,
} from '../api/auth';
import { setTokens, clearTokens, getAccessToken } from '../utils/token';
import {
  isFirebaseConfigured,
  signInWithGooglePopup,
  ensureFirebaseSession,
  signOutOfFirebase,
} from '../services/firebase';

const AuthContext = createContext(null);

// AuthContext owns the "who is logged in" state for the whole app.
// user shape (from GET /api/users/profile/):
// { username, email, rooms_created, problems_solved, total_submissions }
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  // Chat needs a Firebase session on top of the Django one. It is tracked
  // separately because it can fail on its own - Firebase being down or
  // unconfigured must not log anyone out of the app itself.
  const [isChatReady, setIsChatReady] = useState(false);
  // Why chat failed, kept so the panel can say something actionable instead
  // of a generic "not connected" that gives nobody anything to go on.
  const [chatError, setChatError] = useState('');

  const loadProfile = useCallback(async () => {
    const { data } = await getProfile();
    setUser(data);
    return data;
  }, []);

  /**
   * Opens the Firebase session used by room chat.
   *
   * Runs after every successful login, not just Google ones - a password user
   * has no Firebase identity otherwise and would silently lose chat. Failures
   * are swallowed deliberately: losing chat is a degraded feature, not a
   * failed login.
   */
  const connectChat = useCallback(async () => {
    if (!isFirebaseConfigured) return false;
    try {
      await ensureFirebaseSession();
      setIsChatReady(true);
      setChatError('');
      return true;
    } catch (err) {
      setIsChatReady(false);
      setChatError(describeChatError(err));
      // Also on the console, where the raw Firebase error is worth having.
      console.error('Chat session could not be opened:', err);
      return false;
    }
  }, []);

  // On first load, if we already have a token in localStorage, fetch the
  // profile so refreshing the page doesn't log the user out.
  useEffect(() => {
    async function init() {
      if (getAccessToken()) {
        try {
          await loadProfile();
          // A page refresh drops the Firebase session too, so re-open it.
          await connectChat();
        } catch {
          clearTokens();
          setUser(null);
        }
      }
      setIsLoading(false);
    }
    init();
  }, [loadProfile, connectChat]);

  // The axios interceptor fires this event when a token refresh fails,
  // meaning the session is dead and we should drop back to "logged out".
  useEffect(() => {
    function handleForcedLogout() {
      setUser(null);
      setIsChatReady(false);
      signOutOfFirebase();
    }
    window.addEventListener('auth:logout', handleForcedLogout);
    return () => window.removeEventListener('auth:logout', handleForcedLogout);
  }, []);

  async function login({ username, password }) {
    const { data } = await loginRequest({ username, password });
    setTokens({ access: data.access, refresh: data.refresh });
    await loadProfile();
    await connectChat();
  }

  /**
   * Google sign-in. The popup proves the Google identity, the backend
   * verifies that token and turns it into this app's own session against a
   * real Django user, and the Firebase session the popup created is kept for
   * chat - so these users get a stable, non-anonymous chat uid.
   */
  async function loginWithGoogle() {
    const idToken = await signInWithGooglePopup();
    const { data } = await googleLoginRequest(idToken);
    setTokens({ access: data.access, refresh: data.refresh });
    await loadProfile();
    await connectChat();
  }

  async function register({ username, email, password }) {
    await registerRequest({ username, email, password });
  }

  function logout() {
    clearTokens();
    setUser(null);
    setIsChatReady(false);
    signOutOfFirebase();
  }

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    isChatReady,
    chatError,
    isChatConfigured: isFirebaseConfigured,
    login,
    loginWithGoogle,
    register,
    logout,
    refreshUser: loadProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/** Turns a Firebase auth error code into something a human can act on. */
function describeChatError(err) {
  switch (err?.code) {
    case 'auth/operation-not-allowed':
    case 'auth/admin-restricted-operation':
      return 'Anonymous sign-in is disabled for this Firebase project. Enable it under Authentication → Sign-in method → Anonymous.';
    case 'auth/configuration-not-found':
      return 'This Firebase project has no Authentication configuration yet. Enable a sign-in provider in the Firebase console.';
    case 'auth/unauthorized-domain':
      return `This domain (${window.location.hostname}) is not in the Firebase project's authorised domains.`;
    case 'auth/network-request-failed':
      return 'Could not reach Firebase. Check your connection.';
    case 'auth/api-key-not-valid':
    case 'auth/invalid-api-key':
      return 'The Firebase API key in this build is not valid for the project.';
    default:
      return err?.code ? `Firebase said: ${err.code}` : 'Could not open a chat session.';
  }
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used inside an AuthProvider');
  }
  return ctx;
}

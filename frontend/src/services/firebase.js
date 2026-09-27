/**
 * Firebase client setup: one app, lazily created, shared by chat and Google
 * sign-in.
 *
 * Everything here tolerates Firebase being unconfigured. A checkout with no
 * VITE_FIREBASE_* values still builds and runs; `isFirebaseConfigured` is
 * false, callers skip the Firebase paths, and the UI says chat is unavailable
 * rather than throwing on a missing API key.
 */
import { initializeApp, getApps } from 'firebase/app';
import {
  getAuth,
  signInAnonymously,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
} from 'firebase/auth';
import { getDatabase } from 'firebase/database';

const config = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: import.meta.env.VITE_FIREBASE_DATABASE_URL,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  // Neither is needed for auth or the database. They are carried through so
  // that adding Storage or messaging later needs no config change here.
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
};

// The database URL is the one value chat cannot work without, and the API key
// is the one Google sign-in cannot work without.
export const isFirebaseConfigured = Boolean(config.apiKey && config.databaseURL);

function getFirebaseApp() {
  if (!isFirebaseConfigured) return null;
  // Vite's HMR re-runs this module, and initializeApp throws on a duplicate.
  return getApps().length ? getApps()[0] : initializeApp(config);
}

export function getFirebaseAuth() {
  const app = getFirebaseApp();
  return app ? getAuth(app) : null;
}

export function getFirebaseDb() {
  const app = getFirebaseApp();
  return app ? getDatabase(app) : null;
}

/**
 * Runs the Google popup and returns the resulting Firebase ID token.
 *
 * That token is not the app's session: it only proves which Google account
 * signed in. The backend verifies it against Google's public certificates and
 * issues this app's own JWT. The Firebase session the popup leaves behind is
 * kept, because chat needs a Firebase identity to write under.
 */
export async function signInWithGooglePopup() {
  const auth = getFirebaseAuth();
  if (!auth) throw new Error('Google sign-in is not configured.');

  const provider = new GoogleAuthProvider();
  // Always show the chooser: without this, a browser with one Google session
  // silently reuses it, which is confusing on a shared machine.
  provider.setCustomParameters({ prompt: 'select_account' });

  const credential = await signInWithPopup(auth, provider);
  return credential.user.getIdToken();
}

/**
 * Makes sure there is *some* Firebase session, so chat can write.
 *
 * A Google sign-in already left one behind, and that is the better case: its
 * uid is stable across devices and sessions. A password user has no Firebase
 * identity at all, and minting one tied to their Django account would need a
 * service account key on the server, which this deployment deliberately does
 * not use - so they get an anonymous session instead. Chat works either way;
 * what an anonymous session cannot do is prove the display name is theirs.
 */
export async function ensureFirebaseSession() {
  const auth = getFirebaseAuth();
  if (!auth) throw new Error('Chat is not configured.');
  if (auth.currentUser) return auth.currentUser;
  const credential = await signInAnonymously(auth);
  return credential.user;
}

export async function signOutOfFirebase() {
  const auth = getFirebaseAuth();
  if (!auth) return;
  try {
    await firebaseSignOut(auth);
  } catch {
    // Logging out of this app must succeed even if Firebase is unreachable.
  }
}

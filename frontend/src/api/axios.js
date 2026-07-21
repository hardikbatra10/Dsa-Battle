import axios from 'axios';
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
  clearTokens,
} from '../utils/token';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

// Attach the JWT access token to every outgoing request, if we have one.
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// When the access token has expired (401), try to refresh it once using the
// refresh token, then retry the original request. If the refresh itself
// fails, the session is dead: clear tokens and let the app react to that by
// broadcasting a window event (AuthContext listens for it).
let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;

    const isAuthEndpoint =
      originalRequest?.url?.includes('/token/') ||
      originalRequest?.url?.includes('/users/register/');

    if (status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      originalRequest._retry = true;
      const refreshToken = getRefreshToken();

      if (!refreshToken) {
        clearTokens();
        window.dispatchEvent(new Event('auth:logout'));
        return Promise.reject(error);
      }

      try {
        if (!refreshPromise) {
          refreshPromise = axios
            .post(`${API_BASE_URL}/api/token/refresh/`, { refresh: refreshToken })
            .finally(() => {
              refreshPromise = null;
            });
        }

        const { data } = await refreshPromise;
        setAccessToken(data.access);

        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        clearTokens();
        window.dispatchEvent(new Event('auth:logout'));
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Pulls the human-readable message out of a Django REST Framework error
// response, falling back to something reasonable if the shape is unexpected.
export function getApiErrorMessage(error, fallback = 'Something went wrong. Please try again.') {
  const data = error?.response?.data;

  if (!data) return error?.message || fallback;
  // A 500 with DEBUG=True returns an HTML traceback page, not JSON. Never
  // show that raw markup to the user.
  if (typeof data === 'string') return data.trim().startsWith('<') ? fallback : data;
  if (data.error) return data.error;
  if (data.detail) return data.detail;

  // DRF validation errors: { field: ["msg1", "msg2"], ... }
  const firstKey = Object.keys(data)[0];
  if (firstKey) {
    const value = data[firstKey];
    const message = Array.isArray(value) ? value[0] : value;
    if (typeof message === 'string') {
      return firstKey === 'non_field_errors' ? message : `${firstKey}: ${message}`;
    }
  }

  return fallback;
}

export default api;

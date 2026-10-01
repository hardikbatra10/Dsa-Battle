import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';

// Wraps private routes: shows a spinner while we check for an existing
// session, then either renders the nested route (<Outlet />) or bounces the
// user to /login.
export default function ProtectedRoute() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center py-24">
        <LoadingSpinner size={28} />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // A Google account still carrying its derived placeholder name has to pick
  // a real one first. Enforced here rather than at the end of the sign-in
  // handler so it survives a refresh, a bookmark, or a direct URL - any of
  // which would otherwise walk straight past the step.
  if (user?.needs_username && location.pathname !== '/choose-username') {
    return <Navigate to="/choose-username" replace />;
  }

  return <Outlet />;
}

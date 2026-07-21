import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';

// Wraps private routes: shows a spinner while we check for an existing
// session, then either renders the nested route (<Outlet />) or bounces the
// user to /login.
export default function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

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

  return <Outlet />;
}

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import ProtectedRoute from './routes/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import LoadingSpinner from './components/LoadingSpinner/LoadingSpinner';

import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CreateRoom from './pages/CreateRoom';
import JoinRoom from './pages/JoinRoom';
import RoomLobby from './pages/RoomLobby';
import Contest from './pages/Contest';
import LeaderboardPage from './pages/LeaderboardPage';
import SubmissionHistory from './pages/SubmissionHistory';
import SubmissionDetail from './pages/SubmissionDetail';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

function Home() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center py-24">
        <LoadingSpinner size={28} />
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <LandingPage />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/rooms/create" element={<CreateRoom />} />
              <Route path="/rooms/join" element={<JoinRoom />} />
              <Route path="/rooms/:roomCode" element={<RoomLobby />} />
              <Route path="/rooms/:roomCode/leaderboard" element={<LeaderboardPage />} />
              <Route path="/rooms/:roomCode/submissions" element={<SubmissionHistory />} />
              <Route path="/submissions/:submissionId" element={<SubmissionDetail />} />
              <Route path="/profile" element={<Profile />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Route>

          {/* The contest page owns its own full-height layout (no navbar/footer). */}
          <Route element={<ProtectedRoute />}>
            <Route path="/rooms/:roomCode/contest" element={<Contest />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

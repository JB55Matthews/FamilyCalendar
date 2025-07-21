import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function AppRoutes() {

  return (
    <Routes>
      <Route path="/" element={
        familyToken ? (
          currentUser ? <CalendarPage /> : <Navigate to="/select-user" replace />
        ) : <AuthPage />
      } />
      <Route path="/setup-family" element={
        familyToken ? <SetupFamilyPage /> : <Navigate to="/" replace />
      } />
      <Route path="/select-user" element={
        familyToken ? <UserSelectPage /> : <Navigate to="/" replace />
      } />
      <Route path="/calendar" element={
        familyToken && currentUser ? <CalendarPage /> : <Navigate to="/" replace />
      } />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
      <Router>
        <AppRoutes />
      </Router>
  );
}
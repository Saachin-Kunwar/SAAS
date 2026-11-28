import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return <div className="p-8 text-slate-500">Loading workspace...</div>;
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function DashboardPlaceholder() {
  const { activeOrg, organizations, switchOrganization, logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-xl border border-slate-200 p-6 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400">
            Active Workspace
          </p>
          <h2 className="text-xl font-bold text-slate-900">
            {activeOrg ? activeOrg.name : 'No Organization Selected'}
          </h2>
          {activeOrg && (
            <p className="text-xs text-slate-500 mt-0.5">
              ID: {activeOrg.id} · Slug: {activeOrg.slug}
            </p>
          )}
        </div>

        <div className="flex items-center gap-3">
          {organizations.length > 0 && (
            <select
              value={activeOrg?.id || ''}
              onChange={(e) => {
                const chosen = organizations.find(
                  (o) => String(o.id) === e.target.value
                );
                if (chosen) switchOrganization(chosen);
              }}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm bg-white"
            >
              {organizations.map((org) => (
                <option key={org.id} value={org.id}>
                  {org.name}
                </option>
              ))}
            </select>
          )}

          <button
            onClick={logout}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPlaceholder />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>


      
    </AuthProvider>
  );
}
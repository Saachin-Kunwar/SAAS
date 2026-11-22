import { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem('access_token'))
  );
  const [organizations, setOrganizations] = useState([]);
  const [activeOrg, setActiveOrg] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchOrganizations = async () => {
    try {
      const response = await apiClient.get('/api/accounts/organizations/');
      const orgList = response.data.results || response.data;
      setOrganizations(orgList);

      const savedOrgId = localStorage.getItem('active_org_id');
      const matchedOrg =
        orgList.find((org) => String(org.id) === String(savedOrgId)) ||
        orgList[0] ||
        null;

      if (matchedOrg) {
        setActiveOrg(matchedOrg);
        localStorage.setItem('active_org_id', String(matchedOrg.id));
      } else {
        setActiveOrg(null);
        localStorage.removeItem('active_org_id');
      }
    } catch (err) {
      console.error('Failed to load organizations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchOrganizations();
    } else {
      setLoading(false);
    }
  }, [isAuthenticated]);

  const login = async (email, password) => {
    const response = await apiClient.post('/api/auth/login/', {
      email,
      password,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    setIsAuthenticated(true);
  };

  const register = async (formData) => {
    await apiClient.post('/api/accounts/register/', formData);
  };

  const switchOrganization = (org) => {
    setActiveOrg(org);
    localStorage.setItem('active_org_id', String(org.id));
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('active_org_id');
    setIsAuthenticated(false);
    setOrganizations([]);
    setActiveOrg(null);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        organizations,
        activeOrg,
        loading,
        login,
        register,
        logout,
        switchOrganization,
        refreshOrganizations: fetchOrganizations,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
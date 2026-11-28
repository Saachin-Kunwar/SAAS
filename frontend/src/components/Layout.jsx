import { NavLink } from 'react-router-dom';
import { Users, TrendingUp, Building2, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Layout({ children }) {
  const { activeOrg, organizations, switchOrganization, logout } = useAuth();

  const navLinkClass = ({ isActive }) =>
    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-50 text-indigo-700'
        : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
    }`;

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between p-4">
        <div>
          <div className="px-3 py-2 mb-6">
            <span className="text-lg font-bold text-indigo-600 tracking-tight">
              SaaS CRM
            </span>
            <p className="text-xs text-slate-400 mt-0.5">Multi-Tenant Workspace</p>
          </div>

          <nav className="space-y-1">
            <NavLink to="/dashboard/customers" className={navLinkClass}>
              <Users className="w-4 h-4" />
              Customers
            </NavLink>
            <NavLink to="/dashboard/leads" className={navLinkClass}>
              <TrendingUp className="w-4 h-4" />
              Leads & Deals
            </NavLink>
            <NavLink to="/dashboard/organizations" className={navLinkClass}>
              <Building2 className="w-4 h-4" />
              Organizations
            </NavLink>
          </nav>
        </div>

        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-600 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between">
          <div>
            <span className="text-xs uppercase tracking-wider text-slate-400">
              Active Organization
            </span>
            <h2 className="text-sm font-semibold text-slate-900">
              {activeOrg ? activeOrg.name : 'No Organization Selected'}
            </h2>
          </div>

          {organizations.length > 0 && (
            <div className="flex items-center gap-2">
              <label className="text-xs text-slate-500">Switch Org:</label>
              <select
                value={activeOrg?.id || ''}
                onChange={(e) => {
                  const chosen = organizations.find(
                    (o) => String(o.id) === e.target.value
                  );
                  if (chosen) switchOrganization(chosen);
                }}
                className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm bg-white focus:border-indigo-600 focus:outline-none"
              >
                {organizations.map((org) => (
                  <option key={org.id} value={org.id}>
                    {org.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </header>

        {/* Page Content */}
        <main className="flex-1 p-8 max-w-6xl w-full mx-auto">{children}</main>
      </div>
    </div>
  );
}
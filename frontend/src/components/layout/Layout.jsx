import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { Menu, Bell } from 'lucide-react';
import { useAuth } from '../../store/AuthContext';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { student } = useAuth();

  return (
    <div className="app-layout">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="main-content">
        {/* Topbar */}
        <header className="topbar">
          <button
            className="btn-ghost btn btn-sm"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{ display: 'none' }}
            aria-label="Toggle sidebar"
            id="sidebar-toggle"
          >
            <Menu size={18} />
          </button>

          {/* Page title slot — injected by pages via document.title */}
          <div style={{ flex: 1 }} />

          <div className="flex items-center gap-3">
            <button className="btn-ghost btn btn-sm" aria-label="Notifications">
              <Bell size={17} />
            </button>

            {student && (
              <div style={{
                width: 32,
                height: 32,
                borderRadius: '50%',
                background: 'linear-gradient(135deg, var(--color-primary), var(--color-accent))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 13,
                fontWeight: 700,
                cursor: 'pointer',
              }}>
                {student.name.charAt(0).toUpperCase()}
              </div>
            )}
          </div>
        </header>

        {/* Page content */}
        <main className="page-content fade-in">
          <Outlet />
        </main>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', zIndex: 40,
          }}
        />
      )}
    </div>
  );
}

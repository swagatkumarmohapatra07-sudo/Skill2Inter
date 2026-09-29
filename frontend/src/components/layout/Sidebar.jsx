import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, User, FileText, Briefcase, GitCompare,
  Sparkles, TrendingUp, Lightbulb, LogOut, Zap,
} from 'lucide-react';
import { useAuth } from '../../store/AuthContext';

const NAV = [
  { label: 'Main', items: [
    { to: '/',               icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/profile',        icon: User,            label: 'My Profile' },
    { to: '/resume',         icon: FileText,        label: 'Resume Analyzer' },
  ]},
  { label: 'Internships', items: [
    { to: '/internships',    icon: Briefcase,       label: 'Browse Internships' },
    { to: '/recommendations',icon: Sparkles,        label: 'Recommendations' },
    { to: '/compare',        icon: GitCompare,      label: 'Compare' },
  ]},
  { label: 'Analysis', items: [
    { to: '/skill-gap',      icon: TrendingUp,      label: 'Skill Gap' },
    { to: '/what-if',        icon: Lightbulb,       label: 'What-If Simulator' },
  ]},
];

export default function Sidebar({ open, onClose }) {
  const { student, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">
          <Zap size={18} color="white" />
        </div>
        <div>
          <div className="sidebar-brand-name">Skill2Inter</div>
          <div className="sidebar-brand-sub">AI Matcher</div>
        </div>
      </div>

      {/* Student Info */}
      {student && (
        <div style={{
          padding: '12px 16px',
          margin: '12px',
          background: 'rgba(99,102,241,0.08)',
          borderRadius: '10px',
          border: '1px solid rgba(99,102,241,0.15)',
        }}>
          <div style={{ fontSize: 13, fontWeight: 600 }}>{student.name}</div>
          <div style={{ fontSize: 11, color: 'var(--color-text-muted)', marginTop: 2 }}>
            Student #{student.student_id}
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="sidebar-nav">
        {NAV.map((section) => (
          <div key={section.label}>
            <div className="nav-section-label">{section.label}</div>
            {section.items.map(({ to, icon: Icon, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                onClick={onClose}
                end={to === '/'}
              >
                <Icon size={17} />
                {label}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* Logout */}
      <div style={{ padding: '12px', borderTop: '1px solid var(--color-border)' }}>
        <button className="nav-item w-full" onClick={handleLogout} style={{ border: 'none', background: 'none' }}>
          <LogOut size={17} />
          Sign Out
        </button>
      </div>
    </aside>
  );
}

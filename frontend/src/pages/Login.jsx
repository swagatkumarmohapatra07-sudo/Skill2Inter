import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, LogIn, UserPlus, AlertCircle } from 'lucide-react';
import { studentAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';

const DEMO_USERS = [
  { name: 'Arjun Sharma', email: 'arjun.demo@skill2inter.com', role: 'AI/ML Student' },
  { name: 'Priya Nair',   email: 'priya.demo@skill2inter.com', role: 'Java Backend Student' },
  { name: 'Riya Patel',   email: 'riya.demo@skill2inter.com', role: 'Frontend Student' },
];

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState('login'); // login | register
  const [form, setForm] = useState({ name: '', email: '', password: 'demo' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const handleLogin = async (email = form.email) => {
    setLoading(true); setError('');
    try {
      const res = await studentAPI.login(email, 'demo');
      login(res);
      navigate('/');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    setLoading(true); setError('');
    try {
      await studentAPI.create({ name: form.name, email: form.email, password: 'demo' });
      const res = await studentAPI.login(form.email, 'demo');
      login(res);
      navigate('/');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'var(--color-bg)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 24,
    }}>
      <div style={{ width: '100%', maxWidth: 420 }}>
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div style={{
            width: 56, height: 56,
            background: 'linear-gradient(135deg, var(--color-primary), var(--color-accent))',
            borderRadius: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            marginBottom: 16,
            boxShadow: '0 8px 32px rgba(99,102,241,0.35)',
          }}>
            <Zap size={28} color="white" />
          </div>
          <h1 style={{ fontFamily: 'Plus Jakarta Sans, sans-serif', fontSize: 26, fontWeight: 800, textAlign: 'center' }}>
            Smart Internship Matcher
          </h1>
          <p className="text-muted text-sm mt-1" style={{ textAlign: 'center' }}>
            AI-powered career decision support
          </p>
        </div>

        {/* Card */}
        <div className="card">
          {/* Tabs */}
          <div className="tabs mb-6">
            <button className={`tab ${mode === 'login' ? 'active' : ''}`} onClick={() => setMode('login')}>
              <LogIn size={14} style={{ marginRight: 6, display: 'inline' }} />Sign In
            </button>
            <button className={`tab ${mode === 'register' ? 'active' : ''}`} onClick={() => setMode('register')}>
              <UserPlus size={14} style={{ marginRight: 6, display: 'inline' }} />Register
            </button>
          </div>

          {error && (
            <div className="alert alert-danger mb-4">
              <AlertCircle size={15} />
              {error}
            </div>
          )}

          {mode === 'login' ? (
            <>
              <div className="form-group">
                <label className="form-label">Email Address</label>
                <input className="form-input" type="email" placeholder="you@example.com" value={form.email} onChange={set('email')} />
              </div>
              <div className="form-group">
                <label className="form-label">Password</label>
                <input className="form-input" type="password" placeholder="Any password works in demo" value={form.password} onChange={set('password')} />
              </div>
              <button className="btn btn-primary w-full" onClick={() => handleLogin()} disabled={loading}>
                {loading ? 'Signing in…' : 'Sign In'}
              </button>

              {/* Demo quick login */}
              <div className="divider" />
              <div className="text-xs text-muted mb-3" style={{ textAlign: 'center' }}>Quick demo login</div>
              <div className="flex flex-col gap-2">
                {DEMO_USERS.map((u) => (
                  <button
                    key={u.email}
                    className="btn btn-outline btn-sm"
                    onClick={() => handleLogin(u.email)}
                    disabled={loading}
                  >
                    <span style={{ flex: 1, textAlign: 'left' }}>
                      {u.name}
                      <span className="text-xs text-muted" style={{ marginLeft: 8 }}>({u.role})</span>
                    </span>
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input className="form-input" type="text" placeholder="Your name" value={form.name} onChange={set('name')} />
              </div>
              <div className="form-group">
                <label className="form-label">Email Address</label>
                <input className="form-input" type="email" placeholder="you@example.com" value={form.email} onChange={set('email')} />
              </div>
              <button className="btn btn-primary w-full" onClick={handleRegister} disabled={loading || !form.name || !form.email}>
                {loading ? 'Creating account…' : 'Create Account'}
              </button>
              <p className="text-xs text-muted mt-3" style={{ textAlign: 'center' }}>
                After registering, complete your profile to get recommendations.
              </p>
            </>
          )}
        </div>

        <p className="text-xs text-muted mt-4" style={{ textAlign: 'center' }}>
          Match scores represent profile compatibility, not hiring probability.
        </p>
      </div>
    </div>
  );
}

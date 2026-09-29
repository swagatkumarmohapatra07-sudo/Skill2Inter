import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Sparkles, TrendingUp, Award,
  BookOpen, Briefcase, ChevronRight, Zap,
} from 'lucide-react';
import { dashboardAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { StatCard, Spinner, ProgressRow, scoreColor } from '../components/ui/index.jsx';

export default function Dashboard() {
  const { student } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!student) return;
    dashboardAPI.get(student.student_id)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [student]);

  if (loading) return <Spinner label="Loading dashboard…" />;

  const d = data || {};

  const profileColor = d.profile_completion >= 80
    ? 'var(--color-success)'
    : d.profile_completion >= 50
    ? 'var(--color-warning)'
    : 'var(--color-danger)';

  return (
    <div className="fade-in">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="text-muted text-sm mt-1">
            Welcome back, <strong>{student?.name}</strong>
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/internships')}>
          <Zap size={15} />
          Find Internships
        </button>
      </div>

      {error && (
        <div className="alert alert-warning mb-4">
          {error} — Run a match first to see dashboard data.
        </div>
      )}

      {/* Stat cards */}
      <div className="grid-4 mb-6">
        <StatCard
          label="Profile Completion"
          value={`${d.profile_completion ?? 0}%`}
          sub="Add more info to improve"
          icon={BookOpen}
          color={profileColor}
        />
        <StatCard
          label="Skills Added"
          value={d.total_skills ?? 0}
          sub={`${d.total_projects ?? 0} projects`}
          icon={Award}
          color="var(--color-accent)"
        />
        <StatCard
          label="Matches Run"
          value={d.recommended_count ?? 0}
          sub={`${d.eligible_count ?? 0} eligible`}
          icon={Briefcase}
          color="var(--color-primary)"
        />
        <StatCard
          label="Avg Match Score"
          value={d.average_match ? `${d.average_match}%` : '—'}
          sub="Across analyzed internships"
          icon={TrendingUp}
          color={d.average_match ? scoreColor(d.average_match) : 'var(--color-text-faint)'}
        />
      </div>

      <div className="grid-2" style={{ alignItems: 'start' }}>
        {/* Profile Completion Card */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="section-title">Profile Strength</h2>
            <button className="btn btn-sm btn-outline" onClick={() => navigate('/profile')}>
              Edit Profile
            </button>
          </div>

          <ProgressRow label="Overall Completion" value={d.profile_completion ?? 0} variant="primary" />

          <div className="divider" />

          <div className="alert alert-info">
            <Sparkles size={14} />
            Complete your profile to get more accurate internship recommendations.
          </div>

          <button className="btn btn-primary w-full mt-4" onClick={() => navigate('/profile')}>
            Complete Profile →
          </button>
        </div>

        {/* Top Skill Gaps */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="section-title">Top Skill Gaps</h2>
            <button className="btn btn-sm btn-outline" onClick={() => navigate('/skill-gap')}>
              View All
            </button>
          </div>

          {d.top_skill_gaps?.length > 0 ? (
            <div className="flex flex-col gap-2">
              {d.top_skill_gaps.map((gap, i) => (
                <div key={gap} className="flex items-center gap-3" style={{
                  padding: '10px 12px',
                  background: 'var(--color-surface-2)',
                  borderRadius: 8,
                  border: '1px solid var(--color-border)',
                }}>
                  <span style={{
                    width: 22, height: 22, borderRadius: 6,
                    background: 'rgba(239,68,68,0.15)', color: 'var(--color-danger)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 11, fontWeight: 700, flexShrink: 0,
                  }}>
                    {i + 1}
                  </span>
                  <span style={{ flex: 1, fontSize: 14 }}>{gap}</span>
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => navigate('/what-if')}
                    style={{ fontSize: 11 }}
                  >
                    What-If →
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state" style={{ padding: '32px 0' }}>
              <div className="text-muted text-sm">No gap data yet. Run a match first.</div>
              <button className="btn btn-primary btn-sm mt-4" onClick={() => navigate('/internships')}>
                Browse Internships
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Recent Matches */}
      {d.recent_matches?.length > 0 && (
        <div className="card mt-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="section-title">Recent Analyses</h2>
            <button className="btn btn-sm btn-outline" onClick={() => navigate('/recommendations')}>
              View All
            </button>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Company</th>
                <th>Role</th>
                <th>Match Score</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {d.recent_matches.map((m) => (
                <tr key={m.match_id}>
                  <td>{m.company}</td>
                  <td>{m.title}</td>
                  <td>
                    <span style={{ fontWeight: 700, color: scoreColor(m.score) }}>
                      {m.score}%
                    </span>
                  </td>
                  <td className="text-muted text-sm">
                    {m.created_at ? new Date(m.created_at).toLocaleDateString() : '—'}
                  </td>
                  <td>
                    <button
                      className="btn btn-ghost btn-sm"
                      onClick={() => navigate(`/match/${m.match_id}`)}
                    >
                      <ChevronRight size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Quick Actions */}
      {(!d.recent_matches || d.recent_matches.length === 0) && (
        <div className="card mt-6">
          <h2 className="section-title mb-4">Get Started</h2>
          <div className="grid-3">
            {[
              { icon: BookOpen, label: 'Complete Profile', desc: 'Add your skills and education', to: '/profile', color: 'var(--color-primary)' },
              { icon: Briefcase, label: 'Browse Internships', desc: 'Find and match internships', to: '/internships', color: 'var(--color-accent)' },
              { icon: Sparkles, label: 'Get Recommendations', desc: 'AI-ranked opportunities', to: '/recommendations', color: 'var(--color-success)' },
            ].map(({ icon: Icon, label, desc, to, color }) => (
              <button
                key={to}
                className="card card-hover"
                onClick={() => navigate(to)}
                style={{ textAlign: 'left', cursor: 'pointer', border: 'none', background: 'var(--color-surface-2)' }}
              >
                <div style={{
                  width: 40, height: 40, borderRadius: 10,
                  background: `${color}20`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  marginBottom: 12,
                }}>
                  <Icon size={20} color={color} />
                </div>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>{label}</div>
                <div className="text-sm text-muted">{desc}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

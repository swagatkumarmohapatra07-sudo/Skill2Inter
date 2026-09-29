import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Target, BookOpen, ChevronRight, Zap } from 'lucide-react';
import { dashboardAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { Spinner, EmptyState } from '../components/ui/index.jsx';

export default function SkillGapPage() {
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

  if (loading) return <Spinner label="Loading skill gaps…" />;
  if (error) return <div className="alert alert-danger">{error}</div>;

  const gaps = data?.top_skill_gaps || [];

  return (
    <div className="fade-in">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="page-title flex items-center gap-2">
            <TrendingUp size={24} color="var(--color-primary)" /> Skill Gap Analysis
          </h1>
          <p className="text-muted text-sm mt-1">
            The most common skills you are missing from the internships you've analyzed.
          </p>
        </div>
      </div>

      {gaps.length === 0 ? (
        <EmptyState 
          icon={Target} 
          title="No significant skill gaps found" 
          description="You haven't run enough matches, or you already have most of the required skills!" 
          action={
            <button className="btn btn-primary" onClick={() => navigate('/internships')}>
              Browse More Internships
            </button>
          }
        />
      ) : (
        <div className="flex flex-col gap-4">
          <div className="alert alert-info mb-2">
            Focusing on the top 1-2 skills from this list will drastically increase your match score across multiple internships.
          </div>

          {gaps.map((gap, index) => (
            <div key={gap} className="card flex items-start gap-4 fade-in" style={{ animationDelay: `${index * 0.05}s` }}>
              <div style={{ 
                width: 48, height: 48, borderRadius: 12, 
                background: 'rgba(239,68,68,0.1)', color: 'var(--color-danger)', 
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 20, fontWeight: 800, flexShrink: 0 
              }}>
                #{index + 1}
              </div>
              
              <div style={{ flex: 1 }}>
                <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>{gap}</h3>
                <p className="text-muted text-sm mb-4">
                  This skill appears frequently in your missing requirements. Learning it will unlock more opportunities.
                </p>
                
                <div style={{ background: 'var(--color-surface-2)', padding: 16, borderRadius: 8, border: '1px solid var(--color-border)' }}>
                  <div className="flex items-center gap-2 mb-2">
                    <BookOpen size={16} color="var(--color-primary-light)" />
                    <span style={{ fontWeight: 600, fontSize: 14 }}>Recommended Action</span>
                  </div>
                  <div className="text-sm">
                    Build a small project that uses <strong>{gap}</strong> and add it to your profile. 
                    (Check specific Match Results for tailored project ideas).
                  </div>
                </div>
              </div>

              <div style={{ width: 140, flexShrink: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
                <button className="btn btn-primary btn-sm w-full" onClick={() => navigate('/what-if')}>
                  <Zap size={14} /> Simulate +{gap}
                </button>
                <button className="btn btn-outline btn-sm w-full" onClick={() => navigate('/profile')}>
                  Add to Profile
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

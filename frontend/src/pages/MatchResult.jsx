import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle, AlertCircle, Info, Lightbulb, Zap, Briefcase } from 'lucide-react';
import { matchAPI, internshipAPI } from '../services/api';
import { ScoreCircle, ProgressRow, SkillBadge, EligibilityRow, Spinner, scoreColor } from '../components/ui/index.jsx';

export default function MatchResultPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [match, setMatch] = useState(null);
  const [internship, setInternship] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    matchAPI.get(id)
      .then(async (m) => {
        setMatch(m);
        const inv = await internshipAPI.get(m.internship_id);
        setInternship(inv);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Spinner label="Loading match result…" />;
  if (error) return <div className="alert alert-danger">{error}</div>;
  if (!match || !internship) return null;

  const matchedSkills = match.skill_gaps.filter((g) => g.gap_type === 'matched');
  const partialSkills = match.skill_gaps.filter((g) => g.gap_type === 'partial');
  const missingSkills = match.skill_gaps.filter((g) => g.gap_type === 'missing');

  const eligible = match.education_eligible && match.experience_eligible && match.location_eligible && match.availability_eligible;

  return (
    <div className="fade-in">
      <button className="btn btn-ghost btn-sm mb-4" onClick={() => navigate('/internships')}>
        <ArrowLeft size={14} />Back to Internships
      </button>

      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="badge badge-domain">{internship.domain}</span>
            {eligible ? (
              <span className="badge" style={{ background: 'rgba(16,185,129,0.1)', color: 'var(--color-success)', border: '1px solid rgba(16,185,129,0.2)' }}>
                <CheckCircle size={12} /> Eligible
              </span>
            ) : (
              <span className="badge" style={{ background: 'rgba(239,68,68,0.1)', color: 'var(--color-danger)', border: '1px solid rgba(239,68,68,0.2)' }}>
                <AlertCircle size={12} /> Eligibility Gaps
              </span>
            )}
          </div>
          <h1 className="page-title" style={{ fontSize: 24 }}>{internship.title}</h1>
          <p className="text-muted" style={{ fontSize: 16 }}>{internship.company} · {internship.location} ({internship.work_mode})</p>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-outline" onClick={() => navigate('/what-if', { state: { internship_id: internship.id } })}>
            <Lightbulb size={15} />What-If Simulator
          </button>
          <button className="btn btn-primary" disabled={!eligible}>
            <Briefcase size={15} />{eligible ? 'Apply Now' : 'Not Eligible'}
          </button>
        </div>
      </div>

      <div className="grid-3 mb-6">
        {/* Main Score Card */}
        <div className="card" style={{ gridColumn: 'span 1', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
          <h3 className="section-title mb-4">Overall Match</h3>
          <ScoreCircle score={match.overall_score} size={160} strokeWidth={12} />
          <p className="text-muted text-sm mt-6 mb-2">
            This score reflects profile compatibility based on your skills, education, and experience.
          </p>
        </div>

        {/* Component Scores */}
        <div className="card" style={{ gridColumn: 'span 2' }}>
          <h3 className="section-title mb-4">Breakdown</h3>
          <div className="grid-2 gap-x-8 gap-y-2">
            <ProgressRow label="Technical Skills" value={match.skill_score} />
            <ProgressRow label="Education" value={match.education_score} />
            <ProgressRow label="Project Relevance" value={match.project_score} />
            <ProgressRow label="Experience" value={match.experience_score} />
            <ProgressRow label="Location" value={match.location_score} />
            <ProgressRow label="Availability" value={match.availability_score} />
          </div>
        </div>
      </div>

      {/* Explanation Summary */}
      {match.summary && (
        <div className="alert alert-info mb-6" style={{ fontSize: 15, padding: 20 }}>
          <Info size={20} style={{ flexShrink: 0, marginTop: 2 }} />
          <div>{match.summary}</div>
        </div>
      )}

      <div className="grid-2">
        {/* Eligibility Check */}
        <div className="card">
          <h3 className="section-title mb-4">Eligibility Requirements</h3>
          <div className="flex flex-col gap-2">
            <EligibilityRow label="Education Requirement" eligible={match.education_eligible} note={internship.education_required} />
            <div className="divider my-2" />
            <EligibilityRow label="Experience Requirement" eligible={match.experience_eligible} note={internship.experience_required} />
            <div className="divider my-2" />
            <EligibilityRow label="Location Compatibility" eligible={match.location_eligible} note={`${internship.location} (${internship.work_mode})`} />
            <div className="divider my-2" />
            <EligibilityRow label="Availability" eligible={match.availability_eligible} />
          </div>
        </div>

        {/* Skill Gap Analysis */}
        <div className="card">
          <h3 className="section-title mb-4">Skill Gap Analysis</h3>
          
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle size={16} color="var(--color-success)" />
              <span style={{ fontWeight: 600 }}>Strong Match ({matchedSkills.length})</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {matchedSkills.map(s => <span key={s.id} className="badge badge-matched">{s.skill}</span>)}
              {matchedSkills.length === 0 && <span className="text-muted text-sm">None detected</span>}
            </div>
          </div>

          <div className="mb-4">
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle size={16} color="var(--color-warning)" />
              <span style={{ fontWeight: 600 }}>Partial Match ({partialSkills.length})</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {partialSkills.map(s => <span key={s.id} className="badge badge-partial">{s.skill}</span>)}
              {partialSkills.length === 0 && <span className="text-muted text-sm">None detected</span>}
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle size={16} color="var(--color-danger)" />
              <span style={{ fontWeight: 600 }}>Missing Skills ({missingSkills.length})</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {missingSkills.map(s => <span key={s.id} className="badge badge-missing">{s.skill}</span>)}
              {missingSkills.length === 0 && <span className="text-muted text-sm">None detected</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Action Plan */}
      {missingSkills.length > 0 && (
        <div className="card mt-6 border border-primary/20" style={{ background: 'var(--color-surface-2)', borderColor: 'var(--color-border-active)' }}>
          <h3 className="section-title mb-4 flex items-center gap-2">
            <Zap size={20} color="var(--color-primary)" />
            Action Plan to Improve
          </h3>
          <p className="text-muted mb-4">Acquire these skills and build projects to improve your match score for this role.</p>
          
          <div className="flex flex-col gap-3">
            {missingSkills.map((gap) => (
              <div key={gap.id} style={{ background: 'var(--color-surface)', padding: 16, borderRadius: 8, border: '1px solid var(--color-border)' }}>
                <div className="flex justify-between items-start mb-2">
                  <div style={{ fontWeight: 600, color: 'var(--color-danger)' }}>Missing: {gap.skill}</div>
                  <span className="badge">Weight: {gap.importance * 100}%</span>
                </div>
                <div className="text-sm">
                  <strong>Recommendation:</strong> {gap.recommendation}
                </div>
              </div>
            ))}
          </div>

          <button className="btn btn-primary mt-4" onClick={() => navigate('/what-if', { state: { internship_id: internship.id } })}>
            <Lightbulb size={15} /> Simulate improvements in What-If
          </button>
        </div>
      )}
    </div>
  );
}

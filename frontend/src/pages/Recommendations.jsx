import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, CheckCircle, AlertCircle, MapPin, Briefcase, ChevronRight, Zap } from 'lucide-react';
import { recommendationAPI, matchAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { Spinner, scoreColor, scoreLabel, EmptyState } from '../components/ui/index.jsx';

export default function RecommendationsPage() {
  const { student } = useAuth();
  const navigate = useNavigate();
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedForCompare, setSelectedForCompare] = useState([]);

  useEffect(() => {
    if (!student) return;
    recommendationAPI.get(student.student_id, 15)
      .then((data) => setRecs(data.recommendations))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [student]);

  const toggleCompare = (id) => {
    if (selectedForCompare.includes(id)) {
      setSelectedForCompare(selectedForCompare.filter(i => i !== id));
    } else {
      if (selectedForCompare.length >= 4) {
        alert('You can compare up to 4 internships at a time.');
        return;
      }
      setSelectedForCompare([...selectedForCompare, id]);
    }
  };

  const handleCompare = () => {
    if (selectedForCompare.length < 2) {
      alert('Select at least 2 internships to compare.');
      return;
    }
    navigate('/compare', { state: { internship_ids: selectedForCompare } });
  };

  if (loading) return <Spinner label="AI is analyzing all internships to find your best matches…" />;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="fade-in">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="page-title flex items-center gap-2">
            <Sparkles size={24} color="var(--color-primary)" /> Recommended For You
          </h1>
          <p className="text-muted text-sm mt-1">
            Based on your skills, projects, and eligibility.
          </p>
        </div>
        {selectedForCompare.length > 0 && (
          <button className="btn btn-primary slide-in" onClick={handleCompare}>
            <Zap size={15} /> Compare {selectedForCompare.length} selected
          </button>
        )}
      </div>

      {recs.length === 0 ? (
        <EmptyState 
          icon={Briefcase} 
          title="No recommendations yet" 
          description="We couldn't find matches. Try adding more skills to your profile or wait for new internships." 
        />
      ) : (
        <div className="flex flex-col gap-4">
          {recs.map((rec, index) => (
            <div key={rec.internship_id} className="card card-hover flex gap-4 items-stretch fade-in" style={{ animationDelay: `${index * 0.05}s` }}>
              
              {/* Score Left Col */}
              <div style={{ width: 100, flexShrink: 0, borderRight: '1px solid var(--color-border)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ fontSize: 32, fontWeight: 800, color: scoreColor(rec.overall_score), lineHeight: 1 }}>
                  {Math.round(rec.overall_score)}%
                </div>
                <div className="text-xs text-muted mt-1 font-semi">
                  {scoreLabel(rec.overall_score)}
                </div>
              </div>

              {/* Main Content */}
              <div style={{ flex: 1 }}>
                <div className="flex justify-between">
                  <div>
                    <div style={{ fontSize: 18, fontWeight: 700 }}>{rec.title}</div>
                    <div className="text-muted text-sm mb-2">{rec.company}</div>
                  </div>
                  <div className="flex items-center gap-2">
                    <input 
                      type="checkbox" 
                      id={`compare-${rec.internship_id}`} 
                      style={{ cursor: 'pointer', width: 16, height: 16 }}
                      checked={selectedForCompare.includes(rec.internship_id)}
                      onChange={() => toggleCompare(rec.internship_id)}
                    />
                    <label htmlFor={`compare-${rec.internship_id}`} className="text-xs text-muted cursor-pointer">Compare</label>
                  </div>
                </div>

                <div className="flex gap-4 text-xs text-muted mb-3">
                  <span className="flex items-center gap-1"><MapPin size={12} /> {rec.location} ({rec.work_mode})</span>
                  <span className="flex items-center gap-1"><Briefcase size={12} /> {rec.domain}</span>
                </div>

                <div className="flex gap-4">
                  {/* Good points */}
                  <div style={{ flex: 1 }}>
                    <div className="text-xs text-muted mb-1 font-semi">Why this matches you:</div>
                    <ul style={{ margin: 0, paddingLeft: 16, fontSize: 13 }} className="text-success">
                      <li>Matches {rec.matched_skills.length} required skills</li>
                      {rec.education_eligible && <li>Education requirements met</li>}
                      {rec.experience_eligible && <li>Experience requirements met</li>}
                    </ul>
                  </div>

                  {/* Gaps */}
                  <div style={{ flex: 1 }}>
                    <div className="text-xs text-muted mb-1 font-semi">Your Gaps:</div>
                    {rec.missing_skills.length > 0 ? (
                      <ul style={{ margin: 0, paddingLeft: 16, fontSize: 13 }} className="text-danger">
                        {rec.missing_skills.slice(0, 3).map(s => <li key={s}>{s}</li>)}
                        {rec.missing_skills.length > 3 && <li>+{rec.missing_skills.length - 3} more</li>}
                      </ul>
                    ) : (
                      <div className="text-xs text-muted flex items-center gap-1 mt-1">
                        <CheckCircle size={12} color="var(--color-success)" /> No major skill gaps
                      </div>
                    )}
                    {(!rec.education_eligible || !rec.experience_eligible) && (
                      <div className="text-xs text-warning flex items-center gap-1 mt-1">
                        <AlertCircle size={12} /> Missing some eligibility criteria
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Action Col */}
              <div style={{ width: 120, flexShrink: 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-end', borderLeft: '1px solid var(--color-border)', paddingLeft: 16 }}>
                <button className="btn btn-outline btn-sm w-full mb-2" onClick={() => navigate(`/match/${rec.match_id}`)}>
                  Details <ChevronRight size={14} />
                </button>
                <button 
                  className="btn btn-ghost btn-sm w-full text-xs" 
                  onClick={() => navigate('/what-if', { state: { internship_id: rec.internship_id } })}
                >
                  What-If <Sparkles size={12} />
                </button>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Lightbulb, Zap, ArrowRight, TrendingUp } from 'lucide-react';
import { internshipAPI, matchAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { ScoreCircle, Spinner, scoreColor } from '../components/ui/index.jsx';

export default function WhatIfPage() {
  const { student } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [internships, setInternships] = useState([]);
  const [selectedInternship, setSelectedInternship] = useState(location.state?.internship_id || '');
  const [skillsInput, setSkillsInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    internshipAPI.list()
      .then((data) => {
        setInternships(data);
        if (!selectedInternship && data.length > 0) {
          setSelectedInternship(data[0].id);
        }
      })
      .finally(() => setInitialLoading(false));
  }, [selectedInternship]);

  const runSimulation = async () => {
    if (!selectedInternship || !skillsInput.trim()) return;
    setLoading(true);
    try {
      const skillsList = skillsInput.split(',').map(s => s.trim()).filter(Boolean);
      const res = await matchAPI.whatIf(student.student_id, selectedInternship, skillsList);
      setResult(res);
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) return <Spinner label="Loading simulator…" />;

  return (
    <div className="fade-in">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="page-title flex items-center gap-2">
            <Lightbulb size={24} color="var(--color-accent)" /> What-If Simulator
          </h1>
          <p className="text-muted text-sm mt-1">
            See how your match score would improve if you acquired new skills.
          </p>
        </div>
      </div>

      <div className="grid-2" style={{ alignItems: 'start' }}>
        
        {/* Input Card */}
        <div className="card">
          <h3 className="section-title mb-4">Simulation Parameters</h3>
          
          <div className="form-group mb-4">
            <label className="form-label">Target Internship</label>
            <select 
              className="form-input" 
              value={selectedInternship} 
              onChange={(e) => { setSelectedInternship(e.target.value); setResult(null); }}
            >
              {internships.map(i => (
                <option key={i.id} value={i.id}>{i.company} - {i.title}</option>
              ))}
            </select>
          </div>

          <div className="form-group mb-6">
            <label className="form-label">Skills to acquire (comma-separated)</label>
            <input 
              className="form-input" 
              placeholder="e.g. React, Docker, Python" 
              value={skillsInput} 
              onChange={(e) => { setSkillsInput(e.target.value); setResult(null); }}
              onKeyDown={(e) => e.key === 'Enter' && runSimulation()}
            />
            <div className="text-xs text-muted mt-2">
              Tip: Check the <strong>Skill Gap</strong> page to see which skills you should add here.
            </div>
          </div>

          <button 
            className="btn btn-primary w-full" 
            onClick={runSimulation} 
            disabled={loading || !skillsInput.trim() || !selectedInternship}
          >
            {loading ? <Spinner /> : <><Zap size={16} /> Run Simulation</>}
          </button>
        </div>

        {/* Results Card */}
        {result ? (
          <div className="card fade-in" style={{ background: 'var(--color-surface-2)', border: '1px solid var(--color-border-active)' }}>
            <h3 className="section-title mb-4">Simulation Result</h3>
            
            <div className="flex items-center justify-around mb-8 mt-4">
              <div className="text-center">
                <div className="text-sm text-muted mb-2 font-semi">Current Match</div>
                <ScoreCircle score={result.current_score} size={100} strokeWidth={8} />
              </div>

              <div className="flex flex-col items-center justify-center text-success" style={{ padding: '0 20px' }}>
                <TrendingUp size={24} className="mb-1" />
                <div style={{ fontSize: 20, fontWeight: 800 }}>+{result.improvement}%</div>
                <ArrowRight size={20} className="mt-2 text-muted" />
              </div>

              <div className="text-center">
                <div className="text-sm text-muted mb-2 font-semi text-primary">Projected Match</div>
                <ScoreCircle score={result.projected_score} size={100} strokeWidth={8} />
              </div>
            </div>

            {result.changed_gaps.length > 0 ? (
              <div className="mb-4">
                <div className="text-sm font-semi mb-2">Gaps Closed:</div>
                <div className="flex flex-col gap-2">
                  {result.changed_gaps.map(g => (
                    <div key={g.skill} className="flex justify-between items-center bg-surface border border-border p-2 rounded">
                      <span className="font-semi">{g.skill}</span>
                      <span className="badge badge-matched">Resolved</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="alert alert-warning mb-4">
                These skills did not close any major gaps for this specific internship.
              </div>
            )}

            <div className="text-xs text-muted" style={{ fontStyle: 'italic', textAlign: 'center' }}>
              {result.note}
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <Lightbulb size={32} className="mb-4 text-muted" />
            <div className="text-muted text-sm text-center">
              Enter the skills you plan to learn and run the simulation to see how much your match score could improve.
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

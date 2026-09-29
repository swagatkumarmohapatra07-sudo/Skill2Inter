import { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { GitCompare, Check, X, AlertTriangle, ArrowLeft } from 'lucide-react';
import { matchAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { Spinner, scoreColor } from '../components/ui/index.jsx';

export default function ComparePage() {
  const { student } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  const initialIds = location.state?.internship_ids || [];
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!student || initialIds.length === 0) {
      setLoading(false);
      return;
    }
    
    matchAPI.compare(student.student_id, initialIds)
      .then(res => setData(res.comparisons))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [student, initialIds]);

  if (loading) return <Spinner label="Generating comparison..." />;

  if (!initialIds.length || data?.length === 0) {
    return (
      <div className="empty-state fade-in">
        <GitCompare size={40} className="mb-4 text-muted" />
        <h2 className="section-title">No Internships Selected</h2>
        <p className="text-muted mt-2 mb-4">Go to Recommendations to select internships to compare.</p>
        <button className="btn btn-primary" onClick={() => navigate('/recommendations')}>
          View Recommendations
        </button>
      </div>
    );
  }

  if (error) return <div className="alert alert-danger">{error}</div>;

  const getEligIcon = (val) => val ? <Check size={16} className="text-success" /> : <AlertTriangle size={16} className="text-warning" />;

  return (
    <div className="fade-in">
      <button className="btn btn-ghost btn-sm mb-4" onClick={() => navigate('/recommendations')}>
        <ArrowLeft size={14} /> Back
      </button>

      <h1 className="page-title flex items-center gap-2 mb-6">
        <GitCompare size={24} color="var(--color-primary)" /> Internship Comparison
      </h1>

      <div className="card" style={{ overflowX: 'auto', padding: 0 }}>
        <table className="data-table" style={{ minWidth: 600 }}>
          <thead>
            <tr>
              <th style={{ width: 140, background: 'var(--color-surface-2)' }}>Criteria</th>
              {data.map(i => (
                <th key={i.internship_id} style={{ textAlign: 'center' }}>
                  <Link to={`/match/${i.internship_id}`} style={{ color: 'inherit', textDecoration: 'none' }} className="hover:text-primary">
                    <div className="font-bold text-sm text-text">{i.company}</div>
                    <div className="font-normal">{i.title}</div>
                  </Link>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Overall Match</td>
              {data.map(i => (
                <td key={i.internship_id} className="text-center font-bold text-lg" style={{ color: scoreColor(i.overall_score) }}>
                  {i.overall_score}%
                </td>
              ))}
            </tr>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Tech Skills</td>
              {data.map(i => <td key={i.internship_id} className="text-center">{i.skill_score}%</td>)}
            </tr>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Education</td>
              {data.map(i => <td key={i.internship_id} className="text-center">{i.education_score}%</td>)}
            </tr>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Project Relevance</td>
              {data.map(i => <td key={i.internship_id} className="text-center">{i.project_score}%</td>)}
            </tr>
            
            {/* Eligibility Section */}
            <tr><td colSpan={data.length + 1} className="bg-surface-3 font-bold text-xs" style={{ padding: '8px 16px' }}>Eligibility & Location</td></tr>
            
            <tr>
              <td className="font-semi text-xs bg-surface-2">Location/Mode</td>
              {data.map(i => <td key={i.internship_id} className="text-center text-sm">{i.location} ({i.work_mode})</td>)}
            </tr>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Edu Eligible</td>
              {data.map(i => <td key={i.internship_id} className="text-center flex justify-center">{getEligIcon(i.education_eligible)}</td>)}
            </tr>
            <tr>
              <td className="font-semi text-xs bg-surface-2">Exp Eligible</td>
              {data.map(i => <td key={i.internship_id} className="text-center flex justify-center">{getEligIcon(i.experience_eligible)}</td>)}
            </tr>

            {/* Gaps Section */}
            <tr><td colSpan={data.length + 1} className="bg-surface-3 font-bold text-xs" style={{ padding: '8px 16px' }}>Key Gaps</td></tr>
            
            <tr>
              <td className="font-semi text-xs bg-surface-2 align-top">Missing Skills</td>
              {data.map(i => (
                <td key={i.internship_id} className="align-top">
                  {i.missing_skills.length > 0 ? (
                    <div className="flex flex-col gap-1 items-center">
                      {i.missing_skills.slice(0,3).map(s => <span key={s} className="badge badge-missing text-xs">{s}</span>)}
                      {i.missing_skills.length > 3 && <span className="text-xs text-muted">+{i.missing_skills.length-3} more</span>}
                    </div>
                  ) : (
                    <div className="text-center text-success text-sm flex items-center justify-center gap-1"><Check size={14} /> None</div>
                  )}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

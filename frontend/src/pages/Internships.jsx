import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, MapPin, Clock, Briefcase, Zap, Plus, ChevronRight } from 'lucide-react';
import { internshipAPI, matchAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { scoreColor } from '../components/ui/index.jsx';

const DOMAINS = ['All', 'AI/ML', 'Data Science', 'Web Development', 'Backend Development', 'Data Analytics', 'Cloud', 'Cybersecurity', 'UI/UX', 'Mobile Development', 'Software Development'];
const MODES = ['All', 'remote', 'onsite', 'hybrid'];

export default function InternshipsPage() {
  const { student } = useAuth();
  const navigate = useNavigate();
  const [internships, setInternships] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [matching, setMatching] = useState({});
  const [search, setSearch] = useState('');
  const [domain, setDomain] = useState('All');
  const [mode, setMode] = useState('All');
  const [showAdd, setShowAdd] = useState(false);
  const [desc, setDesc] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(null);
  const [newInternship, setNewInternship] = useState({ company: '', title: '', domain: 'AI/ML', location: '', work_mode: 'remote', duration: '', stipend: '', description: '' });

  useEffect(() => {
    internshipAPI.list().then(setInternships).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    let list = internships;
    if (domain !== 'All') list = list.filter((i) => i.domain === domain);
    if (mode !== 'All') list = list.filter((i) => i.work_mode === mode);
    if (search) list = list.filter((i) =>
      i.title.toLowerCase().includes(search.toLowerCase()) ||
      i.company.toLowerCase().includes(search.toLowerCase())
    );
    setFiltered(list);
  }, [internships, domain, mode, search]);

  const runMatch = async (internship_id) => {
    if (!student) return;
    setMatching((m) => ({ ...m, [internship_id]: true }));
    try {
      const result = await matchAPI.calculate(student.student_id, internship_id);
      navigate(`/match/${result.id}`);
    } catch (e) {
      alert('Match error: ' + e.message);
    } finally {
      setMatching((m) => ({ ...m, [internship_id]: false }));
    }
  };

  const analyzeDesc = async () => {
    if (!desc.trim()) return;
    setAnalyzing(true);
    try {
      const res = await internshipAPI.analyzeDescription(desc);
      setAnalyzed(res);
    } catch (e) { alert(e.message); }
    finally { setAnalyzing(false); }
  };

  const createFromDesc = async () => {
    if (!newInternship.company || !newInternship.title) { alert('Company and title required'); return; }
    try {
      const payload = {
        ...newInternship,
        description: desc,
        requirements: analyzed?.raw_requirements || [],
      };
      const created = await internshipAPI.create(payload);
      setInternships([created, ...internships]);
      setShowAdd(false);
      setDesc(''); setAnalyzed(null);
      setNewInternship({ company: '', title: '', domain: 'AI/ML', location: '', work_mode: 'remote', duration: '', stipend: '', description: '' });
      await runMatch(created.id);
    } catch (e) { alert(e.message); }
  };

  return (
    <div className="fade-in">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="page-title">Internships</h1>
          <p className="text-muted text-sm mt-1">{filtered.length} opportunities available</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowAdd(!showAdd)}>
          <Plus size={15} />Add / Paste Internship
        </button>
      </div>

      {/* Add Internship Panel */}
      {showAdd && (
        <div className="card mb-6 fade-in">
          <h3 className="section-title mb-4">Add New Internship</h3>

          <div className="grid-2 mb-4">
            <div className="form-group">
              <label className="form-label">Company Name *</label>
              <input className="form-input" placeholder="e.g. Google" value={newInternship.company} onChange={(e) => setNewInternship({ ...newInternship, company: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Role Title *</label>
              <input className="form-input" placeholder="e.g. ML Engineer Intern" value={newInternship.title} onChange={(e) => setNewInternship({ ...newInternship, title: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Domain</label>
              <select className="form-input" value={newInternship.domain} onChange={(e) => setNewInternship({ ...newInternship, domain: e.target.value })}>
                {DOMAINS.slice(1).map((d) => <option key={d}>{d}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Work Mode</label>
              <select className="form-input" value={newInternship.work_mode} onChange={(e) => setNewInternship({ ...newInternship, work_mode: e.target.value })}>
                {MODES.slice(1).map((m) => <option key={m}>{m}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Location</label>
              <input className="form-input" placeholder="e.g. Remote, Bangalore" value={newInternship.location} onChange={(e) => setNewInternship({ ...newInternship, location: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Duration</label>
              <input className="form-input" placeholder="e.g. 3 months" value={newInternship.duration} onChange={(e) => setNewInternship({ ...newInternship, duration: e.target.value })} />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Paste Internship Description (optional — AI will extract requirements)</label>
            <textarea className="form-input" rows={6} placeholder="Paste the full job description here..." value={desc} onChange={(e) => setDesc(e.target.value)} />
          </div>

          {desc && !analyzed && (
            <button className="btn btn-outline btn-sm mb-4" onClick={analyzeDesc} disabled={analyzing}>
              <Zap size={14} />{analyzing ? 'Analyzing…' : 'Extract Requirements from Description'}
            </button>
          )}

          {analyzed && (
            <div className="card mb-4 fade-in" style={{ background: 'var(--color-surface-2)' }}>
              <div style={{ fontWeight: 600, marginBottom: 8, fontSize: 13 }}>Extracted Requirements</div>
              <div className="flex flex-col gap-2">
                {analyzed.skills.length > 0 && (
                  <div>
                    <span className="text-xs text-muted">Skills: </span>
                    {analyzed.skills.map((s) => <span key={s} className="badge badge-skill" style={{ marginRight: 4 }}>{s}</span>)}
                  </div>
                )}
                {analyzed.education.length > 0 && (
                  <div>
                    <span className="text-xs text-muted">Education: </span>
                    {analyzed.education.map((e) => <span key={e} className="badge badge-domain" style={{ marginRight: 4 }}>{e}</span>)}
                  </div>
                )}
                {analyzed.preferred_skills.length > 0 && (
                  <div>
                    <span className="text-xs text-muted">Preferred: </span>
                    {analyzed.preferred_skills.map((s) => <span key={s} className="badge badge-partial" style={{ marginRight: 4 }}>{s}</span>)}
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="flex gap-3">
            <button className="btn btn-primary" onClick={createFromDesc}>
              <Zap size={15} />Save & Match Now
            </button>
            <button className="btn btn-outline" onClick={() => setShowAdd(false)}>Cancel</button>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-3 mb-6" style={{ flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: '1 1 240px' }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--color-text-faint)' }} />
          <input className="form-input" style={{ paddingLeft: 36 }} placeholder="Search by role or company…" value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <select className="form-input" style={{ flex: '0 1 180px' }} value={domain} onChange={(e) => setDomain(e.target.value)}>
          {DOMAINS.map((d) => <option key={d}>{d}</option>)}
        </select>
        <select className="form-input" style={{ flex: '0 1 140px' }} value={mode} onChange={(e) => setMode(e.target.value)}>
          {MODES.map((m) => <option key={m}>{m.charAt(0).toUpperCase() + m.slice(1)}</option>)}
        </select>
      </div>

      {/* Internship Cards */}
      {loading ? (
        <div className="text-muted text-sm">Loading internships…</div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"><Briefcase size={28} /></div>
          <div className="section-title">No internships found</div>
          <div className="text-muted text-sm mt-2">Try adjusting your filters or add a new internship.</div>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((i) => (
            <div key={i.id} className="internship-card">
              {/* Left */}
              <div style={{ flex: 1 }}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="badge badge-domain">{i.domain}</span>
                  <span className={`badge ${i.work_mode === 'remote' ? 'badge-matched' : 'badge-skill'}`}>
                    {i.work_mode}
                  </span>
                  {i.is_sample && <span className="badge" style={{ background: 'rgba(6,182,212,0.1)', color: 'var(--color-accent)', border: '1px solid rgba(6,182,212,0.2)', fontSize: 11 }}>Sample</span>}
                </div>
                <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 2 }}>{i.title}</div>
                <div className="text-muted text-sm">{i.company}</div>
                <div className="flex gap-4 mt-2" style={{ flexWrap: 'wrap' }}>
                  {i.location && <span className="text-xs text-muted flex items-center gap-1"><MapPin size={11} />{i.location}</span>}
                  {i.duration && <span className="text-xs text-muted flex items-center gap-1"><Clock size={11} />{i.duration}</span>}
                  {i.stipend && <span className="text-xs text-muted">{i.stipend}</span>}
                </div>
                {/* Skill pills */}
                {i.requirements?.slice(0, 6).filter(r => r.category === 'skill').length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
                    {i.requirements.filter(r => r.category === 'skill').slice(0, 6).map((r) => (
                      <span key={r.id} className="badge badge-skill" style={{ fontSize: 11 }}>{r.requirement}</span>
                    ))}
                    {i.requirements.filter(r => r.category === 'skill').length > 6 && (
                      <span className="badge badge-skill" style={{ fontSize: 11 }}>+{i.requirements.filter(r => r.category === 'skill').length - 6} more</span>
                    )}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex flex-col gap-2 items-center" style={{ flexShrink: 0 }}>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => runMatch(i.id)}
                  disabled={matching[i.id]}
                >
                  <Zap size={13} />
                  {matching[i.id] ? 'Matching…' : 'Match Me'}
                </button>
                <button className="btn btn-ghost btn-sm" onClick={() => navigate(`/internships/${i.id}`)}>
                  Details <ChevronRight size={13} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

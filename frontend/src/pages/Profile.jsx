import { useEffect, useState } from 'react';
import { Plus, X, Save, Loader } from 'lucide-react';
import { studentAPI } from '../services/api';
import { useAuth } from '../store/AuthContext';
import { Spinner } from '../components/ui/index.jsx';

const SKILL_CATS = ['programming', 'ml', 'web', 'database', 'cloud', 'devops', 'tool', 'soft'];
const PROFICIENCIES = ['beginner', 'intermediate', 'advanced', 'expert'];

export default function ProfilePage() {
  const { student, login } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');
  const [newSkill, setNewSkill] = useState({ skill_name: '', category: 'programming', proficiency: 'intermediate' });
  const [newProject, setNewProject] = useState({ title: '', description: '', technologies: '' });
  const [activeTab, setActiveTab] = useState('info');

  useEffect(() => {
    if (!student) return;
    studentAPI.get(student.student_id)
      .then(setProfile)
      .finally(() => setLoading(false));
  }, [student]);

  if (loading) return <Spinner label="Loading profile…" />;
  if (!profile) return <div className="alert alert-danger">Failed to load profile.</div>;

  const saveProfile = async () => {
    setSaving(true);
    try {
      const { skills, projects, experiences, certifications, ...rest } = profile;
      await studentAPI.update(profile.id, rest);
      setMsg('Profile saved!');
      setTimeout(() => setMsg(''), 3000);
    } catch (e) {
      setMsg('Error: ' + e.message);
    } finally {
      setSaving(false);
    }
  };

  const addSkill = async () => {
    if (!newSkill.skill_name.trim()) return;
    try {
      const sk = await studentAPI.addSkill(profile.id, newSkill);
      setProfile({ ...profile, skills: [...profile.skills, sk] });
      setNewSkill({ skill_name: '', category: 'programming', proficiency: 'intermediate' });
    } catch (e) { setMsg('Error: ' + e.message); }
  };

  const removeSkill = async (skid) => {
    try {
      await studentAPI.removeSkill(profile.id, skid);
      setProfile({ ...profile, skills: profile.skills.filter((s) => s.id !== skid) });
    } catch (e) { setMsg('Error: ' + e.message); }
  };

  const addProject = async () => {
    if (!newProject.title.trim()) return;
    try {
      const pr = await studentAPI.addProject(profile.id, newProject);
      setProfile({ ...profile, projects: [...profile.projects, pr] });
      setNewProject({ title: '', description: '', technologies: '' });
    } catch (e) { setMsg('Error: ' + e.message); }
  };

  const removeProject = async (pid) => {
    try {
      await studentAPI.removeProject(profile.id, pid);
      setProfile({ ...profile, projects: profile.projects.filter((p) => p.id !== pid) });
    } catch (e) { setMsg('Error: ' + e.message); }
  };

  const field = (key) => (e) => setProfile({ ...profile, [key]: e.target.value });

  const TABS = ['info', 'skills', 'projects', 'experience'];

  return (
    <div className="fade-in">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="page-title">My Profile</h1>
          <p className="text-muted text-sm mt-1">Keep your profile updated for better matches</p>
        </div>
        <button className="btn btn-primary" onClick={saveProfile} disabled={saving}>
          {saving ? <Loader size={15} className="spinner" style={{ width: 15, height: 15 }} /> : <Save size={15} />}
          Save Changes
        </button>
      </div>

      {msg && <div className={`alert ${msg.startsWith('Error') ? 'alert-danger' : 'alert-success'} mb-4`}>{msg}</div>}

      {/* Tabs */}
      <div className="tabs">
        {TABS.map((t) => (
          <button key={t} className={`tab ${activeTab === t ? 'active' : ''}`} onClick={() => setActiveTab(t)}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* Info Tab */}
      {activeTab === 'info' && (
        <div className="grid-2 gap-4">
          <div className="card">
            <h3 className="section-title mb-4">Personal Info</h3>
            {[
              ['Full Name', 'name', 'text'],
              ['Email', 'email', 'email'],
              ['Phone', 'phone', 'text'],
              ['Location', 'location', 'text'],
              ['Bio', 'bio', 'textarea'],
            ].map(([label, key, type]) => (
              <div className="form-group" key={key}>
                <label className="form-label">{label}</label>
                {type === 'textarea' ? (
                  <textarea className="form-input" rows={3} value={profile[key] || ''} onChange={field(key)} />
                ) : (
                  <input className="form-input" type={type} value={profile[key] || ''} onChange={field(key)} />
                )}
              </div>
            ))}
          </div>
          <div className="card">
            <h3 className="section-title mb-4">Education & Preferences</h3>
            {[
              ['College', 'college', 'text'],
              ['Degree (e.g. B.Tech)', 'degree', 'text'],
              ['Branch (e.g. CSE)', 'branch', 'text'],
              ['Graduation Year', 'graduation_year', 'number'],
              ['CGPA', 'cgpa', 'number'],
            ].map(([label, key, type]) => (
              <div className="form-group" key={key}>
                <label className="form-label">{label}</label>
                <input className="form-input" type={type} value={profile[key] || ''} onChange={field(key)} />
              </div>
            ))}
            <div className="form-group">
              <label className="form-label">Remote Preference</label>
              <select className="form-input" value={profile.remote_preference || 'open'} onChange={field('remote_preference')}>
                <option value="remote">Remote Only</option>
                <option value="onsite">Onsite Only</option>
                <option value="open">Open to Both</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Availability</label>
              <input className="form-input" type="text" placeholder="e.g. 3 months, immediate" value={profile.availability || ''} onChange={field('availability')} />
            </div>
            <div className="form-group">
              <label className="form-label">Preferred Location</label>
              <input className="form-input" type="text" placeholder="e.g. Bangalore, Remote" value={profile.preferred_location || ''} onChange={field('preferred_location')} />
            </div>
          </div>
        </div>
      )}

      {/* Skills Tab */}
      {activeTab === 'skills' && (
        <div className="card">
          <h3 className="section-title mb-4">Skills ({profile.skills.length})</h3>

          {/* Add skill */}
          <div className="flex gap-2 mb-4" style={{ flexWrap: 'wrap' }}>
            <input
              className="form-input" style={{ flex: '1 1 180px', minWidth: 160 }}
              placeholder="Skill name (e.g. Python)"
              value={newSkill.skill_name}
              onChange={(e) => setNewSkill({ ...newSkill, skill_name: e.target.value })}
              onKeyDown={(e) => e.key === 'Enter' && addSkill()}
            />
            <select className="form-input" style={{ flex: '1 1 140px' }} value={newSkill.category} onChange={(e) => setNewSkill({ ...newSkill, category: e.target.value })}>
              {SKILL_CATS.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
            <select className="form-input" style={{ flex: '1 1 140px' }} value={newSkill.proficiency} onChange={(e) => setNewSkill({ ...newSkill, proficiency: e.target.value })}>
              {PROFICIENCIES.map((p) => <option key={p} value={p}>{p}</option>)}
            </select>
            <button className="btn btn-primary" onClick={addSkill}>
              <Plus size={15} />Add
            </button>
          </div>

          {/* Skill list */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {profile.skills.map((sk) => (
              <div key={sk.id} className="badge badge-skill" style={{ padding: '6px 12px', fontSize: 13 }}>
                <span>{sk.skill_name}</span>
                <span className="text-faint" style={{ marginLeft: 4, fontSize: 11 }}>· {sk.proficiency}</span>
                <button
                  onClick={() => removeSkill(sk.id)}
                  style={{ marginLeft: 6, background: 'none', border: 'none', cursor: 'pointer', color: 'inherit', padding: 0, lineHeight: 1 }}
                >
                  <X size={12} />
                </button>
              </div>
            ))}
            {profile.skills.length === 0 && (
              <div className="text-muted text-sm">No skills added yet. Add your first skill above.</div>
            )}
          </div>
        </div>
      )}

      {/* Projects Tab */}
      {activeTab === 'projects' && (
        <div className="card">
          <h3 className="section-title mb-4">Projects ({profile.projects.length})</h3>

          {/* Add project */}
          <div className="card" style={{ background: 'var(--color-surface-2)', marginBottom: 20 }}>
            <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Add Project</h4>
            <div className="form-group">
              <label className="form-label">Project Title</label>
              <input className="form-input" placeholder="e.g. ML Price Predictor" value={newProject.title} onChange={(e) => setNewProject({ ...newProject, title: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea className="form-input" rows={2} placeholder="What does it do?" value={newProject.description} onChange={(e) => setNewProject({ ...newProject, description: e.target.value })} />
            </div>
            <div className="form-group">
              <label className="form-label">Technologies (comma-separated)</label>
              <input className="form-input" placeholder="python, react, docker" value={newProject.technologies} onChange={(e) => setNewProject({ ...newProject, technologies: e.target.value })} />
            </div>
            <button className="btn btn-primary btn-sm" onClick={addProject} disabled={!newProject.title}>
              <Plus size={14} />Add Project
            </button>
          </div>

          {/* Project list */}
          <div className="flex flex-col gap-3">
            {profile.projects.map((pr) => (
              <div key={pr.id} className="card card-sm" style={{ background: 'var(--color-surface-2)' }}>
                <div className="flex justify-between items-start">
                  <div>
                    <div style={{ fontWeight: 600, marginBottom: 4 }}>{pr.title}</div>
                    {pr.description && <div className="text-sm text-muted mb-2">{pr.description}</div>}
                    {pr.technologies && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                        {pr.technologies.split(',').map((t) => (
                          <span key={t} className="badge badge-domain">{t.trim()}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  <button className="btn btn-ghost btn-sm" onClick={() => removeProject(pr.id)}>
                    <X size={14} />
                  </button>
                </div>
              </div>
            ))}
            {profile.projects.length === 0 && (
              <div className="text-muted text-sm">No projects yet. Projects boost your match score significantly.</div>
            )}
          </div>
        </div>
      )}

      {/* Experience Tab */}
      {activeTab === 'experience' && (
        <div className="card">
          <h3 className="section-title mb-4">Experience & Certifications</h3>
          <div className="alert alert-info">
            Experience and certification tracking will be enhanced in Phase 2.
            For now, focus on skills and projects for the best match results.
          </div>
          <div className="flex flex-col gap-2 mt-4">
            {profile.experiences?.map((e) => (
              <div key={e.id} className="card card-sm" style={{ background: 'var(--color-surface-2)' }}>
                <div style={{ fontWeight: 600 }}>{e.role} at {e.company}</div>
                <div className="text-xs text-muted">{e.start_date} – {e.is_current ? 'Present' : e.end_date}</div>
              </div>
            ))}
            {(!profile.experiences || profile.experiences.length === 0) && (
              <div className="text-muted text-sm">No experience records yet.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

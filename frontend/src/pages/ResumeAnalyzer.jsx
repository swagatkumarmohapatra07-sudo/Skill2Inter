import { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Info } from 'lucide-react';
import { resumeAPI } from '../services/api';

export default function ResumeAnalyzerPage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragging, setDragging] = useState(false);

  const handleFile = (f) => {
    if (!f) return;
    const allowed = ['.pdf', '.docx', '.doc', '.txt'];
    const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase();
    if (!allowed.includes(ext)) {
      setError(`Unsupported file type: ${ext}`);
      return;
    }
    setFile(f);
    setError('');
    setResult(null);
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true); setError('');
    try {
      const res = await resumeAPI.analyze(file);
      setResult(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  return (
    <div className="fade-in">
      <h1 className="page-title mb-1">Resume Analyzer</h1>
      <p className="text-muted text-sm mb-6">
        Upload your resume — AI will extract skills, education, and projects automatically.
      </p>

      <div className="alert alert-info mb-6">
        <Info size={14} />
        <span>
          <strong>Phase 1 Notice:</strong> Full NLP-based extraction is coming in Phase 4.
          For now, upload validates your file and provides manual profile editing.
          Your profile skills and projects are already used for matching.
        </span>
      </div>

      {/* Drop Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => document.getElementById('resume-file-input').click()}
        style={{
          border: `2px dashed ${dragging ? 'var(--color-primary)' : 'var(--color-border)'}`,
          borderRadius: 'var(--radius-lg)',
          padding: '48px 32px',
          textAlign: 'center',
          cursor: 'pointer',
          background: dragging ? 'rgba(99,102,241,0.05)' : 'var(--color-surface)',
          transition: 'all 0.2s ease',
          marginBottom: 16,
        }}
      >
        <input
          id="resume-file-input"
          type="file"
          accept=".pdf,.docx,.doc,.txt"
          style={{ display: 'none' }}
          onChange={(e) => handleFile(e.target.files[0])}
        />
        <Upload size={36} color="var(--color-text-faint)" style={{ marginBottom: 12 }} />
        <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 6 }}>
          {file ? file.name : 'Drop your resume here or click to upload'}
        </div>
        <div className="text-muted text-sm">Supported: PDF, DOCX, DOC, TXT · Max 5 MB</div>
      </div>

      {error && (
        <div className="alert alert-danger mb-4">
          <AlertCircle size={15} />{error}
        </div>
      )}

      {file && !result && (
        <button className="btn btn-primary" onClick={analyze} disabled={loading}>
          {loading ? 'Analyzing…' : 'Analyze Resume'}
        </button>
      )}

      {/* Result */}
      {result && (
        <div className="card mt-6 fade-in">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle size={20} color="var(--color-success)" />
            <span className="section-title">Extraction Complete</span>
          </div>

          <div className="alert alert-warning mb-4">
            <Info size={14} />
            {result.note}
          </div>

          {result.skills?.length > 0 && (
            <div className="mb-4">
              <div className="form-label">Extracted Skills</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 6 }}>
                {result.skills.map((s) => (
                  <span key={s} className="badge badge-skill">{s}</span>
                ))}
              </div>
            </div>
          )}

          <div className="text-sm text-muted" style={{ fontFamily: 'monospace', background: 'var(--color-surface-2)', padding: 12, borderRadius: 8 }}>
            {result.raw_text_preview}
          </div>

          <div className="mt-4 alert alert-info">
            <FileText size={14} />
            Go to <strong>My Profile</strong> to manually add your skills and projects for accurate matching.
          </div>
        </div>
      )}
    </div>
  );
}

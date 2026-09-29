/** ScoreCircle — SVG circular progress with score number */
export function ScoreCircle({ score = 0, size = 120, strokeWidth = 8 }) {
  const radius = (size - strokeWidth * 2) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color = score >= 75 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444';
  const label = score >= 75 ? 'Strong Match' : score >= 50 ? 'Partial Match' : 'Weak Match';

  return (
    <div className="score-circle" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke={color} strokeWidth={strokeWidth}
          strokeDasharray={circumference} strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.8s cubic-bezier(.4,0,.2,1)' }}
        />
      </svg>
      <div className="score-circle-text">
        <div style={{ fontSize: size * 0.22, fontWeight: 800, color, lineHeight: 1 }}>
          {Math.round(score)}%
        </div>
        <div style={{ fontSize: size * 0.09, color: 'var(--color-text-muted)', marginTop: 4 }}>
          {label}
        </div>
      </div>
    </div>
  );
}

/** ProgressRow — labeled horizontal progress bar */
export function ProgressRow({ label, value, variant = 'primary', showValue = true }) {
  return (
    <div style={{ marginBottom: 12 }}>
      <div className="flex justify-between mb-1">
        <span className="text-sm text-muted">{label}</span>
        {showValue && (
          <span className="text-sm font-semi" style={{
            color: value >= 75 ? 'var(--color-success)' : value >= 50 ? 'var(--color-warning)' : 'var(--color-danger)',
          }}>
            {Math.round(value)}%
          </span>
        )}
      </div>
      <div className="progress-bar">
        <div
          className={`progress-fill ${variant}`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
    </div>
  );
}

/** SkillBadge */
export function SkillBadge({ label, type = 'skill' }) {
  return <span className={`badge badge-${type}`}>{label}</span>;
}

/** StatCard */
export function StatCard({ label, value, sub, icon: Icon, color = 'var(--color-primary)' }) {
  return (
    <div className="stat-card" style={{ '--accent-color': color }}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-muted">{label}</span>
        {Icon && (
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: `${color}20`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Icon size={18} color={color} />
          </div>
        )}
      </div>
      <div style={{ fontSize: 28, fontWeight: 800, lineHeight: 1 }}>{value}</div>
      {sub && <div className="text-xs text-muted mt-1">{sub}</div>}
    </div>
  );
}

/** LoadingSpinner */
export function Spinner({ label = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center" style={{ padding: '48px 0', gap: 12 }}>
      <div className="spinner" />
      <span className="text-sm text-muted">{label}</span>
    </div>
  );
}

/** EmptyState */
export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="empty-state">
      {Icon && (
        <div className="empty-state-icon">
          <Icon size={28} />
        </div>
      )}
      <div className="section-title mb-2">{title}</div>
      {description && <p className="text-muted" style={{ maxWidth: 360 }}>{description}</p>}
      {action && <div style={{ marginTop: 20 }}>{action}</div>}
    </div>
  );
}

/** EligibilityRow */
export function EligibilityRow({ label, eligible, note }) {
  const type = eligible === true ? 'ok' : eligible === false ? 'fail' : 'warn';
  const symbol = type === 'ok' ? '✓' : type === 'fail' ? '✗' : '⚠';
  return (
    <div className="eligibility-item">
      <div className={`eligibility-icon ${type}`}>{symbol}</div>
      <div>
        <div style={{ fontSize: 14 }}>{label}</div>
        {note && <div className="text-xs text-muted">{note}</div>}
      </div>
    </div>
  );
}

/** ScoreColor helper */
export function scoreColor(score) {
  if (score >= 75) return 'var(--color-success)';
  if (score >= 50) return 'var(--color-warning)';
  return 'var(--color-danger)';
}

/** ScoreLabel helper */
export function scoreLabel(score) {
  if (score >= 85) return 'Excellent';
  if (score >= 70) return 'Strong';
  if (score >= 55) return 'Moderate';
  if (score >= 40) return 'Partial';
  return 'Low';
}

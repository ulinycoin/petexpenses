// ───────────────────────────────────────────────────────────────
// Reusable UI components: Paw, Sticker, Slider, etc.
// ───────────────────────────────────────────────────────────────
const { useState, useEffect, useRef, useMemo, useCallback } = React;

// ── PAW GLYPH (5 simple circles, no complex SVG) ──────────────
function Paw({ size = 32, color = 'currentColor', className = '', style = {} }) {
  return (
    <svg viewBox="0 0 40 40" width={size} height={size} className={className} style={style} aria-hidden="true">
      <circle cx="20" cy="24" r="10" fill={color} />
      <circle cx="8"  cy="14" r="4.5" fill={color} />
      <circle cx="32" cy="14" r="4.5" fill={color} />
      <circle cx="14" cy="5"  r="3.6" fill={color} />
      <circle cx="26" cy="5"  r="3.6" fill={color} />
    </svg>
  );
}

// ── STICKER (rotated card-as-sticker) ─────────────────────────
function Sticker({ rotate = 0, children, className = '', style = {}, onClick }) {
  return (
    <div
      className={`sticker ${className}`}
      style={{
        transform: `rotate(${rotate}deg)`,
        ...style,
      }}
      onClick={onClick}
    >
      {children}
    </div>
  );
}

// ── DOTTED HALFTONE BACKGROUND ────────────────────────────────
function HalftoneBg({ color = 'rgba(27,19,64,0.07)', size = 14 }) {
  return (
    <div
      aria-hidden="true"
      style={{
        position: 'absolute', inset: 0,
        backgroundImage: `radial-gradient(${color} 1.4px, transparent 1.6px)`,
        backgroundSize: `${size}px ${size}px`,
        pointerEvents: 'none',
      }}
    />
  );
}

// ── BIG BOLD SLIDER ───────────────────────────────────────────
function BigSlider({ label, value, onChange, min, max, step = 1, format = (v) => v, ticks = null, accent = '#FF5A3C' }) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <div className="bigslider">
      <div className="bigslider-head">
        <div className="bigslider-label">{label}</div>
        <div className="bigslider-value" style={{ color: accent }}>{format(value)}</div>
      </div>
      <div className="bigslider-track-wrap">
        <input
          type="range"
          min={min} max={max} step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="bigslider-input"
          style={{ '--pct': pct + '%', '--accent': accent }}
          aria-label={label}
        />
      </div>
      {ticks && (
        <div className="bigslider-ticks">
          {ticks.map((t, i) => <span key={i}>{t}</span>)}
        </div>
      )}
    </div>
  );
}

// ── PILL SEGMENT (segmented toggle, big and chunky) ───────────
function PillSegment({ options, value, onChange, accent = '#FF5A3C', size = 'md' }) {
  return (
    <div className={`pill-seg pill-seg-${size}`}>
      {options.map((opt) => {
        const active = opt.value === value;
        return (
          <button
            key={opt.value}
            className={`pill-seg-btn ${active ? 'active' : ''}`}
            style={active ? { background: accent, color: '#fff' } : {}}
            onClick={() => onChange(opt.value)}
          >
            {opt.icon && <span className="pill-seg-icon">{opt.icon}</span>}
            <span>{opt.label}</span>
          </button>
        );
      })}
    </div>
  );
}

// ── BREED SEARCH (autocomplete) ───────────────────────────────
function BreedSearch({ breeds, value, onChange, placeholder, accent = '#FF5A3C' }) {
  const [open, setOpen] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const wrapRef = useRef(null);
  const names = useMemo(() => Object.keys(breeds).sort(), [breeds]);
  const q = (value || '').toLowerCase().trim();
  const matches = useMemo(() => {
    if (!q) return [];
    return names.filter((n) => n.toLowerCase().includes(q)).slice(0, 7);
  }, [q, names]);

  useEffect(() => {
    function onDoc(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, []);

  function pick(name) {
    onChange(name);
    setOpen(false);
    setActiveIdx(-1);
  }

  function onKey(e) {
    if (!open || !matches.length) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); setActiveIdx(i => Math.min(i + 1, matches.length - 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActiveIdx(i => Math.max(i - 1, 0)); }
    else if (e.key === 'Enter' && activeIdx >= 0) { e.preventDefault(); pick(matches[activeIdx]); }
    else if (e.key === 'Escape') { setOpen(false); }
  }

  return (
    <div className="breed-search" ref={wrapRef}>
      <input
        className="breed-input"
        value={value}
        onChange={(e) => { onChange(e.target.value); setOpen(true); setActiveIdx(-1); }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKey}
        placeholder={placeholder}
        autoComplete="off"
        style={{ '--accent': accent }}
      />
      {open && matches.length > 0 && (
        <ul className="breed-list" role="listbox">
          {matches.map((name, i) => {
            const [size, coat] = breeds[name];
            const sizeMap = { small: 'Small', medium: 'Medium', large: 'Large', giant: 'Giant' };
            const coatMap = { short: 'Short', long: 'Long', wire: 'Curly/Wire' };
            return (
              <li
                key={name}
                onMouseDown={() => pick(name)}
                className={i === activeIdx ? 'active' : ''}
              >
                <span className="bl-name">{name}</span>
                <span className="bl-meta">{sizeMap[size]} · {coatMap[coat]}</span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

// ── ANIMATED $ NUMBER ─────────────────────────────────────────
function AnimatedDollar({ value, duration = 700, className = '', style = {} }) {
  const [display, setDisplay] = useState(value);
  const fromRef = useRef(value);
  const startRef = useRef(0);
  const rafRef = useRef(0);

  useEffect(() => {
    cancelAnimationFrame(rafRef.current);
    fromRef.current = display;
    startRef.current = performance.now();
    function tick(now) {
      const t = Math.min(1, (now - startRef.current) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const v = Math.round(fromRef.current + (value - fromRef.current) * eased);
      setDisplay(v);
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
    }
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value]);

  return <span className={className} style={style}>${display.toLocaleString()}</span>;
}

// ── DONUT BREAKDOWN ───────────────────────────────────────────
function Donut({ items, total, size = 220, stroke = 36 }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  let offset = 0;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(27,19,64,0.08)" strokeWidth={stroke} />
      {items.map((it, i) => {
        const frac = it.amount / total;
        const dash = frac * c;
        const seg = (
          <circle
            key={i}
            cx={size/2} cy={size/2} r={r} fill="none"
            stroke={it.color} strokeWidth={stroke}
            strokeDasharray={`${dash} ${c - dash}`}
            strokeDashoffset={-offset}
            transform={`rotate(-90 ${size/2} ${size/2})`}
            style={{ transition: 'stroke-dasharray 0.5s ease, stroke-dashoffset 0.5s ease' }}
            strokeLinecap="butt"
          />
        );
        offset += dash;
        return seg;
      })}
    </svg>
  );
}

// ── EXPOSE TO GLOBAL ──────────────────────────────────────────
Object.assign(window, { Paw, Sticker, HalftoneBg, BigSlider, PillSegment, BreedSearch, AnimatedDollar, Donut });

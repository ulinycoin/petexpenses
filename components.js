const { useState, useEffect, useRef, useMemo, useCallback } = React;
function Paw({ size = 32, color = "currentColor", className = "", style = {} }) {
  return /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 40 40", width: size, height: size, className, style, "aria-hidden": "true" }, /* @__PURE__ */ React.createElement("circle", { cx: "20", cy: "24", r: "10", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "8", cy: "14", r: "4.5", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "32", cy: "14", r: "4.5", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "14", cy: "5", r: "3.6", fill: color }), /* @__PURE__ */ React.createElement("circle", { cx: "26", cy: "5", r: "3.6", fill: color }));
}
function Sticker({ rotate = 0, children, className = "", style = {}, onClick }) {
  return /* @__PURE__ */ React.createElement(
    "div",
    {
      className: `sticker ${className}`,
      style: {
        transform: `rotate(${rotate}deg)`,
        ...style
      },
      onClick
    },
    children
  );
}
function HalftoneBg({ color = "rgba(27,19,64,0.07)", size = 14 }) {
  return /* @__PURE__ */ React.createElement(
    "div",
    {
      "aria-hidden": "true",
      style: {
        position: "absolute",
        inset: 0,
        backgroundImage: `radial-gradient(${color} 1.4px, transparent 1.6px)`,
        backgroundSize: `${size}px ${size}px`,
        pointerEvents: "none"
      }
    }
  );
}
function BigSlider({ label, value, onChange, min, max, step = 1, format = (v) => v, ticks = null, accent = "#FF5A3C" }) {
  const pct = (value - min) / (max - min) * 100;
  return /* @__PURE__ */ React.createElement("div", { className: "bigslider" }, /* @__PURE__ */ React.createElement("div", { className: "bigslider-head" }, /* @__PURE__ */ React.createElement("div", { className: "bigslider-label" }, label), /* @__PURE__ */ React.createElement("div", { className: "bigslider-value", style: { color: accent } }, format(value))), /* @__PURE__ */ React.createElement("div", { className: "bigslider-track-wrap" }, /* @__PURE__ */ React.createElement(
    "input",
    {
      type: "range",
      min,
      max,
      step,
      value,
      onChange: (e) => onChange(Number(e.target.value)),
      className: "bigslider-input",
      style: { "--pct": pct + "%", "--accent": accent }
    }
  )), ticks && /* @__PURE__ */ React.createElement("div", { className: "bigslider-ticks" }, ticks.map((t, i) => /* @__PURE__ */ React.createElement("span", { key: i }, t))));
}
function PillSegment({ options, value, onChange, accent = "#FF5A3C", size = "md" }) {
  return /* @__PURE__ */ React.createElement("div", { className: `pill-seg pill-seg-${size}` }, options.map((opt) => {
    const active = opt.value === value;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: opt.value,
        className: `pill-seg-btn ${active ? "active" : ""}`,
        style: active ? { background: accent, color: "#fff" } : {},
        onClick: () => onChange(opt.value)
      },
      opt.icon && /* @__PURE__ */ React.createElement("span", { className: "pill-seg-icon" }, opt.icon),
      /* @__PURE__ */ React.createElement("span", null, opt.label)
    );
  }));
}
function BreedSearch({ breeds, value, onChange, placeholder, accent = "#FF5A3C" }) {
  const [open, setOpen] = useState(false);
  const [activeIdx, setActiveIdx] = useState(-1);
  const wrapRef = useRef(null);
  const names = useMemo(() => Object.keys(breeds).sort(), [breeds]);
  const q = (value || "").toLowerCase().trim();
  const matches = useMemo(() => {
    if (!q) return [];
    return names.filter((n) => n.toLowerCase().includes(q)).slice(0, 7);
  }, [q, names]);
  useEffect(() => {
    function onDoc(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, []);
  function pick(name) {
    onChange(name);
    setOpen(false);
    setActiveIdx(-1);
  }
  function onKey(e) {
    if (!open || !matches.length) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActiveIdx((i) => Math.min(i + 1, matches.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIdx((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && activeIdx >= 0) {
      e.preventDefault();
      pick(matches[activeIdx]);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  }
  return /* @__PURE__ */ React.createElement("div", { className: "breed-search", ref: wrapRef }, /* @__PURE__ */ React.createElement(
    "input",
    {
      className: "breed-input",
      value,
      onChange: (e) => {
        onChange(e.target.value);
        setOpen(true);
        setActiveIdx(-1);
      },
      onFocus: () => setOpen(true),
      onKeyDown: onKey,
      placeholder,
      autoComplete: "off",
      style: { "--accent": accent }
    }
  ), open && matches.length > 0 && /* @__PURE__ */ React.createElement("ul", { className: "breed-list", role: "listbox" }, matches.map((name, i) => {
    const [size, coat] = breeds[name];
    const sizeMap = { small: "Small", medium: "Medium", large: "Large", giant: "Giant" };
    const coatMap = { short: "Short", long: "Long", wire: "Curly/Wire" };
    return /* @__PURE__ */ React.createElement(
      "li",
      {
        key: name,
        onMouseDown: () => pick(name),
        className: i === activeIdx ? "active" : ""
      },
      /* @__PURE__ */ React.createElement("span", { className: "bl-name" }, name),
      /* @__PURE__ */ React.createElement("span", { className: "bl-meta" }, sizeMap[size], " \xB7 ", coatMap[coat])
    );
  })));
}
function AnimatedDollar({ value, duration = 700, className = "", style = {} }) {
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
  }, [value]);
  return /* @__PURE__ */ React.createElement("span", { className, style }, "$", display.toLocaleString());
}
function Donut({ items, total, size = 220, stroke = 36 }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  let offset = 0;
  return /* @__PURE__ */ React.createElement("svg", { width: size, height: size, viewBox: `0 0 ${size} ${size}` }, /* @__PURE__ */ React.createElement("circle", { cx: size / 2, cy: size / 2, r, fill: "none", stroke: "rgba(27,19,64,0.08)", strokeWidth: stroke }), items.map((it, i) => {
    const frac = it.amount / total;
    const dash = frac * c;
    const seg = /* @__PURE__ */ React.createElement(
      "circle",
      {
        key: i,
        cx: size / 2,
        cy: size / 2,
        r,
        fill: "none",
        stroke: it.color,
        strokeWidth: stroke,
        strokeDasharray: `${dash} ${c - dash}`,
        strokeDashoffset: -offset,
        transform: `rotate(-90 ${size / 2} ${size / 2})`,
        style: { transition: "stroke-dasharray 0.5s ease, stroke-dashoffset 0.5s ease" },
        strokeLinecap: "butt"
      }
    );
    offset += dash;
    return seg;
  }));
}
Object.assign(window, { Paw, Sticker, HalftoneBg, BigSlider, PillSegment, BreedSearch, AnimatedDollar, Donut });

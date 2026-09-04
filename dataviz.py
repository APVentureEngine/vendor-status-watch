"""Inline-SVG charts from real data, for a venture's static pages.

Copy this file into ventures/<slug>/product/ and import it from your site
generator. Standard library only, like gen_site.py.

WHY INLINE SVG AND NOT A CHART LIBRARY. These pages are static files built by a
Python pipeline and served from GitHub Pages. A CDN chart library would add a
blocking third-party request, break the reviewer's no-unknown-script rule, show
nothing until JS runs, and render an empty box for anyone whose script blocked.
SVG generated at build time has the numbers baked in: it paints instantly, it
works with JS off, it survives being screenshotted into a post, and the figure
cannot silently disagree with the dataset because it IS the dataset.

WHAT A CHART IS FOR HERE. Not a research paper. A stranger gives the page about
two seconds. One number, large, that makes the scale of the thing land — then
the shape of the data underneath it. Accurate AND arresting; the accuracy is
what makes it arresting, because the numbers are real and specific.

Rules baked in so they cannot be forgotten:
  * every mark is DIRECTLY LABELLED — no hover, no legend to decode, and it
    keeps the palette legal for colour-blind readers;
  * one axis, never two scales on one chart;
  * a single series uses the sequential blue ramp; multiple series use a
    validated categorical order, never cycled;
  * text is ink-coloured, never series-coloured — a mark beside it carries
    identity;
  * grid and axes recede;
  * every figure carries a caption naming the source and the date, because an
    unattributed number on a page selling data is worth nothing;
  * dark mode is honoured via prefers-color-scheme.

Palette validated with the dataviz palette checker (light and dark): lightness
band, chroma floor, CVD separation, normal-vision floor, contrast.
"""
import html
import math

# Sequential blue, light -> dark. Single-series magnitude uses the 450 step.
BLUE = {100: "#cde2fb", 200: "#9ec5f4", 300: "#6da7ec",
        400: "#3987e5", 450: "#2a78d6", 550: "#1c5cab", 650: "#104281"}
# Categorical, in FIXED order. Never cycle; a 4th series means rethink the chart.
SERIES = ("#2a78d6", "#eb6834", "#1baf7a")
INK = "#1a1a19"
INK_DIM = "#5b5b57"
GRID = "#e6e6e3"

# Ink AND surface move together. Setting a dark text colour without a dark
# ground is how you get invisible numbers on a light page — caught by rendering
# this, not by reading it. The components carry their own surface so the library
# is safe to drop into a host page whose background it does not control, and the
# SVGs use currentColor so their text follows the same token.
CSS = """
.dv{
  --dv-ink:%(ink)s; --dv-dim:%(dim)s; --dv-grid:%(grid)s;
  --dv-surface:#fcfcfb; --dv-accent:%(accent)s;
  --dv-line:%(line)s; --dv-area:%(area)s;
  font:14px/1.4 -apple-system,system-ui,"Segoe UI",Roboto,sans-serif;
  color:var(--dv-ink);
}
@media (prefers-color-scheme:dark){
  .dv{--dv-ink:#f2f2f0; --dv-dim:#a9a9a4; --dv-grid:#333330;
      --dv-surface:#1a1a19; --dv-accent:%(accent_dark)s;
      /* dark takes its OWN steps from the same ramp, not a flipped light one */
      --dv-line:%(line_dark)s; --dv-area:%(area_dark)s}
}
.dv figure{margin:0 0 28px}
.dv figcaption{margin-top:8px;font-size:12px;color:var(--dv-dim)}
.dv-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:18px}
.dv-kpi{
  padding:16px 18px;border:1px solid var(--dv-grid);border-radius:12px;
  background:var(--dv-surface);color:var(--dv-ink);
}
.dv-kpi b{display:block;font-size:clamp(1.9rem,5vw,2.9rem);font-weight:800;
          letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums;
          color:var(--dv-ink)}
.dv-kpi span{display:block;margin-top:7px;font-size:12.5px;color:var(--dv-dim)}
.dv-kpi i{font-style:normal;font-size:12px;font-weight:700;color:var(--dv-accent)}
.dv-svg{display:block;max-width:100%%;height:auto;color:var(--dv-ink)}
.dv table{border-collapse:collapse;font-size:13px;color:var(--dv-ink)}
.dv th,.dv td{padding:5px 12px 5px 0;text-align:left;
              border-bottom:1px solid var(--dv-grid)}
""" % {"ink": INK, "dim": INK_DIM, "grid": GRID,
       "accent": BLUE[550], "accent_dark": BLUE[300],
       "line": BLUE[450], "area": BLUE[100],
       "line_dark": BLUE[400], "area_dark": BLUE[650]}


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def _num(v) -> str:
    """Thousands separators. A page selling 45,772 records must not print 45772."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return _e(v)
    return f"{int(round(f)):,}" if abs(f - round(f)) < 1e-9 else f"{f:,.1f}"


def _require(rows, what: str):
    """Refuse to draw nothing. A chart of placeholder data is worse than no
    chart: it looks like evidence and is not."""
    if not rows:
        raise ValueError(
            f"{what}: no data. Do not publish an empty or invented chart — "
            "either pass the real rows or leave the figure out.")


def figure(svg: str, caption: str, source: str = "", asof: str = "") -> str:
    bits = [caption]
    if source:
        bits.append(f"Source: {source}")
    if asof:
        bits.append(f"as of {asof}")
    return (f'<figure>{svg}<figcaption>{_e(" · ".join(b for b in bits if b))}'
            f"</figcaption></figure>")


def kpi_row(items) -> str:
    """The most important form on a landing page: a few real numbers, large.

    items: [(value, label)] or [(value, label, note)] — note is a short delta
    or qualifier ("last 90 days", "+12% vs Aug").
    """
    _require(items, "kpi_row")
    out = ['<div class="dv-kpis">']
    for it in items:
        value, label = it[0], it[1]
        note = it[2] if len(it) > 2 else ""
        out.append('<div class="dv-kpi">')
        out.append(f"<b>{_e(_num(value))}</b>")
        out.append(f"<span>{_e(label)}</span>")
        if note:
            out.append(f'<i style="color:{BLUE[550]}">{_e(note)}</i>')
        out.append("</div>")
    out.append("</div>")
    return "".join(out)


def bar_chart(rows, unit: str = "", width: int = 680, bar_h: int = 26,
              gap: int = 10, title: str = "") -> str:
    """Horizontal bars, sorted, every bar directly labelled.

    rows: [(label, value)]. Horizontal because real category names are words,
    not three-letter codes, and rotated x-labels are unreadable.
    """
    _require(rows, "bar_chart")
    rows = [(str(a), float(b)) for a, b in rows]
    rows.sort(key=lambda r: -r[1])
    top = max(v for _, v in rows) or 1.0
    label_w = min(190, max(90, 8 * max(len(a) for a, _ in rows)))
    # Size the value gutter from the widest label that will actually be drawn.
    # A fixed gutter clipped "1,240 notices" to "1,240 notic" — the palette
    # validator cannot see that; only rendering it can.
    longest = max(len(_num(v) + unit) for _, v in rows)
    val_w = max(46, int(longest * 7.1) + 14)
    plot_w = max(80, width - label_w - val_w)
    height = len(rows) * (bar_h + gap) + 8

    p = [f'<svg class="dv-svg" viewBox="0 0 {width} {height}" width="100%" '
         f'height="{height}" role="img" xmlns="http://www.w3.org/2000/svg" '
         f'aria-label="{_e(title or "bar chart")}">']
    if title:
        p.append(f"<title>{_e(title)}</title>")
    for i, (label, value) in enumerate(rows):
        y = i * (bar_h + gap)
        w = max(2.0, plot_w * (value / top))
        p.append(f'<text x="0" y="{y + bar_h * 0.72:.0f}" font-size="13" '
                 f'fill="currentColor">{_e(label)}</text>')
        # 4px rounded data-end, anchored flat to the baseline at x=label_w
        p.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" '
                 f'rx="4" fill="var(--dv-line)"/>')
        p.append(f'<text x="{label_w + w + 9:.1f}" y="{y + bar_h * 0.72:.0f}" '
                 f'font-size="12.5" font-weight="700" fill="currentColor" '
                 f'opacity=".72">'
                 f'{_e(_num(value))}{_e(unit)}</text>')
    p.append("</svg>")
    return "".join(p)


def trend(points, width: int = 680, height: int = 190, unit: str = "",
          title: str = "") -> str:
    """One series over time, with the latest value labelled at the end.

    points: [(label, value)] in chronological order. One axis only — if you
    have two measures, draw two charts.
    """
    _require(points, "trend")
    vals = [float(v) for _, v in points]
    if len(vals) < 2:
        raise ValueError("trend: needs at least two points to show a trend")
    lo, hi = min(vals), max(vals)
    # c137: this is a FILLED AREA chart, and a filled area implies magnitude
    # measured from zero. Baselining at min(vals) makes the fill lie — a moderate
    # decline plunges from the top of the frame to the floor and reads as a
    # collapse. (Found on warn-feed by the partner, report M007; same library, same
    # bug here.) Area and bar charts start at zero; only line-only charts may crop.
    base = 0.0 if lo >= 0 else lo
    span = (hi - base) or 1.0
    # Right pad sized from the end label, for the same reason bar_chart sizes
    # its value gutter: a fixed 78 clipped "760 notices" to "760 notice".
    end_label = _num(vals[-1]) + unit
    pad_l, pad_t, pad_b = 8, 16, 26
    pad_r = max(52, int(len(end_label) * 7.6) + 22)
    pw = width - pad_l - pad_r
    ph = height - pad_t - pad_b

    def xy(i, v):
        x = pad_l + pw * (i / (len(vals) - 1))
        y = pad_t + ph * (1 - (v - base) / span)
        return x, y

    pts = [xy(i, v) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = (f"{pad_l},{pad_t + ph:.1f} " + line +
            f" {pad_l + pw:.1f},{pad_t + ph:.1f}")

    p = [f'<svg class="dv-svg" viewBox="0 0 {width} {height}" width="100%" '
         f'height="{height}" role="img" xmlns="http://www.w3.org/2000/svg" '
         f'aria-label="{_e(title or "trend")}">']
    if title:
        p.append(f"<title>{_e(title)}</title>")
    p.append(f'<line x1="{pad_l}" y1="{pad_t + ph:.1f}" x2="{pad_l + pw:.1f}" '
             f'y2="{pad_t + ph:.1f}" stroke="currentColor" stroke-opacity=".14" stroke-width="1"/>')
    p.append(f'<polygon points="{area}" fill="var(--dv-area)" opacity="0.55"/>')
    p.append(f'<polyline points="{line}" fill="none" stroke="var(--dv-line)" '
             f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    lx, ly = pts[-1]
    p.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="var(--dv-line)"/>')
    p.append(f'<text x="{lx + 10:.1f}" y="{ly + 4:.0f}" font-size="13" '
             f'font-weight="700" fill="currentColor">{_e(_num(vals[-1]))}{_e(unit)}</text>')
    p.append(f'<text x="{pad_l}" y="{height - 6}" font-size="11.5" '
             f'fill="currentColor" opacity=".72">{_e(points[0][0])}</text>')
    p.append(f'<text x="{pad_l + pw:.1f}" y="{height - 6}" font-size="11.5" '
             f'text-anchor="end" fill="currentColor" opacity=".72">{_e(points[-1][0])}</text>')
    p.append("</svg>")
    return "".join(p)


def sparkline(values, width: int = 120, height: int = 30) -> str:
    """A trend small enough to sit inside a sentence or a stat tile."""
    _require(values, "sparkline")
    vals = [float(v) for v in values]
    if len(vals) < 2:
        raise ValueError("sparkline: needs at least two values")
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    pts = " ".join(
        f"{(width - 4) * i / (len(vals) - 1) + 2:.1f},"
        f"{2 + (height - 4) * (1 - (v - lo) / span):.1f}"
        for i, v in enumerate(vals))
    return (f'<svg viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}" role="img" aria-label="trend" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<polyline points="{pts}" fill="none" stroke="var(--dv-line)" '
            f'stroke-width="2" stroke-linejoin="round"/></svg>')


def table_fallback(rows, headers=("", "")) -> str:
    """The same numbers as markup. Ship it beside any chart a screen reader or
    a text-only client would otherwise get nothing from."""
    _require(rows, "table_fallback")
    head = "".join(f"<th>{_e(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{_e(_num(c) if i else c)}</td>"
                         for i, c in enumerate(r)) + "</tr>"
        for r in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

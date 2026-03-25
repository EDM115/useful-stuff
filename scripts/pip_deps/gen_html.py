import json
import os
import re

# Layout constants
BOX_PADDING_X = 12
BOX_PADDING_Y = 8
COLUMN_WIDTH = 210
ROW_HEIGHT = 34
H_MARGIN = 70
V_MARGIN = 95
LEFT_PAD = 56
TOP_PAD = 56
LAYER_COLORS = [
    "#3b82f6",
    "#06b6d4",
    "#22c55e",
    "#f59e0b",
    "#ec4899",
    "#8b5cf6",
    "#ef4444",
    "#eab308",
]


def load_dependencies(json_path="output/dependencies.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_safe_id(name, fallback_index):
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-")
    if not slug:
        slug = f"pkg-{fallback_index}"
    return f"box-{slug}-{fallback_index}"


def generate_html(dep_map, output_path="output/dependencies.html"):
    print("Preparing dependency layout...")

    buckets = {}
    for pkg, info in dep_map.items():
        info.setdefault("requires", [])
        info.setdefault("required_by", [])
        count = len(info["required_by"])
        buckets.setdefault(count, []).append(pkg)

    sorted_counts = sorted(buckets.keys())

    positions = {}
    box_ids = {}
    max_cols = 0
    id_counter = 1
    for row, count in enumerate(sorted_counts):
        pkgs = sorted(buckets[count])
        max_cols = max(max_cols, len(pkgs))
        for col, pkg in enumerate(pkgs):
            positions[pkg] = (row, col)
            box_ids[pkg] = make_safe_id(pkg, id_counter)
            id_counter += 1

    num_rows = len(sorted_counts)
    container_width = (
        LEFT_PAD * 2 + max_cols * COLUMN_WIDTH + max(0, max_cols - 1) * H_MARGIN
    )
    container_height = (
        TOP_PAD * 2 + num_rows * ROW_HEIGHT + max(0, num_rows - 1) * V_MARGIN
    )

    print(
        f"Rendering map for {len(dep_map)} packages ({num_rows} layers, {max_cols} max columns)..."
    )

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'/>")
    html.append(
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'/>"
    )
    html.append("<title>Pip Dependency Map</title>")
    html.append("<style>")
    html.append("  :root { color-scheme: light; }")
    html.append(
        "  body { margin:0; padding:86px 20px 20px; overflow:auto; font-family: Inter, Segoe UI, Arial, sans-serif; background:#f3f4f6; color:#111827; transition:background-color 140ms ease, color 140ms ease; }"
    )
    html.append(
        "  .topbar-wrap { position:fixed; top:12px; left:50%; transform:translateX(-50%); z-index:9999; display:flex; align-items:center; gap:10px; }"
    )
    html.append(
        "  .topbar { position:fixed; top:12px; left:50%; transform:translateX(-50%); z-index:9999; display:flex; align-items:center; gap:10px; padding:8px 14px; background:rgba(255,255,255,0.95); border:1px solid #d1d5db; border-radius:999px; box-shadow:0 8px 24px rgba(15, 23, 42, 0.14); backdrop-filter: blur(6px); transition:background-color 140ms ease, border-color 140ms ease; }"
    )
    html.append("  .topbar { position:static; transform:none; left:auto; top:auto; }")
    html.append(
        "  .page-title { margin:0; font-size:17px; font-weight:600; color:#0f172a; white-space:nowrap; }"
    )
    html.append(
        "  .deselect-btn { border:1px solid #dc2626; background:#ef4444; color:#ffffff; border-radius:999px; padding:6px 10px; font-size:12px; font-weight:600; cursor:pointer; }"
    )
    html.append(
        "  .deselect-btn:disabled { background:#fecaca; border-color:#fca5a5; color:#7f1d1d; cursor:not-allowed; opacity:0.7; }"
    )
    html.append(
        "  .theme-btn { border:1px solid #94a3b8; background:#ffffff; color:#0f172a; border-radius:999px; width:38px; height:34px; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; padding:0; }"
    )
    html.append(
        "  .search-wrap { background:rgba(255,255,255,0.95); border:1px solid #d1d5db; border-radius:999px; box-shadow:0 8px 24px rgba(15, 23, 42, 0.14); backdrop-filter: blur(6px); padding:8px 14px; display:flex; align-items:center; gap:8px; }"
    )
    html.append(
        "  .search-input { width:220px; border:none; outline:none; background:transparent; color:#0f172a; font-size:13px; line-height:1; }"
    )
    html.append(
        "  .search-clear { width:24px; height:24px; border-radius:999px; border:1px solid #cbd5e1; background:#ffffff; color:#475569; display:none; align-items:center; justify-content:center; cursor:pointer; font-size:15px; line-height:1; padding:0; }"
    )
    html.append("  .search-clear.visible { display:inline-flex; }")
    html.append("  .theme-icon { width:18px; height:18px; display:block; }")
    html.append("  .theme-icon.sun { display:none; }")
    html.append("  body[data-theme='dark'] .theme-icon.sun { display:block; }")
    html.append("  body[data-theme='dark'] .theme-icon.moon { display:none; }")
    html.append(
        f"  .container {{ position:relative; width:{container_width}px; height:{container_height}px; background:#ffffff; border:1px solid #d1d5db; border-radius:12px; box-shadow:0 10px 28px rgba(15, 23, 42, 0.08); transition:background-color 140ms ease, border-color 140ms ease; }}"
    )
    html.append(
        "  .edges { position:absolute; inset:0; z-index:1; pointer-events:none; }"
    )
    html.append(
        "  .edge { fill:none; stroke:#64748b; stroke-opacity:0.2; stroke-width:1.2; stroke-linecap:round; transition:stroke-opacity 120ms ease, stroke-width 120ms ease; }"
    )
    html.append("  .edge.is-dim { stroke-opacity:0.04; }")
    html.append(
        "  .edge.rel-out { stroke:#2f9e73; stroke-opacity:0.92; stroke-width:2.2; }"
    )
    html.append(
        "  .edge.rel-in { stroke:#c97373; stroke-opacity:0.92; stroke-width:2.2; }"
    )
    html.append(
        f"  .box {{ position:absolute; min-width:120px; max-width:{COLUMN_WIDTH}px; box-sizing:border-box; padding:{BOX_PADDING_Y}px {BOX_PADDING_X}px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; display:inline-block; z-index:2; box-shadow:0 2px 6px rgba(15, 23, 42, 0.06); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; transition:background-color 120ms ease, border-color 120ms ease, color 120ms ease, opacity 120ms ease; }}"
    )
    html.append("  .box:hover { background:#eef2ff; border-color:#94a3b8; }")
    html.append("  .box.is-dim { opacity:0.22; filter:saturate(0.35); }")
    html.append(
        "  .box.rel-source { background:#dff3e9; border-color:#5ca98a; color:#1f5b45; font-weight:600; }"
    )
    html.append(
        "  .box.rel-out { background:#e9f6ef; border-color:#7ab59e; color:#285f49; }"
    )
    html.append(
        "  .box.rel-in { background:#fbeeee; border-color:#d8a0a0; color:#7a3f3f; }"
    )
    html.append(
        "  .pkg-info { position:fixed; top:74px; left:50%; transform:translateX(-50%); z-index:9998; width:min(620px, calc(100vw - 40px)); max-height:62vh; overflow:auto; background:rgba(255,255,255,0.96); border:1px solid #d1d5db; border-radius:12px; box-shadow:0 8px 22px rgba(15,23,42,0.14); padding:10px 12px; pointer-events:auto; }"
    )
    html.append("  .pkg-info.hidden { display:none; }")
    html.append(
        "  .pkg-info-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:4px; }"
    )
    html.append(
        "  .pkg-info-title { margin:0; font-size:14px; font-weight:700; color:#111827; overflow-wrap:anywhere; }"
    )
    html.append(
        "  .pkg-info-toggle { border:1px solid #94a3b8; background:#ffffff; color:#334155; border-radius:999px; width:30px; height:30px; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; flex:0 0 auto; pointer-events:auto; }"
    )
    html.append("  .pkg-info-toggle svg { width:16px; height:16px; display:block; }")
    html.append("  .pkg-info-toggle .eye-open { display:none; }")
    html.append("  .pkg-info.minimized .pkg-info-toggle .eye-open { display:block; }")
    html.append("  .pkg-info.minimized .pkg-info-toggle .eye-closed { display:none; }")
    html.append("  .pkg-info.minimized .pkg-info-body { display:none; }")
    html.append(
        "  .pkg-section-title { margin:8px 0 4px; font-size:12px; font-weight:700; color:#334155; text-transform:uppercase; letter-spacing:0.04em; }"
    )
    html.append("  .pkg-section-title.deps { color:#2f9e73; }")
    html.append("  .pkg-section-title.dependents { color:#c97373; }")
    html.append(
        "  .pkg-list { margin:0; padding:0; font-size:12px; color:#1f2937; display:grid; grid-template-columns:repeat(var(--col-count, 1), minmax(0, 1fr)); gap:4px 10px; max-height:230px; overflow-y:auto; }"
    )
    html.append(
        "  .pkg-cell { margin:0; padding:4px 6px; border:1px solid #e2e8f0; border-radius:6px; background:rgba(248,250,252,0.9); min-height:24px; overflow-wrap:anywhere; word-break:break-word; white-space:normal; line-height:1.2; }"
    )
    html.append("  .pkg-cell.placeholder { visibility:hidden; }")
    html.append("  body[data-theme='dark'] { background:#0f172a; color:#e2e8f0; }")
    html.append(
        "  body[data-theme='dark'] .topbar { background:rgba(15, 23, 42, 0.92); border-color:#334155; }"
    )
    html.append(
        "  body[data-theme='dark'] .search-wrap { background:rgba(15, 23, 42, 0.92); border-color:#334155; }"
    )
    html.append("  body[data-theme='dark'] .search-input { color:#e2e8f0; }")
    html.append(
        "  body[data-theme='dark'] .search-clear { background:#1e293b; border-color:#475569; color:#cbd5e1; }"
    )
    html.append("  body[data-theme='dark'] .page-title { color:#e2e8f0; }")
    html.append(
        "  body[data-theme='dark'] .theme-btn { background:#1e293b; color:#e2e8f0; border-color:#475569; }"
    )
    html.append(
        "  body[data-theme='dark'] .pkg-info-toggle { background:#1e293b; color:#e2e8f0; border-color:#475569; }"
    )
    html.append(
        f"  body[data-theme='dark'] .container {{ background:#111827; border-color:#334155; box-shadow:0 10px 28px rgba(2, 6, 23, 0.55); }}"
    )
    html.append(
        "  body[data-theme='dark'] .edge { stroke:#64748b; stroke-opacity:0.35; }"
    )
    html.append("  body[data-theme='dark'] .edge.is-dim { stroke-opacity:0.1; }")
    html.append(
        "  body[data-theme='dark'] .edge.rel-out { stroke:#2f9e73; stroke-opacity:0.96; }"
    )
    html.append(
        "  body[data-theme='dark'] .edge.rel-in { stroke:#c97373; stroke-opacity:0.96; }"
    )
    html.append(
        "  body[data-theme='dark'] .box { background:#0b1220; border-color:#334155; color:#e2e8f0; box-shadow:0 2px 6px rgba(2, 6, 23, 0.4); }"
    )
    html.append(
        "  body[data-theme='dark'] .box:hover { background:#172036; border-color:#4b5d7a; }"
    )
    html.append(
        "  body[data-theme='dark'] .pkg-info { background:rgba(15, 23, 42, 0.95); border-color:#334155; }"
    )
    html.append("  body[data-theme='dark'] .pkg-info-title { color:#e2e8f0; }")
    html.append("  body[data-theme='dark'] .pkg-section-title { color:#93c5fd; }")
    html.append("  body[data-theme='dark'] .pkg-section-title.deps { color:#6bc2a0; }")
    html.append(
        "  body[data-theme='dark'] .pkg-section-title.dependents { color:#d69a9a; }"
    )
    html.append("  body[data-theme='dark'] .pkg-list { color:#cbd5e1; }")
    html.append(
        "  body[data-theme='dark'] .pkg-list li { border-color:#334155; background:rgba(15,23,42,0.72); }"
    )
    html.append(
        "  body[data-theme='dark'] .pkg-cell { border-color:#334155; background:rgba(15,23,42,0.72); }"
    )
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='topbar-wrap'>")
    html.append("<div class='topbar'>")
    html.append("<h1 id='page-title' class='page-title'>Pip dependency map</h1>")
    html.append(
        "<button id='deselect-btn' class='deselect-btn' type='button' disabled>Deselect</button>"
    )
    html.append(
        "<button id='theme-btn' class='theme-btn' type='button' aria-label='Toggle dark theme' title='Toggle dark theme'><svg class='theme-icon moon' viewBox='0 0 24 24' fill='none' aria-hidden='true'><path d='M12 3a9 9 0 1 0 9 9 7 7 0 1 1-9-9z' fill='currentColor'/></svg><svg class='theme-icon sun' viewBox='0 0 24 24' fill='none' aria-hidden='true'><circle cx='12' cy='12' r='4' fill='currentColor'/><path d='M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41' stroke='currentColor' stroke-width='1.8' stroke-linecap='round'/></svg></button>"
    )
    html.append("</div>")
    html.append("<div class='search-wrap'>")
    html.append(
        "<input id='search-input' class='search-input' type='text' placeholder='Search dependencies...' autocomplete='off'/>"
    )
    html.append(
        "<button id='search-clear' class='search-clear' type='button' aria-label='Clear search' title='Clear search'>&times;</button>"
    )
    html.append("</div>")
    html.append("</div>")
    html.append("<aside id='pkg-info' class='pkg-info hidden'>")
    html.append("<div class='pkg-info-head'>")
    html.append("<h2 id='pkg-info-title' class='pkg-info-title'>Package details</h2>")
    html.append(
        "<button id='pkg-info-toggle' class='pkg-info-toggle' type='button' aria-label='Minimize details panel' title='Minimize details panel'><svg class='eye-closed' viewBox='0 0 24 24' fill='none' aria-hidden='true'><path d='M3 12c2.2-3.6 5.2-5.5 9-5.5s6.8 1.9 9 5.5c-2.2 3.6-5.2 5.5-9 5.5s-6.8-1.9-9-5.5z' stroke='currentColor' stroke-width='1.8'/><circle cx='12' cy='12' r='2.6' stroke='currentColor' stroke-width='1.8'/><path d='M4 4l16 16' stroke='currentColor' stroke-width='1.8' stroke-linecap='round'/></svg><svg class='eye-open' viewBox='0 0 24 24' fill='none' aria-hidden='true'><path d='M3 12c2.2-3.6 5.2-5.5 9-5.5s6.8 1.9 9 5.5c-2.2 3.6-5.2 5.5-9 5.5s-6.8-1.9-9-5.5z' stroke='currentColor' stroke-width='1.8'/><circle cx='12' cy='12' r='2.6' stroke='currentColor' stroke-width='1.8'/></svg></button>"
    )
    html.append("</div>")
    html.append("<div class='pkg-info-body'>")
    html.append(
        "<div id='pkg-deps-title' class='pkg-section-title deps'>Dependencies (0)</div>"
    )
    html.append("<div id='pkg-deps-list' class='pkg-list'></div>")
    html.append(
        "<div id='pkg-dependents-title' class='pkg-section-title dependents'>Dependents (0)</div>"
    )
    html.append("<div id='pkg-dependents-list' class='pkg-list'></div>")
    html.append("</div>")
    html.append("</aside>")
    html.append("<div class='container'>")
    html.append("<svg class='edges' id='edge-layer' aria-hidden='true'>")
    html.append(
        "<defs><marker id='arrowhead-green' markerWidth='8' markerHeight='8' refX='7' refY='4' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L8,4 L0,8 z' fill='#2f9e73'/></marker><marker id='arrowhead-red' markerWidth='8' markerHeight='8' refX='7' refY='4' orient='auto' markerUnits='strokeWidth'><path d='M0,0 L8,4 L0,8 z' fill='#c97373'/></marker></defs>"
    )
    html.append("</svg>")
    html.append("</div>")

    js = f"""
<script>
  const positions = {json.dumps(positions)};
  const boxIds = {json.dumps(box_ids)};
  const requires = {json.dumps({k: v.get("requires", []) for k, v in dep_map.items()})};
  const layerColors = {json.dumps(LAYER_COLORS)};
    const CANVAS_LEFT_PAD = {LEFT_PAD};
    const CANVAS_TOP_PAD = {TOP_PAD};
    const BASE_H_MARGIN = {H_MARGIN};
    const BASE_V_MARGIN = {V_MARGIN};
    const BASE_COLUMN_WIDTH = {COLUMN_WIDTH};
    const BASE_ROW_HEIGHT = {ROW_HEIGHT};
  const edgeLayer = document.getElementById('edge-layer');
    const container = document.querySelector('.container');
    const titleEl = document.getElementById('page-title');
    const deselectBtn = document.getElementById('deselect-btn');
    const themeBtn = document.getElementById('theme-btn');
    const searchInput = document.getElementById('search-input');
    const searchClearBtn = document.getElementById('search-clear');
    const infoPanel = document.getElementById('pkg-info');
    const infoTitle = document.getElementById('pkg-info-title');
    const depsTitle = document.getElementById('pkg-deps-title');
    const depsList = document.getElementById('pkg-deps-list');
    const dependentsTitle = document.getElementById('pkg-dependents-title');
    const dependentsList = document.getElementById('pkg-dependents-list');
    const infoToggleBtn = document.getElementById('pkg-info-toggle');
    let allEdges = [];
    let selectedPkg = null;
    let hoveredPkg = null;
    let infoMinimized = false;
    let searchLevels = null;
    let visiblePkgSet = new Set(Object.keys(boxIds));
    let currentLayout = {{}};
    let isPanning = false;
    let panStartX = 0;
    let panStartY = 0;
    let panScrollX = 0;
    let panScrollY = 0;

    const packages = Object.keys(boxIds).sort();
    const baseLayout = {{}};

    const dependents = {{}};
    Object.entries(requires).forEach(([src, deps]) => {{
        deps.forEach(dep => {{
            if (!dependents[dep]) dependents[dep] = [];
            dependents[dep].push(src);
        }});
    }});

    packages.forEach(pkg => {{
        const [row, col] = positions[pkg];
        baseLayout[pkg] = {{
            x: CANVAS_LEFT_PAD + col * (BASE_COLUMN_WIDTH + BASE_H_MARGIN),
            y: CANVAS_TOP_PAD + row * (BASE_ROW_HEIGHT + BASE_V_MARGIN),
        }};
    }});

    function activePkg() {{
        return selectedPkg || hoveredPkg;
    }}

    function depthOpacity(level) {{
        if (level <= 0) return 1;
        if (level === 1) return 0.6;
        return 0.4;
    }}

    function neighborsOf(pkg) {{
        const req = requires[pkg] || [];
        const dep = dependents[pkg] || [];
        return [...new Set([...req, ...dep])].filter(name => name in boxIds);
    }}

    function computeSearchLevels(rawQuery) {{
        const q = rawQuery.trim().toLowerCase();
        if (!q) return null;

        const matches = Object.keys(boxIds).filter(name => name.toLowerCase().includes(q));
        if (matches.length === 0) return {{}};

        const levels = {{}};
        const queue = [];
        matches.forEach(name => {{
            levels[name] = 0;
            queue.push(name);
        }});

        while (queue.length > 0) {{
            const current = queue.shift();
            const currentLevel = levels[current];
            neighborsOf(current).forEach(nextNode => {{
                const next = currentLevel + 1;
                if (!(nextNode in levels) || next < levels[nextNode]) {{
                    levels[nextNode] = next;
                    queue.push(nextNode);
                }}
            }});
        }}

        return levels;
    }}

    function buildSearchLayout(levels) {{
        const buckets = {{}};
        let maxLevel = 0;
        Object.entries(levels).forEach(([pkg, level]) => {{
            const key = Math.max(0, level);
            if (!buckets[key]) buckets[key] = [];
            buckets[key].push(pkg);
            maxLevel = Math.max(maxLevel, key);
        }});

        for (let lvl = 0; lvl <= maxLevel; lvl += 1) {{
            if (!buckets[lvl]) buckets[lvl] = [];
            buckets[lvl].sort((a, b) => a.localeCompare(b));
        }}

        const layout = {{}};
        const compactColStep = 180;
        const compactRowStep = 58;

        for (let col = 0; col <= maxLevel; col += 1) {{
            buckets[col].forEach((pkg, idx) => {{
                layout[pkg] = {{
                    x: CANVAS_LEFT_PAD + col * compactColStep,
                    y: CANVAS_TOP_PAD + idx * compactRowStep,
                }};
            }});
        }}

        return layout;
    }}

    function renderNodes(layout, levels) {{
        container.querySelectorAll('.box').forEach(el => el.remove());

        visiblePkgSet = new Set(Object.keys(layout));
        currentLayout = layout;

        let maxRight = 0;
        let maxBottom = 0;

        Object.entries(layout)
            .sort((a, b) => (a[1].y - b[1].y) || (a[1].x - b[1].x))
            .forEach(([pkg, pos]) => {{
                const el = document.createElement('div');
                el.id = boxIds[pkg];
                el.className = 'box';
                el.dataset.pkg = pkg;
                el.title = pkg;
                el.textContent = pkg;
                el.style.left = `${{pos.x}}px`;
                el.style.top = `${{pos.y}}px`;
                const level = levels && pkg in levels ? levels[pkg] : 0;
                el.dataset.searchOpacity = String(depthOpacity(level));
                el.style.opacity = el.dataset.searchOpacity;
                container.appendChild(el);

                maxRight = Math.max(maxRight, pos.x + el.offsetWidth);
                maxBottom = Math.max(maxBottom, pos.y + el.offsetHeight);
            }});

        container.style.width = `${{Math.max(420, Math.ceil(maxRight + CANVAS_LEFT_PAD))}}px`;
        container.style.height = `${{Math.max(260, Math.ceil(maxBottom + CANVAS_TOP_PAD))}}px`;
    }}

    function renderList(listEl, items, emptyLabel) {{
        listEl.innerHTML = '';

        const colCount = Number(listEl.style.getPropertyValue('--col-count') || '1');

        if (items.length === 0) {{
            const cell = document.createElement('div');
            cell.className = 'pkg-cell';
            cell.textContent = emptyLabel;
            listEl.appendChild(cell);
            return;
        }}

        const MAX_ROWS = 8;
        const maxVisibleNoScroll = colCount * MAX_ROWS;

        const matrixCells = [];
        if (items.length <= maxVisibleNoScroll) {{
            const rows = items.length <= MAX_ROWS ? items.length : MAX_ROWS;
            const columns = [];
            for (let c = 0; c < colCount; c += 1) {{
                columns.push(items.slice(c * MAX_ROWS, (c + 1) * MAX_ROWS));
            }}

            for (let r = 0; r < rows; r += 1) {{
                for (let c = 0; c < colCount; c += 1) {{
                    matrixCells.push(columns[c][r] ?? null);
                }}
            }}
        }} else {{
            const first = items.slice(0, maxVisibleNoScroll);
            const rest = items.slice(maxVisibleNoScroll);

            const columns = [];
            for (let c = 0; c < colCount; c += 1) {{
                columns.push(first.slice(c * MAX_ROWS, (c + 1) * MAX_ROWS));
            }}
            for (let r = 0; r < MAX_ROWS; r += 1) {{
                for (let c = 0; c < colCount; c += 1) {{
                    matrixCells.push(columns[c][r] ?? null);
                }}
            }}
            matrixCells.push(...rest);
        }}

        matrixCells.forEach(name => {{
            const cell = document.createElement('div');
            cell.className = 'pkg-cell';
            if (!name) {{
                cell.classList.add('placeholder');
                cell.textContent = ' ';
            }} else {{
                cell.textContent = name;
            }}
            listEl.appendChild(cell);
        }});
    }}

    function listColumnCount(length) {{
        if (length <= 8) return 1;
        if (length <= 16) return 2;
        return 3;
    }}

    function updatePanelWidth(depCount, dependentCount) {{
        const maxCount = Math.max(depCount, dependentCount);
        const cols = listColumnCount(maxCount);
        const base = 230;
        const perCol = 150;
        const width = Math.min(620, Math.max(260, base + (cols - 1) * perCol));
        infoPanel.style.width = `min(${{width}}px, calc(100vw - 40px))`;
    }}

    function updateInfoToggle() {{
        infoPanel.classList.toggle('minimized', infoMinimized);
        const nextLabel = infoMinimized ? 'Expand details panel' : 'Minimize details panel';
        infoToggleBtn.setAttribute('aria-label', nextLabel);
        infoToggleBtn.setAttribute('title', nextLabel);
    }}

    function updateInfoPanel(pkg) {{
        if (!pkg || !boxIds[pkg]) {{
            infoPanel.classList.add('hidden');
            return;
        }}

        const outgoing = ((requires[pkg] || []).filter(name => boxIds[name])).sort();
        const incoming = ((dependents[pkg] || []).filter(name => boxIds[name])).sort();

        infoTitle.textContent = pkg;
        depsTitle.textContent = `Dependencies (${{outgoing.length}})`;
        dependentsTitle.textContent = `Dependents (${{incoming.length}})`;
        depsList.style.setProperty('--col-count', String(listColumnCount(outgoing.length)));
        dependentsList.style.setProperty('--col-count', String(listColumnCount(incoming.length)));
        updatePanelWidth(outgoing.length, incoming.length);
        renderList(depsList, outgoing, 'No dependencies in map');
        renderList(dependentsList, incoming, 'No dependents in map');
        infoPanel.classList.remove('hidden');
        updateInfoToggle();
    }}

    function resetStyles() {{
        allEdges.forEach(edge => {{
            edge.classList.remove('is-dim', 'rel-out', 'rel-in');
            edge.removeAttribute('marker-end');
            edge.setAttribute('stroke', edge.dataset.baseColor);
            edge.style.opacity = edge.dataset.searchOpacity || '';
        }});

        Object.values(boxIds).forEach(id => {{
            const box = document.getElementById(id);
            if (!box) return;
            box.classList.remove('is-dim', 'rel-source', 'rel-out', 'rel-in');
            box.style.opacity = box.dataset.searchOpacity || '';
        }});
    }}

    function updateTopbar() {{
        if (selectedPkg) {{
            titleEl.textContent = `Pip dependency map - ${{selectedPkg}}`;
            deselectBtn.disabled = false;
        }} else {{
            titleEl.textContent = 'Pip dependency map';
            deselectBtn.disabled = true;
        }}
    }}

    function applyRelations(pkg) {{
        resetStyles();
        updateInfoPanel(pkg);

        if (!pkg || !boxIds[pkg] || !visiblePkgSet.has(pkg)) {{
            updateTopbar();
            return;
        }}

        const outgoing = new Set((requires[pkg] || []).filter(name => boxIds[name]));
        const incoming = new Set((dependents[pkg] || []).filter(name => boxIds[name]));
        const linked = new Set([pkg, ...outgoing, ...incoming]);

        Object.keys(boxIds).forEach(name => {{
            const box = document.getElementById(boxIds[name]);
            if (!box) return;

            if (!visiblePkgSet.has(name)) {{
                return;
            }}

            if (!linked.has(name)) {{
                box.classList.add('is-dim');
                return;
            }}

            if (name === pkg) {{
                box.classList.add('rel-source');
            }} else if (outgoing.has(name)) {{
                box.classList.add('rel-out');
            }} else if (incoming.has(name)) {{
                box.classList.add('rel-in');
            }}
        }});

        allEdges.forEach(edge => {{
            const src = edge.dataset.src;
            const dst = edge.dataset.dst;

            if (!visiblePkgSet.has(src) || !visiblePkgSet.has(dst)) {{
                return;
            }}

            if (src === pkg && outgoing.has(dst)) {{
                edge.classList.add('rel-out');
                edge.setAttribute('marker-end', 'url(#arrowhead-green)');
            }} else if (dst === pkg && incoming.has(src)) {{
                edge.classList.add('rel-in');
                edge.setAttribute('marker-end', 'url(#arrowhead-red)');
            }} else {{
                edge.classList.add('is-dim');
            }}
        }});

        updateTopbar();
    }}

  function spreadOffset(index, total, step, maxAbs) {{
    if (!total || total <= 1) return 0;
    const centered = index - (total - 1) / 2;
    return Math.max(-maxAbs, Math.min(maxAbs, centered * step));
  }}

  function drawConnections() {{
        while (edgeLayer.lastChild && edgeLayer.lastChild.tagName !== 'defs') {{
      edgeLayer.removeChild(edgeLayer.lastChild);
    }}

    allEdges = [];
    const containerRect = container.getBoundingClientRect();

        edgeLayer.setAttribute('width', String(container.clientWidth));
        edgeLayer.setAttribute('height', String(container.clientHeight));
        edgeLayer.setAttribute('viewBox', `0 0 ${{container.clientWidth}} ${{container.clientHeight}}`);

    const info = {{}};
        Object.keys(positions).forEach(pkg => {{
            if (!visiblePkgSet.has(pkg)) return;
      const el = document.getElementById(boxIds[pkg]);
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const left = rect.left - containerRect.left;
      const top = rect.top - containerRect.top;
      info[pkg] = {{
        cx: left + rect.width / 2,
        top,
        bottom: top + rect.height,
      }};
    }});

    const incoming = {{}};
    Object.entries(requires).forEach(([src, deps]) => {{
      deps.forEach(dep => {{
        if (!info[src] || !info[dep]) return;
        if (!incoming[dep]) incoming[dep] = [];
        incoming[dep].push(src);
      }});
    }});

    Object.entries(requires).forEach(([src, deps]) => {{
    if (!visiblePkgSet.has(src) || !info[src]) return;

    const visibleDeps = deps.filter(dep => visiblePkgSet.has(dep) && info[dep]);
      const outTotal = visibleDeps.length;
      const srcLayer = positions[src][0];
      const layerColor = layerColors[srcLayer % layerColors.length];

      visibleDeps.forEach((dep, outIndex) => {{
        const srcInfo = info[src];
        const tgtInfo = info[dep];
        const inList = incoming[dep] || [];
        const inIndex = Math.max(0, inList.indexOf(src));
        const inTotal = inList.length || 1;

        const sx = srcInfo.cx + spreadOffset(outIndex, outTotal, 8, 28);
        const sy = srcInfo.bottom + 2;
        const tx = tgtInfo.cx + spreadOffset(inIndex, inTotal, 8, 28);
        const ty = tgtInfo.top - 8;

        const verticalGap = ty - sy;
        const cp1y = sy + Math.max(24, verticalGap * 0.35);
        const cp2y = ty - Math.max(24, verticalGap * 0.35);

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('class', 'edge');
        path.setAttribute('stroke', layerColor);
        path.dataset.baseColor = layerColor;
        const srcDepth = searchLevels && src in searchLevels ? searchLevels[src] : 0;
        const depDepth = searchLevels && dep in searchLevels ? searchLevels[dep] : 0;
        path.dataset.searchOpacity = String(depthOpacity(Math.max(srcDepth, depDepth)));
        path.style.opacity = path.dataset.searchOpacity;
        path.setAttribute('d', `M ${{sx}} ${{sy}} C ${{sx}} ${{cp1y}}, ${{tx}} ${{cp2y}}, ${{tx}} ${{ty}}`);
        path.dataset.src = src;
        path.dataset.dst = dep;
        edgeLayer.appendChild(path);
        allEdges.push(path);
      }});
    }});

        Object.entries(boxIds).forEach(([pkg, id]) => {{
            const box = document.getElementById(id);
            if (!box) return;

            box.onmouseenter = () => {{
                if (selectedPkg) return;
                if (!visiblePkgSet.has(pkg)) return;
                hoveredPkg = pkg;
                applyRelations(activePkg());
            }};

            box.onmouseleave = event => {{
                if (selectedPkg) return;
                if (event.relatedTarget && infoPanel.contains(event.relatedTarget)) return;
                hoveredPkg = null;
                applyRelations(activePkg());
            }};

            box.onclick = () => {{
                if (!visiblePkgSet.has(pkg)) return;
                selectedPkg = pkg;
                hoveredPkg = null;
                applyRelations(activePkg());
            }};
        }});

        applyRelations(activePkg());
  }}

    function drawGraph() {{
        const levels = searchLevels;
        let layout;

        if (!levels) {{
            layout = {{ ...baseLayout }};
        }} else {{
            layout = buildSearchLayout(levels);
        }}

        if (selectedPkg && !(selectedPkg in layout)) selectedPkg = null;
        if (hoveredPkg && !(hoveredPkg in layout)) hoveredPkg = null;

        renderNodes(layout, levels);
        drawConnections();
    }}

    infoPanel.addEventListener('mouseleave', () => {{
        if (selectedPkg) return;
        hoveredPkg = null;
        applyRelations(activePkg());
    }});

    function setTheme(nextTheme) {{
        const theme = nextTheme === 'dark' ? 'dark' : 'light';
        document.body.dataset.theme = theme;
        const nextLabel = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
        themeBtn.setAttribute('aria-label', nextLabel);
        themeBtn.setAttribute('title', nextLabel);
    }}

    infoToggleBtn.addEventListener('click', event => {{
        event.stopPropagation();
        if (!activePkg()) return;
        infoMinimized = !infoMinimized;
        updateInfoToggle();
    }});

    themeBtn.addEventListener('click', () => {{
        const nextTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
        setTheme(nextTheme);
    }});

    deselectBtn.addEventListener('click', () => {{
        selectedPkg = null;
        hoveredPkg = null;
        applyRelations(activePkg());
    }});

    document.addEventListener('keydown', event => {{
        if (event.key !== 'Escape') return;
        selectedPkg = null;
        hoveredPkg = null;
        applyRelations(activePkg());
    }});

    setTheme('light');

    function applySearch() {{
        searchLevels = computeSearchLevels(searchInput.value || '');
        const hasQuery = (searchInput.value || '').trim().length > 0;
        searchClearBtn.classList.toggle('visible', hasQuery);
        drawGraph();
    }}

    searchInput.addEventListener('input', applySearch);

    searchClearBtn.addEventListener('click', () => {{
        searchInput.value = '';
        searchInput.focus();
        applySearch();
    }});

    function canStartPan(target) {{
        if (!target) return false;
        if (target.closest('.box')) return false;
        if (target.closest('.topbar-wrap')) return false;
        if (target.closest('.pkg-info')) return false;
        return true;
    }}

    document.addEventListener('mousedown', event => {{
        if (event.button !== 0) return;
        if (!canStartPan(event.target)) return;
        isPanning = true;
        panStartX = event.clientX;
        panStartY = event.clientY;
        panScrollX = window.scrollX;
        panScrollY = window.scrollY;
        document.body.style.cursor = 'grabbing';
        event.preventDefault();
    }});

    window.addEventListener('mousemove', event => {{
        if (!isPanning) return;
        const dx = event.clientX - panStartX;
        const dy = event.clientY - panStartY;
        window.scrollTo(panScrollX - dx, panScrollY - dy);
    }});

    window.addEventListener('mouseup', () => {{
        if (!isPanning) return;
        isPanning = false;
        document.body.style.cursor = '';
    }});

    window.addEventListener('load', drawGraph);
    window.addEventListener('resize', drawGraph);
</script>
"""
    html.append(js)

    html.append("</body>")
    html.append("</html>")

    content = "\n".join(html)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated HTML dependency map at {output_path}")


if __name__ == "__main__":
    dep_map = load_dependencies()
    generate_html(dep_map)

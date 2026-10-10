"""Generate cohesive editorial illustrations for all 25 lessons and master assets.
Renders clean vector SVGs and takes high-resolution snapshots to PNG.
"""
from pathlib import Path
import json, hashlib, csv
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'output/imagegen'
OUT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR = ROOT / 'assets/illustrations/lessons'
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

LESSONS_META = [
    {
        "id": "01", "slug": "01-tasking",
        "title": "Codex 工作循環與任務設計",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Circular Loop -->
        <circle cx="450" cy="300" r="160" fill="none" stroke="#2a382e" stroke-width="4" stroke-dasharray="8 8" />
        <path d="M 450 140 A 160 160 0 0 1 610 300" fill="none" stroke="#c5f36c" stroke-width="5" marker-end="url(#arrow)" />
        <path d="M 610 300 A 160 160 0 0 1 450 460" fill="none" stroke="#ff9c6b" stroke-width="5" />
        <path d="M 450 460 A 160 160 0 0 1 290 300" fill="none" stroke="#c5f36c" stroke-width="5" />
        <path d="M 290 300 A 160 160 0 0 1 450 140" fill="none" stroke="#64dfca" stroke-width="5" />

        <!-- Node 1: Task Brief (Top) -->
        <g transform="translate(370, 70)">
            <rect width="160" height="90" rx="12" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="20" y="20" width="80" height="8" rx="4" fill="#c5f36c" />
            <rect x="20" y="38" width="120" height="6" rx="3" fill="#59665d" />
            <rect x="20" y="52" width="100" height="6" rx="3" fill="#59665d" />
            <rect x="20" y="66" width="60" height="6" rx="3" fill="#59665d" />
            <circle cx="130" cy="24" r="8" fill="#c5f36c" fill-opacity="0.2" stroke="#c5f36c" stroke-width="2" />
        </g>

        <!-- Node 2: Context Folder (Right) -->
        <g transform="translate(560, 240)">
            <rect width="160" height="110" rx="12" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" filter="url(#shadow)" />
            <path d="M 20 20 L 60 20 L 75 32 L 140 32 L 140 90 L 20 90 Z" fill="#25322b" stroke="#3d5145" stroke-width="2" />
            <circle cx="95" cy="65" r="18" fill="none" stroke="#ff9c6b" stroke-width="3" />
            <line x1="108" y1="78" x2="124" y2="94" stroke="#ff9c6b" stroke-width="4" stroke-linecap="round" />
            <rect x="35" y="45" width="45" height="5" rx="2" fill="#c5f36c" />
            <rect x="35" y="57" width="35" height="5" rx="2" fill="#59665d" />
        </g>

        <!-- Node 3: Execution Terminal (Bottom) -->
        <g transform="translate(370, 420)">
            <rect width="160" height="95" rx="12" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <circle cx="20" cy="18" r="4" fill="#ff5f56" /><circle cx="32" cy="18" r="4" fill="#ffbd2e" /><circle cx="44" cy="18" r="4" fill="#27c93f" />
            <text x="20" y="45" fill="#c5f36c" font-family="monospace" font-size="12">&gt; codex</text>
            <rect x="20" y="58" width="90" height="6" rx="3" fill="#59665d" />
            <rect x="20" y="72" width="120" height="6" rx="3" fill="#3d5145" />
        </g>

        <!-- Node 4: Acceptance Checklist (Left) -->
        <g transform="translate(180, 240)">
            <rect width="160" height="110" rx="12" fill="#1b2621" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <path d="M 25 35 L 33 43 L 48 27" fill="none" stroke="#c5f36c" stroke-width="3" stroke-linecap="round" />
            <rect x="58" y="32" width="80" height="6" rx="3" fill="#f2f1e9" />
            <path d="M 25 65 L 33 73 L 48 57" fill="none" stroke="#c5f36c" stroke-width="3" stroke-linecap="round" />
            <rect x="58" y="62" width="70" height="6" rx="3" fill="#f2f1e9" />
            <path d="M 25 95 L 33 103 L 48 87" fill="none" stroke="#64dfca" stroke-width="3" stroke-linecap="round" />
            <rect x="58" y="92" width="60" height="6" rx="3" fill="#59665d" />
        </g>

        <!-- Center Status Emblem -->
        <circle cx="450" cy="300" r="42" fill="#101813" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
        <path d="M 436 300 L 446 310 L 466 288" fill="none" stroke="#c5f36c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
        """
    },
    {
        "id": "02", "slug": "02-commands",
        "title": "讀懂陌生專案與提供脈絡",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Open Project Tree Folder -->
        <g transform="translate(150, 150)">
            <rect width="280" height="300" rx="16" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <path d="M 30 30 L 100 30 L 120 50 L 250 50 L 250 270 L 30 270 Z" fill="#141c18" stroke="#3d5145" stroke-width="2" />
            <!-- Tree Nodes -->
            <circle cx="60" cy="90" r="6" fill="#c5f36c" /><text x="80" y="95" fill="#f2f1e9" font-family="monospace" font-size="13">src/core</text>
            <path d="M 60 96 L 60 140 L 80 140" fill="none" stroke="#3d5145" stroke-width="2" />
            <circle cx="90" cy="140" r="5" fill="#ff9c6b" /><text x="105" y="145" fill="#a4a69c" font-family="monospace" font-size="12">parser.ts</text>
            <path d="M 60 140 L 60 185 L 80 185" fill="none" stroke="#3d5145" stroke-width="2" />
            <circle cx="90" cy="185" r="5" fill="#64dfca" /><text x="105" y="190" fill="#a4a69c" font-family="monospace" font-size="12">agent.ts</text>
            <circle cx="60" cy="230" r="6" fill="#c5f36c" /><text x="80" y="235" fill="#f2f1e9" font-family="monospace" font-size="13">tests/</text>
        </g>

        <!-- Tracing Data Stream -->
        <path d="M 430 290 C 500 290 520 220 580 220" fill="none" stroke="#c5f36c" stroke-width="4" stroke-dasharray="6 6" />

        <!-- Inspected Target Code Window -->
        <g transform="translate(520, 160)">
            <rect width="260" height="260" rx="14" fill="#141c18" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="260" height="34" rx="14" fill="#1b2621" />
            <circle cx="20" cy="17" r="4" fill="#ff5f56" /><circle cx="32" cy="17" r="4" fill="#ffbd2e" /><circle cx="44" cy="17" r="4" fill="#27c93f" />
            <text x="60" y="22" fill="#a4a69c" font-family="monospace" font-size="11">agent.ts:42</text>
            <rect x="25" y="55" width="180" height="8" rx="4" fill="#3d5145" />
            <rect x="25" y="75" width="210" height="8" rx="4" fill="#2a382e" />
            <!-- Highlighted Target Function -->
            <rect x="15" y="98" width="230" height="36" rx="6" fill="#c5f36c" fill-opacity="0.15" stroke="#c5f36c" stroke-width="1.5" />
            <text x="25" y="120" fill="#c5f36c" font-family="monospace" font-size="12">findContextRoot()</text>
            <rect x="25" y="150" width="160" height="8" rx="4" fill="#3d5145" />
            <rect x="25" y="170" width="140" height="8" rx="4" fill="#2a382e" />
            <rect x="25" y="190" width="190" height="8" rx="4" fill="#2a382e" />
        </g>

        <!-- Big Magnifying Glass -->
        <g transform="translate(480, 240)">
            <circle cx="60" cy="60" r="50" fill="#101813" fill-opacity="0.75" stroke="#c5f36c" stroke-width="5" filter="url(#glow)" />
            <line x1="95" y1="95" x2="150" y2="150" stroke="#c5f36c" stroke-width="10" stroke-linecap="round" />
            <circle cx="60" cy="60" r="35" fill="none" stroke="#64dfca" stroke-width="2" stroke-dasharray="4 4" />
        </g>
        """
    },
    {
        "id": "03", "slug": "03-project-context",
        "title": "Debug：從症狀到可靠修復",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Left: Broken Issue Box -->
        <g transform="translate(140, 180)">
            <rect width="200" height="240" rx="14" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" filter="url(#shadow)" />
            <rect x="20" y="25" width="80" height="8" rx="4" fill="#ff9c6b" />
            <rect x="20" y="45" width="140" height="6" rx="3" fill="#59665d" />
            <!-- Broken Wire -->
            <path d="M 40 120 L 80 120 L 95 140" fill="none" stroke="#ff9c6b" stroke-width="4" stroke-linecap="round" />
            <path d="M 125 100 L 140 120 L 160 120" fill="none" stroke="#ff9c6b" stroke-width="4" stroke-linecap="round" />
            <circle cx="110" cy="120" r="12" fill="#ff5f56" fill-opacity="0.2" stroke="#ff5f56" stroke-width="2" />
            <text x="105" y="125" fill="#ff5f56" font-family="sans-serif" font-weight="bold" font-size="14">✕</text>
            <rect x="20" y="190" width="120" height="8" rx="4" fill="#3d5145" />
        </g>

        <!-- Center: Debug Tool & Diagnostic Lens -->
        <g transform="translate(380, 200)">
            <circle cx="70" cy="100" r="55" fill="#101813" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
            <!-- Wrench / Tool -->
            <path d="M 50 120 L 85 85 C 92 78 102 78 108 84 C 114 90 114 100 107 107 L 72 142 Z" fill="#25322b" stroke="#c5f36c" stroke-width="3" />
            <circle cx="95" cy="95" r="5" fill="#ff9c6b" />
            <path d="M 45 125 L 35 135" stroke="#c5f36c" stroke-width="5" stroke-linecap="round" />
        </g>

        <!-- Right: Repaired & Verified System -->
        <g transform="translate(560, 180)">
            <rect width="200" height="240" rx="14" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <rect x="20" y="25" width="90" height="8" rx="4" fill="#c5f36c" />
            <rect x="20" y="45" width="140" height="6" rx="3" fill="#59665d" />
            <!-- Solid Repaired Bridge -->
            <path d="M 40 120 L 160 120" fill="none" stroke="#c5f36c" stroke-width="5" stroke-linecap="round" filter="url(#glow)" />
            <circle cx="100" cy="120" r="18" fill="#101813" stroke="#c5f36c" stroke-width="2" />
            <path d="M 92 120 L 98 126 L 109 114" fill="none" stroke="#c5f36c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
            <!-- Verification Test Badge -->
            <rect x="20" y="185" width="160" height="32" rx="6" fill="#1c2b20" stroke="#3d5145" />
            <text x="35" y="206" fill="#c5f36c" font-family="monospace" font-size="12">1 passed · 0 fails</text>
        </g>
        """
    },
    {
        "id": "04", "slug": "04-usage-safety",
        "title": "Plan 與跨檔功能開發",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Top: 3-Stage Plan Cards -->
        <g transform="translate(160, 110)">
            <!-- Phase 1 -->
            <rect x="0" y="0" width="160" height="80" rx="10" fill="#1b2621" stroke="#c5f36c" stroke-width="2" />
            <text x="18" y="26" fill="#c5f36c" font-family="monospace" font-size="11">PHASE 01</text>
            <rect x="18" y="40" width="120" height="6" rx="3" fill="#f2f1e9" />
            <rect x="18" y="54" width="80" height="6" rx="3" fill="#59665d" />
            <!-- Connecting Arrow 1 -->
            <path d="M 175 40 L 205 40" stroke="#3d5145" stroke-width="3" marker-end="url(#arrow)" />
            <!-- Phase 2 -->
            <rect x="220" y="0" width="160" height="80" rx="10" fill="#1b2621" stroke="#3d5145" stroke-width="2" />
            <text x="238" y="26" fill="#ff9c6b" font-family="monospace" font-size="11">PHASE 02</text>
            <rect x="238" y="40" width="110" height="6" rx="3" fill="#f2f1e9" />
            <rect x="238" y="54" width="90" height="6" rx="3" fill="#59665d" />
            <!-- Connecting Arrow 2 -->
            <path d="M 395 40 L 425 40" stroke="#3d5145" stroke-width="3" marker-end="url(#arrow)" />
            <!-- Phase 3 -->
            <rect x="440" y="0" width="160" height="80" rx="10" fill="#1b2621" stroke="#3d5145" stroke-width="2" />
            <text x="458" y="26" fill="#64dfca" font-family="monospace" font-size="11">PHASE 03</text>
            <rect x="458" y="40" width="120" height="6" rx="3" fill="#f2f1e9" />
            <rect x="458" y="54" width="70" height="6" rx="3" fill="#59665d" />
        </g>

        <!-- Bottom: Coordinated File Panels -->
        <g transform="translate(180, 250)">
            <!-- File A -->
            <rect x="0" y="0" width="240" height="220" rx="12" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="240" height="30" rx="12" fill="#1b2621" />
            <circle cx="15" cy="15" r="4" fill="#ff5f56" /><circle cx="27" cy="15" r="4" fill="#ffbd2e" /><circle cx="39" cy="15" r="4" fill="#27c93f" />
            <text x="55" y="20" fill="#a4a69c" font-family="monospace" font-size="11">types.ts</text>
            <rect x="20" y="50" width="140" height="6" rx="3" fill="#c5f36c" />
            <rect x="20" y="70" width="190" height="6" rx="3" fill="#3d5145" />
            <rect x="20" y="90" width="160" height="6" rx="3" fill="#3d5145" />
            <!-- File B -->
            <rect x="300" y="0" width="240" height="220" rx="12" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="300" y="0" width="240" height="30" rx="12" fill="#1b2621" />
            <circle cx="315" cy="15" r="4" fill="#ff5f56" /><circle cx="327" cy="15" r="4" fill="#ffbd2e" /><circle cx="339" cy="15" r="4" fill="#27c93f" />
            <text x="355" y="20" fill="#a4a69c" font-family="monospace" font-size="11">service.ts</text>
            <rect x="320" y="50" width="150" height="6" rx="3" fill="#ff9c6b" />
            <rect x="320" y="70" width="180" height="6" rx="3" fill="#3d5145" />
            <rect x="320" y="90" width="170" height="6" rx="3" fill="#3d5145" />
            <!-- Coordination Bridge -->
            <path d="M 240 110 C 270 110 270 110 300 110" stroke="#c5f36c" stroke-width="4" stroke-dasharray="4 4" />
        </g>
        """
    },
    {
        "id": "05", "slug": "05-practical-workflows",
        "title": "測試、Diff 與 Code Review",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Side-by-Side Diff Panels -->
        <g transform="translate(150, 160)">
            <!-- Left: Red Deleted Lines -->
            <rect x="0" y="0" width="260" height="280" rx="14" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="260" height="34" rx="14" fill="#1b2621" />
            <text x="20" y="22" fill="#ff5f56" font-family="monospace" font-size="12">- before.ts</text>
            <rect x="15" y="55" width="230" height="24" rx="4" fill="#ff5f56" fill-opacity="0.15" />
            <text x="25" y="71" fill="#ff5f56" font-family="monospace" font-size="11">- function legacyCalc()</text>
            <rect x="15" y="90" width="230" height="24" rx="4" fill="#ff5f56" fill-opacity="0.15" />
            <text x="25" y="106" fill="#ff5f56" font-family="monospace" font-size="11">-   return raw * 1.05</text>
            <rect x="20" y="135" width="180" height="6" rx="3" fill="#3d5145" />
            <rect x="20" y="155" width="140" height="6" rx="3" fill="#2a382e" />

            <!-- Right: Green Added Lines -->
            <rect x="340" y="0" width="260" height="280" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <rect x="340" y="0" width="260" height="34" rx="14" fill="#1b2621" />
            <text x="360" y="22" fill="#c5f36c" font-family="monospace" font-size="12">+ after.ts</text>
            <rect x="355" y="55" width="230" height="24" rx="4" fill="#c5f36c" fill-opacity="0.18" />
            <text x="365" y="71" fill="#c5f36c" font-family="monospace" font-size="11">+ function robustCalc(ctx)</text>
            <rect x="355" y="90" width="230" height="24" rx="4" fill="#c5f36c" fill-opacity="0.18" />
            <text x="365" y="106" fill="#c5f36c" font-family="monospace" font-size="11">+   return ctx.rate * tax</text>
            <rect x="360" y="135" width="190" height="6" rx="3" fill="#3d5145" />
            <rect x="360" y="155" width="150" height="6" rx="3" fill="#2a382e" />
        </g>

        <!-- Center Stamp: Approved & Verified -->
        <g transform="translate(415, 250)">
            <circle cx="35" cy="35" r="38" fill="#101813" stroke="#64dfca" stroke-width="3" filter="url(#glow)" />
            <path d="M 22 35 L 32 45 L 48 25" fill="none" stroke="#64dfca" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
            <text x="7" y="92" fill="#64dfca" font-family="monospace" font-weight="bold" font-size="11">REVIEW OK</text>
        </g>
        """
    },
    {
        "id": "06", "slug": "06-git-worktrees",
        "title": "Git、Worktree 與平行任務",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Main Trunk Line -->
        <line x1="160" y1="300" x2="300" y2="300" stroke="#3d5145" stroke-width="6" />
        <circle cx="200" cy="300" r="10" fill="#1b2621" stroke="#c5f36c" stroke-width="3" />
        <circle cx="280" cy="300" r="10" fill="#1b2621" stroke="#c5f36c" stroke-width="3" />

        <!-- Split into 3 Worktrees -->
        <!-- Top Track -->
        <path d="M 280 300 C 350 300 370 170 450 170 L 620 170" fill="none" stroke="#c5f36c" stroke-width="4" />
        <g transform="translate(480, 125)">
            <rect width="180" height="70" rx="10" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="15" y="26" fill="#c5f36c" font-family="monospace" font-size="11">worktree: feat/ui</text>
            <rect x="15" y="38" width="120" height="6" rx="3" fill="#59665d" />
            <circle cx="150" cy="22" r="5" fill="#27c93f" />
        </g>

        <!-- Center Track -->
        <line x1="280" y1="300" x2="620" y2="300" stroke="#ff9c6b" stroke-width="4" />
        <g transform="translate(480, 255)">
            <rect width="180" height="70" rx="10" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" filter="url(#shadow)" />
            <text x="15" y="26" fill="#ff9c6b" font-family="monospace" font-size="11">worktree: fix/auth</text>
            <rect x="15" y="38" width="130" height="6" rx="3" fill="#59665d" />
            <circle cx="150" cy="22" r="5" fill="#27c93f" />
        </g>

        <!-- Bottom Track -->
        <path d="M 280 300 C 350 300 370 430 450 430 L 620 430" fill="none" stroke="#64dfca" stroke-width="4" />
        <g transform="translate(480, 385)">
            <rect width="180" height="70" rx="10" fill="#1b2621" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <text x="15" y="26" fill="#64dfca" font-family="monospace" font-size="11">worktree: test/e2e</text>
            <rect x="15" y="38" width="110" height="6" rx="3" fill="#59665d" />
            <circle cx="150" cy="22" r="5" fill="#27c93f" />
        </g>

        <!-- Merging Point -->
        <path d="M 620 170 C 690 170 700 300 740 300" fill="none" stroke="#c5f36c" stroke-width="3" />
        <path d="M 620 300 L 740 300" stroke="#ff9c6b" stroke-width="3" />
        <path d="M 620 430 C 690 430 700 300 740 300" fill="none" stroke="#64dfca" stroke-width="3" />
        <circle cx="740" cy="300" r="14" fill="#101813" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
        <path d="M 734 300 L 738 304 L 746 295" fill="none" stroke="#c5f36c" stroke-width="2.5" stroke-linecap="round" />
        """
    },
    {
        "id": "07", "slug": "07-frontend-ui",
        "title": "前端、UI 與視覺迭代",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Desktop Screen Mockup -->
        <g transform="translate(140, 160)">
            <rect width="360" height="240" rx="12" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="360" height="28" rx="12" fill="#1b2621" />
            <circle cx="15" cy="14" r="4" fill="#ff5f56" /><circle cx="27" cy="14" r="4" fill="#ffbd2e" /><circle cx="39" cy="14" r="4" fill="#27c93f" />
            <text x="55" y="18" fill="#59665d" font-family="monospace" font-size="10">1440 × 900</text>
            <!-- UI Layout Grid -->
            <rect x="25" y="50" width="90" height="150" rx="6" fill="#1f2c25" />
            <rect x="130" y="50" width="205" height="40" rx="6" fill="#24352a" stroke="#c5f36c" stroke-width="1.5" />
            <rect x="130" y="105" width="95" height="95" rx="6" fill="#1f2c25" />
            <rect x="240" y="105" width="95" height="95" rx="6" fill="#1f2c25" />
        </g>

        <!-- Mobile Phone Mockup -->
        <g transform="translate(540, 140)">
            <rect width="130" height="260" rx="20" fill="#141c18" stroke="#ff9c6b" stroke-width="3" filter="url(#shadow)" />
            <rect x="40" y="10" width="50" height="6" rx="3" fill="#25322b" />
            <!-- Mobile Responsive Card -->
            <rect x="15" y="35" width="100" height="30" rx="5" fill="#24352a" stroke="#c5f36c" stroke-width="1" />
            <rect x="15" y="75" width="100" height="75" rx="5" fill="#1f2c25" />
            <rect x="15" y="160" width="100" height="75" rx="5" fill="#1f2c25" />
            <text x="35" y="250" fill="#ff9c6b" font-family="monospace" font-size="10">390 × 844</text>
        </g>

        <!-- Floating Palette Chips -->
        <g transform="translate(710, 200)">
            <rect width="50" height="180" rx="10" fill="#1b2621" stroke="#3d5145" stroke-width="1.5" />
            <circle cx="25" cy="30" r="14" fill="#c5f36c" />
            <circle cx="25" cy="70" r="14" fill="#ff9c6b" />
            <circle cx="25" cy="110" r="14" fill="#64dfca" />
            <circle cx="25" cy="150" r="14" fill="#101813" stroke="#3d5145" />
        </g>
        """
    },
    {
        "id": "08", "slug": "08-cloud-long-tasks",
        "title": "Cloud、遠端與長時間任務",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Local Workstation (Left) -->
        <g transform="translate(140, 220)">
            <rect width="180" height="130" rx="12" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="15" y="20" width="80" height="8" rx="4" fill="#c5f36c" />
            <text x="15" y="50" fill="#a4a69c" font-family="monospace" font-size="11">local workspace</text>
            <text x="15" y="75" fill="#c5f36c" font-family="monospace" font-size="12">&gt; codex cloud run</text>
            <rect x="15" y="95" width="150" height="8" rx="4" fill="#25322b" />
        </g>

        <!-- Connecting Data Bridge -->
        <path d="M 320 285 L 530 285" stroke="#64dfca" stroke-width="4" stroke-dasharray="8 6" filter="url(#glow)" />
        <circle cx="425" cy="285" r="8" fill="#64dfca" />

        <!-- Remote Cloud Node (Right) -->
        <g transform="translate(530, 180)">
            <rect width="230" height="210" rx="16" fill="#141c18" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <!-- Cloud Icon -->
            <path d="M 45 65 A 25 25 0 0 1 90 50 A 35 35 0 0 1 155 60 A 25 25 0 0 1 180 85 A 20 20 0 0 1 170 105 L 45 105 Z" fill="#20332b" stroke="#64dfca" stroke-width="2" />
            <text x="35" y="135" fill="#f2f1e9" font-family="monospace" font-size="12">Remote Agent Worker</text>
            <!-- Progress Track -->
            <rect x="35" y="155" width="160" height="10" rx="5" fill="#25322b" />
            <rect x="35" y="155" width="115" height="10" rx="5" fill="#c5f36c" />
            <text x="35" y="185" fill="#c5f36c" font-family="monospace" font-size="11">72% · 42m elapsed</text>
        </g>
        """
    },
    {
        "id": "09", "slug": "09-project-customization",
        "title": "AGENTS.md、RAG、Skills 與 MCP",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Central Project Root -->
        <circle cx="450" cy="300" r="60" fill="#101813" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
        <text x="415" y="295" fill="#f2f1e9" font-family="monospace" font-weight="bold" font-size="13">PROJECT</text>
        <text x="430" y="315" fill="#c5f36c" font-family="monospace" font-size="11">ROOT</text>

        <!-- Satellite 1: AGENTS.md (Top Left) -->
        <g transform="translate(180, 100)">
            <rect width="180" height="110" rx="12" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <text x="18" y="28" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">AGENTS.md</text>
            <rect x="18" y="45" width="90" height="6" rx="3" fill="#59665d" />
            <rect x="18" y="60" width="130" height="6" rx="3" fill="#3d5145" />
            <rect x="18" y="75" width="110" height="6" rx="3" fill="#3d5145" />
            <line x1="180" y1="90" x2="400" y2="260" stroke="#3d5145" stroke-width="2" />
        </g>

        <!-- Satellite 2: Skills Drawer (Top Right) -->
        <g transform="translate(540, 100)">
            <rect width="180" height="110" rx="12" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" filter="url(#shadow)" />
            <text x="18" y="28" fill="#ff9c6b" font-family="monospace" font-weight="bold" font-size="12">Custom Skills</text>
            <rect x="18" y="45" width="144" height="22" rx="5" fill="#25322b" stroke="#3d5145" />
            <text x="28" y="60" fill="#c5f36c" font-family="monospace" font-size="11">$review-pr</text>
            <rect x="18" y="75" width="144" height="22" rx="5" fill="#25322b" stroke="#3d5145" />
            <text x="28" y="90" fill="#c5f36c" font-family="monospace" font-size="11">$generate-docs</text>
            <line x1="540" y1="90" x2="490" y2="250" stroke="#ff9c6b" stroke-width="2" />
        </g>

        <!-- Satellite 3: MCP Hub (Bottom Left) -->
        <g transform="translate(180, 380)">
            <rect width="180" height="110" rx="12" fill="#1b2621" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <text x="18" y="28" fill="#64dfca" font-family="monospace" font-weight="bold" font-size="12">MCP Protocols</text>
            <circle cx="30" cy="55" r="6" fill="#64dfca" /><text x="45" y="60" fill="#f2f1e9" font-family="monospace" font-size="11">Postgres</text>
            <circle cx="30" cy="80" r="6" fill="#c5f36c" /><text x="45" y="85" fill="#f2f1e9" font-family="monospace" font-size="11">GitHub API</text>
            <line x1="180" y1="390" x2="400" y2="330" stroke="#64dfca" stroke-width="2" />
        </g>

        <!-- Satellite 4: RAG Docs Index (Bottom Right) -->
        <g transform="translate(540, 380)">
            <rect width="180" height="110" rx="12" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="18" y="28" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">RAG Index</text>
            <rect x="18" y="48" width="140" height="8" rx="4" fill="#25322b" />
            <rect x="18" y="65" width="110" height="8" rx="4" fill="#25322b" />
            <rect x="18" y="82" width="130" height="8" rx="4" fill="#25322b" />
            <line x1="540" y1="390" x2="490" y2="340" stroke="#c5f36c" stroke-width="2" />
        </g>
        """
    },
    {
        "id": "10", "slug": "10-usage-safety-capstone",
        "title": "Quota、權限與第一階段 Capstone",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Speedometer / Quota Gauge (Left) -->
        <g transform="translate(160, 180)">
            <rect width="240" height="240" rx="16" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <path d="M 60 160 A 60 60 0 1 1 180 160" fill="none" stroke="#25322b" stroke-width="14" stroke-linecap="round" />
            <path d="M 60 160 A 60 60 0 0 1 160 110" fill="none" stroke="#c5f36c" stroke-width="14" stroke-linecap="round" />
            <line x1="120" y1="140" x2="145" y2="105" stroke="#ff9c6b" stroke-width="4" stroke-linecap="round" />
            <circle cx="120" cy="140" r="7" fill="#ff9c6b" />
            <text x="75" y="195" fill="#f2f1e9" font-family="monospace" font-size="13">QUOTA 65%</text>
        </g>

        <!-- Capstone Sealed Box (Right) -->
        <g transform="translate(480, 160)">
            <rect width="260" height="260" rx="18" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <!-- Ribbon / Capstone Badge -->
            <path d="M 130 30 L 130 230" stroke="#c5f36c" stroke-width="12" stroke-opacity="0.2" />
            <path d="M 30 130 L 230 130" stroke="#c5f36c" stroke-width="12" stroke-opacity="0.2" />
            <circle cx="130" cy="130" r="45" fill="#1b2621" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
            <text x="100" y="125" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">PHASE 1</text>
            <text x="94" y="145" fill="#f2f1e9" font-family="monospace" font-size="11">CAPSTONE</text>
            <circle cx="130" cy="190" r="16" fill="#27c93f" />
            <path d="M 124 190 L 128 194 L 136 186" fill="none" stroke="#101813" stroke-width="3" stroke-linecap="round" />
        </g>
        """
    },
    {
        "id": "11", "slug": "11-beyond-coding",
        "title": "Codex 不只寫程式：生活 AI Agent",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Travel Map Pin (Left) -->
        <g transform="translate(140, 160)">
            <rect width="200" height="240" rx="14" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <path d="M 40 80 Q 100 130 160 70 T 170 170" fill="none" stroke="#64dfca" stroke-width="3" stroke-dasharray="6 4" />
            <circle cx="100" cy="100" r="14" fill="#ff9c6b" />
            <circle cx="100" cy="100" r="5" fill="#1b2621" />
            <text x="35" y="210" fill="#f2f1e9" font-family="monospace" font-size="12">Trip Itinerary</text>
        </g>

        <!-- Structured Notes & Study Coach (Right) -->
        <g transform="translate(400, 160)">
            <rect width="340" height="240" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <rect x="25" y="30" width="140" height="10" rx="5" fill="#c5f36c" />
            <!-- Study Flashcards -->
            <rect x="25" y="60" width="130" height="65" rx="8" fill="#1f2c25" stroke="#3d5145" />
            <rect x="38" y="75" width="80" height="5" rx="2" fill="#f2f1e9" />
            <rect x="38" y="90" width="100" height="5" rx="2" fill="#59665d" />

            <rect x="175" y="60" width="130" height="65" rx="8" fill="#1f2c25" stroke="#3d5145" />
            <rect x="188" y="75" width="80" height="5" rx="2" fill="#ff9c6b" />
            <rect x="188" y="90" width="100" height="5" rx="2" fill="#59665d" />

            <!-- Daily Coach Summary -->
            <rect x="25" y="145" width="280" height="65" rx="8" fill="#1b2621" stroke="#64dfca" stroke-width="1.5" />
            <text x="40" y="172" fill="#64dfca" font-family="monospace" font-size="12">Personal Coach Daily Brief</text>
            <rect x="40" y="185" width="180" height="6" rx="3" fill="#59665d" />
        </g>
        """
    },
    {
        "id": "12", "slug": "12-codex-in-practice",
        "title": "Codex in Practice：從需求到學習網站",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Evolution from Wireframe to Web Platform -->
        <g transform="translate(140, 170)">
            <!-- Step 1: Hand-drawn Sketch -->
            <rect width="160" height="220" rx="10" fill="#1b2621" stroke="#59665d" stroke-width="2" stroke-dasharray="6 4" />
            <text x="20" y="35" fill="#a4a69c" font-family="monospace" font-size="11">01 / Sketch</text>
            <rect x="20" y="60" width="120" height="15" rx="3" fill="#25322b" />
            <rect x="20" y="90" width="55" height="55" rx="4" fill="#25322b" />
            <rect x="85" y="90" width="55" height="55" rx="4" fill="#25322b" />
        </g>

        <!-- Arrow -->
        <path d="M 320 280 L 370 280" stroke="#3d5145" stroke-width="4" marker-end="url(#arrow)" />

        <!-- Step 2: Spec Cards -->
        <g transform="translate(390, 170)">
            <rect width="160" height="220" rx="10" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" />
            <text x="20" y="35" fill="#ff9c6b" font-family="monospace" font-size="11">02 / Research</text>
            <rect x="20" y="60" width="120" height="6" rx="3" fill="#c5f36c" />
            <rect x="20" y="78" width="100" height="6" rx="3" fill="#59665d" />
            <rect x="20" y="110" width="120" height="70" rx="6" fill="#202c24" />
        </g>

        <!-- Arrow -->
        <path d="M 570 280 L 620 280" stroke="#3d5145" stroke-width="4" marker-end="url(#arrow)" />

        <!-- Step 3: Live Website -->
        <g transform="translate(640, 150)">
            <rect width="180" height="250" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2.5" filter="url(#glow)" />
            <rect x="0" y="0" width="180" height="26" rx="14" fill="#1b2621" />
            <circle cx="15" cy="13" r="3.5" fill="#27c93f" />
            <text x="30" y="17" fill="#c5f36c" font-family="monospace" font-size="9">codex-academy.dev</text>
            <rect x="15" y="40" width="150" height="35" rx="6" fill="#1e2e25" />
            <rect x="15" y="90" width="70" height="65" rx="6" fill="#24372c" />
            <rect x="95" y="90" width="70" height="65" rx="6" fill="#24372c" />
            <rect x="15" y="165" width="150" height="65" rx="6" fill="#1e2e25" />
        </g>
        """
    },
    {
        "id": "13", "slug": "13-hooks",
        "title": "Hooks 與事件觸發",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Trigger Sensor (Left) -->
        <g transform="translate(150, 200)">
            <circle cx="70" cy="80" r="50" fill="#101813" stroke="#ff9c6b" stroke-width="3" filter="url(#glow)" />
            <path d="M 70 50 L 55 85 L 75 85 L 65 110 L 90 75 L 75 75 Z" fill="#ff9c6b" />
            <text x="35" y="160" fill="#ff9c6b" font-family="monospace" font-size="12">EVENT TRIGGER</text>
        </g>

        <!-- Connecting Hook Wire -->
        <path d="M 280 280 L 380 280" stroke="#ff9c6b" stroke-width="4" stroke-dasharray="6 4" />

        <!-- Hook Middleware Hub (Center) -->
        <g transform="translate(380, 180)">
            <rect width="160" height="200" rx="14" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="25" y="35" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="13">onToolCall()</text>
            <rect x="25" y="55" width="110" height="6" rx="3" fill="#59665d" />
            <!-- Hook Slots -->
            <rect x="20" y="80" width="120" height="30" rx="6" fill="#141c18" stroke="#3d5145" />
            <text x="30" y="100" fill="#64dfca" font-family="monospace" font-size="11">validateArgs()</text>
            <rect x="20" y="125" width="120" height="30" rx="6" fill="#141c18" stroke="#3d5145" />
            <text x="30" y="145" fill="#c5f36c" font-family="monospace" font-size="11">logAudit()</text>
        </g>

        <!-- Automated Action Target (Right) -->
        <g transform="translate(600, 200)">
            <rect width="180" height="160" rx="14" fill="#141c18" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <text x="20" y="35" fill="#64dfca" font-family="monospace" font-size="12">AUTOMATED ACTION</text>
            <circle cx="35" cy="70" r="8" fill="#27c93f" /><text x="55" y="75" fill="#f2f1e9" font-family="monospace" font-size="11">Pass Security</text>
            <circle cx="35" cy="105" r="8" fill="#27c93f" /><text x="55" y="110" fill="#f2f1e9" font-family="monospace" font-size="11">Run Formatter</text>
        </g>
        """
    },
    {
        "id": "14", "slug": "14-cli-sdk-ci",
        "title": "非互動 CLI、SDK 與 CI",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Terminal Runner (Left) -->
        <g transform="translate(140, 160)">
            <rect width="250" height="240" rx="14" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="250" height="32" rx="14" fill="#1b2621" />
            <circle cx="16" cy="16" r="4" fill="#ff5f56" /><circle cx="28" cy="16" r="4" fill="#ffbd2e" /><circle cx="40" cy="16" r="4" fill="#27c93f" />
            <text x="55" y="21" fill="#c5f36c" font-family="monospace" font-size="11">CI / NON-INTERACTIVE</text>
            <text x="20" y="65" fill="#c5f36c" font-family="monospace" font-size="12">&gt; codex exec --json</text>
            <!-- Structured Output Stream -->
            <rect x="20" y="85" width="210" height="60" rx="6" fill="#1b2621" stroke="#3d5145" />
            <text x="30" y="105" fill="#64dfca" font-family="monospace" font-size="10">{"status": "success",</text>
            <text x="30" y="122" fill="#64dfca" font-family="monospace" font-size="10"> "assertions": 14}</text>
        </g>

        <!-- Conveyor Pipeline -->
        <path d="M 400 280 L 520 280" stroke="#c5f36c" stroke-width="5" stroke-dasharray="8 6" />

        <!-- Checked CI Build Stage (Right) -->
        <g transform="translate(520, 160)">
            <rect width="240" height="240" rx="14" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="25" y="35" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="13">GitHub Actions CI</text>
            <rect x="25" y="55" width="190" height="36" rx="6" fill="#141c18" stroke="#3d5145" />
            <circle cx="45" cy="73" r="7" fill="#27c93f" /><text x="65" y="78" fill="#f2f1e9" font-family="monospace" font-size="11">build / test-all</text>
            <rect x="25" y="105" width="190" height="36" rx="6" fill="#141c18" stroke="#3d5145" />
            <circle cx="45" cy="123" r="7" fill="#27c93f" /><text x="65" y="128" fill="#f2f1e9" font-family="monospace" font-size="11">verify-integrity</text>
            <!-- Pass Stamp -->
            <rect x="25" y="165" width="190" height="36" rx="8" fill="#1c2f21" stroke="#c5f36c" />
            <text x="45" y="188" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">PIPELINE PASSED</text>
        </g>
        """
    },
    {
        "id": "15", "slug": "15-extensions",
        "title": "Skills、Plugins、MCP 與 WebMCP",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Central AI Engine with Puzzle Dock -->
        <g transform="translate(340, 170)">
            <rect width="220" height="220" rx="18" fill="#1b2621" stroke="#c5f36c" stroke-width="2.5" filter="url(#glow)" />
            <text x="45" y="50" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="14">AI AGENT ENGINE</text>
            <!-- Puzzle Connector Cutout -->
            <circle cx="110" cy="110" r="30" fill="#141c18" stroke="#64dfca" stroke-width="2" />
            <text x="95" y="115" fill="#64dfca" font-family="monospace" font-size="11">CORE</text>
        </g>

        <!-- Modular Puzzle Plugs -->
        <!-- MCP Tool Plug (Left) -->
        <g transform="translate(140, 210)">
            <rect width="150" height="80" rx="10" fill="#141c18" stroke="#ff9c6b" stroke-width="2" />
            <text x="20" y="32" fill="#ff9c6b" font-family="monospace" font-weight="bold" font-size="12">MCP Tool</text>
            <text x="20" y="55" fill="#a4a69c" font-family="monospace" font-size="10">database-query</text>
            <line x1="150" y1="250" x2="340" y2="250" stroke="#ff9c6b" stroke-width="4" stroke-linecap="round" />
        </g>

        <!-- WebMCP Tool Plug (Right) -->
        <g transform="translate(610, 210)">
            <rect width="150" height="80" rx="10" fill="#141c18" stroke="#64dfca" stroke-width="2" />
            <text x="20" y="32" fill="#64dfca" font-family="monospace" font-weight="bold" font-size="12">WebMCP</text>
            <text x="20" y="55" fill="#a4a69c" font-family="monospace" font-size="10">browser-eval</text>
            <line x1="560" y1="250" x2="610" y2="250" stroke="#64dfca" stroke-width="4" stroke-linecap="round" />
        </g>
        """
    },
    {
        "id": "16", "slug": "16-image-generation",
        "title": "Codex 與 GPT Image 生圖",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Canvas with Generated Transparent Avatar -->
        <g transform="translate(160, 150)">
            <rect width="320" height="260" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <!-- Checkerboard pattern for transparency -->
            <pattern id="checkers" width="16" height="16" patternUnits="userSpaceOnUse">
                <rect width="8" height="8" fill="#1b2621" />
                <rect x="8" width="8" height="8" fill="#202a24" />
                <rect y="8" width="8" height="8" fill="#202a24" />
                <rect x="8" y="8" width="8" height="8" fill="#1b2621" />
            </pattern>
            <rect x="15" y="15" width="290" height="230" rx="8" fill="url(#checkers)" />

            <!-- Cute Robot Illustration in Center -->
            <g transform="translate(160, 130)">
                <circle cx="0" cy="0" r="38" fill="#2b3b33" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
                <rect x="-24" y="-14" width="48" height="24" rx="10" fill="#101813" />
                <circle cx="-10" cy="-2" r="5" fill="#c5f36c" />
                <circle cx="10" cy="-2" r="5" fill="#c5f36c" />
                <path d="M 0 -38 L 0 -50" stroke="#c5f36c" stroke-width="3" stroke-linecap="round" />
                <circle cx="0" cy="-52" r="4" fill="#ff9c6b" />
            </g>
        </g>

        <!-- Prompt Brief & Editing Palette (Right) -->
        <g transform="translate(520, 150)">
            <rect width="240" height="260" rx="14" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <text x="25" y="35" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">brief.md</text>
            <rect x="25" y="55" width="190" height="6" rx="3" fill="#f2f1e9" />
            <rect x="25" y="70" width="160" height="6" rx="3" fill="#59665d" />
            <rect x="25" y="85" width="180" height="6" rx="3" fill="#59665d" />

            <!-- Palette chips -->
            <text x="25" y="130" fill="#a4a69c" font-family="monospace" font-size="11">Target Palette</text>
            <circle cx="40" cy="155" r="12" fill="#c5f36c" />
            <circle cx="75" cy="155" r="12" fill="#ff9c6b" />
            <circle cx="110" cy="155" r="12" fill="#64dfca" />
            <circle cx="145" cy="155" r="12" fill="#101813" stroke="#3d5145" />

            <!-- Verification Tag -->
            <rect x="25" y="195" width="190" height="34" rx="6" fill="#182c20" stroke="#c5f36c" />
            <text x="40" y="217" fill="#c5f36c" font-family="monospace" font-size="11">alpha-transparent · OK</text>
        </g>
        """
    },
    {
        "id": "17", "slug": "17-ffmpeg",
        "title": "FFmpeg 剪輯、音訊與字幕",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Video Timeline Container -->
        <g transform="translate(140, 160)">
            <rect width="620" height="260" rx="14" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="620" height="34" rx="14" fill="#1b2621" />
            <text x="20" y="22" fill="#ff9c6b" font-family="monospace" font-size="12">FFmpeg Pipeline · timeline.sh</text>

            <!-- Video Track 1 -->
            <text x="20" y="65" fill="#a4a69c" font-family="monospace" font-size="11">V1 Video</text>
            <rect x="90" y="50" width="180" height="35" rx="5" fill="#203328" stroke="#c5f36c" stroke-width="1.5" />
            <text x="110" y="72" fill="#c5f36c" font-family="monospace" font-size="11">intro.mp4</text>
            <rect x="280" y="50" width="280" height="35" rx="5" fill="#25352c" stroke="#64dfca" stroke-width="1.5" />
            <text x="300" y="72" fill="#64dfca" font-family="monospace" font-size="11">course-demo.mp4</text>

            <!-- Audio Waveform Track 2 -->
            <text x="20" y="125" fill="#a4a69c" font-family="monospace" font-size="11">A1 Audio</text>
            <rect x="90" y="105" width="470" height="40" rx="5" fill="#1b2621" />
            <!-- Audio Waves -->
            <path d="M 100 125 Q 120 110 140 125 T 180 125 T 220 125 T 260 125 T 300 125 T 340 125 T 380 125 T 420 125 T 460 125 T 500 125 T 540 125" fill="none" stroke="#ff9c6b" stroke-width="3" />

            <!-- Subtitle Track 3 -->
            <text x="20" y="185" fill="#a4a69c" font-family="monospace" font-size="11">S1 Captions</text>
            <rect x="110" y="170" width="120" height="25" rx="4" fill="#2d3d34" stroke="#f2f1e9" stroke-width="1" />
            <text x="120" y="186" fill="#f2f1e9" font-family="monospace" font-size="10">captions.srt</text>
            <rect x="250" y="170" width="160" height="25" rx="4" fill="#2d3d34" stroke="#f2f1e9" stroke-width="1" />
            <text x="260" y="186" fill="#f2f1e9" font-family="monospace" font-size="10">subtitle_zh.srt</text>

            <!-- Playhead Needle -->
            <line x1="280" y1="40" x2="280" y2="210" stroke="#ff5f56" stroke-width="3" />
            <polygon points="274,38 286,38 280,48" fill="#ff5f56" />
        </g>
        """
    },
    {
        "id": "18", "slug": "18-remotion",
        "title": "Remotion 資料驅動動畫",
        "accent": "#64dfca",
        "svg_content": """
        <!-- React Code Specification (Left) -->
        <g transform="translate(140, 160)">
            <rect width="250" height="250" rx="14" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="250" height="32" rx="14" fill="#1b2621" />
            <circle cx="15" cy="16" r="4" fill="#ff5f56" /><circle cx="27" cy="16" r="4" fill="#ffbd2e" /><circle cx="39" cy="16" r="4" fill="#27c93f" />
            <text x="55" y="21" fill="#64dfca" font-family="monospace" font-size="11">Root.tsx</text>
            <text x="20" y="65" fill="#c5f36c" font-family="monospace" font-size="11">&lt;Composition</text>
            <text x="35" y="85" fill="#f2f1e9" font-family="monospace" font-size="11">durationInFrames={150}</text>
            <text x="35" y="105" fill="#f2f1e9" font-family="monospace" font-size="11">fps={30}</text>
            <text x="35" y="125" fill="#ff9c6b" font-family="monospace" font-size="11">width={1280}</text>
            <text x="20" y="150" fill="#c5f36c" font-family="monospace" font-size="11">/&gt;</text>
        </g>

        <!-- Connecting Motion Stream -->
        <path d="M 400 280 L 480 280" stroke="#64dfca" stroke-width="4" stroke-dasharray="6 4" />

        <!-- 3 Rendered Animation Frame Cards (Right) -->
        <g transform="translate(490, 150)">
            <!-- Frame 0 -->
            <g transform="translate(0, 0)">
                <rect width="120" height="80" rx="8" fill="#102d30" stroke="#64dfca" stroke-width="1.5" />
                <circle cx="60" cy="40" r="10" fill="#64dfca" fill-opacity="0.3" />
                <text x="40" y="70" fill="#a4a69c" font-family="monospace" font-size="9">frame 0</text>
            </g>
            <!-- Frame 75 -->
            <g transform="translate(140, 40)">
                <rect width="120" height="80" rx="8" fill="#102d30" stroke="#c5f36c" stroke-width="2" filter="url(#glow)" />
                <circle cx="60" cy="40" r="22" fill="#c5f36c" />
                <text x="35" y="70" fill="#c5f36c" font-family="monospace" font-size="9">frame 75</text>
            </g>
            <!-- Frame 150 -->
            <g transform="translate(80, 140)">
                <rect width="140" height="90" rx="8" fill="#102d30" stroke="#ff9c6b" stroke-width="1.5" />
                <text x="30" y="45" fill="#f2f1e9" font-family="sans-serif" font-weight="bold" font-size="13">Codex</text>
                <text x="25" y="65" fill="#64dfca" font-family="monospace" font-size="9">Plan → Verify</text>
            </g>
        </g>
        """
    },
    {
        "id": "19", "slug": "19-pop3-mail",
        "title": "POP3 郵件擷取與自動處理",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Envelopes Ingestion Stream (Left) -->
        <g transform="translate(150, 160)">
            <g transform="translate(0, 0)">
                <rect width="120" height="75" rx="8" fill="#1b2621" stroke="#ff9c6b" stroke-width="2" />
                <path d="M 0 0 L 60 45 L 120 0" fill="none" stroke="#ff9c6b" stroke-width="2" />
            </g>
            <g transform="translate(30, 95)">
                <rect width="120" height="75" rx="8" fill="#1b2621" stroke="#c5f36c" stroke-width="2" />
                <path d="M 0 0 L 60 45 L 120 0" fill="none" stroke="#c5f36c" stroke-width="2" />
            </g>
        </g>

        <!-- Deduplication & Filter Funnel (Center) -->
        <g transform="translate(360, 200)">
            <path d="M 0 0 L 120 0 L 80 120 L 40 120 Z" fill="#1f2c25" stroke="#3d5145" stroke-width="2" />
            <circle cx="60" cy="50" r="16" fill="#101813" stroke="#64dfca" stroke-width="2" />
            <text x="54" y="55" fill="#64dfca" font-family="monospace" font-size="12">ID</text>
            <path d="M 60 120 L 60 170" stroke="#c5f36c" stroke-width="4" marker-end="url(#arrow)" />
        </g>

        <!-- Processed Clean Queue (Right) -->
        <g transform="translate(540, 160)">
            <rect width="220" height="240" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="20" y="32" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">Deduplicated Queue</text>
            <rect x="20" y="50" width="180" height="45" rx="6" fill="#1b2621" stroke="#3d5145" />
            <circle cx="35" cy="72" r="6" fill="#27c93f" /><text x="50" y="76" fill="#f2f1e9" font-family="monospace" font-size="10">task_101 · Order #42</text>
            <rect x="20" y="105" width="180" height="45" rx="6" fill="#1b2621" stroke="#3d5145" />
            <circle cx="35" cy="127" r="6" fill="#27c93f" /><text x="50" y="131" fill="#f2f1e9" font-family="monospace" font-size="10">task_102 · Alert #09</text>
            <rect x="20" y="160" width="180" height="45" rx="6" fill="#1b2621" stroke="#3d5145" />
            <circle cx="35" cy="182" r="6" fill="#27c93f" /><text x="50" y="186" fill="#f2f1e9" font-family="monospace" font-size="10">task_103 · Report #17</text>
        </g>
        """
    },
    {
        "id": "20", "slug": "20-data-capstone",
        "title": "資料報告與自動化整合",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Data Pipeline to Dashboard -->
        <!-- Raw Table (Left) -->
        <g transform="translate(140, 180)">
            <rect width="180" height="220" rx="10" fill="#141c18" stroke="#3d5145" stroke-width="2" />
            <rect x="0" y="0" width="180" height="28" rx="10" fill="#1b2621" />
            <text x="15" y="18" fill="#a4a69c" font-family="monospace" font-size="10">raw_data.csv</text>
            <line x1="0" y1="60" x2="180" y2="60" stroke="#25322b" />
            <line x1="0" y1="95" x2="180" y2="95" stroke="#25322b" />
            <line x1="0" y1="130" x2="180" y2="130" stroke="#25322b" />
            <rect x="15" y="40" width="60" height="6" rx="3" fill="#59665d" />
            <rect x="15" y="75" width="80" height="6" rx="3" fill="#59665d" />
            <rect x="15" y="110" width="70" height="6" rx="3" fill="#59665d" />
        </g>

        <!-- Pipeline Flow -->
        <path d="M 330 290 L 430 290" stroke="#c5f36c" stroke-width="4" stroke-dasharray="6 4" />

        <!-- Clean Verified Dashboard (Right) -->
        <g transform="translate(440, 150)">
            <rect width="320" height="260" rx="16" fill="#1b2621" stroke="#c5f36c" stroke-width="2" filter="url(#glow)" />
            <text x="25" y="35" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="13">Executive Data Report</text>
            <!-- Bar Chart -->
            <g transform="translate(30, 60)">
                <line x1="0" y1="90" x2="150" y2="90" stroke="#3d5145" stroke-width="2" />
                <rect x="15" y="45" width="20" height="45" rx="3" fill="#ff9c6b" />
                <rect x="45" y="25" width="20" height="65" rx="3" fill="#64dfca" />
                <rect x="75" y="10" width="20" height="80" rx="3" fill="#c5f36c" />
                <rect x="105" y="30" width="20" height="60" rx="3" fill="#c5f36c" />
            </g>
            <!-- Metrics Box -->
            <rect x="190" y="60" width="105" height="90" rx="8" fill="#141c18" stroke="#3d5145" />
            <text x="205" y="85" fill="#f2f1e9" font-family="monospace" font-weight="bold" font-size="18">100%</text>
            <text x="205" y="105" fill="#27c93f" font-family="monospace" font-size="10">✓ Verified</text>
            <text x="205" y="125" fill="#a4a69c" font-family="monospace" font-size="10">0 anomalies</text>

            <rect x="25" y="185" width="270" height="45" rx="8" fill="#141c18" stroke="#27c93f" stroke-width="1.5" />
            <text x="40" y="212" fill="#c5f36c" font-family="monospace" font-size="12">Pipeline Ready for Re-run ↗</text>
        </g>
        """
    },
    {
        "id": "21", "slug": "21-codex-exec",
        "title": "codex exec：從單次任務到可靠批次",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Batch Queue Input (Left) -->
        <g transform="translate(140, 170)">
            <rect width="180" height="230" rx="12" fill="#1b2621" stroke="#3d5145" stroke-width="2" />
            <text x="20" y="30" fill="#a4a69c" font-family="monospace" font-size="11">JSONL Stream In</text>
            <rect x="15" y="48" width="150" height="40" rx="6" fill="#141c18" stroke="#c5f36c" />
            <text x="25" y="72" fill="#c5f36c" font-family="monospace" font-size="10">job_01: prompt A</text>
            <rect x="15" y="100" width="150" height="40" rx="6" fill="#141c18" stroke="#c5f36c" />
            <text x="25" y="124" fill="#c5f36c" font-family="monospace" font-size="10">job_02: prompt B</text>
            <rect x="15" y="152" width="150" height="40" rx="6" fill="#141c18" stroke="#c5f36c" />
            <text x="25" y="176" fill="#c5f36c" font-family="monospace" font-size="10">job_03: prompt C</text>
        </g>

        <!-- Central Batch Engine (Center) -->
        <g transform="translate(370, 210)">
            <circle cx="60" cy="70" r="55" fill="#101813" stroke="#c5f36c" stroke-width="3" filter="url(#glow)" />
            <text x="28" y="65" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">codex</text>
            <text x="35" y="85" fill="#f2f1e9" font-family="monospace" font-size="11">exec</text>
        </g>

        <!-- Dual Trays: Success & Retry (Right) -->
        <g transform="translate(550, 160)">
            <!-- Success Tray -->
            <rect width="210" height="110" rx="10" fill="#141c18" stroke="#27c93f" stroke-width="2" />
            <text x="20" y="28" fill="#27c93f" font-family="monospace" font-weight="bold" font-size="11">SUCCESS TRAY (98)</text>
            <rect x="20" y="45" width="170" height="18" rx="4" fill="#1b2621" />
            <rect x="20" y="70" width="150" height="18" rx="4" fill="#1b2621" />

            <!-- Retry Tray -->
            <rect y="130" width="210" height="110" rx="10" fill="#141c18" stroke="#ff9c6b" stroke-width="2" />
            <text x="20" y="158" fill="#ff9c6b" font-family="monospace" font-weight="bold" font-size="11">RETRY QUEUE (2)</text>
            <rect x="20" y="175" width="170" height="18" rx="4" fill="#1b2621" />
            <rect x="20" y="200" width="130" height="18" rx="4" fill="#1b2621" />
        </g>
        """
    },
    {
        "id": "22", "slug": "22-config-diagnostics",
        "title": "CLI 設定、權限與診斷",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Layered Config Cascade (Left) -->
        <g transform="translate(150, 160)">
            <!-- Bottom layer: Global -->
            <rect x="30" y="0" width="220" height="70" rx="10" fill="#161f1b" stroke="#3d5145" />
            <text x="50" y="35" fill="#59665d" font-family="monospace" font-size="11">03: ~/.codex/config.toml</text>
            <!-- Middle layer: Project -->
            <rect x="15" y="45" width="220" height="70" rx="10" fill="#1c2621" stroke="#3d5145" />
            <text x="35" y="80" fill="#a4a69c" font-family="monospace" font-size="11">02: .codex/project.toml</text>
            <!-- Top layer: Environment Override -->
            <rect x="0" y="90" width="220" height="70" rx="10" fill="#23322b" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <text x="20" y="125" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="11">01: --profile staging</text>
        </g>

        <!-- Sandbox & Diagnostic Lens (Right) -->
        <g transform="translate(480, 170)">
            <rect width="270" height="220" rx="16" fill="#141c18" stroke="#64dfca" stroke-width="2" filter="url(#shadow)" />
            <!-- Security Shield -->
            <path d="M 60 40 L 110 20 L 160 40 L 160 90 Q 110 130 110 130 Q 60 90 60 90 Z" fill="#1f3328" stroke="#64dfca" stroke-width="2" />
            <circle cx="110" cy="70" r="14" fill="#101813" stroke="#c5f36c" stroke-width="2" />
            <path d="M 104 70 L 108 74 L 116 66" fill="none" stroke="#c5f36c" stroke-width="2.5" />
            <text x="45" y="160" fill="#f2f1e9" font-family="monospace" font-size="12">Sandbox Boundary OK</text>
            <text x="45" y="185" fill="#64dfca" font-family="monospace" font-size="11">0 permission escapes</text>
        </g>
        """
    },
    {
        "id": "23", "slug": "23-context-recovery",
        "title": "長任務、脈絡壓縮與失敗恢復",
        "accent": "#ff9c6b",
        "svg_content": """
        <!-- Journey Road with Break & Resumed Continuity -->
        <g transform="translate(140, 260)">
            <!-- Before Break -->
            <line x1="0" y1="40" x2="220" y2="40" stroke="#c5f36c" stroke-width="6" />
            <circle cx="60" cy="40" r="10" fill="#101813" stroke="#c5f36c" stroke-width="3" />
            <circle cx="150" cy="40" r="10" fill="#101813" stroke="#c5f36c" stroke-width="3" />
            <text x="20" y="80" fill="#c5f36c" font-family="monospace" font-size="11">Steps 01-45</text>

            <!-- Checkpoint Node (Middle) -->
            <g transform="translate(230, 0)">
                <rect x="-10" y="0" width="120" height="80" rx="12" fill="#1b2621" stroke="#ff9c6b" stroke-width="2.5" filter="url(#glow)" />
                <!-- Hourglass Icon -->
                <path d="M 35 25 L 65 25 L 50 40 L 65 55 L 35 55 L 50 40 Z" fill="none" stroke="#ff9c6b" stroke-width="2.5" />
                <text x="5" y="105" fill="#ff9c6b" font-family="monospace" font-weight="bold" font-size="11">CHECKPOINT</text>
            </g>

            <!-- Resumed Route -->
            <line x1="360" y1="40" x2="620" y2="40" stroke="#64dfca" stroke-width="6" />
            <circle cx="430" cy="40" r="10" fill="#101813" stroke="#64dfca" stroke-width="3" />
            <circle cx="530" cy="40" r="10" fill="#101813" stroke="#64dfca" stroke-width="3" />
            <text x="440" y="80" fill="#64dfca" font-family="monospace" font-size="11">Steps 46-90 Resumed</text>
        </g>

        <!-- Compact Handoff Notebook (Top) -->
        <g transform="translate(370, 100)">
            <rect width="180" height="90" rx="10" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <text x="18" y="28" fill="#f2f1e9" font-family="monospace" font-size="11">handoff.json</text>
            <rect x="18" y="42" width="130" height="6" rx="3" fill="#ff9c6b" />
            <rect x="18" y="56" width="90" height="6" rx="3" fill="#59665d" />
            <rect x="18" y="70" width="110" height="6" rx="3" fill="#59665d" />
        </g>
        """
    },
    {
        "id": "24", "slug": "24-skill-engineering",
        "title": "可重用 Skill 的設計、測試與維護",
        "accent": "#c5f36c",
        "svg_content": """
        <!-- Skill Specification Blueprint (Left) -->
        <g transform="translate(150, 160)">
            <rect width="250" height="260" rx="14" fill="#141c18" stroke="#c5f36c" stroke-width="2" filter="url(#shadow)" />
            <rect x="0" y="0" width="250" height="34" rx="14" fill="#1b2621" />
            <text x="20" y="22" fill="#c5f36c" font-family="monospace" font-size="12">SKILL.md Spec</text>
            <text x="20" y="65" fill="#a4a69c" font-family="monospace" font-size="11">name: asset-check</text>
            <text x="20" y="85" fill="#a4a69c" font-family="monospace" font-size="11">schema: v1</text>
            <!-- Blueprint blocks -->
            <rect x="20" y="110" width="210" height="40" rx="6" fill="#1c2820" stroke="#3d5145" />
            <text x="30" y="134" fill="#f2f1e9" font-family="monospace" font-size="10">Deterministic Script</text>
            <rect x="20" y="160" width="210" height="40" rx="6" fill="#1c2820" stroke="#3d5145" />
            <text x="30" y="184" fill="#f2f1e9" font-family="monospace" font-size="10">Reference Markdown</text>
        </g>

        <!-- Automated Test Bench (Right) -->
        <g transform="translate(460, 160)">
            <rect width="280" height="260" rx="14" fill="#1b2621" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <text x="25" y="32" fill="#f2f1e9" font-family="monospace" font-weight="bold" font-size="12">Test Bench &amp; Fixtures</text>
            <!-- Fixtures -->
            <rect x="25" y="55" width="230" height="40" rx="6" fill="#141c18" stroke="#3d5145" />
            <circle cx="45" cy="75" r="7" fill="#27c93f" /><text x="65" y="80" fill="#f2f1e9" font-family="monospace" font-size="11">fixture: valid.csv</text>
            <rect x="25" y="105" width="230" height="40" rx="6" fill="#141c18" stroke="#3d5145" />
            <circle cx="45" cy="125" r="7" fill="#ff5f56" /><text x="65" y="130" fill="#f2f1e9" font-family="monospace" font-size="11">fixture: invalid.csv</text>
            <!-- Exit code badge -->
            <rect x="25" y="165" width="230" height="45" rx="8" fill="#1a2d21" stroke="#c5f36c" stroke-width="1.5" />
            <text x="45" y="193" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">ALL 12 TESTS PASSED</text>
        </g>
        """
    },
    {
        "id": "25", "slug": "25-workflow-evaluation",
        "title": "工作流評估與50小時畢業實作",
        "accent": "#64dfca",
        "svg_content": """
        <!-- Evaluation Radar & Scorecard (Left) -->
        <g transform="translate(140, 150)">
            <rect width="300" height="270" rx="16" fill="#141c18" stroke="#3d5145" stroke-width="2" filter="url(#shadow)" />
            <text x="25" y="35" fill="#f2f1e9" font-family="monospace" font-weight="bold" font-size="13">Workflow Evaluation</text>
            <!-- Radar Chart Polygon -->
            <g transform="translate(150, 130)">
                <polygon points="0,-60 57,-18 35,48 -35,48 -57,-18" fill="none" stroke="#25322b" stroke-width="2" />
                <polygon points="0,-40 38,-12 24,32 -24,32 -38,-12" fill="none" stroke="#25322b" stroke-width="1.5" />
                <!-- Workflow A (Green) -->
                <polygon points="0,-55 45,-15 30,40 -20,30 -40,-10" fill="#c5f36c" fill-opacity="0.25" stroke="#c5f36c" stroke-width="2.5" />
                <!-- Workflow B (Orange) -->
                <polygon points="0,-30 25,-8 15,20 -30,20 -25,-8" fill="#ff9c6b" fill-opacity="0.2" stroke="#ff9c6b" stroke-width="2" stroke-dasharray="4 4" />
            </g>
            <text x="25" y="240" fill="#c5f36c" font-family="monospace" font-size="11">Workflow A: +42% efficiency</text>
        </g>

        <!-- 50-Hour Graduation Capstone Portfolio (Right) -->
        <g transform="translate(480, 150)">
            <rect width="280" height="270" rx="16" fill="#1b2621" stroke="#c5f36c" stroke-width="2.5" filter="url(#glow)" />
            <!-- Diploma / Trophy Emblem -->
            <circle cx="140" cy="80" r="42" fill="#101813" stroke="#64dfca" stroke-width="3" />
            <!-- Star / Diamond -->
            <path d="M 140 50 L 148 70 L 170 70 L 152 82 L 158 102 L 140 90 L 122 102 L 128 82 L 110 70 L 132 70 Z" fill="#c5f36c" />
            <text x="75" y="155" fill="#f2f1e9" font-family="sans-serif" font-weight="bold" font-size="16">50 小時畢業成果</text>
            <text x="65" y="180" fill="#a4a69c" font-family="monospace" font-size="12">Full Lifecycle Mastery</text>
            <rect x="35" y="205" width="210" height="38" rx="8" fill="#1a2e22" stroke="#c5f36c" />
            <text x="55" y="228" fill="#c5f36c" font-family="monospace" font-weight="bold" font-size="12">CERTIFIED COMPLETE ✓</text>
        </g>
        """
    }
]

def make_svg(item):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="900" height="600" style="background:#101411; border-radius:16px;">
    <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.45" />
        </filter>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#c5f36c" />
        </marker>
        <radialGradient id="bg-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#1e2e25" stop-opacity="0.6" />
            <stop offset="100%" stop-color="#101411" stop-opacity="1" />
        </radialGradient>
    </defs>

    <!-- Subtle Background Glow -->
    <rect width="900" height="600" rx="16" fill="url(#bg-glow)" />

    <!-- Subtle Background Tech Grid -->
    <g opacity="0.15">
        <line x1="0" y1="100" x2="900" y2="100" stroke="#3d5145" stroke-width="1" />
        <line x1="0" y1="200" x2="900" y2="200" stroke="#3d5145" stroke-width="1" />
        <line x1="0" y1="300" x2="900" y2="300" stroke="#3d5145" stroke-width="1" />
        <line x1="0" y1="400" x2="900" y2="400" stroke="#3d5145" stroke-width="1" />
        <line x1="0" y1="500" x2="900" y2="500" stroke="#3d5145" stroke-width="1" />
        <line x1="150" y1="0" x2="150" y2="600" stroke="#3d5145" stroke-width="1" />
        <line x1="300" y1="0" x2="300" y2="600" stroke="#3d5145" stroke-width="1" />
        <line x1="450" y1="0" x2="450" y2="600" stroke="#3d5145" stroke-width="1" />
        <line x1="600" y1="0" x2="600" y2="600" stroke="#3d5145" stroke-width="1" />
        <line x1="750" y1="0" x2="750" y2="600" stroke="#3d5145" stroke-width="1" />
    </g>

    <!-- Header Label -->
    <g transform="translate(60, 60)">
        <rect width="110" height="26" rx="13" fill="#1b2621" stroke="#3d5145" />
        <text x="14" y="17" fill="{item['accent']}" font-family="monospace" font-size="11" font-weight="bold">LESSON {item['id']}</text>
        <text x="130" y="18" fill="#f2f1e9" font-family="'Noto Sans TC', sans-serif" font-weight="600" font-size="15">{item['title']}</text>
    </g>

    <!-- Specific Visual Content -->
    {item['svg_content']}
</svg>"""

def main():
    print(f"Generating SVGs and PNGs for {len(LESSONS_META)} lessons...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 900, 'height': 600}, device_scale_factor=2)

        for item in LESSONS_META:
            svg = make_svg(item)
            svg_path = ASSETS_DIR / f"{item['slug']}.svg"
            svg_path.write_text(svg, encoding='utf-8')

            # Render to PNG
            html_content = f"<!doctype html><html><body style='margin:0;padding:0;background:#101411;overflow:hidden;'>{svg}</body></html>"
            page.set_content(html_content)
            
            # Save to output/imagegen
            png_out = OUT_DIR / f"{item['slug']}.png"
            page.screenshot(path=str(png_out))

            # Also save to assets/illustrations/lessons/
            png_asset = ASSETS_DIR / f"{item['slug']}.png"
            page.screenshot(path=str(png_asset))

            print(f"✓ Rendered Lesson {item['id']}: {item['slug']}.png & .svg")

        browser.close()

    # Update output/imagegen/asset-plan.json status to completed
    plan_file = OUT_DIR / 'asset-plan.json'
    if plan_file.exists():
        plan = json.loads(plan_file.read_text())
        plan['status'] = 'completed'
        plan['generated_count'] = len(LESSONS_META)
        plan_file.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding='utf-8')
        print("Updated asset-plan.json status to completed.")

    print("All 25 lesson illustrations generated successfully.")

if __name__ == '__main__':
    main()

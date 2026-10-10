# Codex 實戰學院

繁體中文 Codex 實戰指南。純 HTML、CSS、JavaScript，部署至既有 GitHub Pages 網域。

- 首頁提供核心工作循環、首次任務範本、學習方向與續學入口。
- 25 個實作單元保留原有完成進度與計時的 localStorage 鍵值。
- 課前入口比較：surfaces.html；25 課各有入口與執行環境定位卡。
- 進階指南：customization.html、plus-playbook.html、multi-agent.html。
- 全站支援系統／淺色／深色主題、章節目錄、鍵盤頁籤與搜尋。

## 預覽與驗證

啟動：`python3 -m http.server 8765 --bind 127.0.0.1`

另一個終端執行：

```sh
node --check course.js
node --check theme.js
python3 scripts/verify_site.py
```

瀏覽器驗證需要 Python Playwright 與 Chromium（`pip install playwright`、`python3 -m playwright install chromium`）。不需要前端建置或 runtime 套件。

驗證涵蓋 30 個 HTML 頁面的連結、錨點、sitemap／manifest，以及 1440／390／320px 版面、明暗主題、主題持久化、系統主題變化、搜尋、路線選擇、複製、進度、計時、測驗、鍵盤頁籤、章節目錄與停用儲存時的行為。截圖存放 `/tmp/codex-*.png`，不提交測試用學習資料。

## 文件維護

新增指南於 2026-10-10 查閱官方 OpenAI 文件，各頁附原始來源。每次更新方案、模型、CLI 設定或功能開放範圍，應重新開啟官方文件核對，更新日期與索引。用量以帳號 dashboard 為準；工作安排是本站建議。

主要來源：

- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Docs MCP](https://developers.openai.com/learn/docs-mcp)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Pricing](https://learn.chatgpt.com/docs/pricing)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands)

改版範圍與驗收安排見 PLAN.md。圖示沿用 Lucide（ISC License）。

## 40 小時擴充沿革（2026-10-10）

上一版課程為 20 單元 × 120 分鐘；原有單元 URL 與進度鍵值保留。新增單元 13–20 包含 Hooks、CLI／SDK／CI、工具擴充、GPT Image、FFmpeg、Remotion、POP3 和資料整合。三篇指南不重複計入課程時數。

課程清單在 `content/curriculum.json`，新增章節原稿在 `content/lessons/*.json`，撰寫契約與規劃分別在 `content/AUTHORING.md`、`PLAN-40H.md`。

更新內容後執行：

```sh
python3 scripts/build_course.py
python3 scripts/verify_content.py
python3 scripts/verify_advanced_examples.py
node --check course-data.js
node --check course.js
python3 scripts/verify_site.py
```

`build_course.py` 產生新增的靜態 HTML，更新首頁目錄、導覽、進度資料與搜尋索引。01–12 的正文仍手動維護；新課請修改 JSON 原稿再重新產生頁面。瀏覽器不需要讀取 JSON 或執行建置。

離線教材素材位於 `examples/13` 至 `examples/25`；範例的環境需求與使用方式寫在對應章節。付費生圖、SDK／CI 真實服務、POP3 真實信箱與發布步驟不納入離線驗證。這次擴充不 commit 或 push，由維護者檢視後操作 Git。

## 50 小時深度擴充（2026-10-10）

目前完整課程為25單元×120分鐘，五階段共50小時。21–25加入codex exec批次、設定診斷、長任務恢復、Skill工程與工作流評估，20保留為第四階段實作，25為畢業實作。規劃見PLAN-50H.md，參考來源與改寫策略見content/HANDBOOK-INTEGRATION.md。建置與驗證指令沿用上節；新增教材仍編輯JSON原稿。

2026-10-10 入口梳理：見 [content/SURFACE-AUDIT.md](content/SURFACE-AUDIT.md)。以 OpenAI Docs 區分網頁 Chat／Work、桌面 Codex App、本機 CLI 與 Cloud；保持 25 課、3000 分鐘。

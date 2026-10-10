# Codex 實戰學院

繁體中文 Codex 實戰指南。純 HTML、CSS、JavaScript，部署至既有 GitHub Pages 網域。

- 首頁提供核心工作循環、首次任務範本、學習方向與續學入口。
- 12 個實作單元保留原有完成進度與計時的 localStorage 鍵值。
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

驗證涵蓋 17 個 HTML 頁面的連結、錨點、sitemap／manifest，以及 1440／390／320px 版面、明暗主題、主題持久化、系統主題變化、搜尋、路線選擇、複製、進度、計時、測驗、鍵盤頁籤、章節目錄與停用儲存時的行為。截圖存放 `/tmp/codex-*.png`，不提交測試用學習資料。

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

# 課程操作入口稽核

查證：2026-10-10。確有混淆，以逐課標示與原文修訂處理。既有 25 課／3000 分鐘、URL、進度鍵與插圖保留；新比較頁不另計時數。

| 位置 | 原本的問題 | 修訂結果 |
| --- | --- | --- |
| 全 25 課、首頁 | 不能立即判斷入口與執行位置 | catalog 的 surface 四欄、每課定位卡、首頁標籤與比較入口 |
| 02 | 六個命令稱為五個，App／CLI 的 /usage、/permissions 混列 | App 與互動 CLI 分欄；shell 命令另外描述 |
| 04 | 規劃方法與 follow-up 按鍵缺少入口區分 | 明列 CLI Enter／Tab、App 控制與網頁自然語言方法 |
| 06 | /worktree、fork 與檔案隔離模糊 | App Worktree／fork 選項，CLI Git worktree／對話 fork 分開 |
| 08 | Cloud 未區別網頁 Work 環境 | 定義 Codex 已配置遠端開發環境，不自動搬入本機資源 |
| 09／客製化指南 | config、Projects 與 Memories 的作用範圍不明 | 本機 Codex host、網頁 Projects、網頁／本機記憶分開 |
| 10／Plus 指南 | 用量和權限控制缺少入口，Work 共用限制不明 | CLI／App 控制、ChatGPT Work／Codex 共用限制、API 計費分列 |
| 11 | 生活任務與本機資料夾操作混在一起、40h 舊標籤 | 說明網頁可用案例與本機必要條件；改成 50h |
| 13–15 | Hook host、App Server、Skill/plugin/MCP 入口不清 | CLI Hook lab、協定程序、本機探索與網頁 Skill 選取分開 |
| 16–20 | 生圖與影音／郵件腳本未明確標示執行端 | 內建／Skill／API 三路徑；FFmpeg、Remotion、POP3、Python 是外部工具 |
| 21–25 | 深度實作可能被讀成各介面通用操作 | exec shell、CLI 啟動旗標、session／Git、local Skill、跨入口評估條件明確 |
| 插圖 01／25 | 示意 CLI 字串 codex run 不存在 | SVG 與產生器改為 codex／codex exec --json；未重做既有 PNG |

## 官方依據

- [入口、Work／Codex 能力與共用限制](https://learn.chatgpt.com/docs/use-chatgpt)
- [網頁](https://learn.chatgpt.com/docs/web)
- [設定共享／網頁不讀本機 config](https://learn.chatgpt.com/docs/developer-settings)
- [桌面 App slash](https://learn.chatgpt.com/docs/reference/slash-commands)
- [CLI slash](https://learn.chatgpt.com/docs/cli/slash-commands)
- [CLI shell reference](https://learn.chatgpt.com/docs/cli/reference)
- [環境模式](https://learn.chatgpt.com/docs/environments/modes)
- [Cloud 環境](https://learn.chatgpt.com/docs/environments/cloud-environments)
- [Projects](https://learn.chatgpt.com/docs/projects)
- [Memories](https://learn.chatgpt.com/docs/customization/memories)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
- [Skills](https://learn.chatgpt.com/docs/build-skills)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [生圖](https://learn.chatgpt.com/docs/image-generation)

## 驗收範圍

- verify_content.py：25 課／3000 分鐘、章節、來源、下載素材與 Python 語法。
- verify_advanced_examples.py：離線批次合約、設定模擬、檢查點、Skill 資產與畢業工作流。
- verify_site.py：32 頁本機連結、錨點；1440／390／320px 深淺主題；搜尋、路線、複製、進度、計時、測驗、鍵盤 tabs、目錄、storage 拒絕與零 JS／本機 HTTP 錯誤；新增比較頁與逐課定位卡。
- 重跑建置器確認冪等，保留插圖。手機比較表用橫向捲動，避免窄欄切碎文字。

本次驗證網站與離線練習，沒有登入各種產品、執行付費模型呼叫或連線真實信箱；功能開放仍以帳號與 host 為準。未 commit／push；由使用者處理。

# 40 小時課程擴充計畫

## 目標與範圍
保留現有網站風格、12 單元 URL 和進度鍵值；增加 8 個完整兩小時單元，形成 20 × 120 分鐘 = 2400 分鐘（40 小時）。三篇進階指南作為隨時可讀的參考，不重複計入時數。時數為建議閱讀／實作安排。

## 學習階段
- 01–05：交辦、脈絡、除錯、規劃、驗收（10 小時）。
- 06–10：協作、UI、Cloud、客製化與第一個整合實作（10 小時）。
- 11–15：生活應用、案例回顧、Hooks、CLI／SDK／CI、擴充工具（10 小時）。
- 16–20：生圖、FFmpeg、Remotion、POP3、資料報告與最終整合（10 小時）。

## 新增單元與平行撰寫
- 作者 A：13 Hooks；14 非互動 CLI、SDK 與 CI；15 Skills、Plugins、MCP、WebMCP。
- 作者 B：16 GPT Image；17 FFmpeg；18 Remotion。
- 作者 C：19 POP3 郵件；20 資料報告與自動化整合。
- 主代理：課程資料／頁面產生、首頁與路線、20 單元進度與計時、來源與內容驗收、離線範例與瀏覽器 QA。

## 內容契約
詳見 content/AUTHORING.md。每單元提供先備、可觀察成果、120 分鐘安排、操作範例、Codex 任務範本、主要實作、變體、排錯、測驗、驗收清單與官方來源。

## 參考與驗收
起點：https://learn.chatgpt.com/docs/developers 。按子主題查閱 Hooks、SDK、Non-interactive、Plugins／MCP／WebMCP、Images API；多媒體查 FFmpeg／Remotion 官方文件，POP3 查 Python／協定與供應商文件。

- 核對技術主張、可用範圍與計費，不保證帳號未提供的功能。
- 不在本次執行付費 API、不連真實信箱、不寄信、不發布。
- 驗證 20 單元、每單元 120 分鐘、總計 40h、來源、導航、索引及舊進度相容。
- 執行 JS／靜態內容／離線範例檢查與桌面、手機、主題、搜尋、複製、進度及計時的瀏覽器 QA。
- 所有變更留在工作目錄，最後由使用者 git push；本次不 commit 或 push。

## 完成驗收（2026-10-10）
- 三組 subagent 完成 13–20 原稿，由主代理核對內容、來源、繁體用語與範例，再產生靜態頁面。
- 課程結構：20 × 120 分鐘 = 40 小時；25 個 HTML 頁面。新章節具備成果、時程、實作、排錯、測驗、驗收與官方來源。
- 通過內容契約、Python 語法、JavaScript 語法、Git whitespace、所有本機連結、錨點、sitemap 與 manifest 檢查。
- Playwright 通過全站 1440／390／320px、明暗主題、主題持久化、搜尋、路線、複製、進度、計時、測驗、鍵盤、目錄與停用儲存測試；無 JavaScript 或本機 HTTP 錯誤。已檢視手機首頁截圖。
- 獨立離線驗收：Hooks allow／deny／invalid JSON、結果 valid／invalid、生圖 dry-run、郵件首次 3 封與重跑 0 封、資料報告 2 接受／1 重複／2 拒絕／TWD 300.30 且重跑一致、FFmpeg 4 秒 360×360 轉檔與 ffprobe。
- Remotion 依官方文件審查範例，未安裝依賴或實際渲染；本機 FFmpeg 未含 libass，字幕燒入命令未執行。付費圖像、連線 SDK／CI／擴充服務及真實 POP3 均未呼叫。
- 未 commit、未 push；由維護者處理 Git。

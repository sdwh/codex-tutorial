# 50 小時深度課程：規劃與驗收

## 課程設計
25 單元 × 120 分鐘 = 3000 分鐘。五階段各10小時，保留01–20 URL、完成與計時鍵值。時數包含閱讀、操作、失敗變體與驗收，不宣稱50小時可保證熟練或效果。

| 新單元 | 先前覆蓋 | 新增深度與可驗收成果 |
|---|---|---|
|21 codex exec|14介紹CLI／SDK／CI|提示檔、工作目錄、stdout／stderr、JSONL／schema、結果驗收、有限重試與批次紀錄|
|22設定與診斷|09與客製化指南|設定優先序、profile、信任與權限、規則診斷，區分配置預設與強制要求|
|23長任務與恢復|06／08協作與遠端|脈絡預算、壓縮、明確session恢復、現場狀態核對與交接契約|
|24 Skill工程|09／15擴充概覽|觸發正反例、漸進載入、確定性腳本、參考資料、測試與版本維護|
|25評估與畢業|05驗收、20資料整合|分開評估觸發／邊界／結構／事實，固定輸入A/B記錄與完整流程交付|

## 參考與來源策略
參考專案：https://github.com/hopecyb/CodexHandbook
檢視快照：`8a4e885fb389d3209b0b4cb0f718a781bf17467b`（2026-10-10）。主要閱讀guide、prompts、skills、cases的具體子頁；逐課列出來源。
未見根目錄全站LICENSE；範例子目錄中的CC0僅覆蓋各自目錄。本站以其議題作為選題參考，獨立撰寫繁體教材與練習，不移植全站正文、CSS、圖片或程式。功能與指令以實際閱讀的OpenAI官方文件為準，來源對照見 `content/HANDBOOK-INTEGRATION.md`。

## 分工
- developer_lessons：21、22與離線範例。
- mail_data_lessons：23、25與離線範例。
- media_lessons：24與離線Skill教材（使用skill-creator檢查）。
- 主代理：來源比對、課程資料、首頁、導覽、學習路線、metadata、建置可重跑性、內容與瀏覽器驗收。

## 驗收範圍
- 每課120分鐘、完整先備／成果／時程／實作／排錯／測驗／驗收／來源。
- 原進度相容，新25課進度與續學正確；導覽與搜尋收錄全部單元。
- JSON、Python、JS、站內連結、metadata與頁面檢查；兩次建置一致。
- 離線例子的正常、失敗與重跑行為。模型、API、真實服務不在這次呼叫範圍。
- 全站桌面與手機、明暗主題、複製、測驗、計時與儲存失效測試。
- 不commit、不push，由使用者最後操作Git。

## 完成驗收（2026-10-10）
- 五個新單元各8個實質章節、120分鐘，總25單元／3000分鐘；先備、成果、操作、失敗變體、測驗、驗收與來源俱全。14/15連到21/24深入實作，20維持第四階段整合，25為畢業實作。
- 三組subagent產出部分素材後遇用量限制，主代理接手完成所有正文、其餘例子與驗收，並已對使用者說明。
- verify_content、verify_advanced_examples、Python/JS語法與git diff --check通過。離線實測八種批次結果、四種配置、invalid TOML、五種checkpoint情況、Skill正反素材與保護舊報告、未執行評分／效能聲稱拒絕、畢業報告數字／hash／重跑一致、CLI wrapper preview不寫檔。
- 本機codex-cli 0.162.0的exec/exec resume help與execpolicy測試通過：git status allow，git push forbidden（沒有執行命令）。模型exec、session續接、profile真正載入與Skill模型路由未呼叫。
- 全站30頁Playwright通過1440／390／320px明暗主題、搜尋、七種路線、複製、測驗、進度（含舊鍵與25/25）、計時、目錄、鍵盤與拒絕儲存測試，無JS／本機HTTP錯誤。已檢視21手機完整截圖；重複建置的頁面與索引逐位元一致。
- Skill creator quick_validate因本機缺PyYAML無法執行；已人工核對frontmatter/路徑與能力範圍，獨立執行checker fixtures。未把此缺口或未執行模型效果標成通過。
- 未commit、未push；變更留在工作目錄。

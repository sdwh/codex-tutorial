# CodexHandbook 內容整合對照

參考：https://github.com/hopecyb/CodexHandbook
快照：8a4e885fb389d3209b0b4cb0f718a781bf17467b；查閱2026-10-10。

| 手冊的有價值議題 | 本站安排 | 採用方式 |
|---|---|---|
|非互動exec、結構化輸出、流水線與重試|14整合概覽 → 21深入實作|原創prompt/schema與合成批次，分開程序、結構與審查結果|
|CLI配置、信任、規則與診斷|09/客製化 → 22|按官方最新優先序改寫，含平面TOML教學模擬，非官方loader|
|token/context、交接與失敗恢復|08 → 23|原創checkpoint hash/HEAD/status檢查，沒有自動回滾或備份宣稱|
|Skill結構、scripts/tests、references、security|15 → 24|原創素材manifest技能，漸進載入、觸發正反例與確定性查核|
|提示對照、工作流評估、團隊資產|05/20 → 25|固定合成資料、四維度記錄、未執行null、獨立報告驗收與交接|
|hooks、MCP、plugins、多代理、圖像、網站案例|13/15/16/12與multi-agent指南|既有覆蓋維持，避免重複計時或再增加同一概覽|

## 來源政策
手冊根目錄未見全站LICENSE；部分examples/complete-workflows與examples/skills有各自CC0 LICENSE，明確限該目錄。本次不搬運原站正文、圖片、程式或樣式，不套用那些子目錄授權到全站。以上議題作為選題參考，教材、腳本與fixtures獨立撰寫；每課有釘選commit的具體來源連結。OpenAI產品主張以實際查閱官方頁為準，不延用手冊較舊的版本描述或試驗數字。

官方核對：
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://learn.chatgpt.com/docs/developer-commands
- https://learn.chatgpt.com/docs/config-file/config-basic
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://learn.chatgpt.com/docs/agent-configuration/rules
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/reference/slash-commands （App指令，未承諾每個CLI版本一致）

## 寫作與分工實況
先規劃25×120分鐘並分派三組既有subagent。它們閱讀來源並產出部分原創scripts、fixtures與Skill骨架後，全部回報用量限制；主代理接手完成21–25正文與其餘素材，再進行驗收。不將未完成的代理撰寫或未執行的模型呼叫回報為完成。

## 驗證界線
離線測試只驗證確定性腳本、契約與網站。本機codex-cli 0.162.0已實際核對help與execpolicy範例git status=allow、git push=forbidden；只評估命令，未執行push。真實模型exec、resume、profile載入、Skill顯式或隱式選用及模型A/B尚未實測，不宣稱模型效果、成本或普遍成功率。Skill creator內建quick_validate因本機缺PyYAML無法執行，改以frontmatter/路徑人工審查加上獨立腳本fixture驗收，沒有隱瞞這個缺口。

window.CODEX_COURSE = {
  "title": "Codex 實戰學院｜50 小時深度實作課程",
  "minutes": 3000,
  "reviewed": "2026-10-10",
  "lessons": [
    {
      "id": "01",
      "slug": "01-tasking",
      "title": "Codex 工作循環與任務設計",
      "description": "理解 agent 工作方式；練習目標、脈絡、限制與驗收。",
      "track": "start",
      "minutes": 120,
      "phase": 1,
      "surface": {
        "entry": "Codex App／CLI・共通方法",
        "environment": "本機專案",
        "operation": "在 Codex 對話交辦；先連接資料夾或從 repo 啟動 CLI。",
        "transfer": "目標、脈絡與驗收也適用 ChatGPT Chat／Work；網頁需上傳資料或使用已連接來源。"
      }
    },
    {
      "id": "02",
      "slug": "02-commands",
      "title": "讀懂陌生專案與提供脈絡",
      "description": "導覽 repo、追資料流，用檔案與錯誤縮小問題。",
      "track": "start",
      "minutes": 120,
      "phase": 1,
      "surface": {
        "entry": "Codex App／互動 CLI",
        "environment": "本機專案",
        "operation": "讀碼提示在對話輸入；codex、codex resume 在終端機執行。",
        "transfer": "本課分開列出 App 與 CLI 的 slash commands；同名命令也可能有不同作用。"
      }
    },
    {
      "id": "03",
      "slug": "03-project-context",
      "title": "Debug：從症狀到可靠修復",
      "description": "重現問題、找根因、做最小修補與回歸驗證。",
      "track": "build",
      "minutes": 120,
      "phase": 1,
      "surface": {
        "entry": "Codex App／CLI・除錯",
        "environment": "本機專案與測試環境",
        "operation": "在對話提供重現步驟，由 agent 的工具執行測試。",
        "transfer": "Chat／Work 可分析提供的程式與錯誤；確認是否有可執行的 repo 和測試工具。"
      }
    },
    {
      "id": "04",
      "slug": "04-usage-safety",
      "title": "Plan 與跨檔功能開發",
      "description": "把模糊需求拆成階段，逐步開發與調整方向。",
      "track": "build",
      "minutes": 120,
      "phase": 1,
      "surface": {
        "entry": "Codex App／互動 CLI・規劃",
        "environment": "本機專案",
        "operation": "自然語言規劃可通用；/plan 在支援的 Codex 對話輸入。",
        "transfer": "網頁 Chat／Work 可要求先提出計畫；不要把 CLI 的按鍵或 slash command 當成網頁操作。"
      }
    },
    {
      "id": "05",
      "slug": "05-practical-workflows",
      "title": "測試、Diff 與 Code Review",
      "description": "設計驗收檢查，用差異與測試證據判斷成果。",
      "track": "start",
      "minutes": 120,
      "phase": 1,
      "surface": {
        "entry": "Codex App／CLI・驗收",
        "environment": "本機 repo",
        "operation": "App 看 diff／review；CLI 透過 /review 或要求工具檢查 Git 差異。",
        "transfer": "驗收方法可通用；網頁 Work 的成果檢查與 Codex 的 Git diff 操作不同。"
      }
    },
    {
      "id": "06",
      "slug": "06-git-worktrees",
      "title": "Git、Worktree 與平行任務",
      "description": "隔離獨立工作，管理分支、檢查點與整合。",
      "track": "scale",
      "minutes": 120,
      "phase": 2,
      "surface": {
        "entry": "Codex App＋CLI／Git",
        "environment": "本機、獨立 worktree",
        "operation": "App 使用 Worktree 控制；CLI 在已建立的 Git worktree 目錄啟動 codex。",
        "transfer": "Git worktree 隔離檔案；fork 分支對話不會自動隔離工作目錄。"
      }
    },
    {
      "id": "07",
      "slug": "07-frontend-ui",
      "title": "前端、UI 與視覺迭代",
      "description": "用尺寸、截圖與互動條件驗收介面。",
      "track": "build",
      "minutes": 120,
      "phase": 2,
      "surface": {
        "entry": "Codex App／CLI＋瀏覽器",
        "environment": "本機開發伺服器",
        "operation": "agent 執行專案命令；在瀏覽器或已提供的預覽工具驗收。",
        "transfer": "網頁 Work 可建立網站；本課 localhost、截圖與 repo 路徑以本機實作為準。"
      }
    },
    {
      "id": "08",
      "slug": "08-cloud-long-tasks",
      "title": "Cloud、遠端與長時間任務",
      "description": "準備環境，派送與回收遠端工作。",
      "track": "scale",
      "minutes": 120,
      "phase": 2,
      "surface": {
        "entry": "Codex Cloud",
        "environment": "已配置的遠端環境",
        "operation": "在支援的 App／網頁入口選 Cloud 與已發布環境，再派送任務。",
        "transfer": "Codex Cloud 與網頁 ChatGPT Work 的受管環境不同；本機檔案不會自動傳入雲端。"
      }
    },
    {
      "id": "09",
      "slug": "09-project-customization",
      "title": "AGENTS.md、RAG、Skills 與 MCP",
      "description": "建立專案規則、文件索引與可重用工作方式。",
      "track": "scale",
      "minutes": 120,
      "phase": 2,
      "surface": {
        "entry": "本機 Codex App／CLI・客製化",
        "environment": "本機 Codex host 與 repo",
        "operation": "在檔案編輯 AGENTS.md、config.toml；CLI 控制與 App Settings 分開操作。",
        "transfer": "ChatGPT 網頁的 Projects、個人偏好與記憶不能直接等同本機 Codex 設定。"
      }
    },
    {
      "id": "10",
      "slug": "10-usage-safety-capstone",
      "title": "Quota、權限與第一階段 Capstone",
      "description": "管理用量與執行邊界，交付第一個整合變更。",
      "track": "scale",
      "minutes": 120,
      "phase": 2,
      "surface": {
        "entry": "Codex App／CLI・用量與權限",
        "environment": "登入帳號與目前工作環境",
        "operation": "CLI 用 /status、/permissions；App 使用設定與用量介面。",
        "transfer": "ChatGPT Work 與 Codex 共用使用限制；API key 另走 API 計費。"
      }
    },
    {
      "id": "11",
      "slug": "11-beyond-coding",
      "title": "Codex 不只寫程式：生活 AI Agent",
      "description": "旅行研究、資料整理與個人學習教練。",
      "track": "automation",
      "minutes": 120,
      "phase": 3,
      "surface": {
        "entry": "ChatGPT Chat／Work＋Codex",
        "environment": "上傳資料、連接來源或本機檔案",
        "operation": "旅遊／學習可在網頁交辦；整理本機資料夾使用 Codex App Local／CLI。",
        "transfer": "挑選入口要看資料存取與交付需求；Work 也能執行程式，Codex 也能處理非程式任務。"
      }
    },
    {
      "id": "12",
      "slug": "12-codex-in-practice",
      "title": "Codex in Practice：從需求到學習網站",
      "description": "以真實案例回顧需求、研究、互動教材與交付。",
      "track": "build",
      "minutes": 120,
      "phase": 3,
      "surface": {
        "entry": "Codex App／CLI・網站實作",
        "environment": "本機網站 repo",
        "operation": "在對話交辦修改，以 shell 與瀏覽器工具驗證。",
        "transfer": "把範例路徑換成實際 repo；網站預覽網址是交付物，不是 Codex 的操作入口。"
      }
    },
    {
      "id": "13",
      "slug": "13-hooks",
      "title": "Hooks 與事件觸發",
      "description": "在工作生命週期加入可測試的自動化步驟。",
      "track": "automation",
      "minutes": 120,
      "phase": 3,
      "surface": {
        "entry": "Codex CLI・Hooks 實作",
        "environment": "本機 Codex runtime",
        "operation": "在 .codex 配置 Hook；先於終端機測 fixtures，再由 Codex 事件觸發。",
        "transfer": "這是 Codex 生命週期 Hook；不是 React Hook。App／plugin 支援須確認 host；網頁提示不會載入本機 hooks.json。"
      }
    },
    {
      "id": "14",
      "slug": "14-cli-sdk-ci",
      "title": "非互動 CLI、SDK 與 CI",
      "description": "輸出結構化結果，把查核接進腳本與 CI。",
      "track": "automation",
      "minutes": 120,
      "phase": 3,
      "surface": {
        "entry": "Codex CLI／SDK／CI",
        "environment": "本機或 CI runner",
        "operation": "codex 與 SDK 程式在終端機／runner 執行；CI 另配置登入與 secrets。",
        "transfer": "app-server 是供客戶端整合的協定程序；不是 Codex 桌面 App，也不是網站伺服器。"
      }
    },
    {
      "id": "15",
      "slug": "15-extensions",
      "title": "Skills、Plugins、MCP 與 WebMCP",
      "description": "選對擴充機制，建立最小工具整合。",
      "track": "automation",
      "minutes": 120,
      "phase": 3,
      "surface": {
        "entry": "Codex＋ChatGPT・擴充比較",
        "environment": "依 host 的工具與資料連線",
        "operation": "本機 Skill、MCP 設定在 Codex host；網頁 plugin 從支援的介面連接。",
        "transfer": "相同 Skill 內容可以封裝到不同入口；本機路徑、MCP、WebMCP 與網頁 plugin 不會自動互通。"
      }
    },
    {
      "id": "16",
      "slug": "16-image-generation",
      "title": "Codex 與 GPT Image 生圖",
      "description": "從素材規格到模型呼叫、編輯與圖像驗收。",
      "track": "creative",
      "minutes": 120,
      "phase": 4,
      "surface": {
        "entry": "Codex／ChatGPT 生圖＋Image API",
        "environment": "內建工具或本機 API 腳本",
        "operation": "自然語言觸發可用的生圖工具；API 範例在終端機執行。",
        "transfer": "先分辨內建工具與 API。$imagegen 的實際行為取決於載入的 SKILL.md；Plus 不提供免費 API 額度。"
      }
    },
    {
      "id": "17",
      "slug": "17-ffmpeg",
      "title": "FFmpeg 剪輯、音訊與字幕",
      "description": "檢查素材，建立可重現的剪輯與輸出流程。",
      "track": "creative",
      "minutes": 120,
      "phase": 4,
      "surface": {
        "entry": "Codex App／CLI＋FFmpeg",
        "environment": "本機影音檔案與 FFmpeg",
        "operation": "agent 呼叫 shell 執行 ffmpeg；這是外部工具的命令。",
        "transfer": "網頁 Work 如有工具可處理上傳影片，但不能直接讀取你的本機路徑；須另核對工具與資源限制。"
      }
    },
    {
      "id": "18",
      "slug": "18-remotion",
      "title": "Remotion 資料驅動動畫",
      "description": "以 React、影格與資料製作可重用動畫。",
      "track": "creative",
      "minutes": 120,
      "phase": 4,
      "surface": {
        "entry": "Codex App／CLI＋Remotion",
        "environment": "本機 Node.js 專案",
        "operation": "agent 在 shell 執行 npm／npx；Remotion Studio 在瀏覽器預覽動畫。",
        "transfer": "Remotion Studio 是作品預覽介面；不是 ChatGPT Work 或 Codex App。"
      }
    },
    {
      "id": "19",
      "slug": "19-pop3-mail",
      "title": "POP3 郵件擷取與自動處理",
      "description": "解析郵件、去重、分類與建立處理佇列。",
      "track": "automation",
      "minutes": 120,
      "phase": 4,
      "surface": {
        "entry": "Codex App／CLI＋Python POP3",
        "environment": "本機腳本與郵件伺服器",
        "operation": "先用離線 .eml 測試；經授權才由 Python 腳本連線 POP3。",
        "transfer": "POP3 是腳本與郵件伺服器的協定；不同於透過 ChatGPT 郵件 plugin 讀信。上傳 .eml 可改用網頁分析。"
      }
    },
    {
      "id": "20",
      "slug": "20-data-capstone",
      "title": "資料報告與自動化整合",
      "description": "清理、驗證與彙整資料，交付可重跑流程。",
      "track": "automation",
      "minutes": 120,
      "phase": 4,
      "surface": {
        "entry": "Codex App／CLI・資料工作流",
        "environment": "本機 Python 與資料集",
        "operation": "用 shell 執行離線資料與報告範例，再由 agent 解釋驗證證據。",
        "transfer": "報告方法可用於網頁 Work；遷移時須上傳材料並確認執行工具，不能沿用本機絕對路徑。"
      }
    },
    {
      "id": "21",
      "slug": "21-codex-exec",
      "title": "codex exec：從單次任務到可靠批次",
      "description": "管理輸入、JSONL、結果驗收與失敗，建立可重跑的批次流程。",
      "track": "automation",
      "minutes": 120,
      "phase": 5,
      "surface": {
        "entry": "Codex CLI・非互動 exec",
        "environment": "本機或批次 runner",
        "operation": "codex exec 是終端機命令；wrapper、重試與 JSONL 解析在程式中執行。",
        "transfer": "貼進 App／ChatGPT 對話只是一段文字；需由真正的 shell 工具啟動 CLI 才會執行。"
      }
    },
    {
      "id": "22",
      "slug": "22-config-diagnostics",
      "title": "CLI 設定、權限與診斷",
      "description": "釐清設定優先序、信任、沙箱與命令規則，診斷環境差異。",
      "track": "scale",
      "minutes": 120,
      "phase": 5,
      "surface": {
        "entry": "Codex CLI・設定診斷",
        "environment": "本機 Codex host",
        "operation": "啟動旗標在終端機傳入；config.toml 在檔案中設定。",
        "transfer": "本機 App／IDE 的 Codex agent 使用相同設定體系；CLI 旗標不是 App 選單，也不是網頁 Work 設定。"
      }
    },
    {
      "id": "23",
      "slug": "23-context-recovery",
      "title": "長任務、脈絡壓縮與失敗恢復",
      "description": "建立檢查點、可核對的交接與恢復策略，延續跨會話工作。",
      "track": "scale",
      "minutes": 120,
      "phase": 5,
      "surface": {
        "entry": "Codex App／CLI・長任務恢復",
        "environment": "本機 session 與 repo",
        "operation": "App 從對話清單接續；CLI 用 codex resume／fork；檢查點另存檔。",
        "transfer": "/compact 是對話脈絡整理；Git、交接文件與 session 是不同資產，不能假設網頁能匯入 CLI session。"
      }
    },
    {
      "id": "24",
      "slug": "24-skill-engineering",
      "title": "可重用 Skill 的設計、測試與維護",
      "description": "設計觸發範圍、確定性腳本、參考資料與版本驗收。",
      "track": "automation",
      "minutes": 120,
      "phase": 5,
      "surface": {
        "entry": "本機 Codex・Skill 工程",
        "environment": "本機 .agents/skills 與測試 fixtures",
        "operation": "在 repo 編寫 SKILL.md；Codex CLI 以 $skill-name 明確選用。",
        "transfer": "ChatGPT 支援的 Skill 使用 @ 選取或 plugin 封裝；網頁不會自動掃描你的本機 .agents/skills。"
      }
    },
    {
      "id": "25",
      "slug": "25-workflow-evaluation",
      "title": "工作流評估與50小時畢業實作",
      "description": "比較提示與工作流，核對證據，交付具恢復能力的完整流程。",
      "track": "scale",
      "minutes": 120,
      "phase": 5,
      "surface": {
        "entry": "Codex App／CLI・工作流評估",
        "environment": "本機離線基線與可重現任務",
        "operation": "用 shell 跑驗收器；記錄所用入口、模型、設定、工具與成本來源。",
        "transfer": "比較 App／CLI／Work 時要記錄環境差異；不能把不同工具造成的結果歸因於提示詞。"
      }
    }
  ]
};

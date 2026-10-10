# 離線郵件 lab

需要 Python 3.10+，不需額外套件。保持 `parse_mail.py` 和 `fixtures/` 相對位置。

```sh
python3 examples/19/parse_mail.py --dry-run
python3 examples/19/parse_mail.py --out /tmp/codex-mail-lab
python3 examples/19/parse_mail.py --out /tmp/codex-mail-lab
```

初次 dry-run 回報 3 封但不寫檔；初次正式執行建立 3 筆 JSON 與 state.json；重跑回報 new=0、skipped=3。帳務範例分類「帳務」、有附件的範例分類「待人工檢查」。所有 send=false，危險附件名稱只列在 metadata，不保存附件。

`pop3_fetch.py` 是閱讀用的可選真實連線範例。直接執行會停止。它只適用允許 USER/PASS 的供應商；Exchange Online POP 應採 OAuth，不能套用這段登入方法。任何真實連線須另行確認帳號設定、權限、資料保存位置及供應商限制。本次教材驗證沒有執行 fetch()，也不寄信、不刪信。

此離線 demo 用內容雜湊模擬 UIDL 去重；真實取信必須使用主機＋帳號＋伺服器 UIDL，不能以訊息編號去重。不要讓多個程序同時寫相同輸出資料夾。

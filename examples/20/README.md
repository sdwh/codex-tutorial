# 資料清理與報告 lab

Python 3.10+，標準函式庫，完全離線。

```sh
python3 examples/20/report.py --dry-run
python3 examples/20/report.py --out /tmp/codex-report-lab
python3 -m json.tool /tmp/codex-report-lab/report.json
```

輸入五列，預期接受 2、相同重複 1、拒絕 2，TWD 總額 `300.30`。A003 金額無效；A004 沒有時區。重複鍵為 source＋order_id，同鍵內容衝突列拒絕，已接受第一筆保留。

輸出 report.json、errors.json、state.json。金額為十進位字串，時間統一 UTC。輸入 SHA-256 記錄在報告和狀態；相同輸入完整重建，重跑不累加。dry-run 不建立目錄，不寫檔。

單檔 replace 不能保證三個檔案形成一個交易；正式消費端須確認狀態來源雜湊與報告相同。此 demo 不支援多程序同時寫同一輸出目錄。

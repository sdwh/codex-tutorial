# 素材清單 v1

CSV 編碼 UTF-8，可有 BOM。必填欄位：file,purpose,source,rights,sha256。

- file：相對於 asset-root 的路徑；拒絕絕對路徑、..、重複值與符號連結。
- purpose：這張圖或文件在交付中的用途。
- source：來源紀錄；只當字串保存，不連線讀取。
- rights：權利紀錄或「synthetic fixture」。非空不代表已取得授權。
- sha256：64 位小寫十六進位，與檔案原始 bytes 的 SHA-256 相同。

一般欄位錯誤報 manifest issue；無法讀 CSV 則退出 2。圖像尺寸、畫面品質、法律資格都不在此 checker 的驗證範圍。

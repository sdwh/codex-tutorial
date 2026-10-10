# FFmpeg 離線練習

下載 lab.sh，在新的練習資料夾執行 `bash lab.sh`。需 Bash、Python 3、ffmpeg、ffprobe、libx264 與 AAC encoder。

腳本只建立本機合成素材，不下載影片。使用 -n 防止覆寫；再次執行請改用新的資料夾。

2026-10-10 以 FFmpeg 8.1 實跑通過：8 秒來源、4 秒剪輯、360×360 方形、音訊存在。另驗證等比例 scale/pad、半音量與 concat 命令。

captions.srt 用於課程字幕變體。燒入字幕需 FFmpeg 建置含 libass；本次環境沒有該依賴，未跑字幕燒入。

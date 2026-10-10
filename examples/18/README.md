# Remotion 片頭原始碼

用官方 `npm init video@latest` 建立 Blank 專案後，將 index.ts 與 Root.tsx 放入 src。

預期 Composition：CodexIntro，1280×720、30fps、150 幀、5 秒，無音訊。

在該專案執行：

```sh
npx remotion still src/index.ts CodexIntro out/frame-30.png --frame=30
npx remotion render src/index.ts CodexIntro out/intro.mp4 --codec=h264
```

先建立 out 資料夾。保持 remotion 與 @remotion/* 版本一致，保留 lockfile。平台、Node 與授權需求見課程官方來源。

2026-10-10：程式與官方 API 查核完成；本次未安裝 Remotion 依賴、下載瀏覽器或實跑渲染。請依課程 lab 完成單幀與最終影片驗收。

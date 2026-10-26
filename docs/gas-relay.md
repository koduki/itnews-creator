# Screenshot Relay v0.10.1 — GAS運用ガイド

## 目的と責任分界

Gemini Tasks が `itnews-screenshot-queue` スプレッドシート（シート名 `queue`）に撮影ジョブを登録し、Google Apps Script が PageSpeed Insights →（設定時）カスタムAPI → Thum.io を使って画像を取得し、Google Drive の `itnews-assets` に保存する。Gemini Tasks は Drive から画像ファイルを回収し、**実画像を開いて内容・出典・権利・品質を確認**してから PPTX に埋め込む。GAS の `captured` は画像バイナリが保存できたという意味で、記事として正しい・ボット画面が映っていない・権利条件を満たすという承認ではない。

## 導入・更新（必要な手動操作）

1. `skills/weekly-it-news-gemini/scripts/screenshot_relay.js` の最新コードを **現在稼働している**スプレッドシートにバインドされた Apps Script のエディタへ反映する。スキルZIPには `.js` として同梱するが、GASエディタでは `Code.gs` などのスクリプトファイルに貼り付けてよい。GitHub の更新だけでは本番GASは更新されない。
2. 既存9列 `asset_id, slide_id, url, status, file_name, drive_file_id, drive_view_url, captured_at, notes` の列名・順序・意味はそのまま維持する。
3. `setupTimeTrigger()` を一度実行し、認可する。1分周期でpending行を処理する。旧版で追加していた `onSheetChange` トリガーはセットアップ中に**このリレーのものだけ**整理し、Apps Script プロジェクト内の無関係なトリガーは削除しない。Sheets APIによる更新にはonChangeが保証されないためポーリングを正とする。
4. オプションの**スクリプトプロパティ**：`ITNEWS_ASSETS_FOLDER_ID`、`ITNEWS_QUEUE_SHEET_NAME`、`PSI_API_KEY`、`SCREENSHOT_API_TEMPLATE`。未設定なら既存のフォルダIDと `queue` を維持。認証情報はソースに記述しない。既存のカスタムAPI設定は維持される。
5. テストはまず小さな公開HTTPS記事URL 1件で `pending` を作り、Drive保存、実画像、Sheetsの`captured`／リンク、Geminiのダウンロードを確認する。

## キュー状態とエラー回復

- `pending` → `processing` → `captured`（成功）／`pending`（一時失敗、バックオフ付き）／`error`（URL不正・最大3回失敗など）。
- スクリプト停止等で8分以上 `processing` が残った場合、次回ポーリングで復旧処理を行う。再試行可能なら `pending` に戻し、一定時間後に再実行。失敗が3回に達したら `error`。
- API失敗後の再試行間隔：1分 → 5分 → 最大15分。PSI 429/503 では10分クールダウンして、同じ処理で次の取得APIへフォールバックする。通常の再試行は一度のトリガー中で連続しない。
- Apps Scriptの実行時間制限への備えとして、1起動につき最大8行・4分以内に新規ジョブを開始する。ただし外部API応答が長いと厳密な4分終了を保証しない。
- `notes`列内の末尾 `\n[ITNEWS_RELAY_META] {...}` に処理試行回数・開始時刻・次回再試行時刻・撮影方式・寸法などを保存。**利用者が手入力した先頭部分は保持する**。再試行時に新しい列の追加は不要。
- 手動で`error`を`pending`に戻すと再試行できる。`captured`を`pending`に戻す場合はDriveの古い画像リンクは新しい撮影成功まで保持される（Geminiはstatusを見て未完了を扱う）。
- 不正URL・秘密情報入りURLは外部サービスへ送らず `error` に記録する。HTTPSの公開ホスト名のみ対象。認証が必要な記事を無理に迂回する仕組みではない。

## 画像保存・検品

- APIが HTTP 200 を返しても**画像とは限らない**。バイト列のPNG/JPEG識別・実際の縦横サイズ・MIME整合・サイズ制限を確認し、HTML・極小画像・壊れたヘッダを受け入れない。JPEGの場合は `.jpg` の拡張子に正規化する。
- 旧画像は**新しい画像がDriveに保存され、Sheetsが新IDへ更新された後にのみ**ゴミ箱へ移す（旧ファイルIDが管理フォルダ内にある場合のみ）。同じファイル名の別ジョブの画像は削除しない。Google Driveで厳密なトランザクションがあるわけではないため、記録書込み失敗では孤立した新画像が残る可能性はあるが、以前の参照を先に削除することはない。
- 保存成功が画像の内容の正しさを意味しない。Cookieモーダル／Cloudflare Bot検証／広告主体／別記事などはGeminiの `view_file` で見て `assets-manifest.json` の品質フラグとレビュー記録に反映する。

## テストの限界

`node --test tests/test_gas_relay.cjs` は Node のモック上で URL検査、429、フォールバック、画像シグネチャ検証、Drive参照の更新、エラー復旧、トリガー設置等を検証する。本番のApps Scriptの認可、外部サービスのレート制限、全Webサイトの撮影品質、Gemini連携を保証するものではない。更新後の1記事PoCで確認する。
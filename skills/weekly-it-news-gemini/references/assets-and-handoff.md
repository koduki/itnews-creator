# 素材収集とPowerPointへの受け渡し

Gemini Tasksはプロットの指定URLおよび添付資料に基づいて、報道写真・ニュース記事の画面・公式発表・技術図を収集する。画像ファイルが得られないとき、Webを開けたことだけで取得済みにしない。

## 1. 添付レポート（DOCX / PDF）からの図解・リンク即時抽出

ユーザーが調査レポート（`.docx` 等）を添付した場合、最初の調査ターンで以下を実行する：
- DOCX（ZIP構造）内の `word/media/*` からすべての画像（PNG/JPEG）を抽出し、解像度・内容を確認してプロットの `asset_ids` に割り当てる。
- `word/_rels/document.xml.rels` からすべてのハイパーリンクURLを抽出し、一次ソースURLとしてプロットおよびスライドの出典欄に引き継ぐ。

## 2. Google Drive ＋ GAS スクリーンショット自動中継フロー

Gemini TasksのサンドボックスVMは外部Webページの直接ブラウザ撮影が制限されているため、以下のGoogle Drive中継フローを使用する：

1. **URLキューへの先行登録（プロット作成・改訂時）**:
   - `SOURCE_IMAGE` 等で使うWeb記事URLが決まった段階で、スプレッドシート `itnews-screenshot-queue`（Spreadsheet ID: `1G3qzrzC4P_y-Kh8YeiJGKiBBC_-gaEDgXbbBD81hZK8`）の `queue` シートに、`sheets_agent:call` で撮影対象行（`asset_id`, `slide_id`, `url`, `status: pending`, `file_name: <asset_id>.png`, `notes`）を登録する。
2. **GASによる自動キャプチャとDrive保存**:
   - スプレッドシートにバインドされたGAS（`scripts/screenshot_relay.js`）が1分周期トリガー（または手動メニュー「📸 IT News スクショ取得 ＞ ▶ pending行を今すぐ一括撮影」）で `status == 'pending'` の行を検知。
   - **第1経路**: Google PageSpeed Insights API (v5, `strategy=desktop`) の `full-page-screenshot` / `final-screenshot` からBase64 PNGを抽出。
   - **第2経路**: スクリプトプロパティ `SCREENSHOT_API_TEMPLATE`（ScreenshotOne / Urlbox等）が設定されていれば使用。
   - **第3経路**: 公開スクリーンショット中継（`image.thum.io` 幅1280・高さ853の設定）へフォールバック。PNG/JPEG実バイト・MIME・画像縦横の検証後、実際の形式に合う拡張子で保存。
   - Google Driveフォルダ `itnews-assets`（Folder ID: `1gha0VJobU6ffTlMm5_ypVOck70cIH4pD`）に `<asset_id>.png`（JPEG応答は `.jpg`）を保存し、シートの `status` を `captured`、`drive_file_id` を記録する。新ファイル保存・シート更新前に前の画像を削除しない。
   - 429/503でPageSpeedを10分クールダウンして他APIへ切替。処理エラーは最大3回、1分・5分などのバックオフ後に再試行。8分以上残った `processing` は復旧する。再試行情報は既存 `notes` 列の末尾に記録し9列キューは維持。Sheets API経由の編集イベントはトリガー発火を保証しないため、GASは1分ポーリングを使用する。
3. **Gemini Tasksによる回収とPPTX埋め込み**:
   - **Sheetsのstatusが`captured`であることを先に確認し、再取得中の古いDrive参照を新しい素材と誤認しない。** PPTX生成前に `drive:search_files`（`parentId = '1gha0VJobU6ffTlMm5_ypVOck70cIH4pD'`）を実行し、保存されたPNGがあれば `drive:download_file_content` でローカルVMにダウンロードしてPPTXの `SOURCE_IMAGE` / `TWO_SOURCES` フレームへアスペクト比を維持して実体埋め込みする。
   - まだGASが未実行で画像が存在しない場合は、勝手にAI生成画像で埋めたりせず、テンプレートのグレープレースホルダー枠に対象記事名・URL・`asset_id` を明記し、`assets-manifest.json` に `status: "unavailable"` として記録する。

## 3. マニフェスト管理と最終納品

各素材を `asset_id`、`slide_ids`、`source_url`、`kind`、`publisher`、`creator`、`captured_at`、`file`、`dimensions`、`status`、`usage_status`、`license_terms`、`purpose` で `assets-manifest.json` に管理する。`status` は `pending` / `captured` / `extracted` / `uploaded` / `embedded` / `unavailable` 等。権利条件とファイル実体を確認する。

最終納品は以下の4点：
- `weekly-it-news-YYYY-MM-DD-base.pptx`（ローカル提示＋Google Drive保存）
- ユーザー承認済み `plot.json` と `plot.md`（`status: "approved"`）
- `assets-manifest.json` と実際に保存・埋め込んだ画像
- 実施済みQA（LibreOffice＋`pypdfium2` による全ページレンダリング目視検査結果）、未取得画像、確認できなかった項目

## 4. 品質ゲート — 実ピクセル確認と承認済み素材

画像取得成功（GASの `captured`）と発表資料への使用可否は別。**各PNGを `view_file` で表示し、記事見出しや必要な内容が遮蔽されていないかを必ず確認**する。特に2026-10-26の20枚版ではNVIDIAのCookie画面とAxiosのCloudflare認証画面が混入した。後者は記事の根拠として使えない。

`assets-manifest.json` の素材ごとに次を記録する：
- `review_status`: 最初は `pending`、内容確認後だけ `approved`。
- `review_notes`: 本文/写真が確認できるか、広告・Cookie・Bot検証が隠していないかの具体的な記録。
- `quality_flags`: 問題があれば `bot_challenge`, `cookie_overlay`, `ad_dominant`, `wrong_article`, `unreadable`, `needs_crop`, `unrelated` 等。問題があれば画像は差し替え・再取得し、承認しない。
- `sha256`: 実際に保存した画像ファイルのハッシュ（任意だが推奨）。再取得で画像が変わったら再検品する。

厳格モード `--assets-manifest assets-manifest.json --strict-assets --qa-report qa/preflight.json` は未承認・欠落・画面不良と明記された画像を差し止め、`story_id` の分断や表の列不一致も検出する。**内容そのものの自動画像認識ではなく、検品記録に対する検証**であるため、警告なしでもLibreOffice/PowerPointで全ページの視覚QAを実施する。例：`templates/assets-manifest.example.json`。
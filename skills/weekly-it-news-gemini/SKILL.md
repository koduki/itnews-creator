---
name: weekly-it-news-gemini
description: Gemini Tasksで技術ニュースを調査・対話し、承認済みページプロットに従って実画像・技術図を収集し固定テンプレートでPPTXを作るスキル。
---
# Weekly IT News — Gemini Tasks 制作担当

目的：技術ニュースの編集判断はユーザーとの対話で決め、ページ単位のプロットを承認してからPPTXを生成する。汎用コンサル資料ではなく元来のWeekly IT News番組形式。Copilot ChatでPPTXを作る従来経路は標準フローから外す。

## 作業順
1. **一次情報・添付資料の調査と抽出**
   - 公式発表・技術文書・報道を調査し、検証済み事実、ベンダー主張、発表者考察を分ける。
   - **添付DOCX等の自動解体**：ユーザーが調査レポート（`.docx` 等）を添付している場合は、初回ターンでZIP展開し、`word/media/*`（実画像・構成図）と `word/_rels/document.xml.rels`（埋め込みハイパーリンクURL）をすべて抽出して素材候補リストに登録する。
2. **トピック選定・見出し・構成の対話**
   - ニュース候補と「何が面白いか」「どの順番・見出しで話すか」「どの画像を見せるか」をユーザーと対話。AIだけで均等なニュースダイジェストを決めない。
   - **番組らしいキャッチーな見出しと日本向け用語への翻訳**：
     - 見出しは硬い報告書調ではなく、視聴者の興味を惹く番組タイトル調にする（例：`Meta Museが日本で解禁！ 常駐型でAIエージェントの戦いは別のステージへ`、`インターネットが壊れた日。首相も宣言したPHP2Shellとは？`、`勝手に証券を売買まで？ GMO/お名前.comデスクトップクラウド侵害`）。
     - 日本で馴染みの薄い直訳カタカナ語（例：「アンビエントAIエージェント」）は避け、直感的に伝わる日本語表現（例：「**常駐型AIエージェント**」）に統一する。
3. **ページごとのプロット作成とスクリーンショット事前キュー登録**
   - ページごとのプロットをMarkdown（`plot.md`）とJSON（`plot.json`）で提示。`slide_id`、`story_id`、`layout_id`、ページの目的、掲載文、発表者ノート、必要な `asset_ids` と出典URLを設定。話題を一巡してから再訪しない（最後の横断比較・結びを除く）。
   - **1ページ1スクショ原則**：報道や反響のスクリーンショットを見せる際は、1スライドに複数詰め込まず「**1ページ1スクショ**（`SOURCE_IMAGE`）」を基本とし、必要なら連続スライドに分割する。
   - **GASスクリーンショット中継キューへの早期登録**：Gemini TasksのVMサンドボックスからは外部Webページの直接画像保存ができないため、プロット作成・改訂段階で必要となるWeb記事スクリーンショットのURLをGoogle Sheet（`itnews-screenshot-queue`）へ先行登録し、Google Driveフォルダ（`itnews-assets`）に既存キャプチャがないか確認する。
4. **プロット承認（必須ゲート）**
   - **プロット承認までPPTXを作らない。** 承認したらスライド枚数、ページ順、話す内容を固定。重要な新情報を発見したら差分と再承認を求める。
5. **実画像・記事スクリーンショットの回収と検証**
   - 承認プロットに従い、添付DOCXからの抽出画像およびGoogle Drive（`itnews-assets`）経由で撮影されたWeb記事スクリーンショット（PNG/JPEG）をVMへ回収する。
   - **画面を見たこととPNG/JPEGファイルを保存できたことは別。** ファイルを再確認し、出典URL、取得日時、著作者、利用条件、`asset_id` を `assets-manifest.json` に残す。取得できなければ未取得と報告。生成イメージを証拠にしない。
6. **ネイティブ図形による技術図解・比較表の設計**
   - 解説の模式図（`TECH_DIAGRAM`）・比較表（`COMPARE`）は編集可能なPowerPointネイティブ図形・テーブルで作成し、数値・矢印の根拠を検証。
   - 添付資料に高品質な構成図画像がある場合でも、1枚の画像に情報を詰め込みすぎず、必要に応じて「システム構成と侵害箇所の図解ページ」と「波及経路（なぜ他社・証券会社まで影響したか）の図解ページ」に分割する。
7. **固定テンプレートの取得と検証**
   - Gitの3月版の表紙・アバターを使い、2ページ目は現行の簡潔な目次、本文は固定レイアウト `COVER` / `AGENDA` / `NEWS` / `SOURCE_IMAGE` / `TECH_DIAGRAM` / `COMPARE` / `TWO_SOURCES`。
   - PowerPointテンプレートはスキルZIPに入れず、**実機で動いたGoogle Drive／ユーザー添付の経路を優先**して実体バイナリを取得し、SHA-256と内部構造を検証する。GitHubは正本・配布場所でありGemini VMの直接取得先ではない。
8. **PPTX生成（1プロット＝1スライド）**
   - `scripts/build_pptx.py` を使用し、承認済みの `plot.json` とDriveから取得したテンプレートPPTX、ローカル素材画像から決定論的に作成する。完成版では下記の**品質ゲート付きコマンド**を使う。
   - 指定のテンプレートを基に、本物の編集可能なPPTXを生成。プロット1ページ＝PPTX1スライド。画像はPPTX中に実体として埋め込み、WordやPDFに代替しない。
9. **視覚QAと最終納品**
   - PPTXをLibreOffice＋`pypdfium2`等で全ページ画像化して開き直し、ページ順、出典、実画像、スライド枚数、元アバター、文字はみ出し・重なり、編集可能性を検査。できなかった検査は未実施と記載。

## 固定テンプレートの取得（PPTX生成に先立つ必須チェック）

- 正本: https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx
- リポジトリ参照: https://github.com/koduki/itnews-creator/blob/main/assets/templates/weekly-it-news-design-template.pptx
- 現行リビジョンのSHA-256: `f343a4fee2d802ce7ce36290d951a4a09526a451ccb16e9d41d0cb62f5ddee73`（将来更新時は `assets/templates/template-manifest.json` の値に従う）

**スキル内Pythonによるrequests/curlで取得できることは前提にしない。**
1. まずGoogle Drive内に同期済みの `weekly-it-news-design-template.pptx` があれば `drive:search_files` → `drive:download_file_content` でVMへダウンロードし、SHA-256を検証する。
2. 取得できない場合は①Google Driveに同期済みの同ファイルを「Driveから追加」、②ユーザーに1回だけファイルアップロードを依頼し、次回以降のためにGoogle Driveへも保存しておく。
3. ファイルの実バイトを取得できたときだけローカルでPPTX（ZIP）として開き、7つの見本スライド、スライド1の元アバター（`ppt/media/image1.jpeg`）と日付枠、スライド2の目次を確認する。**別デザインのテンプレートを勝手に作らず、取得不能を明示する。**

## 品質ゲート（v0.9.4）

**ユーザー向け完成稿には `--strict-assets --assets-manifest assets-manifest.json --qa-report qa/preflight.json` を必ず付ける。** ベース稿で不足画像を見えるプレースホルダーとして残したいときだけ `--strict-assets` なしで実行し、`qa/preflight.json` の未達と手作業を明記する。欠落のあるベース稿を完成版と呼ばない。

1. GAS の `captured` は「PNGが保存できた」状態であり、内容に合う証拠が撮れたという意味ではない。Driveから回収後、Geminiの `view_file` 等で画像の**実ピクセルを全件確認**する。Cloudflare画面、Cookie同意モーダル、広告が主役、別記事、読めない画像は `quality_flags` に `bot_challenge` / `cookie_overlay` / `ad_dominant` / `wrong_article` / `unreadable` / `needs_crop` を記録して再取得する。
2. 問題のない実画像のみ、`assets-manifest.json` の各素材に `review_status: "approved"`、具体的な `review_notes`、`source_url`（DOCX由来なら `source_docx`）、任意の `sha256` を記録する。GAS実行だけで `review_status` を自動承認してはいけない。
3. `scripts/build_pptx.py` はプロットの `story_id` 連続性・スライドID重複・比較表の列数を確認する。Strictでは画像欠落・出典食い違い・レビュー未了・`quality_flags` のある素材を**生成前に拒否**。失敗時も `qa/preflight.json` に理由を残す。
4. レイアウトが混み合っている比較表・技術図・解像度不足の画像は警告される。**警告がゼロでも視覚QAが終わったわけではない**。LibreOfficeで全ページを画像化し、はみ出し・重なり・記事の正しさを人が最終確認する。

厳格生成例：

```bash
python scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads/ \
  --assets-manifest assets-manifest.json --strict-assets \
  --qa-report qa/preflight.json --render-qa-dir qa/ \
  --out weekly-it-news-base.pptx
```

`assets-manifest.json` はリポジトリの `templates/assets-manifest.example.json` を参考にする（最初から approved にしない）。

## 最終成果物
- `weekly-it-news-YYYY-MM-DD-base.pptx`（Google Driveへのアップロード＋Canvas/ファイル提示）
- ユーザー承認済み `plot.json` と `plot.md`
- `assets-manifest.json` と実際に保存・埋め込みした画像
- 実施済みQA、未取得画像、確認できなかった項目

詳細：`references/plot-and-layout.md`、`references/assets-and-handoff.md`、GAS中継スクリプト `scripts/screenshot_relay.js`、PPTX生成器 `scripts/build_pptx.py`。
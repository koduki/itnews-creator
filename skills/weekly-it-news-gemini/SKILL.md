---
name: weekly-it-news-gemini
description: Gemini TasksでWeekly IT Newsの企画・証拠収集・テンプレート準拠の編集可能PPTX生成を行う。
---

# Weekly IT News — Gemini Tasks 制作

**テンプレートPPTXを唯一の視覚仕様とする。** 固定した配色・座標・フォント・装飾をスキルの文章から再適用しない。8枚の原本に対して`scripts/build_pptx.py`で文章・実画像・図解を流し込み、最後に実際のスライドを検品する。

## 実行順序

1. **調査と対話**：公式発表・技術資料・ニュース・添付DOCXを確認。事実、ベンダー主張、推測、発表者の解釈を区別する。DOCXの`word/media/*`と`document.xml.rels`から画像・出典も抽出する。毎回テーマを選び直し、以前の号のニュースや説明文を複写しない。表現は硬い報告書調でなく興味を引くニュース番組の見出し。
2. **承認型ページプロット**：`plot.md`/`plot.json`にページごとの目的・`story_id`・`layout_id`・見出し・本文・発表者ノート・素材ID・出典を記載。ニュース単位で連続させる。COVER → AGENDA → ニュース別のNEWS_TITLE（章扉）→ 内容ページ。章扉が自動追加される場合を含む出力枚数を表示し、**明示的な承認までPPTXを生成しない**。
3. **写真・スクショ収集**：`itnews-screenshot-queue`にURLを登録し、Google Apps Script (`scripts/screenshot_relay.js`) → Driveの`itnews-assets`へ中継。Gemini Tasksのブラウザ閲覧から直接PNG保存は前提にしない。実画像は1ページ1スクショを原則とし、個別の根拠を明確にする。
4. **証拠の検品**：Driveから画像ファイルを回収して`view_file`等で開き、Cloudflare/Cookie同意/広告/別記事/読み取れない画面を差し戻す。正常な画像だけ`assets-manifest.json`に`review_status: approved`、出典URL、具体的な`review_notes`、利用条件を記録する。`captured`は承認状態ではない。
5. **テンプレート取得**：正本は [GitHubテンプレート](https://github.com/koduki/itnews-creator/blob/main/assets/templates/weekly-it-news-design-template.pptx) 。Gemini VMでGitHub rawのバイナリは取得できないため、まずGoogle Driveから `weekly-it-news-design-template.pptx` を `drive:search_files` → `drive:download_file_content` で取得し、または添付`user_uploaded_files/`を使う。SHA-256 `f871047b53f839a47bb77732770f7648a4e904bc64d696e04e85d2e639778f05` と8スライド構造を検査。**取得できない場合は作成を止め、別デザインを捏造しない。** 公開raw参照： https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx
6. **生成**：編集可能なPPTXを`scripts/build_pptx.py`で生成。元テンプレートの既存段落・図形の配色、書体、位置を引き継ぎ、データ量に応じた最小限のフィット調整のみ行う。NEWS_TITLEは章扉の固有デザインを保持。NEWS/比較表/技術図の色を手動で塗り直さない。
7. **検査・引き継ぎ**：`--strict-assets --assets-manifest assets-manifest.json --qa-report qa/preflight.json --render-qa-dir qa`で生成。LibreOffice等で全ページPNGを確認し、未検品画像・出典・文字はみ出し・**テンプレートとの配色差**を確認。`base.pptx`、承認済みプロット、素材記録、QAを渡す。最終編集はCopilot in PowerPointのClaudeで実施する。

## 標準コマンド

```bash
python scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads \
  --assets-manifest assets-manifest.json --strict-assets \
  --qa-report qa/preflight.json --render-qa-dir qa \
  --out weekly-it-news-base.pptx
```

`--strict-assets`なしで作成したプレースホルダー付きデッキは途中稿。完成稿とは呼ばない。新しいニュースごとの構成方法や出典検証は`references/plot-and-layout.md`、`references/assets-and-handoff.md`を参照。

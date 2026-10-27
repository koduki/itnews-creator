---
name: weekly-it-news-gemini
description: Gemini TasksでWeekly IT Newsを調査・構成し、承認済みプロットと検証済みPPTXテンプレートから編集可能な資料を生成する。
---

# Weekly IT News — Gemini Tasks

**役割:** ニュースの調査、ユーザーとの編集判断、実素材の収集、承認済みプロットからのPPTX生成。PowerPointでの最終調整は `itnews-powerpoint-polish` の担当。

## デザインと実行の最上位契約

- **デザインの唯一の正本は、実バイトとSHA-256を検証した8枚のPPTXテンプレート。** 表紙だけ元の赤黒を使う。AGENDA以降の青基調、NEWS_TITLE、装飾、配色、図表、文字組、位置はテンプレートから継承する。スキルの文章や過去の資料、画像生成、任意の配色・図形生成で上書きしない。
- **PPTXはこのスキルZIPに同梱された `scripts/build_pptx.py` でのみ生成する。** 古いローカルスクリプト、他の自作ジェネレータ、LLMによるPPTXの作り直しへ切り替えない。ZIP内の `SKILL.md` だけを差し替えてもスクリプトは更新されないため、必ず同じ配布版の一式を使用する。
- テンプレートを取得できない、同梱スクリプトがない、ハッシュが異なる、生成後のテンプレート書式検査が失敗した場合は**完成稿を出さずに停止**。色を目視や指示文で後から直して合格扱いにしない。

## 作業フロー

1. **調査と抽出。** 公式文書・報道と添付レポートを読み、事実・ベンダーの主張・発表者の考察を区別。添付DOCXから `word/media/*` と `word/_rels/document.xml.rels` の画像・出典URLを抽出する。
2. **ユーザーと番組構成を決める。** 技術的な面白さ、日本語で伝わる見出し、ニュース順、見せたい実資料を対話し、`plot.md` と `plot.json` を提示する。ページごとに `slide_id`、`story_id`、`layout_id`、`title`、`on_slide`、`speaker_notes`、`asset_ids`、`source_urls` を設定。話題の再登場は原則避ける。**承認前はPPTXを生成しない。**
3. **素材を先行して集める。** 報道画面は**1ページ1スクショ**を原則とする。記事URLを `itnews-screenshot-queue` に早期登録し、`scripts/screenshot_relay.js`（GAS）経由でDriveの `itnews-assets` からPNG/JPEGを回収。DOCX由来の画像も含め実ピクセルで検品する。取得と検品は別状態であり、Cloudflare・Cookie遮蔽・別記事などは承認しない。運用詳細は `references/assets-and-handoff.md`。
4. **テンプレートを取得・検証。** 実行環境ではGoogle Driveまたはユーザー添付のPPTX実体を優先する（GitHub rawの直接取得に依存しない）。`assets/templates/template-manifest.json` のSHA-256と8レイアウトを検証する。取得できない場合はユーザーに同じ正本の添付を依頼し、仮デザインのPPTXは作らない。
5. **承認済みプロットから生成。** `COVER`、`AGENDA`、各ニュースの `NEWS_TITLE`、本文各レイアウトを使用。既にプロットにある `NEWS_TITLE` は重複生成しない。実画像は埋め込み、技術図と表は編集可能なネイティブ要素を継承・更新する。スキル内の生成器の**色・スタイル監査がPASS**であることを必須とする。
6. **QAと納品。** Strictモードで画像欠落・未承認・出典不一致を拒否し、全ページをPDF/PNGにレンダリングして重なり・読みやすさ・図表・出典を確認。実PPTXの保存とQAが完了したときだけ完成版と呼ぶ。

## テンプレートの識別

- 正本: https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx
- GitHub: https://github.com/koduki/itnews-creator/blob/main/assets/templates/weekly-it-news-design-template.pptx
- 現行SHA-256: `f871047b53f839a47bb77732770f7648a4e904bc64d696e04e85d2e639778f05`（更新時はマニフェストと生成器も同時に更新）。
- 順番: `COVER` / `AGENDA` / `NEWS_TITLE` / `NEWS` / `SOURCE_IMAGE` / `TECH_DIAGRAM` / `COMPARE` / `TWO_SOURCES`。
- デザイン・プロット上の責務分界は `references/plot-and-layout.md`。色コード、フォント、座標、図形装飾をSKILLで再定義しない。

## 必須実行コマンド

```bash
# 必ず今回インストールしたスキルZIP内で実行。旧版の同名スクリプトは使わない。
python scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads/ \
  --assets-manifest assets-manifest.json --strict-assets \
  --qa-report qa/preflight.json --render-qa-dir qa/ \
  --out weekly-it-news-base.pptx
```

`qa/preflight.json` の `template_sha256`、`generator_sha256`、`template_style_audit` を確認し、失敗・欠落時は受け渡さない。画像の実内容は別途目視する。ベース稿に未取得の画像をプレースホルダーとして残すときだけ `--strict-assets` を外し、**未完成**として報告する。

## 引き継ぎ

完成PPTXと承認済み `plot.json`/`plot.md`、`assets-manifest.json`、`qa/preflight.json`、埋め込んだ素材とQA結果を納品する。素材の検品基準とDrive/GAS運用は `references/assets-and-handoff.md`、レイアウトの意味は `references/plot-and-layout.md` を参照。

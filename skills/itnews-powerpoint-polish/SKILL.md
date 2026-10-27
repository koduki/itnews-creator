---
name: itnews-powerpoint-polish
description: Gemini Tasks製Weekly IT Newsの既存PPTXを、Copilot in PowerPointのClaudeでテンプレート書式を維持して仕上げる。
---

# Weekly IT News — PowerPoint仕上げ

**Gemini Tasks製のexisting .pptxを開いてから編集する。** 調査、プロット承認、素材収集、PPTXの再生成は行わない。利用可能なClaudeモデル（可能ならClaude 5.5）を選び、実際に使ったモデル名を記録する。

## 編集禁止の範囲

- 承認済みニュースの順序・事実・考察・出典・実画像・発表者ノートを勝手に変更しない。追加調査や素材不良はGeminiへ差し戻す。
- **色・線・背景・書体・図表の外観は既存PPTXに埋め込まれたテンプレートが正本。** 表紙とAGENDA以降では元からデザインが異なる。本文を表紙の赤色に統一したり、汎用テーマを適用し直したりしない。
- `NEWS_TITLE` は各ニュースの章扉として保持。生成器の自動追加を含むため `plot.json` の入力枚数と実際のPPTX枚数が違うだけでは削除しない。

## 手順

1. 既存PPTXをコピーして開き、必要に応じ `plot.json`、`assets-manifest.json`、`qa/preflight.json` を参照する。`template_style_audit` がPASSでない、または欠落している場合は**Geminiに差し戻す**。古い資料を手直しして正本にしない。
2. 全ページを表示し、見出し・文字のはみ出し、図の意味、表の数字・単位、画像のクロップと出典を点検する。
3. 元の要素を使い、文字サイズや余白を必要な範囲で局所調整する。テーマ、色、図形セットを再生成しない。技術図・比較表は編集可能性を維持する。
4. 修正ページを再確認し、`final.pptx`、変更点、未検証項目、モデル名を報告する。素材や配色の問題が未解決ならFINALと呼ばない。

検査基準は `references/review-rubric.md`、編集内容は `references/visual-repair.md`、引き継ぎの責任分界は `references/gemini-claude-handoff.md`。

## 実行指示例

Geminiで生成したbase.pptxを編集してください。色とレイアウトは既存PPTXの各ページから継承し、再配色しないでください。NEWS_TITLE、ニュース順、出典、実画像と考察を保持して、可読性・図表・写真・ノートだけを仕上げ、変更点と実際に使用したモデルを報告してください。

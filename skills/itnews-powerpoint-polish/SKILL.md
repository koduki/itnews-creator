---
name: itnews-powerpoint-polish
description: Gemini Tasksで生成されたWeekly IT Newsの既存PowerPointを、Copilot in PowerPointでClaudeモデルを用いて構成を守りながら仕上げる。
---

# Weekly IT News — PowerPoint最終調整

**Gemini Tasks製のexisting .pptxを開いてから編集する。** ニュース調査、企画、スクショ収集、最初のPPTX生成はGemini側が担当。Do not restart news selection.

## モデル選択
実際に利用可能なClaudeモデル（可能であればClaude 5.5）を編集モードで選択する。モデルが使えない場合は使用したことにせず、実際に表示されたモデルを記録する。

## 保持するもの
- 承認済み`plot.json`のニュース構成、ニュース順序、事実・考察、出典、実画像。改稿が必要ならGeminiへ差し戻す。
- 元表紙（赤黒タイトル、青い日付枠、アバター）、2枚目の目次、各ニュース前の`NEWS_TITLE`（青い`NEWS NN`、濃紺タイトル、淡青番号）。
- 本文8レイアウトの`NEWS`／`SOURCE_IMAGE`／`TECH_DIAGRAM`／`COMPARE`／`TWO_SOURCES`と編集可能な図形・表。
- 章扉はGemini生成器によって自動追加される場合がある。`plot.json`のslides要素数と実PPTXの枚数が違うだけでは削除しない。

## 編集工程
1. Gemini生成済みPPTXをコピーし、必要なら`plot.json`／`assets-manifest.json`／`qa/preflight.json`を参照。
2. 全ページで文字の衝突・はみ出し、表紙の日付、NEWS番号、画像のクロップ、図の矢印、表の単位と可読性を確認。
3. ニュースの順番・技術的主張・出典と写真を変更せず、余白・文字・編集可能な図表・発表者ノートを局所的に仕上げる。
4. Cloudflare／Cookieモーダルなどの不良画像が残ればGeminiへ差し戻す。見かけだけ隠すことはしない。
5. 編集後の全ページを再確認し、`final.pptx`と変更箇所・未完了項目・使用モデルを報告。未完了ならFINALと呼ばない。

## 参照
- references/gemini-claude-handoff.md：Geminiとの引き継ぎ
- references/review-rubric.md：優先修正と合格判定
- references/visual-repair.md：ネイティブ図表・画像・文字組
- templates/review-report.md：成果報告書

## 依頼例
Geminiで生成したbase.pptxを開いています。章扉NEWS_TITLE、ニュース順序、元の写真と出典、発表者の考察を変えずに、文字・余白・画像・技術図と比較表を最終調整してください。確認できなかった項目と実際に選んだモデル名も報告してください。

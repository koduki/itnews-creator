---
name: itnews-powerpoint-polish
description: Gemini Tasks製の承認済みニュースPPTXを、Copilot in PowerPointのClaude 5.5で内容と順番を変えずにレイアウト・図形・表・ノートを磨く。
---

# Weekly IT News — PowerPoint / Claude最終調整

## 主担当
**既に開いているGemini Tasks製のexisting .pptxを編集する。** 新規のニュースキュレーションやページプロット、画像/スクリーンショットの取材はGemini Tasks側が済ませる。**Do not restart news selection.** 旧版のCopilot Chat製BASE DRAFTをPowerPointで完成させる工程はレガシー。今回の標準はGemini Tasksの編集可能なPPTXを仕上げること。

## モデル選択
PowerPointのCopilot編集モードでモデルスイッチャーを開き、使えるClaude 5.5 (Sonnet/Opusなど) を選択する。特定モデルが表示されるかはテナント、管理者のAnthropic有効化、サブスクリプションとセッションで異なる。**実際に選べない場合はClaude 5.5を使ったと断言しない。** 選択モデル名をQAに残す。

## 制作物の不変条件
- Gemini Tasksで承認されたplot.jsonの **スライド枚数・順番・story_id・layout_id・記事画像と出典・技術上の主張・発表者の考察** を変えない。どうしても修正が必要なら変更提案を出し、承認前の編集をしない。
- 2026-03-15版表紙の赤黒Weekly IT News！、青い日付欄、右上のアバターを保持。2ページ目の簡潔な「今週のトピック」を維持。2026-01-25/2026-04-12の編集思想「ニュース説明 → 実資料 → 技術背景と考察 → 次のニュース」を守る。
- SOURCE_IMAGE・TWO_SOURCES等の実素材を生成イメージで置き換えない。既存の画像を良い位置で見せることが主担当。ソース画像が足りない場合はGemini Tasks側への差し戻しとして報告。
- 自作説明図・表の数値、矢印の意味、比較条件を変えない。Native PowerPoint図形/表として編集可能なまま整える。

ニュースを別の話題のあとで再登場させる reopened topic block は原則不合格。Geminiのプロットに差し戻し、Claude側で独断でページ順を変えない。

## 作業工程
1. 既存.pptxをコピーして保存。plot.jsonとassets-manifest.jsonが参照できればページ順・出典・素材状態を照合。
2. 各スライドのはみ出し、読みにくい文字、余白、行間、配置、スクリーンショットの切り抜き、比較表の単位、図形の接続を検査。
3. 元の固定レイアウトCOVER/AGENDA/NEWS/SOURCE_IMAGE/TECH_DIAGRAM/COMPARE/TWO_SOURCESを保った**局所的な修正**を実行。大規模なデザイン変更や新しい企業向けカード構成は禁止。
4. 編集可能な技術図・矢印・表の体裁を整える。真偽を再確認できない主張を勝手に書き換えない。出典URLと利用条件を消さない。
5. 仕上げ前後のページ数、順番、写真、出典、図表、発表者ノートを検査。できなかった確認は未実施と明示。
6. 編集されたfinal.pptxと、改善箇所、残課題、実際に選択したAIモデルを報告。必須画像が欠落する場合は完成と称さない。

## 参照
- references/gemini-claude-handoff.md：新しい素材・プロット受渡契約（最優先）。
- references/handoff-contract.md：旧版Copilot Chat経路の参考。新契約と矛盾したら新契約を優先。
- references/review-rubric.md：客観的な品質基準。
- references/visual-repair.md：レイアウト/図形/出典修正。
- references/topic-repair.md：過去の話題再登場問題の反例。
- templates/review-report.md：報告形式。

## 依頼例
Gemini Tasksで作ったbase.pptxを今開いています。承認済みplot.jsonを守り、ページ・話の順番・記事画像・内容・出典を変更しないでください。全ページの文字、余白、画像、編集可能な技術図と比較表を最終調整してください。変更が必要なところは提案だけに留め、実際に使ったClaudeモデルと未完了項目を報告してください。
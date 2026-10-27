---
name: itnews-powerpoint-polish
description: Gemini Tasksで作られた既存Weekly IT News PPTXをPowerPointのClaudeでテンプレートの意図を保ち仕上げる。
---

# Weekly IT News — PowerPoint最終調整

Gemini生成済みの**existing .pptx**を開き、利用可能なClaudeモデルで仕上げる。調査・キュレーション・PPTX初稿はGeminiが担当し、ここでは再構成しない。使用できたモデル名を記録する。

## 最優先ルール：テンプレートを再設計しない

- **GitHub管理の8枚PPTXテンプレートが唯一の視覚的正本**。既存スライドの色・罫線・フォント・余白はそのままに、読みにくい箇所だけ局所修正する。
- 表紙は原本の専用デザイン。AGENDA、各ニュースのNEWS_TITLE、NEWS、SOURCE_IMAGE、TECH_DIAGRAM、COMPARE、TWO_SOURCESは**原本で決められたそれぞれのスタイル**を維持する。本文が青なのに過去の赤系スタイルへ戻さない。
- NEWS_TITLEの章扉はニュース単位で1枚。青ラベル・濃紺タイトル・淡い番号を保持し、削除・追加・並べ替えをしない。
- 承認済みプロットのニュース順序、引用、画像、技術的な主張、発表者の考察を変更しない。出典画像をAI生成画像で代替しない。ネイティブ表／図をラスタ化しない。

## 仕上げとQA

1. base.pptxをコピーして保存。必要ならplot.json／assets-manifest.json／qa/preflight.jsonを確認。
2. 全ページで表紙の日付枠、文字の衝突、タイトル折り返し、表の可読性、画像の内容・クロップ、出典を点検。
3. テンプレートの色と形を維持して文字配置・行間・図形接続・比較表を最小限修正。内容や素材の変更はGeminiへの差し戻しとする。
4. 修正後全ページを見直し、`final.pptx`と変更箇所・使用モデル・未確認項目を報告。Cookie／Cloudflareが残る場合は完成扱いにしない。

参考：`references/gemini-claude-handoff.md`、`references/review-rubric.md`、`references/visual-repair.md`、`templates/review-report.md`。

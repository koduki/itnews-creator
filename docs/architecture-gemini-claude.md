# Weekly IT News v0.9 アーキテクチャ

基本構成：**Gemini Tasksで対話・取材・プロット承認・実画像収集・固定デザインPPTXを生成し、Copilot in PowerPointのClaude 5.5で最終調整**。

## 役割と成果物
1. Gemini Tasks: ユーザーの興味を軸にニュース調査と議論。ページ単位のplot.md/plot.jsonを作り、ユーザーが構成を承認。
2. Gemini Tasks: 承認された各ページに必要な補足情報と**実際の**スクリーンショットや写真を回収。取得した画像実体と出典、利用条件をassets-manifest.jsonに記録。失敗は未取得扱い。
3. Gemini Tasks: Gitの3月版表紙・アバターを維持し、2ページ目以降の固定レイアウトに流し込んだ編集可能なbase.pptxを生成。プロットと順序・素材・実画像埋め込みを照合。
4. Copilot in PowerPoint: 実際に選択可能なClaude 5.5モデルで既存のPPTXを開き、レイアウト・テキストオーバーフロー・図形・表・ノートを磨き、final.pptxを保存。

## 重要な制約
- Gemini Tasksがブラウザ操作可能でも、スクリーンショットがファイルとして取得できるかは別途実証が必要。
- GeminiスキルのPythonコードは外部ネットワークアクセスを保証しない。
- PowerPointスキルZIPへバイナリのPPTX/PNGを梱包しない。固定テンプレートはGitHubの `assets/templates/weekly-it-news-design-template.pptx` にあり、Tasksから raw URL `https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx` を取得・ファイル検証する。取得できない場合はDrive/手動添付へフォールバックする。
- 3月版の元表紙を厳密に再現し、今の目次形式は維持。本文はCOVER/AGENDA/NEWS/SOURCE_IMAGE/TECH_DIAGRAM/COMPARE/TWO_SOURCESの指定レイアウト。プロットのページ順とニュースの連続性は変更しない。
- PowerPointのClaude 5.5モデル選択はテナント・契約・管理者設定に依存する。実際に選んだモデル名をQA報告に記録する。
- GitHubのレイアウト規定は指示文であり、pixel-perfectな生成を保証するものではない。必要なら将来決定論的なPPTX生成器を追加する。

## 成功基準
承認されたページ数/順序/画像が一致し、編集可能なPPTXが存在し、実資料は出典付き画像として埋め込まれ、PowerPoint側で内容を勝手に変更せず投影品質を改善できたこと。

Gemini公式 https://support.google.com/gemini/answer/17094507?hl=ja
Geminiスキル https://support.google.com/gemini/answer/17094296?hl=ja
PowerPointモデル https://support.microsoft.com/ja-jp/office/choose-your-model-when-editing-with-copilot-in-powerpoint
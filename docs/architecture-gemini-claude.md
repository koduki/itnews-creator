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
## GAS + Google Drive スクリーンショット中継パイプライン（v0.9.2追加）
- Gemini TasksのVMサンドボックスからは外部Webページのスクリーンショット画像を直接ファイル保存できない場合がある。
- これを解決するため、プロット作成・改訂段階で撮影対象URLをGoogleスプレッドシート（`itnews-screenshot-queue`）へ先行登録し、バインドされたGASスクリプト（`skills/weekly-it-news-gemini/scripts/screenshot_relay.js`）がPageSpeed Insights API（v5）またはフォールバックAPI経由で16:9スクリーンショットPNGをGoogle Driveフォルダ（`itnews-assets`）へ保存する。
- Gemini Tasksは `drive:search_files` / `drive:download_file_content` で `itnews-assets` から実PNGを回収し、`base.pptx` の `SOURCE_IMAGE` スライドへ実体埋め込みする。Cloudflare等のBot検証画面が撮影された場合はQAレポートと `assets-manifest.json` に明記し、必要に応じて二次報道URLへ切り替える。

## Gemini Tasksの決定論的PPTX生成器（v0.9.3）

`skills/weekly-it-news-gemini/scripts/build_pptx.py` を正規の制作実装とし、承認済み `plot.json`・Driveから得た実体PPTX・GAS/DOCX由来の実画像を渡す。`python-pptx`/Pillowが必須、LibreOfficeと`pypdfium2`でPDF/PNG QAを任意実行できる。7種類の編集可能なレイアウトをテンプレートから複製し、画像を中身として埋め込む。

実測で判明した元テンプレートの表紙タイトルと日付枠の重なりは、生成時にネイティブテキストを2行に分け年の帯を下げる補正を追加した。元の赤黒配色・青い日付帯・元アバターを保持する。

```bash
python skills/weekly-it-news-gemini/scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads \
  --out weekly-it-news-base.pptx --render-qa-dir qa
```

なお画面検品ではクッキーモーダルやCloudflare検証画面など記事の証拠にならない画像が混ざり得るため、取得成功と記事スクリーンショットの合格を区別する。画像ファイル取得時の実在性・内容検品は制作前工程で行う。動的タイトル文字サイズはヒューリスティックであり、すべての日本語フォント・長さで一行表示を保証するものではない。
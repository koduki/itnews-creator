---
name: weekly-it-news-gemini
description: Gemini Tasksで技術ニュースを調査・対話し、承認済みページプロットに従って実画像・技術図を収集し固定テンプレートでPPTXを作るスキル。
---

# Weekly IT News — Gemini Tasks 制作担当

目的：技術ニュースの編集判断はユーザーとの対話で決め、ページ単位のプロットを承認してからPPTXを生成する。汎用コンサル資料ではなく元来のWeekly IT News番組形式。Copilot ChatでPPTXを作る従来経路は標準フローから外す。

## 作業順
1. 公式発表・技術文書・報道を調査し、検証済み事実、ベンダー主張、発表者考察を分ける。
2. ニュース候補と「何が面白いか」「どの画像を見せるか」をユーザーと対話。AIだけで均等なニュースダイジェストを決めない。
3. ページごとのプロットをMarkdownとJSONで提示。slide_id、story_id、layout_id、ページの目的、掲載文、発表者ノート、必要なasset_idsと出典URLを設定。話題を一巡してから再訪しない。
4. **プロット承認までPPTXを作らない。** 承認したらスライド枚数、ページ順、話す内容を固定。重要な新情報を発見したら差分と再承認を求める。
5. 承認プロットに従いブラウザで公式サイト・ニュース記事を訪問。写真・記事内図版は可能なら実画像を取得、ページの見出し・文脈が必要なら実際の画面を撮影。**画面を見たこととPNG/JPEGファイルを保存できたことは別。** ファイルを再確認し、出典URL、取得日時、著作者、利用条件、asset_idをmanifestに残す。取得できなければ未取得と報告。生成イメージを証拠にしない。
6. 解説の模式図・比較表は編集可能なネイティブ図形を優先し、数値・矢印の根拠を検証。
7. Gitの3月版の表紙・アバターを使い、2ページ目は現行の簡潔な目次、本文は固定レイアウトCOVER/AGENDA/NEWS/SOURCE_IMAGE/TECH_DIAGRAM/COMPARE/TWO_SOURCES。PowerPointテンプレートはスキルZIPに入れず、GitHubの公開URLからGemini Tasks本体に取得させる。利用環境で取得ができないときだけDrive/手動添付に切り替える。
8. 指定のテンプレートを基に、本物の編集可能なPPTXを生成。プロット1ページ＝PPTX1スライド。画像はPPTX中に実体として埋め込み、WordやPDFに代替しない。
9. PPTXを開き直して、ページ順、出典、実画像、スライド枚数、元アバター、はみ出し、編集可能性を検査。できなかった検査は未実施と記載。

## 固定テンプレートの取得（PPTX生成に先立つ必須チェック）

- 正本: https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx
- リポジトリ参照: https://github.com/koduki/itnews-creator/blob/main/assets/templates/weekly-it-news-design-template.pptx
- 現行リビジョンのSHA-256: `f343a4fee2d802ce7ce36290d951a4a09526a451ccb16e9d41d0cb62f5ddee73`（将来更新時は `assets/templates/template-manifest.json` の値に従う）

**スキル内Pythonによるrequests/curlで取得できることは前提にしない。** Gemini Tasks本体でURLをブラウザで開く/ファイルとしてダウンロードする。ファイルの実バイトを取得できたときだけローカルでPPTX（ZIP）として開き、7つの見本スライド、スライド1の元アバターと日付枠、スライド2の目次を確認する。可能ならSHA-256も検証する。画面上でGitHubを閲覧しただけ、URLを記載しただけでは使用可能なテンプレートを取得したとはみなさない。

取得できない場合は①Google Driveに同期済みの同ファイルを「Driveから追加」、②ユーザーに1回だけファイルアップロードを依頼する。**別デザインのテンプレートを勝手に作らず、取得不能を明示する。** GeminiのGitHubリポジトリ取り込みはスナップショットで自動更新されないため、それだけでバイナリPPTXを実際に取得できたと見なさない。

## 最終成果物
- weekly-it-news-YYYY-MM-DD-base.pptx
- ユーザー承認済みplot.jsonとplot.md
- assets-manifest.jsonと実際に保存した画像
- 実施済みQA、未取得画像、確認できなかった項目

画像収集をPowerPointのClaudeへ引き継がない。PowerPoint Claude担当は配置・図形・フォント・ノートの最終調整のみ。Geminiのスキルスクリプトで外部Web通信は保証されないため、ブラウザ操作は実際に利用できるGemini Tasks機能を使う。

詳細：references/plot-and-layout.md、references/assets-and-handoff.md。
# itnews-creator — Weekly IT News v0.9.4

[ライセンス: MIT](LICENSE)

**Gemini Tasksで対話・調査・プロット作成・実画像収集・PPTX制作、Copilot in PowerPointでClaude 5.5を使って最後の仕上げ**を行う構成です。Microsoft 365 Copilot Chatが一から資料を作る従来の経路はレガシーです。

## 新しい制作フロー

| 段階 | 担当 | 出力 |
| --- | --- | --- |
| ニュース選定と対話 | Gemini Tasks | 事実/考察を分けたニュース選定 |
| **ページ単位の編集プロット** | Gemini Tasks + 発表者 | 承認済みplot.md + plot.json |
| 補足取材と画像の回収 | Gemini Tasks | 本物のスクリーンショット/写真、出典、撮影日時、assets-manifest.json |
| 固定テンプレートで生成 | Gemini Tasks | **編集可能なbase.pptx**。ページ順・配置・本物の画像を照合 |
| スライドの最終調整 | Copilot in PowerPoint、**Claude 5.5** | 原稿と写真を変えずに文字、画像、図、表、ノートを改善したfinal.pptx |

詳細な役割分担：[新アーキテクチャ](docs/architecture-gemini-claude.md)

## v0.9.4 実戦フィードバック反映（バックポート内容）

1. **番組らしい見出し・日本向け用語統一と「1ページ1スクショ」原則**
   - 硬い調査報告書調の見出しを避け、視聴者の興味を惹く番組タイトル調に統一。
   - 日本で馴染みの薄い直訳語（例：「アンビエントAIエージェント」）を避け、「**常駐型AIエージェント**」等の直感的な日本語へ変換。
   - 報道・反響のスクリーンショットは1スライドに複数詰め込まず「**1ページ1スクショ**（`SOURCE_IMAGE`）」を基本とする。
2. **深掘り展開の3つの標準アーキタイプ（`references/plot-and-layout.md`）**
   - **型A（新プロダクト・新パラダイム型）**：概要＆個人利用等の特徴 → 人気報道スクショ → 3世代構造比較図（Chat型 vs タスク型 vs 常駐型） → 起源OSS/推進企業のスクショ＆革新と課題 → 商用比較表 → 勝因深掘り。
   - **型B（重大脆弱性・インシデント型）**：事実整理 → 政治・経営トップ発信の意味と「予防的メンテ停止」の壁（AI時代の攻撃速度変化） → 過去事例（Log4Shell等）との凶悪さ類似点＆世間認知度の逆転比較表 → 技術発火図＆社会波及図。
   - **型C（インフラ侵害・サプライチェーン波及＆総括型）**：公式確認事実と攻撃者主張の切り分け → 直接被害スクショ → 政府エスカレーションスクショ → 3層アーキテクチャ侵害図 → 他社（証券会社等）が緊急対応した構成図 → 境界越え図解 → 横断トピック（米銀AI制限等）スクショ → 「当たり前のことを今まで以上に速やかにやる」総括。
3. **初回ターンの添付DOCX自動解体とGASスクリーンショット中継機構（`scripts/screenshot_relay.js`）**
   - 添付された調査レポート（`.docx`）から `word/media/*`（実画像・図解）と `word/_rels/document.xml.rels`（出典URL）を初回ターンで自動抽出。
   - Gemini Tasksサンドボックスの外部ブラウザ画像保存制限を回避するため、Googleスプレッドシート（`itnews-screenshot-queue`）＋Google Apps Script（`scripts/screenshot_relay.js`）＋Google Driveフォルダ（`itnews-assets`）による自動スクリーンショット撮影・回収パイプラインを標準装備（GeminiのZIP MIME検査を通過するよう `.js` 拡張子で同梱）。
4. **固定テンプレート（`weekly-it-news-design-template.pptx`）の決定論的座標・フォント仕様の明文化**
   - 全7レイアウトのShape座標、フォント設定（Meiryo UI）、下端 `6.55"` 上限ルール、スライド複製時のXML/リレーション引き継ぎ手順を `references/plot-and-layout.md` に明記。

## 配布とセットアップ

[GitHub Actions — Build skill packages](https://github.com/koduki/itnews-creator/actions/workflows/package.yml) で成功した最新実行のArtifactsをダウンロードし、外側のZIPだけを展開します。

- **Gemini Tasks用**：itnews-creator-gemini-task-skill-v0.9.4.zip。Geminiアプリの「スキル」へアップロードしてGemini Tasksから呼び出します。
- **PowerPoint用**：itnews-creator-powerpoint-polish-skill-v0.9.4.zip。PowerPointのCopilotで「スキルの管理」から追加します。
- **旧Copilot Chat用**：itnews-creator-copilot-skill-v0.9.4.zip。互換性用であり、新しい標準ワークフローには使いません。
- **ChatGPT用**：itnews-creator-chatgpt-plugin-v0.9.4.zip。Microsoft 365やGeminiには登録しません。

**重要：テンプレートの正本はGitHub、Gemini Tasksへの実ファイル提供はGoogle Driveまたは添付です。** 実機ではVMからGitHubのraw URLのPPTXバイナリを直接ダウンロードできませんでした。毎回の直接取得を標準手順にしません。

- [Gitで管理する7枚テンプレート](assets/templates/weekly-it-news-design-template.pptx) / [ハッシュとバージョン](assets/templates/template-manifest.json)
- **実際の取得順**：①`user_uploaded_files/` 内の添付、② Google Driveの `weekly-it-news-design-template.pptx` を `drive:search_files` → `drive:download_file_content` でVMの `downloads/` に取得
- 取得後SHA-256 `f343a4fee2d802ce7ce36290d951a4a09526a451ccb16e9d41d0cb62f5ddee73` と7枚構成を検証
- [3月版の元表紙](assets/cover/weekly-it-news-cover-20260315.pptx) / [元アバター](assets/cover/avatar-20260315.jpg) を保持

画像はGAS中継のスプレッドシート `itnews-screenshot-queue` → Driveフォルダ `itnews-assets` → `drive:download_file_content` でVMに回収します。スクショのPNGが実在してもCloudflare認証画面やCookie同意が写り込む場合があるため、**画像を開いて内容を検品してから**PPTXに使用します。PowerPoint仕上げスキルZIPへテンプレートのバイナリを同梱する必要はありません。

## Gemini Tasksへの依頼

Geminiのスキル weekly-it-news-gemini を使い、ニュースを調査して技術的な面白さを対話してください。まず各ページの目的・タイトル・出典URL・見せる画像・レイアウトIDを記した編集プロットを提示し、私の承認を得てください。承認後だけ指定URLの実画像を回収し、撮影画像のファイル実体を確認して、Driveまたは添付からテンプレート実体を取得・SHA-256検証してください。GitHubのraw URLからの直接取得は前提にしないでください。取得できたテンプレートに沿う編集可能なPPTXを作ってください。1枚目は3月版の元表紙、2枚目は今のシンプルな目次です。画像取得不能は必ず報告してください。

## PowerPointでのClaude 5.5仕上げ

Gemini製のbase.pptxをPowerPointで開き、**Copilot編集モードのモデルスイッチャーで実際に利用可能なClaudeモデル**を選択します。Claude Sonnet/Opus 5.5など表示されたモデルを選びます。Anthropicの利用可否、契約、地域、テナント設定により異なり、セッションごとに設定が戻る場合があります。

スキル itnews-powerpoint-polish を使い、**既存PPTXのページ数・順番・素材・ニュースの切り口は変えず、レイアウト/画像のクロップ/編集可能な図表/ノートだけ磨く**よう依頼します。画像が足りない場合はGeminiへの差し戻しを明示します。

## 完了基準

- 人が承認したplot.jsonとPPTXがページ単位で一致する。
- 3月版の1ページ目（赤黒タイトル、青い日付、実アバター）を保持し、2ページ目の目次書式を変えない。
- 実際の報道写真やWeb画面を**保存された画像ファイルからPPTXへ埋め込む**。ブラウザで見るだけ、架空画像、URLだけでは不合格。
- 自作図・表は可能な限りネイティブで編集可能。
- 画像・出典の使用条件を守る。事実と分析を区別する。
- Microsoft/Gemini間の実地E2E動作は未検証であり、CI成功をもって製品機能が動いたと断定しない。

旧版の詳細：[2026-03版表紙の説明](skills/weekly-it-news/references/march-cover.md) / [元の編集哲学](docs/design-philosophy.md)。

## ビルド

Python標準ライブラリの scripts/build_packages.py でバージョン付きZIPを4種類生成し、GitHub Actionsで構造テストと再現性を確認します。ZIPの公開と各社のスキル登録は別作業です。

独自ソースはMIT。元のアバター、ユーザー提供PPTX、外部記事の写真や技術図は元の権利者に帰属し、自動的にMITの対象にはなりません。
## Gemini Tasks内の決定論的PPTX生成（v0.9.4）

GASで取得した画像を `downloads/` へ保存し、承認済み `plot.json` を渡して、同梱するPython生成器を実行します。

```bash
python skills/weekly-it-news-gemini/scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads \
  --out weekly-it-news-base.pptx --render-qa-dir qa
```

実体がGitの7枚テンプレートと一致するかSHA-256検証し、ネイティブ図形・比較表・DOCX画像素材・ノートの制作に対応します。画面表示のCookie同意やCloudflare検証が写ったスクショは生成前の素材検品で差し戻します。7枚テンプレートの表紙に存在するタイトル/日付の重なりを補正する処理を含みます。


## v0.9.4：完成稿の品質ゲート

2026-10-26の20枚デッキで、GAS取得成功の画像にCookie同意画面やCloudflare検証画面が混入したため、**「画像ファイルがある」だけでは完成扱いしません**。Geminiが回収した実画像を一枚ずつ表示し、問題がない場合のみ `assets-manifest.json` の `review_status: approved` と `review_notes` に明記してください。問題があれば `quality_flags`（`bot_challenge`, `cookie_overlay`, `ad_dominant`, `wrong_article`, `unreadable`, `needs_crop` 等）を付けて差し戻します。

```bash
python skills/weekly-it-news-gemini/scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads \
  --assets-manifest assets-manifest.json --strict-assets \
  --qa-report qa/preflight.json --render-qa-dir qa \
  --out weekly-it-news-base.pptx
```

品質チェックは、画像の有無・画像ハッシュ・検品状態・承認プロットのニュース連続性・比較表の列数を生成前に検証します。未承認や未取得はエラーとなり、理由をJSONに保存します。**Cloudflare画像等の内容そのものの自動画像認識ではありません。** Gemini/人間による実画像確認と、全ページの投影時目視確認が必要です。ベース稿の未取得素材をプレースホルダーで残したいときだけ `--strict-assets` を省略し、未完了と明記してください。

- [素材マニフェストの雛形](skills/weekly-it-news-gemini/templates/assets-manifest.example.json)（初期状態は `pending`）
- [品質ゲートの回帰テスト](tests/test_gemini_quality_gate.py)
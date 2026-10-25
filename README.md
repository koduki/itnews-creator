# itnews-creator — Weekly IT News v0.9.1

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

## 配布とセットアップ

[GitHub Actions — Build skill packages](https://github.com/koduki/itnews-creator/actions/workflows/package.yml) で成功した最新実行のArtifactsをダウンロードし、外側のZIPだけを展開します。

- **Gemini Tasks用**：itnews-creator-gemini-task-skill-v0.9.1.zip。Geminiアプリの「スキル」へアップロードしてGemini Tasksから呼び出します。
- **PowerPoint用**：itnews-creator-powerpoint-polish-skill-v0.9.1.zip。PowerPointのCopilotで「スキルの管理」から追加します。
- **旧Copilot Chat用**：itnews-creator-copilot-skill-v0.9.1.zip。互換性用であり、新しい標準ワークフローには使いません。
- **ChatGPT用**：itnews-creator-chatgpt-plugin-v0.9.1.zip。Microsoft 365やGeminiには登録しません。

**重要：テンプレートの正本はGitHubです。** Gemini Tasks用スキルは、まず次の公開URLから実際のPPTXファイルを取得・検証するよう指示します。

- [7枚の編集可能なデザインテンプレート](assets/templates/weekly-it-news-design-template.pptx)
- [テンプレートの直接ダウンロード（raw）](https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx)
- [ハッシュと配布情報](assets/templates/template-manifest.json)
- [3月版の元表紙](assets/cover/weekly-it-news-cover-20260315.pptx) / [元アバター](assets/cover/avatar-20260315.jpg)

Gemini Tasks本体のブラウザ・ファイル操作で取得を試します。**Geminiスキル内のネットワークスクリプトはサポートされず、URLを読むだけではバイナリを使用できません。** 取得したPPTXを開き直して7枚と先頭の表紙を検証することが必須です。できない場合は、Google Driveのファイルを「Driveから追加」するか、GitHubから取得したPPTXをタスクへ添付してください。GeminiのGitHubリポジトリ取り込みは自動更新されず、ファイルを実際に開いたことの代わりにはなりません。PowerPoint仕上げスキルZIPにこのバイナリを入れる必要はありません。

## Gemini Tasksへの依頼

Geminiのスキル weekly-it-news-gemini を使い、ニュースを調査して技術的な面白さを対話してください。まず各ページの目的・タイトル・出典URL・見せる画像・レイアウトIDを記した編集プロットを提示し、私の承認を得てください。承認後だけ指定URLの実画像を回収し、撮影画像のファイル実体を確認して、まずスキル記載のGitHubのraw URLからテンプレート実体を取得・検証し、取得できなければDriveまたは手動添付を依頼してください。取得できたテンプレートに沿う編集可能なPPTXを作ってください。1枚目は3月版の元表紙、2枚目は今のシンプルな目次です。画像取得不能は必ず報告してください。

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
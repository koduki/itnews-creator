# itnews-creator — Weekly IT News

**Gemini Tasksでの調査・素材収集・PPTX生成 → Copilot in PowerPoint（Claude）で仕上げる**、2スキル専用リポジトリです。旧Copilot Chat生成器とChatGPTプラグインの配布は廃止しました。

## 現在のワークフロー

| フェーズ | 担当 | 内容 |
| --- | --- | --- |
| 企画 | Gemini Tasks | ニュースの調査・対話的キュレーション、ページ単位プロットをユーザーが承認 |
| 素材収集 | Gemini＋Google Apps Script | 添付DOCXの画像・出典抽出、Google Sheetsの撮影キュー→GAS→Driveの中継 |
| PPTX生成／QA | Gemini＋python-pptx | 固定8レイアウトテンプレートで編集可能なPPTX生成、画像検品、全ページレンダリング |
| 最終仕上げ | Copilot in PowerPoint（利用可能なClaudeモデル） | 既存PPTXのレイアウト、文字、画像、ネイティブ図表、ノートの調整 |

詳細：[アーキテクチャ](docs/architecture-gemini-claude.md)

## 配布ZIPは2種類だけ

[GitHub Actions — Build Gemini and PowerPoint skills](https://github.com/koduki/itnews-creator/actions/workflows/package.yml) の最新成功runのArtifactsから取得してください。Actionsの外側ZIPを展開すると以下のスキルがあります。

- `itnews-creator-gemini-task-skill-v<version>.zip`（Gemini Tasks用）
- `itnews-creator-powerpoint-polish-skill-v<version>.zip`（Copilot in PowerPoint用）

配布版は[VERSION](VERSION)が正本です。ローカルでは `python scripts/build_packages.py --out-dir dist` で同じ2 ZIPを作れます。`v<VERSION>` のタグはReleaseにも公開されます。

## Gemini Tasks側

1. [固定PPTXテンプレート](assets/templates/weekly-it-news-design-template.pptx)を**Google Driveに同期**するか、タスクに添付。GeminiのVMからGitHub rawのPPTXを直接ダウンロードできると想定せず、[template-manifest.json](assets/templates/template-manifest.json)のSHA-256で検証します。
2. `weekly-it-news-gemini` でニュースの候補、技術的な面白さ、ページ構成をユーザーと議論し、承認済み`plot.json`を作る。承認前にPPTXを生成しません。
3. 添付DOCXの `word/media/*` と出典リンク、またはスキル同梱`scripts/screenshot_relay.js`を使うSheet＋GAS中継で、実際の記事画像をDriveに保存。キュー名は`itnews-screenshot-queue`、保存先は`itnews-assets`。**GAS v0.10.1** は途中停止したジョブの復旧、429時のクールダウン、再試行、画像バイト列・寸法の検証、旧画像を失わないDrive差し替えに対応。
4. 画像を開いて検品し、Cloudflare／Cookie同意／広告・別記事等が混入したものは差し戻す。取得済みと検品承認済みは別状態。`assets-manifest.json`に出典・利用条件・検品記録を保持する。
5. `COVER`→`AGENDA`→ニュース別の`NEWS_TITLE`（青い`NEWS 01`など）→`NEWS`／`SOURCE_IMAGE`／`TECH_DIAGRAM`／`COMPARE`／`TWO_SOURCES`を生成。章扉を自動挿入するが、プロットで明示されていれば重複させません。
6. 完成版は **`--strict-assets`** で画像不足・未承認の素材を生成前に拒否し、LibreOffice/PDF→PNGで全ページを検品します。

~~~bash
# GeminiスキルZIPの中で実行
python scripts/build_pptx.py \
  --template downloads/weekly-it-news-design-template.pptx \
  --plot plot.json --assets-dir downloads \
  --assets-manifest assets-manifest.json --strict-assets \
  --qa-report qa/preflight.json --render-qa-dir qa \
  --out weekly-it-news-base.pptx
~~~

`--strict-assets`を外して未取得画像のプレースホルダーを残せるのは途中稿だけです。Pythonのファイル検査が画像の意味まで認識したと誤解せず、Geminiによる実画像の検品を実施します。

## PowerPoint側

生成済みの`base.pptx`をPowerPointで開き`itnews-powerpoint-polish`を使用。**ニュースの順序、各NEWS_TITLE章扉、実画像・出典、発表者の意見を変更せず**、余白・文字・クロップ・編集可能な技術図や表を仕上げます。実際に選べたClaudeモデルを記録し、必要な追加取材はGeminiに差し戻します。

## ソース構成

- [Gemini Tasksスキル](skills/weekly-it-news-gemini/)：プロット・画像中継GAS・Python生成器・品質ゲート
- [PowerPoint仕上げスキル](skills/itnews-powerpoint-polish/)：仕上げ専用
- [8枚のPPTXテンプレート](assets/templates/)：構造とファイルハッシュ
- [3月版表紙の原本](assets/cover/)：アバターを含む制作資産
- [現行の回帰テスト](tests/)

**GAS本番の更新方法と運用は [GAS運用ガイド](docs/gas-relay.md) を参照。** `.js` はGeminiスキルZIP用の拡張子で、Apps Scriptエディタへ反映する際は `.gs` のスクリプトとして貼り付けられます。再度 `setupTimeTrigger()` を実行し、1分周期の監視に整理してください。

GitHub変更はDrive上のPPTXや稼働中のGAS、インストール済みのスキルには自動反映されません。CI成功は製品間の実機E2E成功を意味しません。

独自ソースはMIT。ユーザー提供の表紙・アバター・第三者の記事画像は自動的にMITの対象にはなりません。

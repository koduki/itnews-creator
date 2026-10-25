# itnews-creator — Weekly IT News 制作スキル

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Microsoft 365 Copilot Chatでニュースを調査・議論してベースPowerPointを作り、PowerPointアプリ内のCopilotで仕上げる**ための、独立した2本のスキルです。

> ニュースの概要を説明し、実際の発表・記事・写真・技術資料を見せながら掘り下げる。きれいな企業向けスライドを量産することではなく、Weekly IT Newsらしい発表を制作することが目標です。

## まず全体像

| 段階 | 利用場所 | スキル | 成果物 |
| --- | --- | --- | --- |
| ① 調査・ベース作成 | Microsoft 365 **Copilot Chat** のAgent Builderエージェント | `weekly-it-news` | 対話・ニュース調査・技術的考察・出典・**編集可能なベース .pptx** |
| ② 仕上げ・検査 | **PowerPointアプリ内**のCopilot | `itnews-powerpoint-polish` | 元PPTXを編集し、実画像・図表・配置・出典・発表者ノートを仕上げた **.pptx** |

2つのスキルは別々にインストールします。**両者をつなぐ基本の受け渡しはPPTXファイルそのもの**です。出典や未取得画像の情報は、スライドまたは発表者ノートに残すことを推奨します。Agent Builderの会話履歴やスキル設定がPowerPointへ自動共有されるわけではありません。

Copilot Chatで完成度の高いPPTXが作れた場合、必ずしも②を実施する必要はありません。一方、Web画像の取得や配置などChatでできなかった作業は、PowerPoint側へ明示的に引き継ぎます。

## 1. 配布ZIPを入手する

[GitHub Actions — Build skill packages](https://github.com/koduki/itnews-creator/actions/workflows/package.yml) を開き、**成功した最新の実行**のページ下部にある **Artifacts** から `itnews-creator-packages-<実行ID>` をダウンロードします。

外側のArtifact ZIPは**展開**してください。その中に次の配布物とチェックサム `SHA256SUMS` が入っています。

| ファイル | 用途 |
| --- | --- |
| `itnews-creator-copilot-skill-v0.8.1.zip` | Copilot ChatのAgent Builderに登録する制作用スキル |
| `itnews-creator-powerpoint-polish-skill-v0.8.1.zip` | PowerPoint内のCopilotに登録する仕上げ用スキル |
| `itnews-creator-chatgpt-plugin-v0.8.1.zip` | ChatGPT向け。Microsoft 365には登録しない |

**外側のZIPと、内側のスキルZIPを取り違えないでください。** 内側のスキルZIPは登録画面がZIPアップロードに対応していればそのまま使用します。PowerPointがファイル・フォルダー指定を求める場合は、仕上げ用ZIPをさらに展開し、`SKILL.md` と付属フォルダーを指定します。

- [ビルドとArtifacts](https://github.com/koduki/itnews-creator/actions/workflows/package.yml)
- [GitHub Releases](https://github.com/koduki/itnews-creator/releases)（タグ付きリリースがある版のみ）

Artifactsの保存期間は**30日**です。GitHubへのログインが必要な場合があります。ZIPの生成と、Microsoft 365へのインストール・更新は別作業です。

## 3月版の表紙を同梱（1ページ目のみ）

**2026年3月15日版の表紙だけ**を切り出した編集可能なPowerPointテンプレートを、元の**右上アバター画像**とともにGitで管理し、Copilot Chat／PowerPointの両スキルZIPに同梱しています。ユーザーはアバターを個別アップロードする必要はありません。

- [編集可能な表紙テンプレート](assets/cover/weekly-it-news-cover-20260315.pptx)
- [元のアバター画像](assets/cover/avatar-20260315.jpg)
- [表紙プレビュー](assets/cover/cover-preview-20260315.jpg)
- [表紙の詳細ルール](skills/weekly-it-news/references/march-cover.md)

巨大な赤黒の **Weekly IT News！**、青い日付枠、右側の赤い「今週のトピック」、右上の実アバターを再現します。**日付とトピック予告だけを毎週更新し、2ページ目以降の現在の目次デザインは変更しません。** 元の固定トピック画像は編集可能なテキストへ置換しています。

元の31枚のプレゼンテーション全体や、そこに登場するニュース記事等の第三者画像は同梱しません。アバター・参考テンプレートの利用条件については[リソースの説明](assets/cover/README.md)を参照してください。

## 2. Copilot Chatに制作スキルを登録する

1. [Microsoft 365 Copilot Chat](https://m365.cloud.microsoft/chat/) を開く。
2. 「エージェントとスキル」から**Agent Builder**に進み、Weekly IT Newsエージェントを新規作成するか、既存エージェントを編集する。
3. **Configure（構成）→ Skills（スキル）** で `itnews-creator-copilot-skill-v0.8.1.zip` を追加する。旧版がある場合は置き換える。
4. スキル名 **`weekly-it-news`** を確認する。
5. **「ドキュメント、グラフ、コードを作成」**（Code Interpreterに対応する機能）が利用可能で有効になっているか確認し、エージェントを保存する。

参考：[Microsoft Learn — Agent Builderにスキルを追加](https://learn.microsoft.com/ja-jp/microsoft-365/copilot/extensibility/agent-builder-add-skills)

### Copilot Chatへの依頼例

```text
weekly-it-newsを使い、2026年10月25日版のWeekly IT Newsを作成してください。
話題はMeta Muse、PHP2Shell、GMO/お名前.com デスクトップクラウド侵害です。
まず対話しながら各話題のポイントと技術的な考察を決めてください。

表紙→今週のトピック→ニュースAの説明・根拠資料・技術解説→
ニュースBの説明・根拠資料・技術解説→ニュースC…、の順とし、
3件を一巡した後に各話題へ戻る構成は禁止します。

実際の公式発表・記事写真・技術図を優先し、未取得の画像については
「必要な理由・確認済みのURL・挿入位置・未取得状態」をスライドや
ノートに残してください。URLを検証できなければ捏造しないでください。

PowerPointで仕上げる前提なので、BASE DRAFTでも構いません。
WordやPDFではなく、実際の編集可能な.pptxを返してください。
```

**Copilot Chat段階の完成条件：** 実際の`.pptx`が存在すること、各ニュースが連続したまとまりになっていること、出典・実画像の未対応事項を隠していないこと。画像や仕上げが未完でも、明示された**BASE DRAFT**ならPowerPointへ引き継げます。Wordは代用品になりません。

カスタムスキル自体がPPTX生成能力を付与するわけではありません。同梱の標準Pythonによる簡易生成スクリプト `skills/weekly-it-news/scripts/build_pptx.py` は、利用環境でコード実行できる場合の補助手段です。Microsoft 365テナントでの実行は未検証です。

## 3. PowerPointに仕上げスキルを登録する

1. Copilot Chatで作ったベース`.pptx`をOneDriveへ保存し、**PowerPointでそのファイルを開く**。
2. PowerPointのCopilotを表示する。
3. 対応する画面では、**「＋」→「スキルの選択」→「スキルの管理」→「スキルの追加」**へ進む。
4. `itnews-creator-powerpoint-polish-skill-v0.8.1.zip` を登録する。ZIPに非対応の画面では、展開した `SKILL.md` と `references/`・`templates/` を用いる。
5. **`itnews-powerpoint-polish`** が認識されたことを確認し、現在開いているPPTXに適用する。対応環境では `@itnews-powerpoint-polish` で指定できる。

個人用OneDriveのSkillsフォルダーに手動配置する方式では、フォルダー名を `itnews-powerpoint-polish` として、その直下に `SKILL.md` を置きます。UIやスキル登録の可否はライセンス、組織設定、機能提供状況により変わります。

参考：[Microsoft サポート — PowerPointのカスタムスキル](https://support.microsoft.com/ja-jp/powerpoint/copilot/copilot-in-powerpoint-skills)

### PowerPointへの仕上げ依頼例

```text
@itnews-powerpoint-polish

このWeekly IT NewsのベースPPTXを完成版に仕上げてください。
ニュースごとの説明・根拠画像・技術解説をひとまとまりにし、
別の話題の後に同じニュースへ戻る順序があれば、まず修正してください。

未取得の報道写真、公式発表画面、ニュース記事内の技術図を、
出典・利用条件を確認したうえで実際に挿入できる範囲で補完してください。
画像URLだけで「挿入済み」と扱わないでください。

意味のある模式図や表は保持し、読みやすさ、画像のクロップ、
余白、文字のはみ出し、出典、発表者ノートを改善してください。
実行できなかったことは具体的な残課題として報告してください。
```

この仕上げは**元原稿の全面書き直しではありません**。ニュースの事実関係と発表者の考察を守り、必要な補完と投影品質に集中します。

## 4. Weekly IT Newsのコンセプト

### 原型となる資料

- **2026-01-25 / 2026-04-12：編集構成の原型。** 日付入り表紙、短い「今週のトピック」、一つのニュースの解説、続く実資料・スクショや技術説明、次のニュースという流れを優先します。以前の読みにくい配置まで再現する必要はありません。
- **2026-09-13 / 2026-10-12：表現上の改善例。** 編集可能な図表、比較、整った余白や文字組みは参考にしますが、章扉・固定スライド枚数・毎回のまとめスライドは必須にしません。
- **2026-03-15：実画像重視の追加参考。** 発表・製品・報道・技術資料の実物を見せながら進める意図を示します。
- **2026-10-25 v0.5生成版：回帰防止の反例。** Meta Muse、PHP2Shell、GMO侵害を説明してから、再び同じ順番で各ニュースの詳細に戻る構成でした。説明内容の価値は残し、**話題の再訪を避ける**よう改善します。

参考比較で観測された画像オブジェクト数（10/25版：22枚中4点、3/15版：31枚中33点）は**最低画像枚数の目標ではありません**。画像は「そのニュースについて何を理解・確認できるか」で採否を決めます。

### 守りたい発表の流れ

```text
表紙「Weekly IT News！」
今週のトピック（実際の話題数）
ニュースA：ニュース概要・技術背景
  ├─ 記事写真、発表画面、実際の製品・UI・技術図
  ├─ 必要な比較表や編集可能な模式図
  └─ 発表者の分析・考察（事実と区別）
ニュースB：ニュース概要→根拠資料→技術的解説・考察
ニュースC：ニュース概要→根拠資料→技術的解説・考察
（必要なら一枚だけ話題横断の考察）
```

**一度終えたニュースに後半から戻らない。** 実際の根拠画像と、説明のために作成した模式図は役割が異なります。数値の根拠、正確な図の矢印、報道写真の撮影者・掲載元、画像の利用条件をそれぞれ確認します。公式サイト以外の良質な報道写真や記事内図版も採用対象です。

**AIが作った写真風画像や架空のUIは、実際のスクリーンショットの代わりにはなりません。** URLは画像そのものではなく、出典を記載しただけで第三者画像の自由な再利用が認められるわけでもありません。

## 5. 各段階のチェックポイント

| 確認項目 | Copilot Chat | PowerPoint |
| --- | --- | --- |
| 編集可能なPPTXファイル | **必須** | そのファイルを編集 |
| ニュースごとの連続性 | **確定させる** | 不整合があれば先に修正 |
| 技術的内容と考察 | 主担当、出典を明確に | 意図を保持、必要なら確認 |
| 出典URLと未取得画像 | 可能な範囲で記録 | 画像を取得・挿入できる範囲で補完 |
| 実画像が本当に埋め込まれたか | 状況を明記 | **最終検証** |
| 文字組み・図表・ノート・読みやすさ | ベース | **最終QA** |

`BASE DRAFT` はベースPPTXが存在しながら画像・品質面の未完了事項がある状態です。`FINAL` として完了を報告できるのは重要な要件を満たした場合のみで、未検証項目がある場合はその旨を残します。

## 6. よくある問題

| 症状 | 対応 |
| --- | --- |
| ZIPリンクから取得できない | [Actions](https://github.com/koduki/itnews-creator/actions/workflows/package.yml)→成功済み実行→Artifactsを取得。外側ZIPだけ展開する |
| Copilot ChatでWordが生成された | Agent Builderのファイル生成機能を確認。**WordをPPTXとして完成扱いしない** |
| PowerPointに仕上げスキルが表示されない | スキル対応状況、UI、組織ポリシー、ライセンスを確認。ZIPではなく展開ファイルを求める場合もある |
| ニュースの話題が途中で再登場する | `story-continuity.md` と `topic-repair.md` に沿って一つのニュースブロックへ統合する |
| 画像がない／URLだけ貼られている | Web検索と画像取得・スクショ撮影は別機能。取得・埋め込み可能な実データか確認し、不可なら未取得と報告する |
| PowerPoint側がChatの背景を知らない | PPTX、スライドノート、出典・画像TODO、必要な追加指示を渡す。会話履歴の自動共有は前提にしない |

## 7. 開発者向け：構成・CI/CD

```text
plugin.json                               ChatGPTプラグインのマニフェスト
LICENSE                                   MITライセンス
skills/weekly-it-news/                    Copilot Chatでの調査とベースPPTX作成
  SKILL.md
  references/story-continuity.md          ニュース構成・画像引き継ぎ
  scripts/build_pptx.py                   簡易PPTX生成（対応環境のみ）
  scripts/check_editorial_flow.py         任意の構成チェック
skills/itnews-powerpoint-polish/          PowerPoint内の仕上げ
  SKILL.md
  references/topic-repair.md              ニュース順序・実資料の補完
scripts/build_packages.py                3種類のZIPを再現可能に生成
scripts/qa_pptx.py                        任意のPPTX実体検査
tests/                                     ZIP構造・生成・構成の回帰テスト
docs/design-philosophy.md                 詳細な設計思想
.github/workflows/package.yml             GitHub Actions
```

```bash
python tests/test_package.py
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/build_packages.py --out-dir dist
```

GitHub ActionsはPR、`main`へのpush、手動実行でテストし、**3種類のZIP**と `SHA256SUMS` をArtifactsに保存します。タグ `vX.Y.Z` によるリリースではマニフェストのバージョン一致を確認します。配布ZIP作成はMicrosoft 365への自動登録ではありません。

詳細資料： [設計思想](docs/design-philosophy.md) / [ニュース構成ルール](skills/weekly-it-news/references/story-continuity.md) / [PowerPointの修復ルール](skills/itnews-powerpoint-polish/references/topic-repair.md) / [Copilot Chat実行ガイド](skills/weekly-it-news/references/copilot-chat-workflow.md) / [受け入れ条件](skills/weekly-it-news/references/acceptance-tests.md)

## ライセンスと制約

独自コード・スキル定義・ドキュメントは [MIT License](LICENSE) です。参考にした過去のPPTX、ニュース記事の画像、企業ロゴ、第三者の図表はMITの対象外で、リポジトリにも同梱していません。

GitHub ActionsのZIP生成とオフラインの構造テストは実施していますが、**Microsoft 365テナントでの両スキルの実行・PowerPoint編集・実画像取得はまだ実地検証が必要です**。スキルはMicrosoftの標準機能や権限を増やすものではなく、PPTX生成、画像キャプチャ、実画像挿入の可否は環境によります。
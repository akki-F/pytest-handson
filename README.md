# Python Test Environment with DevContainer

## 開発環境について

このプロジェクトはVS Code DevContainerを使用して、Python開発環境を構築しています。

### 環境構成
- Python 3.11
- pytest (テストフレームワーク)
- pylint (コード解析ツール)

## セットアップ手順

1. 前提条件
   - VS Code
   - Docker Desktop
   - Remote Development 拡張機能

2. プロジェクトの開始
   ```bash
   git clone <repository-url>
   code python-test
   ```

3. DevContainerの起動
   - VS Codeで「Reopen in Container」を選択
   - 初回は環境構築に数分かかります

## テストの実行方法

1. VS Code上でのテスト実行
   - テストエクスプローラーから実行
   - もしくは、テストファイル内の実行ボタンをクリック

2. コマンドラインでのテスト実行
   ```bash
   pytest handson/tests
   ```

## フォルダ構成
```
python-test/
├── .devcontainer/     # DevContainer設定
├── handson/
│   ├── src/          # ソースコード
│   └── tests/        # テストコード
└── README.md
```

---
inclusion: always
---

# プロジェクト構造とコーディング規約

## アーキテクチャパターン

### コア構成
- **main.py**: アプリケーションエントリーポイント
- **mandelbrot_core.py**: フラクタル計算ロジック（`mandelbrot_point`, `generate_mandelbrot_image`等）
- **mandelbrot_window.py**: PyQt6メインGUIウィンドウ（`MandelbrotWindow`クラス）
- **mandelbrot_worker.py**: QThreadベースの非同期計算ワーカー
- **numba_utils.py**: Numba最適化関数

### モジュール分離原則
- GUI層（window）、計算層（core）、ワーカー層（worker）を明確に分離
- 各ファイルは単一責任を持つ
- `sample/`ディレクトリには参考実装（MVC、プラグインシステム等）

## コーディング規約

### 必須要件
- **言語**: 日本語コメント・ドキュメント
- **命名**: snake_case（Python標準）
- **型ヒント**: 全関数・クラスに必須
- **docstring**: 引数・戻り値・機能説明を含む

### コード品質
- 短くても多めのコメント
- 複雑なロジックには説明コメント
- 適切なエラーハンドリング
- パフォーマンス考慮（Numba活用）

### テスト
- `test/`フォルダに配置
- `test_`プレフィックス使用
- 既存テスト: logger、optimization、performance

## 開発環境
- **仮想環境**: 必ず`venv`をアクティベート
- **ログ**: `logger/custom_logger.py`を使用、出力先は`logs/`
- **設定**: `config.json`で動作カスタマイズ
- **依存関係**: `requirements.txt`で管理

## 重要な実装パターン
- QThread + pyqtSignalでUI応答性確保
- 制限付きeval()で安全な数式評価
- シグナル・スロットパターンでUI更新
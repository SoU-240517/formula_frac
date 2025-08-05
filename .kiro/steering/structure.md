---
inclusion: always
---

# プロジェクト構造とコーディング規約

## アーキテクチャパターン

### レイヤー分離（必須）
- **GUI層**: `mandelbrot_window.py` - PyQt6 UI コンポーネント
- **計算層**: `mandelbrot_core.py` - フラクタル数学ロジック
- **ワーカー層**: `mandelbrot_worker.py` - QThread非同期処理
- **最適化層**: `numba_utils.py` - パフォーマンス最適化

### ファイル責任
- `main.py`: アプリケーションエントリーポイントのみ
- `mandelbrot_core.py`: `mandelbrot_point()`, `generate_mandelbrot_image()` 関数
- `mandelbrot_window.py`: `MandelbrotWindow` クラス、UI イベント処理
- `mandelbrot_worker.py`: バックグラウンド計算、進捗シグナル
- `config.json`: アプリケーション設定（解像度、反復回数等）

## コーディング規約（厳守）

### 言語・命名
- **コメント・docstring**: 日本語必須
- **変数・関数名**: snake_case
- **クラス名**: PascalCase
- **定数**: UPPER_SNAKE_CASE

### 型安全性
- 全関数に型ヒント必須: `def func(x: int) -> str:`
- 複雑な型は `typing` モジュール使用
- docstring形式: 引数、戻り値、例外を明記

### PyQt6 パターン
- シグナル・スロット接続: `signal.connect(slot)`
- QThread継承時は `run()` メソッドオーバーライド
- UI更新は必ずメインスレッドで実行
- `pyqtSignal` でスレッド間通信

### エラーハンドリング
- 数式評価は try-except で囲む
- ユーザー入力検証を必ず実装
- ログ出力は `logger/custom_logger.py` 使用

## ディレクトリ構造

### 開発ファイル
- `test/`: テストファイル（`test_*.py`）
- `sample/`: 参考実装・実験コード
  - `jules_frac/`, `kiro_frac/`, `max_frac/`: フラクタル実装例
  - `advanced_optimization.py`: 最適化サンプル
- `logger/`: カスタムログシステム
- `logs/`: ログ出力先

### 設定・環境
- `venv/`: 仮想環境（必須使用）
- `requirements.txt`: 依存関係管理
- `config.json`: アプリケーション設定

## 実装ガイドライン

### パフォーマンス
- 計算集約的関数は Numba `@jit` デコレータ使用
- 大きな配列操作は NumPy 活用
- UI ブロッキング回避のため QThread 使用

### セキュリティ
- `eval()` 使用時は制限付き名前空間で実行
- ユーザー入力は必ず検証・サニタイズ

### UI応答性
- 長時間処理は QThread で分離
- 進捗表示は `pyqtSignal` で更新
- キャンセル機能を提供

### テスト戦略
- 既存テスト: `test_logger.py`, `test_optimization.py`, `test_performance.py`
- 新機能追加時は対応するテストも作成
- パフォーマンステストでベンチマーク測定
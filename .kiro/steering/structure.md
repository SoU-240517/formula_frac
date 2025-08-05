# プロジェクト構造

## ルートディレクトリ
```
├── main.py              # メインアプリケーションエントリーポイント
├── mandelbrot_core.py   # コアフラクタル計算ロジック
├── mandelbrot_window.py # メインGUIウィンドウクラス
├── mandelbrot_worker.py # バックグラウンド計算スレッド
├── numba_utils.py       # Numba最適化ユーティリティ
├── benchmark.py         # パフォーマンステスト
├── config.json          # アプリケーション設定
├── requirements.txt     # Python依存関係
├── docs/                # ドキュメント
│   └── README.md        # プロジェクト説明
├── logger/              # ログ機能モジュール
│   ├── __init__.py
│   └── custom_logger.py
├── logs/                # ログファイル出力先
│   └── app.log
├── test/                # テストファイル
│   ├── __init__.py
│   ├── test_logger.py
│   └── test_optimization.py
├── sample/              # サンプル実装とバリエーション
│   ├── jules_frac/      # MVCアーキテクチャを持つ複雑なフラクタルエディタ
│   ├── kiro_frac/       # プラグインシステムを持つ高度なフラクタルエディタ
│   └── max_frac/        # 追加のフラクタル実装
├── venv/                # Python仮想環境（gitから除外）
├── .gitignore           # Git無視ルール
└── .kiro/               # Kiro AIアシスタント設定
    ├── specs/           # 仕様書
    └── steering/        # AIガイダンス文書
```

## コード組織パターン

### メインアプリケーション
- **main.py**: アプリケーションエントリーポイント
- **mandelbrot_core.py**: コアフラクタル計算ロジック
  - `mandelbrot_point()`: 基本マンデルブロ計算
  - `complex_from_pixel()`: ピクセル座標から複素数への変換
  - `pixel_color()`: 反復回数から色への変換
  - `generate_mandelbrot_image()`: 画像生成メイン関数
- **mandelbrot_window.py**: メインGUIウィンドウ
  - `MandelbrotWindow`: PyQt6ベースのメインウィンドウクラス
- **mandelbrot_worker.py**: バックグラウンド処理
  - `MandelbrotWorker`: QThreadベースの計算ワーカー
- **numba_utils.py**: パフォーマンス最適化
  - Numbaを使用した高速化関数

### サンプルプロジェクト
- **jules_frac/**: コントローラー、モデル、ビューを分離した完全なMVCアーキテクチャ
- **kiro_frac/**: 包括的なテストスイートを持つプラグインベースシステム
- **max_frac/**: 最小実装例

## ファイル命名規則
- PythonファイルとファンクションにはSnake_case
- 機能を反映した説明的な名前
- テストファイルには`test_`プレフィックス
- マークダウン形式のドキュメント

## 理解すべき主要ディレクトリ
- `sample/`: 異なるアーキテクチャアプローチを示すリファレンス実装を含む
- `docs/`: プロジェクトドキュメント、主に日本語
- `logger/`: カスタムログ機能の実装
- `test/`: ユニットテストとパフォーマンステスト
- `logs/`: アプリケーションログファイルの出力先
- `.kiro/steering/`: AIアシスタントガイダンス文書（このディレクトリ）
- `.kiro/specs/`: プロジェクト仕様書

## 開発注記
- プロジェクト作業時は常に仮想環境をアクティベートする必要がある
- コードはモジュール化されており、各ファイルが特定の責任を持つ
- ログ機能が統合されており、デバッグとモニタリングが可能
- テストファイルが含まれており、品質保証が考慮されている
- Numbaによる最適化が実装されており、高速な計算が可能
- サンプルプロジェクトは例とテスト場の両方として機能する
- 設定ファイル（config.json）により動作をカスタマイズ可能
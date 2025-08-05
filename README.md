# マンデルブロ集合ビジュアライザ

PyQt6を使用したインタラクティブなマンデルブロ集合ビジュアライザです。ユーザーが任意の数式を入力してフラクタルパターンを探索できます。

## 主な機能

- **カスタム数式入力**: `z * z + c` などの任意の更新式を入力可能
- **リアルタイム描画**: マルチスレッドによる非ブロッキング画像生成
- **高速化**: Numba JITコンパイルによる大幅な性能向上
- **進捗表示**: アニメーション付きステータス表示
- **設定ファイル**: JSONによる柔軟な設定管理

## パフォーマンス最適化

### Numba JIT最適化
基本的なマンデルブロ式（`z * z + c`, `z**2 + c`）では自動的にNumba JITコンパイルが適用され、大幅な高速化を実現：

- **並列処理**: マルチコアCPUを活用した並列計算
- **ネイティブコード**: PythonコードをC/C++レベルの速度で実行
- **メモリ最適化**: NumPy配列による効率的なメモリアクセス

### 性能比較
- **従来版**: Pythonのevalによる逐次計算
- **最適化版**: Numba JITによる並列計算（10-50倍高速）

## セットアップ

### 必要な環境
- Python 3.12+
- PyQt6
- Numba
- NumPy

### インストール
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 実行
```bash
# アプリケーションの起動
python main.py

# ベンチマークの実行
python benchmark.py
```

## 使用方法

1. アプリケーションを起動
2. 数式入力欄に更新式を入力（例: `z * z + c`）
3. 「再描画」ボタンをクリックまたはEnterキーを押下
4. 画像生成の進捗をステータスバーで確認

### 対応する数式例
- `z * z + c` - 基本的なマンデルブロ集合（高速化対応）
- `z**2 + c` - 同上（高速化対応）
- `z * z * z + c` - 3次のマンデルブロ集合
- `sin(z) + c` - 三角関数を使用した変形
- `z * z + c * n` - 反復回数を含む式

## ファイル構成

```
├── main.py              # メインエントリーポイント
├── mandelbrot_window.py # GUI ウィンドウクラス
├── mandelbrot_core.py   # フラクタル計算コア（Numba最適化）
├── mandelbrot_worker.py # バックグラウンド計算スレッド
├── numba_utils.py       # Numba設定ユーティリティ
├── benchmark.py         # 性能ベンチマークツール
├── config.json          # アプリケーション設定
├── requirements.txt     # Python依存関係
└── README.md           # このファイル
```

## 設定

`config.json`で以下の設定をカスタマイズできます：

- **ウィンドウサイズ**: 表示ウィンドウの大きさ
- **画像サイズ**: 生成する画像の解像度
- **複素平面範囲**: 表示する複素平面の範囲
- **最大反復回数**: 発散判定の反復回数
- **UI設定**: ボタンテキストやアニメーション間隔
- **ログ設定**: ログレベル、出力ファイル、クリア設定

### ログファイルのクリア

ログファイルの内容をクリアする方法は2つあります：

#### 1. 自動クリア（起動時）
`config.json`の`logging`セクションで`clear_on_startup`を`true`に設定：

```json
{
  "logging": {
    "level": "INFO",
    "enabled": true,
    "file": "logs/app.log",
    "clear_on_startup": true
  }
}
```

#### 2. 手動クリア（プログラムから）
```python
from logger.custom_logger import CustomLogger

# ログファイルをクリア
success = CustomLogger.clear_log_file()
if success:
    print("ログファイルをクリアしました")
else:
    print("ログファイルのクリアに失敗しました")
```

## 技術詳細

### アーキテクチャ
- **MVC パターン**: モデル、ビュー、コントローラーの分離
- **マルチスレッド**: QThreadによるUI応答性の維持
- **モジュール化**: 機能別のファイル分割

### 最適化技術
- **Numba JIT**: `@jit(nopython=True, parallel=True)`による高速化
- **NumPy配列**: 効率的な数値計算
- **並列処理**: `prange`によるマルチコア活用
- **キャッシュ**: Numbaコンパイル結果のキャッシュ

## トラブルシューティング

### Numbaのインストールエラー
```bash
# Condaを使用する場合
conda install numba

# pipでの強制再インストール
pip install --force-reinstall numba
```

### 性能が出ない場合
1. 初回実行時はJITコンパイルのため時間がかかります
2. `benchmark.py`で性能を測定してください
3. CPUのコア数を確認してください（並列処理の効果）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
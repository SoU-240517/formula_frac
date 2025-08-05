# 技術スタック

## コア技術
- **Python 3.12+**: 主要プログラミング言語
- **PyQt6**: メインアプリケーションインターフェース用GUIフレームワーク
- **仮想環境**: 依存関係分離のための`venv`

## 主要ライブラリ
- `PyQt6.QtWidgets`: UIコンポーネント（QApplication、QMainWindow、QLineEditなど）
- `PyQt6.QtGui`: グラフィック処理（QImage、QPixmap）
- `PyQt6.QtCore`: スレッドとシグナル（QThread、pyqtSignal、QTimer）
- `math` & `cmath`: 複素数計算のための数学演算

## 開発環境
- **言語**: 日本語コメントとドキュメント
- **IDE**: VSCode（バージョン管理から除外）
- **バージョン管理**: 標準Python .gitignoreを使用したGit

## 共通コマンド

### 環境セットアップ
```bash
# 仮想環境作成
python -m venv venv

# 仮想環境アクティベート（Windows）
venv\Scripts\activate

# 依存関係インストール（requirements.txtが存在する場合）
pip install -r requirements.txt
```

### アプリケーション実行
```bash
# メインアプリケーション実行
python main.py
```

### 開発
```bash
# PyQt6インストール（主要依存関係）
pip install PyQt6
```

## アーキテクチャ注記
- ノンブロッキング画像生成のためのQThreadを使用したマルチスレッド設計
- 制御された名前空間での制限付きeval()を使用した安全な式評価
- UI更新とスレッド通信のためのシグナル・スロットパターン
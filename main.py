"""
PyQt6を用いて、ユーザーが任意のzの更新式を入力できるマンデルブロ集合ビジュアライザ。
設定はJSONファイルから読み込み、モジュール化された構造で実装。
"""
import sys
import json
from PyQt6.QtWidgets import QApplication, QMessageBox
from mandelbrot_window import MandelbrotWindow


def load_config(config_path: str = "config.json") -> dict:
    """
    設定ファイルを読み込む。

    Args:
        config_path (str): 設定ファイルのパス

    Returns:
        dict: 設定情報

    Raises:
        FileNotFoundError: 設定ファイルが見つからない場合
        json.JSONDecodeError: JSONの形式が不正な場合
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"設定ファイル '{config_path}' が見つかりません。")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"設定ファイルのJSON形式が不正です: {e}")


def main():
    """
    アプリケーションを起動し、メインウィンドウを表示するエントリーポイント。
    """
    print("main")
    app = QApplication(sys.argv)

    try:
        # 設定ファイルを読み込み
        config = load_config()

        # メインウィンドウを作成・表示
        window = MandelbrotWindow(config)
        window.show()

        sys.exit(app.exec())

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # 設定ファイルの読み込みエラーを表示
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("設定エラー")
        error_dialog.setText(str(e))
        error_dialog.exec()
        sys.exit(1)
    except Exception as e:
        # その他の予期しないエラー
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("アプリケーションエラー")
        error_dialog.setText(f"予期しないエラーが発生しました: {e}")
        error_dialog.exec()
        sys.exit(1)


if __name__ == "__main__":
    main()

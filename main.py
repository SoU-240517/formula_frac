"""
PyQt6を用いて、ユーザーが任意のzの更新式を入力できるマンデルブロ集合ビジュアライザ。
設定はJSONファイルから読み込み、モジュール化された構造で実装。
Numbaを使用した高速化を適用。
"""
import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from mandelbrot_window import MandelbrotWindow
from numba_utils import configure_numba, get_numba_info
from logger.custom_logger import logger


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
    logger.debug(f"設定ファイルを読み込み中: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"設定ファイルの読み込みが完了しました: {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"設定ファイルが見つかりません: {config_path}")
        raise FileNotFoundError(f"設定ファイル '{config_path}' が見つかりません。")
    except json.JSONDecodeError as e:
        logger.error(f"設定ファイルのJSON形式が不正です: {e}")
        raise json.JSONDecodeError(f"設定ファイルのJSON形式が不正です: {e}")


def main():
    """
    アプリケーションを起動し、メインウィンドウを表示するエントリーポイント。
    """
    # プロジェクトルートを設定
    from logger.custom_logger import CustomLogger
    CustomLogger.set_project_root(Path(__file__).parent)

    logger.info("アプリケーションを開始します")

    # Numbaの初期化と設定
    logger.info("Numbaを初期化中...")
    configure_numba(cache_enabled=True)
    get_numba_info()

    app = QApplication(sys.argv)
    logger.debug("QApplicationを作成しました")

    try:
        # 設定ファイルを読み込み
        config = load_config()

        # メインウィンドウを作成・表示
        logger.info("メインウィンドウを作成中...")
        window = MandelbrotWindow(config)
        window.show()
        logger.info("メインウィンドウを表示しました")

        logger.info("アプリケーションのメインループを開始します")
        sys.exit(app.exec())

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # 設定ファイルの読み込みエラーを表示
        logger.critical(f"設定ファイルエラー: {e}", exc_info=True)
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("設定エラー")
        error_dialog.setText(str(e))
        error_dialog.exec()
        sys.exit(1)
    except Exception as e:
        # その他の予期しないエラー
        logger.critical(f"予期しないエラーが発生しました: {e}", exc_info=True)
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("アプリケーションエラー")
        error_dialog.setText(f"予期しないエラーが発生しました: {e}")
        error_dialog.exec()
        sys.exit(1)


if __name__ == "__main__":
    main()

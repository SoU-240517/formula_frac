#!/usr/bin/env python3
"""
ロガーの動作テスト用スクリプト。
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger.custom_logger import logger, CustomLogger


def test_logger_basic():
    """基本的なロガー機能をテストする"""
    print("=== ロガー基本機能テスト ===")
    
    # プロジェクトルートを設定
    CustomLogger.set_project_root(Path(__file__).parent.parent)
    
    # 各レベルでのログ出力テスト
    logger.debug("これはDEBUGメッセージです")
    logger.info("これはINFOメッセージです")
    logger.warning("これはWARNINGメッセージです")
    logger.error("これはERRORメッセージです")
    logger.critical("これはCRITICALメッセージです")
    
    print("\n=== ログレベル変更テスト ===")
    logger.info("ログレベルをWARNINGに変更します")
    logger.set_level("WARNING")
    
    logger.debug("このDEBUGメッセージは表示されません")
    logger.info("このINFOメッセージは表示されません")
    logger.warning("このWARNINGメッセージは表示されます")
    logger.error("このERRORメッセージは表示されます")
    
    print("\n=== ログレベルをINFOに戻します ===")
    logger.set_level("INFO")
    logger.info("ログレベルをINFOに戻しました")
    
    print("\n=== 例外情報テスト ===")
    try:
        # 意図的にエラーを発生させる
        result = 1 / 0
    except ZeroDivisionError:
        logger.error("ゼロ除算エラーが発生しました", exc_info=True)
    
    print("\n=== ロガー無効化テスト ===")
    logger.info("ロガーを無効化します")
    logger.set_enabled(False)
    logger.info("このメッセージは表示されません")
    
    logger.set_enabled(True)
    logger.info("ロガーを再度有効化しました")
    
    print("\n=== テスト完了 ===")


def test_logger_in_function():
    """関数内でのロガー使用をテストする"""
    logger.info("test_logger_in_function関数内からのログです")
    
    def nested_function():
        logger.debug("ネストした関数からのログです")
    
    nested_function()


class TestClass:
    """クラス内でのロガー使用をテストするクラス"""
    
    def __init__(self):
        logger.info("TestClassのインスタンスが作成されました")
    
    def test_method(self):
        logger.info("TestClassのtest_methodが呼び出されました")
    
    @classmethod
    def test_classmethod(cls):
        logger.info("TestClassのtest_classmethodが呼び出されました")


if __name__ == "__main__":
    # 基本機能テスト
    test_logger_basic()
    
    # 関数内テスト
    test_logger_in_function()
    
    # クラス内テスト
    test_obj = TestClass()
    test_obj.test_method()
    TestClass.test_classmethod()
    
    # ログファイルの確認
    log_file = Path("logs/app.log")
    if log_file.exists():
        print(f"\nログファイルが作成されました: {log_file}")
        print(f"ログファイルサイズ: {log_file.stat().st_size} bytes")
    else:
        print("\nログファイルが見つかりません")
"""
Numbaの設定とキャッシュ管理のためのユーティリティモジュール。
"""
import shutil
from pathlib import Path
import numba


def configure_numba(cache_enabled: bool = True):
    """
    Numbaのキャッシュ設定を適用する。
    
    Args:
        cache_enabled (bool): キャッシュを有効にするかどうか
    """
    from logger.custom_logger import logger
    numba.config.CACHE = cache_enabled
    logger.info(f"Numbaキャッシュ設定: {'有効' if cache_enabled else '無効'}")


def clear_numba_cache():
    """
    Numbaのキャッシュディレクトリを安全に削除する。
    """
    try:
        numba_cache_dir_path_str = numba.config.CACHE_DIR
        if numba_cache_dir_path_str:
            numba_cache_dir = Path(numba_cache_dir_path_str)
            if numba_cache_dir.exists() and numba_cache_dir.is_dir():
                print(f"Numbaキャッシュディレクトリをクリアします: {numba_cache_dir}")
                shutil.rmtree(numba_cache_dir, ignore_errors=True)
                print("Numbaキャッシュディレクトリをクリアしました。")
            else:
                print("Numbaキャッシュディレクトリが見つかりません。")
        else:
            print("Numbaキャッシュディレクトリが設定されていません。")
    except Exception as e:
        print(f"Numbaキャッシュディレクトリのクリア中にエラーが発生しました: {e}")


def get_numba_info():
    """
    Numbaの設定情報を表示する。
    """
    from logger.custom_logger import logger
    logger.info(f"Numba バージョン: {numba.__version__}")
    logger.info(f"キャッシュ有効: {numba.config.CACHE}")
    logger.info(f"キャッシュディレクトリ: {numba.config.CACHE_DIR}")
    logger.info(f"並列処理スレッド数: {numba.config.NUMBA_NUM_THREADS}")
import time
import inspect
from pathlib import Path
import sys
import traceback
import json
from typing import Optional, Union


class CustomLogger:
    """
    カスタムロガーシングルトンクラス。
    経過時間、呼び出し元情報、設定可能なログレベル、有効/無効スイッチを含むフォーマットされたログメッセージを出力します。
    設定は config.json から読み込まれます。
    """
    _instance = None
    _start_time = None  # ロガーの最初のインスタンス化からの開始時刻
    _initializing = False  # 初期化中の循環呼び出しを防ぐためのフラグ

    LOG_LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }
    
    LOG_COLORS = {
        "DEBUG": "\033[94m",      # 青
        "INFO": "\033[92m",       # 緑
        "WARNING": "\033[93m",    # 黄
        "ERROR": "\033[91m",      # 赤
        "CRITICAL": "\033[91m\033[1m",  # 太字赤
        "DIM_GRAY": "\033[90m",   # 暗いグレー
    }
    
    RESET_COLOR = "\033[0m"
    
    _current_level_int: int
    _is_enabled: bool
    _log_file_path: Optional[Path] = None
    _project_root_path: Optional[Path] = None

    def __new__(cls, *args, **kwargs) -> 'CustomLogger':
        """シングルトンインスタンスを作成または返します。初回作成時に初期化を行います。"""
        if not cls._instance:
            cls._initializing = True  # 初期化開始のフラグを設定

            instance = super(CustomLogger, cls).__new__(cls)

            # _start_time は最初のインスタンス作成時に一度だけ設定
            if cls._start_time is None:
                cls._start_time = time.time()

            # クラス属性として基本的なデフォルト値を設定
            cls._current_level_int = cls.LOG_LEVELS.get("INFO", 20)
            cls._is_enabled = True
            cls._log_file_path = Path("logs/app.log")  # デフォルトのログファイルパス

            instance._configure_from_settings()  # 設定ファイルからの読み込みと適用

            cls._instance = instance
            cls._initializing = False  # 初期化終了のフラグを解除
        return cls._instance

    def __init__(self) -> None:
        """シングルトンなので、__new__ で全ての初期化を完結させるため、__init__ では何もしない。"""
        pass

    def _configure_from_settings(self) -> None:
        """
        config.jsonから設定を読み込み、シングルトンのクラス属性に適用します。
        このメソッドは __new__ から一度だけ、最初のインスタンス作成時に呼び出されます。
        """
        try:
            # config.jsonファイルを読み込み
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # logging設定を取得（存在しない場合はデフォルト値を使用）
                logging_config = config.get("logging", {})
                
                # ログレベルの設定
                level_str = logging_config.get("level", "INFO").upper()
                CustomLogger._current_level_int = CustomLogger.LOG_LEVELS.get(level_str, CustomLogger.LOG_LEVELS["INFO"])
                
                # 有効/無効の設定
                enabled_setting = logging_config.get("enabled", True)
                if isinstance(enabled_setting, str):
                    CustomLogger._is_enabled = enabled_setting.lower() == "true"
                else:
                    CustomLogger._is_enabled = bool(enabled_setting)
                
                # ログファイルパスの設定
                log_file_setting = logging_config.get("file", "logs/app.log")
                CustomLogger._log_file_path = Path(log_file_setting)
                
                # ログファイルディレクトリの作成
                if CustomLogger._log_file_path and CustomLogger._log_file_path.parent:
                    CustomLogger._log_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 設定適用完了をログに出力
                if CustomLogger._is_enabled:
                    self.log(f"CustomLogger: 設定ファイルからロガー設定を適用しました。レベル: {level_str}, 有効: {enabled_setting}, ファイル: {CustomLogger._log_file_path}", level="INFO")
            else:
                # config.jsonが存在しない場合はデフォルト設定を使用
                if CustomLogger._log_file_path and CustomLogger._log_file_path.parent:
                    CustomLogger._log_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                if CustomLogger._is_enabled:
                    self.log("CustomLogger: config.jsonが見つからないため、デフォルト設定を使用します。", level="WARNING")

        except Exception as e:
            # 初期化中にエラーが発生した場合のフォールバック
            print(f"[CRITICAL] CustomLogger: 設定からのロガー初期化に失敗しました: {e}. デフォルト設定を使用します。", flush=True)
            
            # ログファイルディレクトリの作成を再度試行
            if CustomLogger._log_file_path and CustomLogger._log_file_path.parent:
                try:
                    CustomLogger._log_file_path.parent.mkdir(parents=True, exist_ok=True)
                except Exception:
                    pass

    def set_level(self, level_name_or_int: Union[str, int]) -> None:
        """ロガーの現在のログレベルを設定します。"""
        if isinstance(level_name_or_int, str):
            CustomLogger._current_level_int = CustomLogger.LOG_LEVELS.get(level_name_or_int.upper(), CustomLogger.LOG_LEVELS["INFO"])
        elif isinstance(level_name_or_int, int):
            CustomLogger._current_level_int = level_name_or_int
        else:
            CustomLogger._current_level_int = CustomLogger.LOG_LEVELS["INFO"]

    def set_enabled(self, enabled: bool) -> None:
        """ロガーの有効/無効状態を設定します。"""
        CustomLogger._is_enabled = enabled

    @classmethod
    def set_project_root(cls, project_root: Path) -> None:
        """プロジェクトのルートパスを設定します。ログ出力時のパス表示に使用されます。"""
        cls._project_root_path = project_root.resolve() if project_root else None

    def log(self, message: str, level: str = "INFO", exc_info: object = None, skip_frames: int = 0) -> None:
        """指定されたレベルでログメッセージを記録します。"""
        # 初期化中のロギング呼び出しをチェック（循環依存を避けるため）
        if hasattr(CustomLogger, '_initializing') and CustomLogger._initializing:
            return

        # 属性が初期化されていることを保証
        if not hasattr(CustomLogger, '_is_enabled'): 
            CustomLogger._is_enabled = True
        if not hasattr(CustomLogger, '_current_level_int'): 
            CustomLogger._current_level_int = CustomLogger.LOG_LEVELS["INFO"]
        if not hasattr(CustomLogger, '_log_file_path'): 
            CustomLogger._log_file_path = Path("logs/app.log")

        if not CustomLogger._is_enabled:
            return

        message_level_str = level.upper()
        message_level_int = CustomLogger.LOG_LEVELS.get(message_level_str, CustomLogger.LOG_LEVELS["INFO"])

        if message_level_int < CustomLogger._current_level_int:
            return

        # 呼び出し元の情報を取得（skip_framesの分だけ追加でスキップ）
        frame = inspect.currentframe().f_back
        for _ in range(skip_frames):
            if frame.f_back is not None:
                frame = frame.f_back
        filepath_abs = Path(frame.f_code.co_filename).resolve()
        lineno = frame.f_lineno

        # コンソール表示用のパス文字列を決定
        display_path_str = str(filepath_abs)  # デフォルトは絶対パス
        if CustomLogger._project_root_path:
            try:
                # プロジェクトルートからの相対パスを取得
                if hasattr(Path, "is_relative_to"):
                    if filepath_abs.is_relative_to(CustomLogger._project_root_path):
                        display_path_str = str(filepath_abs.relative_to(CustomLogger._project_root_path))
                else:
                    try:
                        possible_relative_path = filepath_abs.relative_to(CustomLogger._project_root_path)
                        display_path_str = str(possible_relative_path)
                    except ValueError:
                        pass  # 絶対パスのまま
            except Exception:
                pass  # 絶対パスのまま

        # 関数名とクラス名を取得
        func_name = frame.f_code.co_name
        qualname_parts = []
        if 'self' in frame.f_locals:
            qualname_parts.append(frame.f_locals['self'].__class__.__name__)
        elif 'cls' in frame.f_locals:
            qualname_parts.append(frame.f_locals['cls'].__name__)
        qualname_parts.append(func_name)
        log_context = ".".join(qualname_parts)

        # 経過時間を計算
        current_time = time.time()
        start_time = CustomLogger._start_time if CustomLogger._start_time is not None else current_time
        elapsed_time_ms = int((current_time - start_time) * 1000)

        # フォーマット
        formatted_elapsed_time_ms = f"{elapsed_time_ms:>5}"
        formatted_level_str = f"{message_level_str:<8}"
        clickable_path = f"{display_path_str}:{lineno}"

        # 色の設定
        level_color_code = CustomLogger.LOG_COLORS.get(message_level_str, "")
        dim_color_code = CustomLogger.LOG_COLORS.get("DIM_GRAY", "")

        # コンソール出力
        log_message_console = (f"{dim_color_code}{formatted_elapsed_time_ms}ms:{CustomLogger.RESET_COLOR} "
                               f"{level_color_code}{formatted_level_str}{CustomLogger.RESET_COLOR} "
                               f"{message} "
                               f"{dim_color_code}[{clickable_path}:{log_context}]{CustomLogger.RESET_COLOR}")
        print(log_message_console, flush=True)

        # ファイル出力
        if CustomLogger._log_file_path:
            log_message_file = (f"{formatted_elapsed_time_ms}ms: "
                                f"{formatted_level_str} "
                                f"{message} "
                                f"[{display_path_str}:{lineno}:{log_context}]")
            try:
                with open(CustomLogger._log_file_path, "a", encoding="utf-8") as f:
                    f.write(log_message_file + "\n")
                    if exc_info:
                        if exc_info is True:
                            traceback_str = traceback.format_exc()
                            if traceback_str and traceback_str != "None\n":
                                f.write(traceback_str)
                        elif isinstance(exc_info, tuple):
                            traceback_str = "".join(traceback.format_exception(*exc_info))
                            if traceback_str:
                                f.write(traceback_str)
            except Exception as e:
                print(f"ログファイルへの書き込みに失敗しました: {CustomLogger._log_file_path}, Error: {e}", flush=True)

        # 例外情報のコンソール出力
        if exc_info:
            if exc_info is True:
                traceback.print_exc()
            elif isinstance(exc_info, tuple):
                traceback.print_exception(*exc_info)

    def debug(self, message: str, exc_info: object = None) -> None:
        """DEBUGレベルでログを出力します。"""
        self.log(message, "DEBUG", exc_info, skip_frames=1)

    def info(self, message: str, exc_info: object = None) -> None:
        """INFOレベルでログを出力します。"""
        self.log(message, "INFO", exc_info, skip_frames=1)

    def warning(self, message: str, exc_info: object = None) -> None:
        """WARNINGレベルでログを出力します。"""
        self.log(message, "WARNING", exc_info, skip_frames=1)

    def error(self, message: str, exc_info: object = None) -> None:
        """ERRORレベルでログを出力します。"""
        self.log(message, "ERROR", exc_info, skip_frames=1)

    def critical(self, message: str, exc_info: object = None) -> None:
        """CRITICALレベルでログを出力します。"""
        self.log(message, "CRITICAL", exc_info, skip_frames=1)


# グローバルロガーインスタンス
logger = CustomLogger()
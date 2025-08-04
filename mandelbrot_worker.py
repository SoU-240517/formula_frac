"""
マンデルブロ集合の画像生成をバックグラウンドで実行するワーカースレッド。
"""
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
from mandelbrot_core import generate_mandelbrot_image
from logger.custom_logger import logger


class MandelbrotWorker(QThread):
    """
    マンデルブロ集合の画像生成をバックグラウンドで実行するワーカースレッド。
    """
    finished = pyqtSignal(QImage)

    def __init__(self, width: int, height: int, formula_str: str, config: dict, parent=None):
        """
        ワーカースレッドを初期化する。
        
        Args:
            width (int): 画像の幅
            height (int): 画像の高さ
            formula_str (str): ユーザーが入力したzの更新式
            config (dict): 設定情報
            parent (QObject): 親オブジェクト
        """
        logger.debug(f"MandelbrotWorker: 初期化 - サイズ: {width}x{height}, 式: '{formula_str}'")
        super().__init__(parent)
        self.width = width
        self.height = height
        self.formula_str = formula_str
        self.config = config

    def run(self):
        """
        画像生成を実行し、完了したらfinishedシグナルを発行する。
        """
        logger.info(f"画像生成を開始します - サイズ: {self.width}x{self.height}, 式: '{self.formula_str}'")
        
        max_iter = self.config['mandelbrot']['max_iterations']
        logger.debug(f"最大反復回数: {max_iter}")
        
        # 計算開始時刻を記録
        import time
        start_time = time.time()
        
        try:
            image = generate_mandelbrot_image(self.width, self.height, self.formula_str, self.config, max_iter)
            
            # 計算時間を表示
            end_time = time.time()
            calculation_time = end_time - start_time
            logger.info(f"画像生成が完了しました: {calculation_time:.2f}秒")
            
            self.finished.emit(image)
        except Exception as e:
            logger.error(f"画像生成中にエラーが発生しました: {e}", exc_info=True)
            # エラーの場合は空の画像を送信
            empty_image = QImage(self.width, self.height, QImage.Format.Format_RGB32)
            empty_image.fill(0)  # 黒で塗りつぶし
            self.finished.emit(empty_image)
"""
マンデルブロ集合の画像生成をバックグラウンドで実行するワーカースレッド。
"""
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage
from mandelbrot_core import generate_mandelbrot_image


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
        print("MandelbrotWorker: __init__")
        super().__init__(parent)
        self.width = width
        self.height = height
        self.formula_str = formula_str
        self.config = config

    def run(self):
        """
        画像生成を実行し、完了したらfinishedシグナルを発行する。
        """
        print("MandelbrotWorker: run")
        print(f"画像サイズ: {self.width}x{self.height}, 式: '{self.formula_str}'")
        
        max_iter = self.config['mandelbrot']['max_iterations']
        
        # 計算開始時刻を記録
        import time
        start_time = time.time()
        
        image = generate_mandelbrot_image(self.width, self.height, self.formula_str, self.config, max_iter)
        
        # 計算時間を表示
        end_time = time.time()
        calculation_time = end_time - start_time
        print(f"計算完了: {calculation_time:.2f}秒")
        
        self.finished.emit(image)
"""
マンデルブロ集合を表示するメインウィンドウクラス。
"""
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from mandelbrot_worker import MandelbrotWorker


class MandelbrotWindow(QMainWindow):
    """
    マンデルブロ集合を表示するメインウィンドウクラス。
    ユーザーが数式を入力し、再描画できる。
    """
    
    def __init__(self, config: dict):
        """
        ウィンドウを初期化し、マンデルブロ集合画像とUIを表示する。
        
        Args:
            config (dict): 設定情報
        """
        print("MandelbrotWindow: __init__")
        super().__init__()
        self.config = config
        self._setup_window()
        self._setup_ui()
        self._setup_status_bar()
        self._setup_animation()
        self._connect_signals()
        
        # 最初の描画
        self.update_image()

    def _setup_window(self):
        """ウィンドウの基本設定を行う。"""
        window_config = self.config['window']
        self.setWindowTitle(window_config['title'])
        self.setFixedSize(window_config['width'], window_config['height'])

    def _setup_ui(self):
        """UIコンポーネントを設定する。"""
        # メインウィジェットとレイアウト
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # 数式入力欄
        ui_config = self.config['ui']
        mandelbrot_config = self.config['mandelbrot']
        
        self.formula_input = QLineEdit(self)
        self.formula_input.setText(mandelbrot_config['default_formula'])
        self.formula_input.setPlaceholderText(ui_config['formula_placeholder'])
        layout.addWidget(self.formula_input)

        # 再描画ボタン
        self.redraw_button = QPushButton(ui_config['redraw_button_text'], self)
        layout.addWidget(self.redraw_button)

        # 画像表示用ラベル
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setCentralWidget(central_widget)

    def _setup_status_bar(self):
        """ステータスバーを設定する。"""
        self.status = self.statusBar()
        self.status.showMessage(self.config['ui']['status_ready'])

    def _setup_animation(self):
        """アニメーション用タイマーを設定する。"""
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(self.config['ui']['animation_interval'])
        self.anim_timer.timeout.connect(self.update_anim)
        self.anim_step = 0
        self.anim_base = self.config['ui']['status_calculating']

    def _connect_signals(self):
        """シグナルとスロットを接続する。"""
        self.redraw_button.clicked.connect(self.update_image)

    def update_anim(self):
        """
        ステータスバーの「計算中...」アニメーションを更新する。
        """
        self.anim_step = (self.anim_step + 1) % 4
        dots = "." * self.anim_step
        self.status.showMessage(self.anim_base + dots)

    def update_image(self):
        """
        入力された式でマンデルブロ集合画像を再生成し、表示する。
        画像生成はワーカースレッドで実行。
        """
        print("MandelbrotWindow: update_image")
        formula_str = self.formula_input.text()
        
        # ステータスバーに計算中を表示しアニメーション開始
        self.anim_step = 0
        self.anim_base = self.config['ui']['status_calculating']
        self.anim_timer.start()
        self.status.showMessage(self.anim_base)
        
        # 画像生成を別スレッドで実行
        window_config = self.config['window']
        self.worker = MandelbrotWorker(
            window_config['image_width'], 
            window_config['image_height'], 
            formula_str, 
            self.config
        )
        self.worker.finished.connect(self.on_image_ready)
        self.worker.start()

    def on_image_ready(self, image: QImage):
        """
        画像生成完了時に呼ばれ、画像を表示し、アニメーションを止める。
        
        Args:
            image (QImage): 生成された画像
        """
        print("MandelbrotWindow: on_image_ready")
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.anim_timer.stop()
        self.status.showMessage(self.config['ui']['status_complete'])
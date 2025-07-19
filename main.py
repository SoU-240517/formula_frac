"""
PyQt6を用いて、ユーザーが任意のzの更新式を入力できるマンデルブロ集合ビジュアライザ。
800x600ピクセルのウィンドウに、グレースケールで描画する。
"""
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
import math
import cmath


def mandelbrot_point(c, formula_str, max_iter=100):
    """
    1点分のマンデルブロ集合の発散判定を行い、発散までの反復回数を返す。
    ユーザーが指定した式（formula_str）でzを更新する。

    Args:
        c (complex): 判定する複素数座標
        formula_str (str): ユーザーが入力したzの更新式（例: 'z * z + c'）
        max_iter (int): 最大反復回数

    Returns:
        int: 発散までの反復回数（発散しなければmax_iter）
    """
    z = 0
    now_itre = 0
    # evalで使う安全な辞書を作成
    safe_dict = {
        'z': z,
        'c': c,
        'n': now_itre,
        # math, cmathの関数を一部許可
        'abs': abs,
        'sin': cmath.sin,
        'cos': cmath.cos,
        'exp': cmath.exp,
        'log': cmath.log,
        'pow': pow,
        'sqrt': cmath.sqrt,
        're': lambda x: x.real,
        'im': lambda x: x.imag,
        'pi': math.pi,
        'e': math.e,
    }
    while abs(z) <= 2 and now_itre < max_iter:
        safe_dict['z'] = z
        safe_dict['c'] = c
        safe_dict['n'] = now_itre
        try:
            z = eval(formula_str, {"__builtins__": {}}, safe_dict)
        except Exception:
            # 数式が不正な場合は0回で終了
            return 0
        now_itre += 1
    return now_itre


def complex_from_pixel(x, y, width, height, re_start, re_end, im_start, im_end):
    """
    ピクセル座標(x, y)を複素平面上の座標に変換する。
    Args:
        x (int): ピクセルのx座標
        y (int): ピクセルのy座標
        width (int): 画像の幅
        height (int): 画像の高さ
        re_start (float): 実部の開始値
        re_end (float): 実部の終了値
        im_start (float): 虚部の開始値
        im_end (float): 虚部の終了値
    Returns:
        complex: 対応する複素数
    """
    c_re = re_start + (x / width) * (re_end - re_start)
    c_im = im_start + (y / height) * (im_end - im_start)
    return complex(c_re, c_im)


def pixel_color(n, max_iter):
    """
    反復回数nからグレースケールの色を計算する。
    Args:
        n (int): 反復回数
        max_iter (int): 最大反復回数
    Returns:
        int: 24bit RGB値（グレースケール）
    """
    color = 255 - int(n * 255 / max_iter)
    return (color << 16) | (color << 8) | color


def generate_mandelbrot_image(width, height, formula_str, max_iter=100):
    """
    マンデルブロ集合の画像を生成する。
    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        formula_str (str): ユーザーが入力したzの更新式
        max_iter (int): 最大反復回数
    Returns:
        QImage: 生成された画像
    """
    print("generate_mandelbrot_image 実行")
    re_start, re_end = -2.0, 1.0  # 実部の範囲
    im_start, im_end = -1.2, 1.2  # 虚部の範囲
    image = QImage(width, height, QImage.Format.Format_RGB32)
    for x in range(width):
        for y in range(height):
            c = complex_from_pixel(x, y, width, height, re_start, re_end, im_start, im_end)
            n = mandelbrot_point(c, formula_str, max_iter)
            image.setPixel(x, y, pixel_color(n, max_iter))
    return image


# 画像生成用ワーカースレッド
class MandelbrotWorker(QThread):
    finished = pyqtSignal(QImage)

    def __init__(self, width, height, formula_str, parent=None):
        print("MandelbrotWorker __init__ 実行")
        super().__init__(parent)
        self.width = width
        self.height = height
        self.formula_str = formula_str

    def run(self):
        print("MandelbrotWorker run 実行")
        image = generate_mandelbrot_image(self.width, self.height, self.formula_str)
        self.finished.emit(image)


class MandelbrotWindow(QMainWindow):
    """
    マンデルブロ集合を表示するメインウィンドウクラス。
    ユーザーが数式を入力し、再描画できる。
    """
    def __init__(self):
        """
        ウィンドウを初期化し、マンデルブロ集合画像とUIを表示する。
        """
        print("MandelbrotWindow __init__ 実行")
        super().__init__()
        self.setWindowTitle("マンデルブロ集合")
        self.setFixedSize(800, 650)  # 入力欄分だけ高さを少し増やす

        # メインウィジェットとレイアウト
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # 数式入力欄
        self.formula_input = QLineEdit(self)
        self.formula_input.setText("z * z + c")  # デフォルト式
        self.formula_input.setPlaceholderText("zの更新式を入力 (例: z * z + c)")
        layout.addWidget(self.formula_input)

        # 再描画ボタン
        self.redraw_button = QPushButton("再描画", self)
        layout.addWidget(self.redraw_button)

        # 画像表示用ラベル
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setCentralWidget(central_widget)

        # ステータスバー追加
        self.status = self.statusBar()
        self.status.showMessage("準備完了")

        # アニメーション用タイマー
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(300)  # 300msごと
        self.anim_timer.timeout.connect(self.update_anim)
        self.anim_step = 0
        self.anim_base = "計算中"

        # 最初の描画
        self.update_image()

        # ボタン押下時の処理を接続
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
        print("MandelbrotWindow update_image 実行")
        formula_str = self.formula_input.text()
        # ステータスバーに計算中を表示しアニメーション開始
        self.anim_step = 0
        self.anim_base = "計算中"
        self.anim_timer.start()
        self.status.showMessage(self.anim_base)
        # 画像生成を別スレッドで実行
        self.worker = MandelbrotWorker(200, 150, formula_str)
        self.worker.finished.connect(self.on_image_ready)
        self.worker.start()

    def on_image_ready(self, image):
        """
        画像生成完了時に呼ばれ、画像を表示し、アニメーションを止める。
        """
        print("MandelbrotWindow on_image_ready 実行")
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.anim_timer.stop()
        self.status.showMessage("完了")


def main():
    """
    アプリケーションを起動し、メインウィンドウを表示するエントリーポイント。
    """
    print("main 実行")
    app = QApplication(sys.argv)
    window = MandelbrotWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

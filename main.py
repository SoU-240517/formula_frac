"""
PyQt6を用いてマンデルブロ集合を静的に表示するシンプルなGUIアプリケーション。
800x600ピクセルのウィンドウにグレースケールで描画します。
"""
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt


def mandelbrot_point(c, max_iter=100):
    """
    1点分のマンデルブロ集合の発散判定を行い、発散までの反復回数を返す。

    Args:
        c (complex): 判定する複素数
        max_iter (int): 発散判定の最大繰り返し回数

    Returns:
        int: 発散までの反復回数（発散しなければmax_iter）
    """
    z = 0
    now_itre = 0
    while abs(z) <= 2 and now_itre < max_iter:
        z = z * z + c
        now_itre += 1
    return now_itre


def complex_from_pixel(x, y, width, height, re_start, re_end, im_start, im_end):
    """
    ピクセル座標(x, y)を複素平面上の座標に変換する。
    """
    c_re = re_start + (x / width) * (re_end - re_start)
    c_im = im_start + (y / height) * (im_end - im_start)
    return complex(c_re, c_im)


def pixel_color(n, max_iter):
    """
    反復回数nからグレースケールの色を計算する。
    """
    color = 255 - int(n * 255 / max_iter)
    return (color << 16) | (color << 8) | color


def generate_mandelbrot_image(width, height, max_iter=100):
    """
    マンデルブロ集合の画像を生成する関数。
    """
    re_start, re_end = -2.0, 1.0
    im_start, im_end = -1.2, 1.2
    image = QImage(width, height, QImage.Format.Format_RGB32)
    for x in range(width):
        for y in range(height):
            c = complex_from_pixel(x, y, width, height, re_start, re_end, im_start, im_end)
            n = mandelbrot_point(c, max_iter)
            image.setPixel(x, y, pixel_color(n, max_iter))
    return image


class MandelbrotWindow(QMainWindow):
    """
    マンデルブロ集合を表示するメインウィンドウクラス。
    """
    def __init__(self):
        """
        ウィンドウを初期化し、マンデルブロ集合画像を表示する。
        """
        super().__init__()
        self.setWindowTitle("マンデルブロ集合")
        self.setFixedSize(800, 600)
        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = generate_mandelbrot_image(800, 600)
        pixmap = QPixmap.fromImage(image)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)


def main():
    """
    アプリケーションを起動し、メインウィンドウを表示するエントリーポイント。
    """
    app = QApplication(sys.argv)
    window = MandelbrotWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt


def mandelbrot(width, height, max_iter=100):
    # 描画範囲
    re_start, re_end = -2.0, 1.0
    im_start, im_end = -1.2, 1.2
    image = QImage(width, height, QImage.Format.Format_RGB32)
    for x in range(width):
        for y in range(height):
            # 複素平面上の座標に変換
            c_re = re_start + (x / width) * (re_end - re_start)
            c_im = im_start + (y / height) * (im_end - im_start)
            c = complex(c_re, c_im)
            z = 0
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            # 色付け（グラデーション）
            color = 255 - int(n * 255 / max_iter)
            image.setPixel(x, y, (color << 16) | (color << 8) | color)
    return image


class MandelbrotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("マンデルブロ集合 (PyQt6)")
        self.setFixedSize(800, 600)
        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = mandelbrot(800, 600)
        pixmap = QPixmap.fromImage(image)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)
    window = MandelbrotWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

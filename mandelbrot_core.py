"""
マンデルブロ集合の数学的計算を担当するコアモジュール。
"""
import math
import cmath
from PyQt6.QtGui import QImage


def mandelbrot_point(c: complex, formula_str: str, max_iter: int = 100) -> int:
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
    now_iter = 0
    # evalで使う安全な辞書を作成
    safe_dict = {
        'z': z,
        'c': c,
        'n': now_iter,
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
    
    while abs(z) <= 2 and now_iter < max_iter:
        safe_dict['z'] = z
        safe_dict['c'] = c
        safe_dict['n'] = now_iter
        try:
            z = eval(formula_str, {"__builtins__": {}}, safe_dict)
        except Exception:
            # 数式が不正な場合は0回で終了
            return 0
        now_iter += 1
    return now_iter


def complex_from_pixel(x: int, y: int, width: int, height: int, 
                      re_start: float, re_end: float, 
                      im_start: float, im_end: float) -> complex:
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


def pixel_color(n: int, max_iter: int) -> int:
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


def generate_mandelbrot_image(width: int, height: int, formula_str: str, 
                            config: dict, max_iter: int = 100) -> QImage:
    """
    マンデルブロ集合の画像を生成する。
    
    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        formula_str (str): ユーザーが入力したzの更新式
        config (dict): 設定情報
        max_iter (int): 最大反復回数
        
    Returns:
        QImage: 生成された画像
    """
    print("generate_mandelbrot_image")
    re_start = config['mandelbrot']['real_range']['start']
    re_end = config['mandelbrot']['real_range']['end']
    im_start = config['mandelbrot']['imaginary_range']['start']
    im_end = config['mandelbrot']['imaginary_range']['end']
    
    image = QImage(width, height, QImage.Format.Format_RGB32)
    for x in range(width):
        for y in range(height):
            c = complex_from_pixel(x, y, width, height, re_start, re_end, im_start, im_end)
            n = mandelbrot_point(c, formula_str, max_iter)
            image.setPixel(x, y, pixel_color(n, max_iter))
    return image
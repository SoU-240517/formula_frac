"""
マンデルブロ集合の数学的計算を担当するコアモジュール。
Numbaを使用した高速化を実装。
"""
import math
import cmath
import numpy as np
from numba import jit, prange
from PyQt6.QtGui import QImage
from logger.custom_logger import logger
import ast
import operator


@jit(nopython=True)
def _mandelbrot_point_basic_jit(c_real: float, c_imag: float, max_iter: int) -> int:
    """
    基本的なマンデルブロ集合の計算（z = z^2 + c）をJITコンパイルで高速化。

    Args:
        c_real (float): 複素数cの実部
        c_imag (float): 複素数cの虚部
        max_iter (int): 最大反復回数

    Returns:
        int: 発散までの反復回数（発散しなければmax_iter）
    """
    z_real = 0.0
    z_imag = 0.0

    for i in range(max_iter):
        # z^2 + c の計算
        z_real_new = z_real * z_real - z_imag * z_imag + c_real
        z_imag_new = 2.0 * z_real * z_imag + c_imag

        # 発散判定
        if z_real_new * z_real_new + z_imag_new * z_imag_new > 4.0:
            return i

        z_real = z_real_new
        z_imag = z_imag_new

    return max_iter


# 式のコンパイル結果をキャッシュ
_compiled_formula_cache = {}


def clear_formula_cache():
    """
    コンパイル済み数式のキャッシュをクリアする。
    メモリ使用量を削減したい場合や、数式の変更が頻繁な場合に使用。
    """
    global _compiled_formula_cache
    cache_size = len(_compiled_formula_cache)
    _compiled_formula_cache.clear()
    logger.info(f"数式キャッシュをクリアしました（{cache_size}個の式）")


def _compile_formula(formula_str: str):
    """
    数式をコンパイルして高速化する。

    Args:
        formula_str (str): 数式文字列

    Returns:
        callable: コンパイルされた関数
    """
    if formula_str in _compiled_formula_cache:
        return _compiled_formula_cache[formula_str]

    try:
        # 安全な関数のマッピング
        safe_functions = {
            'abs': abs,
            'sin': cmath.sin,
            'cos': cmath.cos,
            'exp': cmath.exp,
            'log': cmath.log,
            'pow': pow,
            'sqrt': cmath.sqrt,
            'pi': math.pi,
            'e': math.e,
        }

        # 式をコンパイル
        compiled_code = compile(formula_str, '<string>', 'eval')

        def compiled_func(z, c, n):
            local_vars = {'z': z, 'c': c, 'n': n, **safe_functions}
            return eval(compiled_code, {"__builtins__": {}}, local_vars)

        _compiled_formula_cache[formula_str] = compiled_func
        return compiled_func

    except Exception:
        # コンパイルに失敗した場合は従来のeval方式
        def fallback_func(z, c, n):
            safe_dict = {
                'z': z, 'c': c, 'n': n,
                'abs': abs, 'sin': cmath.sin, 'cos': cmath.cos,
                'exp': cmath.exp, 'log': cmath.log, 'pow': pow,
                'sqrt': cmath.sqrt, 'pi': math.pi, 'e': math.e,
            }
            return eval(formula_str, {"__builtins__": {}}, safe_dict)

        _compiled_formula_cache[formula_str] = fallback_func
        return fallback_func


def mandelbrot_point(c: complex, formula_str: str, max_iter: int = 100) -> int:
    """
    1点分のマンデルブロ集合の発散判定を行い、発散までの反復回数を返す。
    基本的な式（z * z + c）の場合はJIT最適化版を使用し、
    カスタム式の場合はコンパイル済み関数を使用して高速化。

    Args:
        c (complex): 判定する複素数座標
        formula_str (str): ユーザーが入力したzの更新式（例: 'z * z + c'）
        max_iter (int): 最大反復回数

    Returns:
        int: 発散までの反復回数（発散しなければmax_iter）
    """
    # 基本的なマンデルブロ式の場合は高速化版を使用
    if formula_str.strip() in ['z * z + c', 'z**2 + c', 'z*z+c']:
        return _mandelbrot_point_basic_jit(c.real, c.imag, max_iter)

    # カスタム式の場合はコンパイル済み関数を使用
    compiled_func = _compile_formula(formula_str)
    z = 0
    now_iter = 0

    while abs(z) <= 2 and now_iter < max_iter:
        try:
            z = compiled_func(z, c, now_iter)
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


@jit(nopython=True, parallel=True)
def _generate_mandelbrot_grid_jit(width: int, height: int,
                                  re_start: float, re_end: float,
                                  im_start: float, im_end: float,
                                  max_iter: int) -> np.ndarray:
    """
    マンデルブロ集合のグリッド計算をJITコンパイルで並列実行。
    基本的なマンデルブロ式（z = z^2 + c）専用の高速化版。

    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        re_start (float): 実部の開始値
        re_end (float): 実部の終了値
        im_start (float): 虚部の開始値
        im_end (float): 虚部の終了値
        max_iter (int): 最大反復回数

    Returns:
        np.ndarray: 反復回数の2次元配列
    """
    result = np.empty((height, width), dtype=np.int32)

    # 複素平面上のピクセル間隔を計算
    pixel_width_complex = (re_end - re_start) / width
    pixel_height_complex = (im_end - im_start) / height

    # 並列処理でy軸方向をループ
    for y in prange(height):
        c_imag = im_start + y * pixel_height_complex
        for x in range(width):
            c_real = re_start + x * pixel_width_complex
            result[y, x] = _mandelbrot_point_basic_jit(
                c_real, c_imag, max_iter)

    return result


@jit(nopython=True)
def _array_to_rgb_jit(iterations: np.ndarray, max_iter: int) -> np.ndarray:
    """
    反復回数配列をRGB値に変換（JIT最適化版）。

    Args:
        iterations (np.ndarray): 反復回数の2次元配列
        max_iter (int): 最大反復回数

    Returns:
        np.ndarray: RGB値の3次元配列 (height, width, 3)
    """
    height, width = iterations.shape
    rgb_array = np.empty((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            n = iterations[y, x]
            color = 255 - int(n * 255 / max_iter)
            rgb_array[y, x, 0] = color  # R
            rgb_array[y, x, 1] = color  # G
            rgb_array[y, x, 2] = color  # B

    return rgb_array


def _numpy_to_qimage_fast(rgb_array: np.ndarray) -> QImage:
    """
    NumPy RGB配列を効率的にQImageに変換する。

    Args:
        rgb_array (np.ndarray): RGB値の3次元配列 (height, width, 3)

    Returns:
        QImage: 変換された画像
    """
    height, width, channels = rgb_array.shape

    # RGBA形式に変換（アルファチャンネルを追加）
    rgba_array = np.empty((height, width, 4), dtype=np.uint8)
    rgba_array[:, :, 0] = rgb_array[:, :, 2]  # B
    rgba_array[:, :, 1] = rgb_array[:, :, 1]  # G
    rgba_array[:, :, 2] = rgb_array[:, :, 0]  # R
    rgba_array[:, :, 3] = 255  # A (完全不透明)

    # QImageを作成
    bytes_per_line = width * 4
    image = QImage(rgba_array.data, width, height,
                   bytes_per_line, QImage.Format.Format_RGBA8888)

    # データのコピーを作成（メモリ安全性のため）
    return image.copy()


def _generate_mandelbrot_custom_vectorized(width: int, height: int,
                                           re_start: float, re_end: float,
                                           im_start: float, im_end: float,
                                           formula_str: str, max_iter: int) -> np.ndarray:
    """
    カスタム式用のベクトル化された計算（部分的な並列化）。

    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        re_start (float): 実部の開始値
        re_end (float): 実部の終了値
        im_start (float): 虚部の開始値
        im_end (float): 虚部の終了値
        formula_str (str): カスタム数式
        max_iter (int): 最大反復回数

    Returns:
        np.ndarray: 反復回数の2次元配列
    """
    # 複素平面のグリッドを作成
    real_vals = np.linspace(re_start, re_end, width)
    imag_vals = np.linspace(im_start, im_end, height)

    # 結果配列を初期化
    result = np.zeros((height, width), dtype=np.int32)

    # コンパイル済み関数を取得
    compiled_func = _compile_formula(formula_str)

    # 行ごとに処理（メモリ効率を考慮）
    for y in range(height):
        c_imag = imag_vals[y]
        # 1行分の複素数配列を作成
        c_row = real_vals + 1j * c_imag

        # 1行分を並列処理
        for x in range(width):
            c = c_row[x]
            z = 0
            for iteration in range(max_iter):
                if abs(z) > 2:
                    result[y, x] = iteration
                    break
                try:
                    z = compiled_func(z, c, iteration)
                except Exception:
                    result[y, x] = 0
                    break
            else:
                result[y, x] = max_iter

    return result


def generate_mandelbrot_image(width: int, height: int, formula_str: str,
                              config: dict, max_iter: int = 100) -> QImage:
    """
    マンデルブロ集合の画像を生成する。
    基本的な式の場合はJIT最適化版を使用し、大幅な高速化を実現。

    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        formula_str (str): ユーザーが入力したzの更新式
        config (dict): 設定情報
        max_iter (int): 最大反復回数

    Returns:
        QImage: 生成された画像
    """
    logger.debug(
        f"画像生成を開始: {width}x{height}, 式: '{formula_str}', 最大反復: {max_iter}")
    re_start = config['mandelbrot']['real_range']['start']
    re_end = config['mandelbrot']['real_range']['end']
    im_start = config['mandelbrot']['imaginary_range']['start']
    im_end = config['mandelbrot']['imaginary_range']['end']

    logger.debug(f"複素平面範囲: 実部[{re_start}, {re_end}], 虚部[{im_start}, {im_end}]")

    # 基本的なマンデルブロ式の場合は高速化版を使用
    if formula_str.strip() in ['z * z + c', 'z**2 + c', 'z*z+c']:
        logger.info("高速化版（JIT最適化）を使用します")
        try:
            # JIT最適化版で計算
            iterations = _generate_mandelbrot_grid_jit(
                width, height, re_start, re_end, im_start, im_end, max_iter
            )

            # RGB配列に変換
            rgb_array = _array_to_rgb_jit(iterations, max_iter)

            # 効率的にQImageに変換
            logger.debug("高速化版での画像生成が完了しました")
            return _numpy_to_qimage_fast(rgb_array)

        except Exception as e:
            logger.warning(f"高速化版でエラーが発生しました: {e}")
            logger.info("従来版にフォールバックします")
            # 従来版にフォールバック

    # カスタム式の場合は最適化版を使用
    logger.info("カスタム式最適化版を使用します")
    try:
        # ベクトル化された計算を実行
        iterations = _generate_mandelbrot_custom_vectorized(
            width, height, re_start, re_end, im_start, im_end, formula_str, max_iter
        )

        # RGB配列に変換
        rgb_array = _array_to_rgb_jit(iterations, max_iter)

        # 効率的にQImageに変換
        logger.debug("カスタム式最適化版での画像生成が完了しました")
        return _numpy_to_qimage_fast(rgb_array)

    except Exception as e:
        logger.warning(f"カスタム式最適化版でエラーが発生しました: {e}")
        logger.info("従来版にフォールバックします")

        # 従来版にフォールバック
        image = QImage(width, height, QImage.Format.Format_RGB32)
        total_pixels = width * height
        processed_pixels = 0

        for x in range(width):
            for y in range(height):
                c = complex_from_pixel(
                    x, y, width, height, re_start, re_end, im_start, im_end)
                n = mandelbrot_point(c, formula_str, max_iter)
                image.setPixel(x, y, pixel_color(n, max_iter))
                processed_pixels += 1

                # 進捗をログ出力（10%刻み）
                if processed_pixels % (total_pixels // 10) == 0:
                    progress = (processed_pixels / total_pixels) * 100
                    logger.debug(f"従来版処理進捗: {progress:.0f}%")

        logger.debug("従来版での画像生成が完了しました")
        return image

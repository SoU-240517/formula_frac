"""
座標変換モジュール - ピクセル座標と複素平面座標の相互変換を担当
"""
from typing import Dict, Tuple
from PyQt6.QtCore import QPoint, QSize
import math


class CoordinateTransform:
    """
    ピクセル座標と複素平面座標の変換を担当するクラス
    ズーム・パン操作に対応した座標変換機能を提供
    """
    
    @staticmethod
    def pixel_to_complex(pixel_x: int, pixel_y: int, 
                        widget_width: int, widget_height: int,
                        complex_region: Dict[str, float], zoom_factor: float = 1.0, 
                        pan_offset: QPoint = QPoint(0, 0)) -> complex:
        """
        ピクセル座標を複素平面座標に変換する
        
        Args:
            pixel_x: ピクセルのX座標
            pixel_y: ピクセルのY座標
            widget_width: ウィジェットの幅
            widget_height: ウィジェットの高さ
            complex_region: 複素平面の範囲辞書
            zoom_factor: ズーム倍率（デフォルト: 1.0）
            pan_offset: パンオフセット（デフォルト: (0, 0)）
            
        Returns:
            complex: 複素平面座標
            
        Raises:
            ValueError: 無効な座標値が渡された場合
        """
        try:
            # 入力値の検証
            if widget_width <= 0 or widget_height <= 0:
                raise ValueError("ウィジェットサイズは正の値である必要があります")
            
            if zoom_factor <= 0:
                raise ValueError("ズーム倍率は正の値である必要があります")
            
            # パンオフセットを適用
            adjusted_x = pixel_x - pan_offset.x()
            adjusted_y = pixel_y - pan_offset.y()
            
            # ピクセル座標を正規化（0.0-1.0の範囲）
            norm_x = adjusted_x / widget_width
            norm_y = adjusted_y / widget_height
            
            # 複素平面の範囲を取得
            real_start = complex_region["real_start"]
            real_end = complex_region["real_end"]
            imag_start = complex_region["imaginary_start"]
            imag_end = complex_region["imaginary_end"]
            
            # ズーム倍率を適用した範囲を計算
            real_width = (real_end - real_start) / zoom_factor
            imag_height = (imag_end - imag_start) / zoom_factor
            
            # 中心点を計算
            real_center = (real_start + real_end) / 2
            imag_center = (imag_start + imag_end) / 2
            
            # ズーム後の範囲を計算
            zoomed_real_start = real_center - real_width / 2
            zoomed_imag_start = imag_center - imag_height / 2
            
            # 複素平面座標を計算
            real_part = zoomed_real_start + norm_x * real_width
            imag_part = zoomed_imag_start + norm_y * imag_height
            
            return complex(real_part, imag_part)
            
        except Exception as e:
            raise ValueError(f"座標変換エラー: {e}")
    
    @staticmethod  
    def complex_to_pixel(complex_point: complex,
                        widget_width: int, widget_height: int,
                        complex_region: Dict[str, float], zoom_factor: float = 1.0,
                        pan_offset: QPoint = QPoint(0, 0)) -> QPoint:
        """
        複素平面座標をピクセル座標に変換する
        
        Args:
            complex_point: 複素平面座標
            widget_width: ウィジェットの幅
            widget_height: ウィジェットの高さ
            complex_region: 複素平面の範囲辞書
            zoom_factor: ズーム倍率（デフォルト: 1.0）
            pan_offset: パンオフセット（デフォルト: (0, 0)）
            
        Returns:
            QPoint: ピクセル座標
            
        Raises:
            ValueError: 無効な座標値が渡された場合
        """
        try:
            # 入力値の検証
            if widget_width <= 0 or widget_height <= 0:
                raise ValueError("ウィジェットサイズは正の値である必要があります")
            
            if zoom_factor <= 0:
                raise ValueError("ズーム倍率は正の値である必要があります")
            
            # 複素平面の範囲を取得
            real_start = complex_region["real_start"]
            real_end = complex_region["real_end"]
            imag_start = complex_region["imaginary_start"]
            imag_end = complex_region["imaginary_end"]
            
            # ズーム倍率を適用した範囲を計算
            real_width = (real_end - real_start) / zoom_factor
            imag_height = (imag_end - imag_start) / zoom_factor
            
            # 中心点を計算
            real_center = (real_start + real_end) / 2
            imag_center = (imag_start + imag_end) / 2
            
            # ズーム後の範囲を計算
            zoomed_real_start = real_center - real_width / 2
            zoomed_imag_start = imag_center - imag_height / 2
            
            # 正規化座標を計算
            norm_x = (complex_point.real - zoomed_real_start) / real_width
            norm_y = (complex_point.imag - zoomed_imag_start) / imag_height
            
            # ピクセル座標を計算
            pixel_x = int(norm_x * widget_width)
            pixel_y = int(norm_y * widget_height)
            
            # パンオフセットを適用
            adjusted_x = pixel_x + pan_offset.x()
            adjusted_y = pixel_y + pan_offset.y()
            
            return QPoint(adjusted_x, adjusted_y)
            
        except Exception as e:
            raise ValueError(f"座標変換エラー: {e}")
    
    @staticmethod
    def calculate_zoom_region(original_region: Dict[str, float], zoom_center: complex,
                             zoom_factor: float) -> Dict[str, float]:
        """
        ズーム操作後の新しい複素平面範囲を計算する
        
        Args:
            original_region: 元の複素平面範囲
            zoom_center: ズームの中心点
            zoom_factor: ズーム倍率
            
        Returns:
            Dict[str, float]: 新しい複素平面範囲
            
        Raises:
            ValueError: 無効なズーム倍率が渡された場合
        """
        try:
            if zoom_factor <= 0:
                raise ValueError("ズーム倍率は正の値である必要があります")
            
            # 元の範囲を取得
            real_start = original_region["real_start"]
            real_end = original_region["real_end"]
            imag_start = original_region["imaginary_start"]
            imag_end = original_region["imaginary_end"]
            
            # 新しい範囲の幅と高さを計算
            new_real_width = (real_end - real_start) / zoom_factor
            new_imag_height = (imag_end - imag_start) / zoom_factor
            
            # ズーム中心を基準に新しい範囲を計算
            new_real_start = zoom_center.real - new_real_width / 2
            new_real_end = zoom_center.real + new_real_width / 2
            new_imag_start = zoom_center.imag - new_imag_height / 2
            new_imag_end = zoom_center.imag + new_imag_height / 2
            
            return {
                "real_start": new_real_start,
                "real_end": new_real_end,
                "imaginary_start": new_imag_start,
                "imaginary_end": new_imag_end,
                "width": new_real_width,
                "height": new_imag_height
            }
            
        except Exception as e:
            raise ValueError(f"ズーム範囲計算エラー: {e}")
    
    @staticmethod
    def calculate_pan_region(current_region: Dict[str, float], pan_delta: QPoint,
                           widget_size: QSize, zoom_factor: float = 1.0) -> Dict[str, float]:
        """
        パン操作後の新しい複素平面範囲を計算する
        
        Args:
            current_region: 現在の複素平面範囲
            pan_delta: パンの移動量（ピクセル）
            widget_size: ウィジェットのサイズ
            zoom_factor: 現在のズーム倍率（デフォルト: 1.0）
            
        Returns:
            Dict[str, float]: 新しい複素平面範囲
            
        Raises:
            ValueError: 無効なパラメータが渡された場合
        """
        try:
            if widget_size.width() <= 0 or widget_size.height() <= 0:
                raise ValueError("ウィジェットサイズは正の値である必要があります")
            
            if zoom_factor <= 0:
                raise ValueError("ズーム倍率は正の値である必要があります")
            
            # 現在の範囲を取得
            real_start = current_region["real_start"]
            real_end = current_region["real_end"]
            imag_start = current_region["imaginary_start"]
            imag_end = current_region["imaginary_end"]
            
            # 複素平面での移動量を計算
            real_width = (real_end - real_start) / zoom_factor
            imag_height = (imag_end - imag_start) / zoom_factor
            
            # ピクセル移動量を複素平面移動量に変換
            real_delta = (pan_delta.x() / widget_size.width()) * real_width
            imag_delta = (pan_delta.y() / widget_size.height()) * imag_height
            
            # 新しい範囲を計算（パンは逆方向に移動）
            new_real_start = real_start - real_delta
            new_real_end = real_end - real_delta
            new_imag_start = imag_start - imag_delta
            new_imag_end = imag_end - imag_delta
            
            return {
                "real_start": new_real_start,
                "real_end": new_real_end,
                "imaginary_start": new_imag_start,
                "imaginary_end": new_imag_end,
                "width": new_real_end - new_real_start,
                "height": new_imag_end - new_imag_start
            }
            
        except Exception as e:
            raise ValueError(f"パン範囲計算エラー: {e}")
    
    @staticmethod
    def clamp_zoom_factor(zoom_factor: float, min_zoom: float = 0.1, 
                         max_zoom: float = 100.0) -> float:
        """
        ズーム倍率を指定された範囲内にクランプする
        
        Args:
            zoom_factor: クランプするズーム倍率
            min_zoom: 最小ズーム倍率（デフォルト: 0.1）
            max_zoom: 最大ズーム倍率（デフォルト: 100.0）
            
        Returns:
            float: クランプされたズーム倍率
        """
        return max(min_zoom, min(max_zoom, zoom_factor))
    
    @staticmethod
    def validate_complex_region(region: Dict[str, float]) -> bool:
        """
        複素平面範囲の妥当性を検証する
        
        Args:
            region: 検証する複素平面範囲
            
        Returns:
            bool: 妥当な場合True、そうでなければFalse
        """
        try:
            required_keys = ["real_start", "real_end", "imaginary_start", "imaginary_end"]
            
            # 必要なキーが存在するかチェック
            for key in required_keys:
                if key not in region:
                    return False
            
            # 範囲の妥当性をチェック
            if region["real_start"] >= region["real_end"]:
                return False
            
            if region["imaginary_start"] >= region["imaginary_end"]:
                return False
            
            # 数値型かチェック
            for key in required_keys:
                if not isinstance(region[key], (int, float)):
                    return False
            
            return True
            
        except Exception:
            return False
"""
座標変換モジュールの単体テスト
"""
import unittest
import math
from PyQt6.QtCore import QPoint, QSize
from coordinate_transform import CoordinateTransform


class TestCoordinateTransform(unittest.TestCase):
    """座標変換機能のテストクラス"""
    
    def setUp(self):
        """テスト用の基本設定"""
        self.widget_width = 800
        self.widget_height = 600
        self.complex_region = {
            "real_start": -2.0,
            "real_end": 1.0,
            "imaginary_start": -1.2,
            "imaginary_end": 1.2,
            "width": 3.0,
            "height": 2.4
        }
    
    def test_pixel_to_complex_basic(self):
        """基本的なピクセル→複素平面座標変換のテスト"""
        # 中心点のテスト
        center_x = self.widget_width // 2
        center_y = self.widget_height // 2
        
        result = CoordinateTransform.pixel_to_complex(
            center_x, center_y, 
            self.widget_width, self.widget_height,
            self.complex_region
        )
        
        expected_real = (self.complex_region["real_start"] + self.complex_region["real_end"]) / 2
        expected_imag = (self.complex_region["imaginary_start"] + self.complex_region["imaginary_end"]) / 2
        
        self.assertAlmostEqual(result.real, expected_real, places=5)
        self.assertAlmostEqual(result.imag, expected_imag, places=5)
    
    def test_pixel_to_complex_corners(self):
        """四隅のピクセル→複素平面座標変換のテスト"""
        # 左上角 (0, 0)
        result_tl = CoordinateTransform.pixel_to_complex(
            0, 0, self.widget_width, self.widget_height, self.complex_region
        )
        self.assertAlmostEqual(result_tl.real, self.complex_region["real_start"], places=5)
        self.assertAlmostEqual(result_tl.imag, self.complex_region["imaginary_start"], places=5)
        
        # 右下角 (width, height)
        result_br = CoordinateTransform.pixel_to_complex(
            self.widget_width, self.widget_height, 
            self.widget_width, self.widget_height, self.complex_region
        )
        self.assertAlmostEqual(result_br.real, self.complex_region["real_end"], places=5)
        self.assertAlmostEqual(result_br.imag, self.complex_region["imaginary_end"], places=5)
    
    def test_complex_to_pixel_basic(self):
        """基本的な複素平面→ピクセル座標変換のテスト"""
        # 中心点のテスト
        center_complex = complex(-0.5, 0.0)  # 複素平面の中心
        
        result = CoordinateTransform.complex_to_pixel(
            center_complex, self.widget_width, self.widget_height, self.complex_region
        )
        
        expected_x = self.widget_width // 2
        expected_y = self.widget_height // 2
        
        self.assertAlmostEqual(result.x(), expected_x, delta=1)
        self.assertAlmostEqual(result.y(), expected_y, delta=1)
    
    def test_coordinate_conversion_roundtrip(self):
        """座標変換の往復精度テスト"""
        test_points = [
            (100, 150),
            (400, 300),
            (700, 450),
            (0, 0),
            (self.widget_width, self.widget_height)
        ]
        
        for pixel_x, pixel_y in test_points:
            # ピクセル → 複素平面 → ピクセル
            complex_point = CoordinateTransform.pixel_to_complex(
                pixel_x, pixel_y, self.widget_width, self.widget_height, self.complex_region
            )
            
            back_to_pixel = CoordinateTransform.complex_to_pixel(
                complex_point, self.widget_width, self.widget_height, self.complex_region
            )
            
            self.assertAlmostEqual(back_to_pixel.x(), pixel_x, delta=1)
            self.assertAlmostEqual(back_to_pixel.y(), pixel_y, delta=1)
    
    def test_zoom_factor_application(self):
        """ズーム倍率適用のテスト"""
        zoom_factor = 2.0
        center_x = self.widget_width // 2
        center_y = self.widget_height // 2
        
        # ズームなしの場合
        result_no_zoom = CoordinateTransform.pixel_to_complex(
            center_x, center_y, self.widget_width, self.widget_height, 
            self.complex_region, zoom_factor=1.0
        )
        
        # 2倍ズームの場合
        result_zoom = CoordinateTransform.pixel_to_complex(
            center_x, center_y, self.widget_width, self.widget_height, 
            self.complex_region, zoom_factor=zoom_factor
        )
        
        # ズーム時は範囲が狭くなるため、同じピクセル位置でも複素平面座標は同じ（中心点）
        self.assertAlmostEqual(result_no_zoom.real, result_zoom.real, places=5)
        self.assertAlmostEqual(result_no_zoom.imag, result_zoom.imag, places=5)
    
    def test_pan_offset_application(self):
        """パンオフセット適用のテスト"""
        pan_offset = QPoint(50, 30)
        test_x, test_y = 400, 300
        
        # パンなしの場合
        result_no_pan = CoordinateTransform.pixel_to_complex(
            test_x, test_y, self.widget_width, self.widget_height, self.complex_region
        )
        
        # パンありの場合
        result_pan = CoordinateTransform.pixel_to_complex(
            test_x, test_y, self.widget_width, self.widget_height, 
            self.complex_region, pan_offset=pan_offset
        )
        
        # パンオフセットにより複素平面座標が変化することを確認
        self.assertNotAlmostEqual(result_no_pan.real, result_pan.real, places=5)
        self.assertNotAlmostEqual(result_no_pan.imag, result_pan.imag, places=5)
    
    def test_calculate_zoom_region(self):
        """ズーム範囲計算のテスト"""
        zoom_center = complex(-0.5, 0.0)
        zoom_factor = 2.0
        
        result = CoordinateTransform.calculate_zoom_region(
            self.complex_region, zoom_center, zoom_factor
        )
        
        # ズーム後の範囲は元の範囲の1/zoom_factor倍になる
        expected_width = self.complex_region["width"] / zoom_factor
        expected_height = self.complex_region["height"] / zoom_factor
        
        self.assertAlmostEqual(result["width"], expected_width, places=5)
        self.assertAlmostEqual(result["height"], expected_height, places=5)
        
        # ズーム中心が新しい範囲の中心になることを確認
        center_real = (result["real_start"] + result["real_end"]) / 2
        center_imag = (result["imaginary_start"] + result["imaginary_end"]) / 2
        
        self.assertAlmostEqual(center_real, zoom_center.real, places=5)
        self.assertAlmostEqual(center_imag, zoom_center.imag, places=5)
    
    def test_calculate_pan_region(self):
        """パン範囲計算のテスト"""
        pan_delta = QPoint(100, 50)  # 右に100px、下に50px移動
        widget_size = QSize(self.widget_width, self.widget_height)
        
        result = CoordinateTransform.calculate_pan_region(
            self.complex_region, pan_delta, widget_size
        )
        
        # パン後も範囲のサイズは変わらない
        self.assertAlmostEqual(result["width"], self.complex_region["width"], places=5)
        self.assertAlmostEqual(result["height"], self.complex_region["height"], places=5)
        
        # パン方向と逆方向に範囲が移動することを確認
        real_shift = result["real_start"] - self.complex_region["real_start"]
        imag_shift = result["imaginary_start"] - self.complex_region["imaginary_start"]
        
        # 右にパンすると複素平面は左に移動（負の方向）
        self.assertLess(real_shift, 0)
        # 下にパンすると複素平面は上に移動（負の方向）
        self.assertLess(imag_shift, 0)
    
    def test_clamp_zoom_factor(self):
        """ズーム倍率クランプのテスト"""
        # 正常範囲内
        self.assertEqual(CoordinateTransform.clamp_zoom_factor(1.0), 1.0)
        self.assertEqual(CoordinateTransform.clamp_zoom_factor(5.0), 5.0)
        
        # 最小値以下
        self.assertEqual(CoordinateTransform.clamp_zoom_factor(0.05), 0.1)
        
        # 最大値以上
        self.assertEqual(CoordinateTransform.clamp_zoom_factor(150.0), 100.0)
        
        # カスタム範囲
        self.assertEqual(
            CoordinateTransform.clamp_zoom_factor(0.5, min_zoom=1.0, max_zoom=10.0), 
            1.0
        )
    
    def test_validate_complex_region(self):
        """複素平面範囲検証のテスト"""
        # 正常な範囲
        self.assertTrue(CoordinateTransform.validate_complex_region(self.complex_region))
        
        # 不正な範囲（real_start >= real_end）
        invalid_region1 = self.complex_region.copy()
        invalid_region1["real_start"] = 2.0
        self.assertFalse(CoordinateTransform.validate_complex_region(invalid_region1))
        
        # 不正な範囲（imaginary_start >= imaginary_end）
        invalid_region2 = self.complex_region.copy()
        invalid_region2["imaginary_start"] = 2.0
        self.assertFalse(CoordinateTransform.validate_complex_region(invalid_region2))
        
        # キーが不足
        invalid_region3 = {"real_start": -2.0, "real_end": 1.0}
        self.assertFalse(CoordinateTransform.validate_complex_region(invalid_region3))
    
    def test_error_handling(self):
        """エラーハンドリングのテスト"""
        # 無効なウィジェットサイズ
        with self.assertRaises(ValueError):
            CoordinateTransform.pixel_to_complex(
                100, 100, 0, 600, self.complex_region
            )
        
        with self.assertRaises(ValueError):
            CoordinateTransform.pixel_to_complex(
                100, 100, 800, -600, self.complex_region
            )
        
        # 無効なズーム倍率
        with self.assertRaises(ValueError):
            CoordinateTransform.pixel_to_complex(
                100, 100, 800, 600, self.complex_region, zoom_factor=0
            )
        
        with self.assertRaises(ValueError):
            CoordinateTransform.calculate_zoom_region(
                self.complex_region, complex(0, 0), -1.0
            )
    
    def test_precision_at_high_zoom(self):
        """高ズーム時の精度テスト"""
        high_zoom = 50.0
        center_x = self.widget_width // 2
        center_y = self.widget_height // 2
        
        # 高ズーム時の座標変換
        result = CoordinateTransform.pixel_to_complex(
            center_x, center_y, self.widget_width, self.widget_height,
            self.complex_region, zoom_factor=high_zoom
        )
        
        # 往復変換での精度確認
        back_to_pixel = CoordinateTransform.complex_to_pixel(
            result, self.widget_width, self.widget_height,
            self.complex_region, zoom_factor=high_zoom
        )
        
        self.assertAlmostEqual(back_to_pixel.x(), center_x, delta=2)
        self.assertAlmostEqual(back_to_pixel.y(), center_y, delta=2)


if __name__ == '__main__':
    unittest.main()
"""
最適化機能のテストスクリプト。
"""
import json
import time
from mandelbrot_core import generate_mandelbrot_image
from numba_utils import configure_numba


def test_basic_functionality():
    """基本的な機能をテストする"""
    print("=== 基本機能テスト ===")
    
    # Numbaを初期化
    configure_numba(cache_enabled=True)
    
    # 設定を読み込み
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 小さな画像でテスト
    width, height = 200, 150
    max_iter = 50
    
    test_cases = [
        "z * z + c",      # 高速化対象
        "z**2 + c",       # 高速化対象
        "z * z * z + c",  # 従来版
    ]
    
    for formula in test_cases:
        print(f"\nテスト式: '{formula}'")
        start_time = time.time()
        
        try:
            image = generate_mandelbrot_image(width, height, formula, config, max_iter)
            end_time = time.time()
            
            print(f"  成功: {end_time - start_time:.3f}秒")
            print(f"  画像サイズ: {image.width()}x{image.height()}")
            
        except Exception as e:
            print(f"  エラー: {e}")
    
    print("\n=== テスト完了 ===")


if __name__ == "__main__":
    test_basic_functionality()
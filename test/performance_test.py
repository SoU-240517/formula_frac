"""
カスタム式の高速化テスト用スクリプト
"""
import time
import json
from mandelbrot_core import generate_mandelbrot_image, clear_formula_cache

def test_formula_performance():
    """様々な数式でパフォーマンステストを実行"""
    
    # 設定を読み込み
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # テスト用の数式リスト
    test_formulas = [
        'z * z + c',  # 基本式（JIT最適化）
        'z**2 + c',   # 基本式の別表記
        'z**3 + c',   # 3次式
        'z**2 + c + 0.1*z',  # 複雑な式
        'sin(z) + c', # 三角関数
        'z**2 + c*cos(z)', # より複雑な式
    ]
    
    width, height = 400, 400  # テスト用サイズ
    max_iter = 100
    
    print("カスタム式高速化テスト")
    print("=" * 50)
    
    for formula in test_formulas:
        print(f"\n数式: {formula}")
        
        # 1回目（コンパイル時間含む）
        start_time = time.time()
        image1 = generate_mandelbrot_image(width, height, formula, config, max_iter)
        first_time = time.time() - start_time
        
        # 2回目（キャッシュ利用）
        start_time = time.time()
        image2 = generate_mandelbrot_image(width, height, formula, config, max_iter)
        second_time = time.time() - start_time
        
        print(f"  1回目: {first_time:.3f}秒 (コンパイル含む)")
        print(f"  2回目: {second_time:.3f}秒 (キャッシュ利用)")
        print(f"  高速化率: {first_time/second_time:.2f}倍")
    
    # キャッシュクリア
    clear_formula_cache()
    print("\n数式キャッシュをクリアしました")

if __name__ == "__main__":
    test_formula_performance()
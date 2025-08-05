"""
カスタム式の高速化テスト用スクリプト
"""
import sys
import os
import time
import json

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mandelbrot_core import generate_mandelbrot_image, clear_formula_cache

def test_formula_performance():
    """様々な数式でパフォーマンステストを実行"""
    
    # 設定を読み込み（プロジェクトルートからの相対パス）
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # テスト用の数式リスト
    test_formulas = [
        ('z * z + c', 'JIT最適化対象の基本式'),
        ('z**2 + c', 'JIT最適化対象の基本式（別表記）'),
        ('z**3 + c', '3次式'),
        ('z**2 + c + 0.1*z', '線形項を含む複雑な式'),
        ('sin(z) + c', '三角関数を含む式'),
        ('z**2 + c*cos(z)', '三角関数と乗算を含む複雑な式'),
    ]
    
    width, height = 400, 400  # テスト用サイズ
    max_iter = 100
    
    print("カスタム式高速化テスト")
    print("=" * 50)
    print(f"テスト条件: {width}x{height}ピクセル, 最大反復回数: {max_iter}")
    print()
    
    total_results = []
    
    for formula, description in test_formulas:
        print(f"数式: {formula}")
        print(f"説明: {description}")
        
        try:
            # 1回目（コンパイル時間含む）
            start_time = time.time()
            image1 = generate_mandelbrot_image(width, height, formula, config, max_iter)
            first_time = time.time() - start_time
            
            # 2回目（キャッシュ利用）
            start_time = time.time()
            image2 = generate_mandelbrot_image(width, height, formula, config, max_iter)
            second_time = time.time() - start_time
            
            # 3回目（安定性確認）
            start_time = time.time()
            image3 = generate_mandelbrot_image(width, height, formula, config, max_iter)
            third_time = time.time() - start_time
            
            print(f"  1回目: {first_time:.3f}秒 (コンパイル含む)")
            print(f"  2回目: {second_time:.3f}秒 (キャッシュ利用)")
            print(f"  3回目: {third_time:.3f}秒 (安定性確認)")
            
            if second_time > 0:
                speedup = first_time / second_time
                print(f"  高速化率: {speedup:.2f}倍")
                total_results.append((formula, first_time, second_time, speedup))
            else:
                print(f"  高速化率: 測定不可（2回目が高速すぎます）")
                total_results.append((formula, first_time, second_time, float('inf')))
                
        except Exception as e:
            print(f"  エラー: {e}")
            total_results.append((formula, 0, 0, 0))
        
        print("-" * 50)
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("テスト結果サマリー")
    print("=" * 50)
    
    if total_results:
        print(f"{'数式':<20} {'1回目(秒)':<10} {'2回目(秒)':<10} {'高速化率':<8}")
        print("-" * 50)
        
        for formula, first, second, speedup in total_results:
            if speedup == float('inf'):
                speedup_str = "∞"
            elif speedup == 0:
                speedup_str = "エラー"
            else:
                speedup_str = f"{speedup:.2f}x"
            
            # 数式が長い場合は短縮
            short_formula = formula[:18] + ".." if len(formula) > 20 else formula
            print(f"{short_formula:<20} {first:<10.3f} {second:<10.3f} {speedup_str:<8}")
    
    # キャッシュクリア
    clear_formula_cache()
    print(f"\n数式キャッシュをクリアしました")

if __name__ == "__main__":
    test_formula_performance()
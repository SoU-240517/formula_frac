"""
フラクタル描画のベンチマークツール。
最適化前後の性能を比較できます。
"""
import time
import json
from mandelbrot_core import generate_mandelbrot_image
from numba_utils import configure_numba, get_numba_info


def load_config():
    """設定ファイルを読み込む"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def benchmark_mandelbrot(width=800, height=600, iterations=100, formula="z * z + c"):
    """
    マンデルブロ集合の描画性能をベンチマークする。
    
    Args:
        width (int): 画像の幅
        height (int): 画像の高さ
        iterations (int): 最大反復回数
        formula (str): 計算式
    """
    print(f"ベンチマーク開始:")
    print(f"  画像サイズ: {width}x{height}")
    print(f"  最大反復回数: {iterations}")
    print(f"  計算式: '{formula}'")
    print()
    
    # 設定を読み込み
    config = load_config()
    config['mandelbrot']['max_iterations'] = iterations
    
    # ベンチマーク実行
    start_time = time.time()
    image = generate_mandelbrot_image(width, height, formula, config, iterations)
    end_time = time.time()
    
    calculation_time = end_time - start_time
    pixels_per_second = (width * height) / calculation_time
    
    print(f"結果:")
    print(f"  計算時間: {calculation_time:.3f}秒")
    print(f"  処理速度: {pixels_per_second:,.0f} ピクセル/秒")
    print(f"  画像生成: 成功 ({image.width()}x{image.height()})")
    print()
    
    return calculation_time, pixels_per_second


def main():
    """ベンチマークのメイン実行"""
    print("=== フラクタル描画ベンチマーク ===")
    print()
    
    # Numba情報を表示
    configure_numba(cache_enabled=True)
    get_numba_info()
    print()
    
    # 複数のテストケース
    test_cases = [
        {"width": 400, "height": 300, "iterations": 50, "formula": "z * z + c"},
        {"width": 800, "height": 600, "iterations": 100, "formula": "z * z + c"},
        {"width": 800, "height": 600, "iterations": 100, "formula": "z**2 + c"},
        {"width": 800, "height": 600, "iterations": 100, "formula": "z * z * z + c"},  # カスタム式
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"テストケース {i}:")
        time_taken, speed = benchmark_mandelbrot(**test_case)
        results.append((test_case, time_taken, speed))
        print("-" * 50)
    
    # 結果サマリー
    print("=== ベンチマーク結果サマリー ===")
    for i, (test_case, time_taken, speed) in enumerate(results, 1):
        optimization = "JIT最適化" if test_case["formula"] in ["z * z + c", "z**2 + c"] else "従来版"
        print(f"テスト{i}: {time_taken:.3f}秒, {speed:,.0f} px/s ({optimization})")


if __name__ == "__main__":
    main()
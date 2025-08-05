# 設計書

## 概要

マンデルブロ集合ビジュアライザーにマウスによる拡縮・パン機能を追加します。この機能は既存のアーキテクチャを拡張し、`MandelbrotWindow`クラスに新しいマウスイベント処理機能を追加し、座標変換とリアルタイム更新機能を実装します。

## アーキテクチャ

### 既存アーキテクチャとの統合

現在のアーキテクチャ：
- **GUI層**: `MandelbrotWindow` - PyQt6 UIコンポーネント
- **計算層**: `mandelbrot_core.py` - フラクタル数学ロジック  
- **ワーカー層**: `MandelbrotWorker` - QThread非同期処理
- **最適化層**: `numba_utils.py` - パフォーマンス最適化

### 新機能の統合点

1. **MandelbrotWindow拡張**: マウスイベント処理とUI状態管理
2. **座標変換モジュール**: ピクセル座標と複素平面座標の相互変換
3. **設定拡張**: config.jsonにズーム・パン関連設定を追加

## コンポーネントと インターフェース

### 1. MandelbrotWindow拡張

#### 新しい属性
```python
class MandelbrotWindow(QMainWindow):
    # ズーム・パン状態
    zoom_factor: float = 1.0
    pan_offset: QPoint = QPoint(0, 0)
    
    # マウス操作状態
    is_panning: bool = False
    last_pan_point: QPoint = QPoint()
    
    # 複素平面範囲
    current_complex_region: dict
    original_complex_region: dict
    
    # 設定
    zoom_sensitivity: float
    min_zoom: float
    max_zoom: float
    update_delay_ms: int
    
    # タイマー
    update_timer: QTimer
```

#### 新しいメソッド
```python
# マウスイベントハンドラ
def wheelEvent(self, event: QWheelEvent) -> None
def mousePressEvent(self, event: QMouseEvent) -> None  
def mouseMoveEvent(self, event: QMouseEvent) -> None
def mouseReleaseEvent(self, event: QMouseEvent) -> None
def mouseDoubleClickEvent(self, event: QMouseEvent) -> None

# 座標変換
def pixel_to_complex(self, pixel_x: int, pixel_y: int) -> complex
def complex_to_pixel(self, complex_point: complex) -> QPoint

# 表示更新
def update_display_immediate(self) -> None
def schedule_image_regeneration(self) -> None
def reset_view(self) -> None

# 設定管理
def load_zoom_pan_config(self) -> None
def update_complex_region(self) -> None
```

### 2. 座標変換モジュール (coordinate_transform.py)

```python
class CoordinateTransform:
    """ピクセル座標と複素平面座標の変換を担当"""
    
    @staticmethod
    def pixel_to_complex(pixel_x: int, pixel_y: int, 
                        widget_width: int, widget_height: int,
                        complex_region: dict, zoom_factor: float, 
                        pan_offset: QPoint) -> complex:
        """ピクセル座標を複素平面座標に変換"""
        
    @staticmethod  
    def complex_to_pixel(complex_point: complex,
                        widget_width: int, widget_height: int,
                        complex_region: dict, zoom_factor: float,
                        pan_offset: QPoint) -> QPoint:
        """複素平面座標をピクセル座標に変換"""
        
    @staticmethod
    def calculate_zoom_region(original_region: dict, zoom_center: complex,
                             zoom_factor: float) -> dict:
        """ズーム操作後の新しい複素平面範囲を計算"""
        
    @staticmethod
    def calculate_pan_region(current_region: dict, pan_delta: QPoint,
                           widget_size: QSize, zoom_factor: float) -> dict:
        """パン操作後の新しい複素平面範囲を計算"""
```

### 3. 画像表示の拡張

#### 即座の視覚フィードバック
- 既存のQPixmapを変形（スケール・移動）して即座に表示
- 操作完了後に高品質な画像を再生成

#### プログレッシブレンダリング
- 低解像度での高速プレビュー
- 段階的に解像度を向上

## データモデル

### 複素平面範囲の表現
```python
complex_region = {
    "real_start": float,
    "real_end": float, 
    "imaginary_start": float,
    "imaginary_end": float,
    "width": float,  # real_end - real_start
    "height": float  # imaginary_end - imaginary_start
}
```

### ズーム・パン状態
```python
zoom_pan_state = {
    "zoom_factor": float,
    "pan_offset_x": int,
    "pan_offset_y": int,
    "complex_region": complex_region,
    "is_panning": bool
}
```

### 設定拡張 (config.json)
```json
{
  "zoom_pan": {
    "zoom_sensitivity": 0.1,
    "min_zoom": 0.1,
    "max_zoom": 100.0,
    "update_delay_ms": 100,
    "smooth_updates": true,
    "progressive_rendering": true
  }
}
```

## エラーハンドリング

### 座標変換エラー
- 無効な座標値の検出とクランプ
- オーバーフロー/アンダーフローの防止
- ログ記録と安全なフォールバック

### メモリ管理
- 高ズーム時の解像度制限
- 画像生成失敗時の前画像保持
- メモリ不足時の自動品質調整

### UI応答性
- 連続操作時の重複処理防止
- タイマーベースの遅延実行
- 操作中断時の安全な状態復帰

## テスト戦略

### 単体テスト
1. **座標変換テスト**
   - ピクセル↔複素平面座標の往復変換精度
   - 境界値での変換正確性
   - ズーム・パン適用時の変換

2. **ズーム計算テスト**
   - 各ズーム倍率での領域計算
   - ズーム中心点の保持
   - 最小・最大ズーム制限

3. **パン計算テスト**
   - パン距離と複素平面移動の対応
   - 境界での安全な処理
   - 連続パン操作の累積精度

### 統合テスト
1. **マウス操作テスト**
   - ホイールズームの動作確認
   - ドラッグパンの動作確認
   - ダブルクリックリセットの動作確認

2. **画像更新テスト**
   - 操作後の画像再生成
   - リアルタイム表示更新
   - エラー時の安全な動作

3. **パフォーマンステスト**
   - 高ズーム時の応答性
   - 連続操作時のメモリ使用量
   - 大きな画像サイズでの動作

### UI/UXテスト
1. **操作性テスト**
   - 直感的なズーム・パン操作
   - スムーズな視覚フィードバック
   - 適切なカーソル表示

2. **エラー処理テスト**
   - 無効操作時の適切な応答
   - エラーメッセージの表示
   - 安全な状態復帰

## 実装フェーズ

### フェーズ1: 基盤実装
- 座標変換モジュールの実装
- config.json設定拡張
- MandelbrotWindow基本拡張

### フェーズ2: マウス操作実装
- ホイールズーム機能
- ドラッグパン機能
- ダブルクリックリセット機能

### フェーズ3: 表示最適化
- 即座の視覚フィードバック
- 遅延画像再生成
- プログレッシブレンダリング

### フェーズ4: エラーハンドリング・最適化
- エラー処理の実装
- パフォーマンス最適化
- メモリ管理改善

## パフォーマンス考慮事項

### 計算最適化
- 座標変換の事前計算とキャッシュ
- 不要な画像再生成の回避
- Numba JITコンパイルとの連携

### メモリ最適化
- 画像バッファの効率的管理
- 高ズーム時の解像度制限
- ガベージコレクション最適化

### UI応答性
- 非同期画像生成の継続使用
- UI更新とバックグラウンド処理の分離
- 適応的品質調整

## セキュリティ考慮事項

### 入力検証
- マウス座標値の範囲チェック
- ズーム・パン値の妥当性検証
- 設定値の安全性確認

### リソース保護
- メモリ使用量の制限
- CPU使用率の監視
- 無限ループの防止

この設計により、既存のアーキテクチャを維持しながら、直感的で高性能なマウス操作機能を追加できます。
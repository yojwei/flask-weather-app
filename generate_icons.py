#!/usr/bin/env python3
"""
PWA 圖示生成腳本
使用方法: python generate_icons.py original_icon.png
"""
from PIL import Image, ImageDraw
import os
import sys


def generate_icons(source_image, output_dir):
    """從原始圖片產生各種尺寸的 PWA 圖示"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 開啟原始圖片
    try:
        img = Image.open(source_image)
        
        # 確保是 RGBA 模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
    except FileNotFoundError:
        print(f"錯誤: 找不到圖片檔案 '{source_image}'")
        print("建立預設圖示...")
        # 建立一個簡單的預設圖示（藍色背景 + 白色雲朵圖案）
        img = create_default_icon(512)
    
    # 產生各種尺寸
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        output_path = f"{output_dir}/icon-{size}x{size}.png"
        resized.save(output_path)
        print(f"✓ 已生成 icon-{size}x{size}.png")
    
    # 產生 maskable 圖示（加上 padding）
    for size in [192, 512]:
        # 藍色背景
        maskable = Image.new('RGBA', (size, size), (59, 130, 246, 255))
        
        # 圖示佔 70%
        icon_size = int(size * 0.7)
        padding = (size - icon_size) // 2
        
        # 調整圖示大小
        resized_icon = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # 貼到中央
        maskable.paste(resized_icon, (padding, padding), resized_icon)
        
        output_path = f"{output_dir}/icon-maskable-{size}x{size}.png"
        maskable.save(output_path)
        print(f"✓ 已生成 icon-maskable-{size}x{size}.png")


def create_default_icon(size):
    """建立預設的天氣應用圖示"""
    # 建立藍色背景
    img = Image.new('RGBA', (size, size), (59, 130, 246, 255))
    draw = ImageDraw.Draw(img)
    
    # 繪製簡單的雲朵和太陽圖案
    center = size // 2
    
    # 繪製太陽（黃色圓圈）
    sun_radius = size // 6
    sun_pos = (center - sun_radius, center - sun_radius * 2, 
               center + sun_radius, center)
    draw.ellipse(sun_pos, fill=(255, 223, 0, 255))
    
    # 繪製雲朵（白色圓圈組合）
    cloud_y = center + sun_radius // 2
    cloud_radius = size // 8
    
    # 雲朵左邊
    draw.ellipse((center - cloud_radius * 2, cloud_y - cloud_radius,
                  center, cloud_y + cloud_radius), fill=(255, 255, 255, 255))
    # 雲朵中間
    draw.ellipse((center - cloud_radius, cloud_y - cloud_radius * 1.5,
                  center + cloud_radius, cloud_y + cloud_radius * 0.5), fill=(255, 255, 255, 255))
    # 雲朵右邊
    draw.ellipse((center, cloud_y - cloud_radius,
                  center + cloud_radius * 2, cloud_y + cloud_radius), fill=(255, 255, 255, 255))
    
    return img


if __name__ == "__main__":
    # 預設參數
    source = "original_icon.png" if len(sys.argv) < 2 else sys.argv[1]
    output = "flask_weather/static/icons"
    
    print("=" * 50)
    print("PWA 圖示生成工具")
    print("=" * 50)
    print(f"來源圖片: {source}")
    print(f"輸出目錄: {output}")
    print("-" * 50)
    
    generate_icons(source, output)
    
    print("-" * 50)
    print("✓ 所有圖示生成完成！")
    print("\n提示:")
    print("1. 如需自訂圖示，請準備 512x512 的 PNG 圖片")
    print("2. 執行: python generate_icons.py your_icon.png")
    print("3. 圖示將儲存在 flask_weather/static/icons/ 目錄")

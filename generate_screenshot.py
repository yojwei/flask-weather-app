"""
建立 PWA 截圖佔位圖片
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_screenshot_placeholder():
    """建立截圖佔位圖片"""
    output_dir = "flask_weather/static/screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # 建立 540x720 的圖片
    img = Image.new("RGB", (540, 720), (59, 130, 246))
    draw = ImageDraw.Draw(img)

    # 繪製文字
    text = "Weather App\nScreenshot"
    bbox = draw.textbbox((0, 0), text, font=None)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((540 - text_width) // 2, (720 - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255), font=None, align="center")

    # 儲存
    output_path = f"{output_dir}/screenshot1.png"
    img.save(output_path)
    print(f"✓ 已生成 {output_path}")


if __name__ == "__main__":
    create_screenshot_placeholder()
    print("\n提示: 請在正式部署前替換為實際應用程式截圖")

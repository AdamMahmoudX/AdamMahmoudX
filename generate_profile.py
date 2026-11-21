import os
from PIL import Image, ImageDraw, ImageFont

width = 1200
height = 2400
img = Image.new("RGBA", (width, height), (5, 9, 23, 255))
draw = ImageDraw.Draw(img)

# رسم خلفية ليلية مع تأثير نيون خفيف
for y in range(height):
    alpha = int(255 * (1 - y / height * 0.3))
    draw.line([(0, y), (width, y)], fill=(3, 7, 18, alpha))

# رسم عمود جانبي (Sidebar) خلفية داكنة مع إطار نيون
sidebar_box = [40, 40, 360, 2360]
draw.rounded_rectangle(sidebar_box, radius=16, fill=(8, 14, 30, 230), outline=(0, 255, 255, 100), width=2)

# رسم البانر العلوي (Main Banner)
banner_box = [390, 40, 1160, 380]
draw.rounded_rectangle(banner_box, radius=16, fill=(12, 20, 42, 230), outline=(0, 255, 255, 120), width=2)

# رسم بطاقات الإحصائيات الأربع
stat_w = 175
stat_h = 110
stat_y = 410
stat_startX = 390
stat_gap = 21

for i in range(4):
    x = stat_startX + i * (stat_w + stat_gap)
    draw.rounded_rectangle([x, stat_y, x + stat_w, stat_y + stat_h], radius=12, fill=(8, 14, 30, 230), outline=(0, 255, 255, 80), width=1)

# رسم قسم Contribution Activity
contrib_box = [390, 545, 1160, 800]
draw.rounded_rectangle(contrib_box, radius=16, fill=(8, 14, 30, 230), outline=(0, 255, 255, 80), width=1)

# رسم Pinned Repositories
pinned_box = [390, 825, 1160, 1030]
draw.rounded_rectangle(pinned_box, radius=16, fill=(8, 14, 30, 230), outline=(0, 255, 255, 80), width=1)

# رسم Activity Overview
activity_box = [390, 1055, 1160, 1450]
draw.rounded_rectangle(activity_box, radius=16, fill=(8, 14, 30, 230), outline=(0, 255, 255, 80), width=1)

# رسم About Me
about_box = [390, 1475, 1160, 1720]
draw.rounded_rectangle(about_box, radius=16, fill=(8, 14, 30, 230), outline=(0, 255, 255, 80), width=1)

# حفظ الصورة النهائية للبروفايل المدمج
os.makedirs("/mnt/ai-data/conquer2/AdamMahmoudX/assets", exist_ok=True)
img.save("/mnt/ai-data/conquer2/AdamMahmoudX/assets/profile_master.png")
print("Master profile banner generated successfully.")

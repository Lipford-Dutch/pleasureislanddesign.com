#!/usr/bin/env python3
"""Generate social media preview image for Pleasure Island Design"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Install with: pip install Pillow")
    exit(1)

def create_social_preview_image():
    """Create a Twitter/Facebook social preview image"""

    # Social media standard size: 1200x630px
    width, height = 1200, 630

    # Create image with coastal gradient background
    img = Image.new('RGB', (width, height), color='#f5f3f0')
    draw = ImageDraw.Draw(img, 'RGBA')

    # Create gradient background (blue to teal)
    for y in range(height):
        # Gradient from navy to teal
        r = int(44 + (72 - 44) * y / height)
        g = int(62 + (163 - 62) * y / height)
        b = int(80 + (163 - 80) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add semi-transparent overlay
    overlay = Image.new('RGBA', (width, height), (255, 255, 255, 30))
    img.paste(overlay, (0, 0), overlay)

    # Draw decorative corner elements
    draw.rectangle([(0, 0), (100, 100)], outline='#d4a574', width=3)
    draw.rectangle([(width-100, 0), (width, 100)], outline='#d4a574', width=3)
    draw.rectangle([(0, height-100), (100, height)], outline='#d4a574', width=3)
    draw.rectangle([(width-100, height-100), (width, height)], outline='#d4a574', width=3)

    # Add wavy lines
    points_top = []
    for x in range(0, width + 20, 20):
        points_top.append((x, int(80 + 20 * (x % 40) / 40)))
    draw.line(points_top, fill='#d4a574', width=2)

    points_bottom = []
    for x in range(0, width + 20, 20):
        points_bottom.append((x, int(height - 80 - 20 * (x % 40) / 40)))
    draw.line(points_bottom, fill='#d4a574', width=2)

    # Add main text - Try multiple font paths and fallback to default
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    body_font = ImageFont.load_default()

    font_paths = [
        "/usr/share/fonts/opentype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/System/Library/Fonts/Times New Roman.ttf",  # macOS
        "C:\\Windows\\Fonts\\times.ttf",  # Windows
    ]

    for font_path in font_paths:
        try:
            title_font = ImageFont.truetype(font_path, 80)
            subtitle_font = ImageFont.truetype(font_path.replace('Serif', 'Sans'), 40) if 'Serif' in font_path else ImageFont.truetype(font_path, 40)
            body_font = ImageFont.truetype(font_path.replace('Serif', 'Sans'), 28) if 'Serif' in font_path else ImageFont.truetype(font_path, 28)
            break
        except:
            continue

    # Title
    title_text = "Transform Your Kitchen"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 100), title_text, fill='#ffffff', font=title_font)

    # Subtitle
    subtitle_text = "5-8 Days. 60-80% Savings."
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 220), subtitle_text, fill='#d4a574', font=subtitle_font)

    # Main message
    message = "Premium Cabinet Refinishing"
    msg_bbox = draw.textbbox((0, 0), message, font=body_font)
    msg_width = msg_bbox[2] - msg_bbox[0]
    msg_x = (width - msg_width) // 2
    draw.text((msg_x, 320), message, fill='#a8d8d8', font=body_font)

    # Tagline
    tagline = "Coastal Cabinet Artisans • Wilmington, NC"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=body_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (width - tagline_width) // 2
    draw.text((tagline_x, 420), tagline, fill='#f5f3f0', font=body_font)

    # CTA
    cta_text = "Request Your Free Consultation"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=body_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_x = (width - cta_width) // 2

    # CTA button background
    button_padding = 20
    button_radius = 10
    draw.rounded_rectangle(
        [(cta_x - button_padding, 500), (cta_x + cta_width + button_padding, 570)],
        radius=button_radius,
        fill='#d4a574',
        outline='#ffffff',
        width=2
    )
    draw.text((cta_x, 515), cta_text, fill='#2c3e50', font=body_font)

    # Contact info
    contact_font = ImageFont.truetype(
        "/usr/share/fonts/opentype/liberation/LiberationSans-Regular.ttf", 20
    ) if img else ImageFont.load_default()

    contact_text = "(910) 444-1230 | pleasureislanddesign@gmail.com"
    contact_bbox = draw.textbbox((0, 0), contact_text, font=contact_font)
    contact_width = contact_bbox[2] - contact_bbox[0]
    contact_x = (width - contact_width) // 2
    draw.text((contact_x, 590), contact_text, fill='#cccccc', font=contact_font)

    # Save image
    output_path = '/home/user/pleasureislanddesign.com/img/pid-social-preview-1200x630.png'
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Social preview image created: {output_path}")

    # Also create square version for profile pictures
    img_square = Image.new('RGB', (1200, 1200), color='#f5f3f0')
    draw_sq = ImageDraw.Draw(img_square, 'RGBA')

    # Gradient background for square
    for y in range(1200):
        r = int(44 + (72 - 44) * y / 1200)
        g = int(62 + (163 - 62) * y / 1200)
        b = int(80 + (163 - 80) * y / 1200)
        draw_sq.line([(0, y), (1200, y)], fill=(r, g, b))

    # Add gold borders
    border_width = 5
    draw_sq.rectangle([(border_width, border_width), (1200-border_width, 1200-border_width)],
                      outline='#d4a574', width=border_width)

    # Center circle
    circle_radius = 300
    circle_x = 600
    circle_y = 600
    draw_sq.ellipse(
        [(circle_x - circle_radius, circle_y - circle_radius),
         (circle_x + circle_radius, circle_y + circle_radius)],
        fill='#2c3e50',
        outline='#d4a574',
        width=3
    )

    # Text on square
    title_sq = "PID"
    title_sq_font = title_font
    subtitle_sq_font = body_font

    title_sq_bbox = draw_sq.textbbox((0, 0), title_sq, font=title_sq_font)
    title_sq_width = title_sq_bbox[2] - title_sq_bbox[0]
    title_sq_x = (1200 - title_sq_width) // 2
    draw_sq.text((title_sq_x, 450), title_sq, fill='#d4a574', font=title_sq_font)

    tagline_sq = "Coastal Cabinet Artisans"
    tagline_sq_bbox = draw_sq.textbbox((0, 0), tagline_sq, font=subtitle_sq_font)
    tagline_sq_width = tagline_sq_bbox[2] - tagline_sq_bbox[0]
    tagline_sq_x = (1200 - tagline_sq_width) // 2
    draw_sq.text((tagline_sq_x, 750), tagline_sq, fill='#a8d8d8', font=subtitle_sq_font)

    output_square = '/home/user/pleasureislanddesign.com/img/pid-social-profile-1200x1200.png'
    img_square.save(output_square, 'PNG', quality=95)
    print(f"✓ Social profile image created: {output_square}")

if __name__ == "__main__":
    create_social_preview_image()
    print("\n✅ Social media assets generated successfully!")
    print("Files created:")
    print("  - img/pid-social-preview-1200x630.png (Twitter/Facebook)")
    print("  - img/pid-social-profile-1200x1200.png (Profile pictures)")

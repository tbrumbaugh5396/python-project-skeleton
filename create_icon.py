#!/usr/bin/env python3
"""
Create macOS Application Icon for Kanban Board
Generates a high-resolution icon with kanban board design
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon():
    """Create a modern kanban board icon"""

    # Create high-resolution image for icon (1024x1024 for macOS)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background with rounded corners and gradient effect
    margin = 80
    bg_rect = [margin, margin, size - margin, size - margin]

    # Draw rounded rectangle background
    corner_radius = 120
    draw.rounded_rectangle(bg_rect, corner_radius,
                           fill=(45, 55, 72, 255))  # Dark blue-gray

    # Add subtle border
    border_margin = margin - 10
    border_rect = [
        border_margin, border_margin, size - border_margin,
        size - border_margin
    ]
    draw.rounded_rectangle(border_rect,
                           corner_radius + 10,
                           outline=(200, 200, 200, 100),
                           width=8)

    # Draw three columns representing kanban board
    col_width = 160
    col_height = 400
    col_spacing = 80
    start_x = (size - (3 * col_width + 2 * col_spacing)) // 2
    start_y = (size - col_height) // 2 + 50

    # Column colors (Todo, In Progress, Done)
    col_colors = [
        (99, 102, 241, 255),  # Indigo
        (245, 158, 11, 255),  # Amber  
        (34, 197, 94, 255)  # Green
    ]

    # Draw columns
    for i in range(3):
        x = start_x + i * (col_width + col_spacing)
        y = start_y

        # Column background
        col_rect = [x, y, x + col_width, y + col_height]
        draw.rounded_rectangle(col_rect, 20, fill=(255, 255, 255, 240))

        # Column header
        header_rect = [x + 10, y + 10, x + col_width - 10, y + 50]
        draw.rounded_rectangle(header_rect, 10, fill=col_colors[i])

        # Draw task cards in each column
        card_height = 60
        card_margin = 15
        num_cards = [3, 2, 4][i]  # Different number of cards per column

        for j in range(num_cards):
            card_y = y + 70 + j * (card_height + card_margin)
            if card_y + card_height > y + col_height - 10:
                break

            card_rect = [
                x + 15, card_y, x + col_width - 15, card_y + card_height
            ]

            # Card background with slight shadow effect
            shadow_rect = [
                x + 17, card_y + 2, x + col_width - 13,
                card_y + card_height + 2
            ]
            draw.rounded_rectangle(shadow_rect, 8, fill=(0, 0, 0, 30))

            draw.rounded_rectangle(card_rect, 8, fill=(255, 255, 255, 255))

            # Card content lines
            line_y1 = card_y + 15
            line_y2 = card_y + 35
            draw.rectangle([x + 25, line_y1, x + col_width - 25, line_y1 + 3],
                           fill=(120, 120, 120, 180))
            draw.rectangle([x + 25, line_y2, x + col_width - 45, line_y2 + 3],
                           fill=(160, 160, 160, 120))

    # Add title text at the top
    try:
        # Try to use a nice font
        font_size = 80
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",
                                  font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    title = "Kanban"
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (size - title_width) // 2
    title_y = 180

    # Draw title with shadow
    draw.text((title_x + 3, title_y + 3),
              title,
              font=font,
              fill=(0, 0, 0, 100))
    draw.text((title_x, title_y), title, font=font, fill=(255, 255, 255, 255))

    return img


def create_icon_set():
    """Create a complete icon set for macOS"""

    base_icon = create_icon()

    # Icon sizes for macOS
    sizes = [16, 32, 64, 128, 256, 512, 1024]

    # Create icons directory
    if not os.path.exists("icons"):
        os.makedirs("icons")

    for size in sizes:
        # Resize image with high quality
        resized = base_icon.resize((size, size), Image.Resampling.LANCZOS)

        # Save as PNG
        filename = f"icons/kanban_icon_{size}x{size}.png"
        resized.save(filename, "PNG")
        print(f"Created {filename}")

    # Save the main icon
    base_icon.save("icons/kanban_icon.png", "PNG")
    print("Created icons/kanban_icon.png")

    # Create ICO file for cross-platform compatibility
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128),
                 (256, 256)]
    ico_images = []

    for size in ico_sizes:
        resized = base_icon.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)

    # Save as ICO
    ico_images[0].save("icons/kanban_icon.ico", format="ICO", sizes=ico_sizes)
    print("Created icons/kanban_icon.ico")

    print("\nIcon set created successfully!")
    print("For macOS app bundle, use the PNG files.")
    print("For cross-platform compatibility, use the ICO file.")


if __name__ == "__main__":
    create_icon_set()

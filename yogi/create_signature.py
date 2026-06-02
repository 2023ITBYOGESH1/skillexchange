"""
Signature Generator Script
Creates a clean, professional handwritten-style signature image
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Signature configuration
SIGNATURE_NAME = "YOUR_NAME_HERE"
OUTPUT_PATH = "static/uploads/signature_template.png"

# Image dimensions (certificate signature area style)
WIDTH = 300
HEIGHT = 100

def create_signature():
    """Create a professional handwritten-style signature"""
    
    # Create white background image
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice handwritten font if available
    # Otherwise we'll use a fallback approach
    font_paths = [
        # Windows common paths
        "C:/Windows/Fonts/Segoe Script.ttf",
        "C:/Windows/Fonts/Georgia.ttf", 
        "C:/Windows/Fonts/Bradley Hand ITC.ttf",
        "C:/Windows/Fonts/Comic Sans MS.ttf",
        "C:/Windows/Fonts/Pristina.ttf",
        "C:/Windows/Fonts/Script MT Bold.ttf",
        # Fallback
        None
    ]
    
    font = None
    for font_path in font_paths:
        if font_path and os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 36)
                break
            except:
                continue
    
    # If no custom font found, use default
    if font is None:
        font = ImageFont.load_default()
    
    # Get text dimensions
    if hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), SIGNATURE_NAME, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = draw.textsize(SIGNATURE_NAME, font=font)[0]
        text_height = draw.textsize(SIGNATURE_NAME, font=font)[1]
    
    # Center the signature
    x = (WIDTH - text_width) // 2
    y = (HEIGHT - text_height) // 2 - 10
    
    # Draw the signature in a professional dark blue/ink color
    # Using a color similar to what's used in the certificate
    ink_color = (26, 54, 93, 255)  # #1a365d - matching certificate theme
    
    # Draw the main signature
    draw.text((x, y), SIGNATURE_NAME, font=font, fill=ink_color)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Save as PNG with transparency
    img.save(OUTPUT_PATH, 'PNG')
    print(f"Signature created successfully at: {OUTPUT_PATH}")
    
    # Also create a version for the "prasanth" style example
    create_prasanth_style_signature()
    
    return OUTPUT_PATH

def create_prasanth_style_signature():
    """Create a signature in the style similar to 'prasanth' example"""
    
    # More elegant signature style
    WIDTH = 350
    HEIGHT = 120
    
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Use a more elegant font
    font = None
    font_paths = [
        "C:/Windows/Fonts/Georgia.ttf",
        "C:/Windows/Fonts/Segoe Script.ttf",
        "C:/Windows/Fonts/Pristina.ttf",
        "C:/Windows/Fonts/Bradley Hand ITC.ttf",
        None
    ]
    
    for font_path in font_paths:
        if font_path and os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 42)
                break
            except:
                continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # Signature name
    name = "YOUR_NAME_HERE"
    
    # Get text dimensions
    if hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = draw.textsize(name, font=font)[0]
        text_height = draw.textsize(name, font=font)[1]
    
    # Center the signature
    x = (WIDTH - text_width) // 2
    y = (HEIGHT - text_height) // 2 - 15
    
    # Draw signature in elegant dark ink color
    ink_color = (26, 54, 93, 255)  # Dark blue matching certificate theme
    
    # Draw the signature text
    draw.text((x, y), name, font=font, fill=ink_color)
    
    # Add a subtle underline flourish (like a handwritten signature)
    # Underline position
    line_y = y + text_height + 5
    line_start = x - 5
    line_end = x + text_width + 5
    
    # Draw a light line under the signature
    draw.line([(line_start, line_y), (line_end, line_y)], fill=(180, 150, 100, 200), width=2)
    
    # Save
    output_path = "static/uploads/signature_prasanth_style.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"Signature (prasanth style) created at: {output_path}")

if __name__ == "__main__":
    create_signature()
    print("\nSignature images have been created!")
    print("You can view them at:")
    print("  - static/uploads/signature_template.png")
    print("  - static/uploads/signature_prasanth_style.png")


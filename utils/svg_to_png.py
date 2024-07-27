import os

# Cài đặt GTK3-Runtime Win64 để sử dụng cairosvg trên windows
# gtkbin = r"C:\Program Files\GTK3-Runtime Win64\bin"
# add_dll_dir = getattr(os, "add_dll_directory", None)
# if callable(add_dll_dir):
#     add_dll_dir(gtkbin)
# else:
#     os.environ["PATH"] = os.pathsep.join((gtkbin, os.environ["PATH"]))

import cairosvg
from PIL import Image
import os
import xml.etree.ElementTree as ET


def get_svg_size(input_path):
    tree = ET.parse(input_path)
    root = tree.getroot()
    width = root.get("width")
    height = root.get("height")

    if width and height:
        return int(float(width)), int(float(height))
    else:
        return None, None


def convert_svg_to_png(input_path, output_path, max_size=None, keep_aspect_ratio=True):
    original_width, original_height = get_svg_size(input_path)

    if max_size is None or not keep_aspect_ratio:
        cairosvg.svg2png(url=input_path, write_to=output_path)
    else:
        if original_width and original_height:
            ratio = min(max_size / original_width, max_size / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        else:
            new_width = new_height = max_size

        cairosvg.svg2png(
            url=input_path,
            write_to=output_path,
            output_width=new_width,
            output_height=new_height,
        )


def process_directory(input_dir, output_dir, max_size=None, keep_aspect_ratio=True):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".svg"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(
                    output_dir, os.path.splitext(relative_path)[0] + ".png"
                )

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    convert_svg_to_png(
                        input_path, output_path, max_size, keep_aspect_ratio
                    )
                    print(f"Converted: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Error converting {input_path}: {str(e)}")


# Sử dụng script
input_directory = "../graphics/map"
output_directory = "../png"
max_size = 256  # Hoặc đặt theo ý muốn
keep_aspect_ratio = True  # Đặt là False nếu muốn sử dụng kích thước gốc của SVG

process_directory(input_directory, output_directory, max_size, keep_aspect_ratio)

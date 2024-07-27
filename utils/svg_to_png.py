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


def convert_svg_to_png(input_path, output_path, max_size=128 * 4):
    cairosvg.svg2png(
        url=input_path,
        write_to=output_path,
        output_width=max_size,
        output_height=max_size,
    )

    with Image.open(output_path) as img:
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        img.save(output_path, "PNG")


def process_directory(input_dir, output_dir):
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
                    convert_svg_to_png(input_path, output_path)
                    print(f"Converted: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Error converting {input_path}: {str(e)}")


# Sử dụng script
input_directory = "../graphics/towers"
output_directory = "../png"
process_directory(input_directory, output_directory)

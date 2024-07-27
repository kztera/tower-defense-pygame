import cairosvg
import os


def convert_svg_to_png(directory_path, width, height):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".svg"):
                svg_path = os.path.join(root, file)
                png_path = os.path.splitext(svg_path)[0] + ".png"

                try:
                    cairosvg.svg2png(
                        url=svg_path,
                        write_to=png_path,
                        output_width=width,
                        output_height=height,
                    )
                    print(f"Converted: {svg_path} to {png_path}")

                    os.remove(svg_path)
                    print(f"Removed original SVG: {svg_path}")
                except Exception as e:
                    print(f"Error processing {svg_path}: {str(e)}")


input_directory = "../graphics/towers"
desired_width = 128
desired_height = 128

convert_svg_to_png(input_directory, desired_width, desired_height)

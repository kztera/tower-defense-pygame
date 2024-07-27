from PIL import Image
import os


def scale_pixel_art(input_path, scale_factor):
    with Image.open(input_path) as img:
        width, height = img.size

        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        resample_method = Image.NEAREST if scale_factor > 1 else Image.LANCZOS

        scaled_img = img.resize((new_width, new_height), resample_method)

        scaled_img.save(input_path)


def process_directory(directory_path, scale_factor):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                file_path = os.path.join(root, file)
                try:
                    scale_pixel_art(file_path, scale_factor)
                    print(f"Scaled and replaced: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")


input_directory = "../graphics/ui/entities"
scale = 0.75


process_directory(input_directory, scale)

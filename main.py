import subprocess
import sys
import os
from PIL import Image, ImageDraw, ImageFont


def printd(*args, **kwargs):
    """Debug print function that can be easily disabled."""
    if "--debug" in sys.argv:
        print(*args, **kwargs)

def clear_directory(dir_name="temp"):
    if os.path.exists(dir_name):
        for filename in os.listdir(dir_name):
            file_path = os.path.join(dir_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"Temporary directory '{dir_name}' cleared.")
    else:
        print(f"Temporary directory '{dir_name}' does not exist.")

def open_directory(dir_name="output"):
    if os.path.exists(dir_name):
        if sys.platform == "win32":
            os.startfile(dir_name)
        elif sys.platform == "darwin":
            subprocess.run(["open", dir_name])
        else:
            subprocess.run(["xdg-open", dir_name])
        print(f"Opened temporary directory: {dir_name}")
    else:
        print(f"Temporary directory '{dir_name}' does not exist.")

def download_soundcloud_thumbnails(profile_url):
    # yt-dlp options:
    # --skip-download: don't download audio/video
    # --write-thumbnail: download thumbnail image
    # --output: set output filename template
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-thumbnail",
        "--output", os.path.join(temp_dir, "%(title)s.%(ext)s"),
        profile_url
    ]
    subprocess.run(cmd, check=True)
    print(f"Thumbnails downloaded to temporary directory: {temp_dir}")

def add_text_to_images(top=False, font_size=36):
    temp_dir = "temp"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    max_width = 240  # pixels, for text area

    for filename in os.listdir(temp_dir):
        printd('---')
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(temp_dir, filename)
            name, _ = os.path.splitext(filename)
            img = Image.open(image_path).convert("RGB")
            img = img.resize((256, 256), Image.LANCZOS)

            # Prepare font
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            # Wrap text to fit width
            lines = []
            words = name.split()
            line = ""
            for word in words:
                test_line = line + (" " if line else "") + word
                dummy_img = Image.new("RGB", (256, 10))
                draw = ImageDraw.Draw(dummy_img)
                text_width = draw.textlength(test_line, font=font)
                if text_width <= max_width:
                    line = test_line
                else:
                    if line:
                        lines.append(line)
                    line = word
            if line:
                lines.append(line)

            # Calculate text box height
            dummy_img = Image.new("RGB", (256, 10))
            draw = ImageDraw.Draw(dummy_img)
            
            # Use getbbox or getsize_multiline instead of deprecated getsize
            if hasattr(font, "getbbox"):
                # For newer Pillow versions
                text_height = font.getbbox("A")[3] - font.getbbox("A")[1]
            else:
                # Fallback for older versions
                text_height = font.getsize("A")[1]
                
            total_text_height = text_height * len(lines)
            line_spacing = int(text_height * 0.2)  # Add some spacing between lines
            total_text_height_with_spacing = total_text_height + line_spacing * (len(lines) - 1 if len(lines) > 1 else 0)
            box_height = total_text_height_with_spacing + 24  # More padding for better appearance
            printd(f"{total_text_height = }")
            printd(f"{box_height = }")
            printd(f"{len(lines) = }")
            printd(f"{lines = }")
            printd(f"{total_text_height_with_spacing = }")

            new_height = 256 + box_height
            new_img = Image.new("RGB", (256, new_height), "white")
            draw = ImageDraw.Draw(new_img)

            if top:
                draw.rectangle([0, 0, 256, box_height], fill="white")
                # Center text block vertically in the white box
                y_start = (box_height - (total_text_height_with_spacing + 11)) // 2
                for i, line in enumerate(lines):
                    text_width = draw.textlength(line, font=font)
                    draw.text(
                        ((256 - text_width) // 2, y_start + i * (text_height + line_spacing)),
                        line,
                        font=font,
                        fill="black"
                    )
                new_img.paste(img, (0, box_height))
            else:
                new_img.paste(img, (0, 0))
                draw.rectangle([0, 256, 256, new_height], fill="white")
                # Center text block vertically in the white box
                y_start = 256 + (box_height - (total_text_height_with_spacing + 11)) // 2
                print(f"{total_text_height_with_spacing = }")
                
                for i, line in enumerate(lines):
                    text_width = draw.textlength(line, font=font)
                    draw.text(
                        ((256 - text_width) // 2, y_start + i * (text_height + line_spacing)),
                        line,
                        font=font,
                        fill="black"
                    )

            out_path = os.path.join(output_dir, filename)
            new_img.save(out_path)
            print(f"Added text to image: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <soundcloud_profile_url> [--top] [--font-size <size>] [--use-temp] [--debug]")
        sys.exit(1)
    profile_url = sys.argv[1]
    if not profile_url.startswith("https://soundcloud.com/"):
        print("Please provide a valid SoundCloud profile URL.")
        sys.exit(1)
    
    # Allow font size to be set via command line argument: --font-size <size>
    font_size = 36  # Default font size
    for i, arg in enumerate(sys.argv):
        if arg == "--font-size" and i + 1 < len(sys.argv):
            try:
                font_size = int(sys.argv[i + 1])
            except ValueError:
                print("Invalid font size specified. Using default.")
    
    if not "--use-temp" in sys.argv:
        clear_directory("temp")
        download_soundcloud_thumbnails(profile_url)
    clear_directory("output")
    add_text_to_images(top="--top" in sys.argv, font_size=font_size)

    open_directory("output")

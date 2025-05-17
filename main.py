import os
import subprocess
import shutil
import threading
from multiprocessing import Pool, cpu_count, Manager
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import time
import customtkinter as ctk
from tkinter import messagebox

ASCII_CHARS = "-_+~;:,'. "

def get_video_resolution(video_path, ffprobe_path="bin/ffprobe"):
    cmd = [
        ffprobe_path,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip().split("\n")
    if len(output) != 2:
        return 150
    try:
        width = int(output[0])
        return width
    except ValueError:
        return 150

def resize_image(image, new_width):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height), resample=Image.Resampling.BILINEAR)

def pixels_to_ascii(image):
    grayscale = image.convert("L")
    pixels = grayscale.getdata()
    ascii_str = ''.join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels)
    return ascii_str

def image_to_ascii(image_path, width):
    img = Image.open(image_path)
    img = resize_image(img, new_width=width)
    ascii_data = pixels_to_ascii(img)
    ascii_lines = [ascii_data[i:i+img.width] for i in range(0, len(ascii_data), img.width)]
    return '\n'.join(ascii_lines)

def clear_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except Exception as e:
            print(f"Error deleting {path}: {e}")

def extract_frames(video_path, output_folder, ffmpeg_path="bin/ffmpeg", target_width=150):
    clear_folder(output_folder)
    scale_filter = f"scale={target_width}:-1"
    cmd = [
        ffmpeg_path,
        '-i', video_path,
        '-vf', scale_filter,
        '-q:v', '2',
        os.path.join(output_folder, 'frame_%04d.jpg')
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def process_frame(args):
    frame_file, temp_dir, output_folder, width = args
    frame_path = os.path.join(temp_dir, frame_file)
    ascii_art = image_to_ascii(frame_path, width)
    txt_path = os.path.join(output_folder, f"{os.path.splitext(frame_file)[0]}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(ascii_art)
    return frame_file

def convert_video_to_ascii(video_path, output_folder, font_size, progress_dict=None):
    temp_dir = "temp_frames"
    clear_folder(temp_dir)
    clear_folder(output_folder)
    width = get_video_resolution(video_path)
    ascii_width = max(50, int(width * 16 / font_size / 10))  # Dynamic width based on font size

    if progress_dict is not None:
        progress_dict['stage'] = "Extracting frames"
        progress_dict['current'] = 0
        progress_dict['total'] = 1

    extract_frames(video_path, temp_dir, target_width=ascii_width)

    frame_list = sorted([f for f in os.listdir(temp_dir) if f.endswith(".jpg")])
    args_list = [(f, temp_dir, output_folder, ascii_width) for f in frame_list]

    if progress_dict is not None:
        progress_dict['stage'] = "Converting frames to ASCII"
        progress_dict['current'] = 0
        progress_dict['total'] = len(frame_list)

    with Pool(cpu_count()) as pool:
        for i, _ in enumerate(pool.imap_unordered(process_frame, args_list), 1):
            if progress_dict is not None:
                progress_dict['current'] = i

    shutil.rmtree(temp_dir)

def ascii_to_video(ascii_folder, output_video, fps, font_path, font_size, audio_input=None, progress_dict=None):
    temp_img_dir = "ascii_temp_images"
    clear_folder(temp_img_dir)

    try:
        frame_files = sorted([f for f in os.listdir(ascii_folder) if f.endswith('.txt')])
        if not frame_files:
            print("No ASCII frame files found.")
            return
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error preparing font or frames: {e}")
        return

    if progress_dict is not None:
        progress_dict['stage'] = "Rendering ASCII frames as images"
        progress_dict['current'] = 0
        progress_dict['total'] = len(frame_files)

    for i, txt_file in enumerate(frame_files, 1):
        try:
            with open(os.path.join(ascii_folder, txt_file), 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            if not lines:
                continue
            max_width = max(len(line) for line in lines)
            img = Image.new("RGB", (max_width * font_size // 2, len(lines) * font_size), "black")
            draw = ImageDraw.Draw(img)
            for j, line in enumerate(lines):
                draw.text((0, j * font_size), line, font=font, fill="white")
            img = img.resize((img.width // 2, img.height // 2), resample=Image.Resampling.BILINEAR)
            img_path = os.path.join(temp_img_dir, f"frame_{i:04d}.jpg")
            img.save(img_path, quality=50, optimize=True)
        except Exception as e:
            print(f"Error processing frame {txt_file}: {e}")
            continue

        if progress_dict is not None:
            progress_dict['current'] = i

    try:
        os.makedirs(os.path.dirname(output_video), exist_ok=True)
        input_pattern = os.path.join(temp_img_dir, "frame_%04d.jpg").replace("\\", "/")
        cmd = [
            "bin/ffmpeg",
            "-y",
            "-framerate", str(fps),
            "-i", input_pattern,
        ]
        if audio_input:
            cmd += ["-i", audio_input, "-c:a", "aac", "-shortest"]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", output_video]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("FFmpeg error:", result.stderr.decode())
        else:
            print("Video created successfully:", output_video)
    except Exception as e:
        print(f"Failed to create video: {e}")
    finally:
        shutil.rmtree(temp_img_dir, ignore_errors=True)

def extract_audio(video_path, output_audio="temp_audio.aac", progress_dict=None):
    if progress_dict is not None:
        progress_dict['stage'] = "Extracting audio"
        progress_dict['current'] = 0
        progress_dict['total'] = 1
    cmd = [
        "bin/ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "aac",
        output_audio
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if progress_dict is not None:
        progress_dict['current'] = 1
    return output_audio

def run_conversion(video_path, font_size, fps, keep_frames, keep_ascii, progress_dict):
    audio_path = extract_audio(video_path, progress_dict=progress_dict)
    convert_video_to_ascii(video_path, output_folder="ascii_frames", font_size=font_size, progress_dict=progress_dict)
    ascii_to_video(
        ascii_folder="ascii_frames",
        output_video=get_output_video_path(),
        fps=fps,
        font_path="C:/Windows/Fonts/consola.ttf",
        font_size=font_size,
        audio_input=audio_path,
        progress_dict=progress_dict
    )
    # Clean up temp files based on user preferences
    if not keep_frames and os.path.exists("temp_frames"):
        shutil.rmtree("temp_frames", ignore_errors=True)
    if not keep_ascii and os.path.exists("ascii_frames"):
        shutil.rmtree("ascii_frames", ignore_errors=True)
    if os.path.exists(audio_path):
        os.remove(audio_path)

def get_next_video_filename(folder="Videos", prefix="vid_", ext=".mp4"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    existing = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith(ext)]
    numbers = [int(f[len(prefix):-len(ext)]) for f in existing if f[len(prefix):-len(ext)].isdigit()]
    next_num = max(numbers, default=0) + 1
    return os.path.join(folder, f"{prefix}{next_num:04d}{ext}")

def get_output_video_path():
    return get_next_video_filename(folder="Videos")

start_time = time.time()

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"
    else:
        return f"{int(seconds // 86400)}d {int((seconds % 86400) // 3600)}h"

def update_progress_ui(progress_label_var, progress_bar, progress_dict, root):
    stage = progress_dict.get('stage', '')
    current = progress_dict.get('current', 0)
    total = progress_dict.get('total', 1)
    percent = int(current / total * 100) if total else 0
    progress_label_var.set(f"{stage}... {percent}%")
    progress_bar.set(percent)
    root.update_idletasks()

def select_video_file(entry):
    filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")]
    filename = filedialog.askopenfilename(title="Select MP4 video file", filetypes=filetypes)
    if filename:
        entry.delete(0, "end")
        entry.insert(0, filename)

def start_conversion_thread(entry, font_slider, fps_slider, keep_frames_var, keep_ascii_var, progress_label_var, progress_bar, root):
    video_path = entry.get()
    if not os.path.exists(video_path):
        progress_label_var.set("Invalid video path")
        return

    font_size = font_slider.get()
    fps = fps_slider.get()
    keep_frames = keep_frames_var.get()
    keep_ascii = keep_ascii_var.get()

    progress_dict = Manager().dict()
    progress_dict['stage'] = "Starting..."
    progress_dict['current'] = 0
    progress_dict['total'] = 1

    def worker():
        try:
            run_conversion(video_path, font_size, fps, keep_frames, keep_ascii, progress_dict)
            progress_dict['stage'] = "Done!"
            progress_dict['current'] = 1
            progress_dict['total'] = 1
        except Exception as e:
            progress_dict['stage'] = f"Error: {e}"

    threading.Thread(target=worker, daemon=True).start()

    def ui_update_loop():
        update_progress_ui(progress_label_var, progress_bar, progress_dict, root)
        if progress_dict.get('stage') != "Done!":
            root.after(100, ui_update_loop)

    ui_update_loop()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    lang_strings = {
        'title': 'Video to ASCII Converter',
        'instructions_text': 'This tool converts videos into ASCII art animations.',
        'instructions_title': 'Instructions',
        'video_entry_placeholder': 'Select video file',
        'browse_button': 'Browse',
        'font_size_label': 'Font Size:',
        'fps_label': 'FPS:',
        'keep_frames': 'Keep Frames',
        'keep_ascii': 'Keep ASCII Files',
        'show_instructions': 'Show Instructions',
        'start_conversion': 'Start Conversion'
    }

    root = ctk.CTk()
    root.title(lang_strings['title'])
    root.geometry("750x600")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, corner_radius=8)
    frame.pack(pady=30, padx=30, fill="both", expand=True)

    title_label = ctk.CTkLabel(frame, text=lang_strings['title'], font=ctk.CTkFont(size=24, weight="bold"))
    title_label.pack(pady=(0, 25))

    video_frame = ctk.CTkFrame(frame)
    video_frame.pack(fill="x", padx=20, pady=(0, 20))

    video_entry = ctk.CTkEntry(video_frame, placeholder_text=lang_strings['video_entry_placeholder'])
    video_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
    browse_btn = ctk.CTkButton(video_frame, text=lang_strings['browse_button'], width=100,
                               command=lambda: select_video_file(video_entry))
    browse_btn.pack(side="left")

    font_frame = ctk.CTkFrame(frame)
    font_frame.pack(fill="x", padx=20, pady=(0, 20))

    font_size_label = ctk.CTkLabel(font_frame, text=lang_strings['font_size_label'])
    font_size_label.pack(side="left")

    font_size_slider = ctk.CTkSlider(font_frame, from_=2, to=100, number_of_steps=100)
    font_size_slider.set(15)
    font_size_slider.pack(side="left", fill="x", expand=True, padx=15)
    font_value_label = ctk.CTkLabel(font_frame, text=f"{int(font_size_slider.get())}", width=30)
    font_value_label.pack(side="right")

    def font_slider_update(value):
        font_value_label.configure(text=f"{int(float(value))}")
    font_size_slider.configure(command=font_slider_update)

    fps_frame = ctk.CTkFrame(frame)
    fps_frame.pack(fill="x", padx=20, pady=(0, 20))

    fps_label = ctk.CTkLabel(fps_frame, text=lang_strings['fps_label'])
    fps_label.pack(side="left")

    fps_slider = ctk.CTkSlider(fps_frame, from_=10, to=60, number_of_steps=50)
    fps_slider.set(30)
    fps_slider.pack(side="left", fill="x", expand=True, padx=15)
    fps_value_label = ctk.CTkLabel(fps_frame, text=f"{int(fps_slider.get())}", width=30)
    fps_value_label.pack(side="right")

    def fps_slider_update(value):
        fps_value_label.configure(text=f"{int(float(value))}")
    fps_slider.configure(command=fps_slider_update)

    keep_frames_var = ctk.BooleanVar(value=False)
    keep_frames_check = ctk.CTkCheckBox(frame, text=lang_strings['keep_frames'], variable=keep_frames_var)
    keep_frames_check.pack(anchor="w", padx=20, pady=(10, 5))

    keep_ascii_var = ctk.BooleanVar(value=False)
    keep_ascii_check = ctk.CTkCheckBox(frame, text=lang_strings['keep_ascii'], variable=keep_ascii_var)
    keep_ascii_check.pack(anchor="w", padx=20, pady=(0, 20))

    progress_label_var = ctk.StringVar(value="")
    progress_label = ctk.CTkLabel(frame, textvariable=progress_label_var, font=ctk.CTkFont(size=14))
    progress_label.pack(pady=(15, 5))
    progress_bar = ctk.CTkProgressBar(frame, width=600)
    progress_bar.pack(pady=(5, 20))

    instructions_btn = ctk.CTkButton(frame, text=lang_strings['show_instructions'], command=lambda: messagebox.showinfo(lang_strings['instructions_title'], lang_strings['instructions_text']))
    instructions_btn.pack(pady=(0, 20))

    start_btn = ctk.CTkButton(frame, text=lang_strings['start_conversion'],
                              command=lambda: start_conversion_thread(video_entry, font_size_slider, fps_slider,
                                                                      keep_frames_var, keep_ascii_var,
                                                                      progress_label_var, progress_bar, root))
    start_btn.pack(pady=(0, 20))

    root.mainloop()

if __name__ == "__main__":
    main()
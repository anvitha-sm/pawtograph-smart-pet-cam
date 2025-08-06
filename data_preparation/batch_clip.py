from moviepy.editor import VideoFileClip
import os
import concurrent.futures

CLIP_DURATION = 2
def extract_clips_for_file(file_path, output_dir):
    try:
        video = VideoFileClip(file_path)
        video_duration = video.duration
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        num_clips = int(video_duration // CLIP_DURATION)
        for i in range(num_clips):
            start = i * CLIP_DURATION
            end = start + CLIP_DURATION
            subclip = video.subclip(start, end)
            out_name = f"{base_name}_clip{i:04d}.mp4"
            out_path = os.path.join(output_dir, out_name)
            subclip.write_videofile(out_path, codec="libx264", audio=False, verbose=False, logger=None)

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")

def extract_all(input_dir, output_dir, max_workers=4):
    os.makedirs(output_dir, exist_ok=True)
    video_paths = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".mp4")
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(extract_clips_for_file, path, output_dir)
            for path in video_paths
        ]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    extract_all(r"C:\yt-dlp\data", r"C:\yt-dlp\clips", max_workers=8)

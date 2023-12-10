import cv2
from skimage.metrics import structural_similarity as ssim
from concurrent.futures import ThreadPoolExecutor
import json

def calculate_ssim(frame1, frame2):
    gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray_frame1, gray_frame2, full=True)
    return score

def process_frame(frame1, frame2, threshold):
    similarity_score = calculate_ssim(frame1, frame2)
    return similarity_score >= threshold

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def detect_slide_durations(video_path, threshold=0.95, resize_factor=0.5, skip_frames=5):
    cap = cv2.VideoCapture(video_path)
    ret, reference_frame = cap.read()

    # Resize reference frame
    reference_frame = cv2.resize(reference_frame, None, fx=resize_factor, fy=resize_factor)

    slide_durations = []
    start_time = 0

    with ThreadPoolExecutor() as executor:
        while True:
            # Skip frames
            for _ in range(skip_frames):
                cap.grab()

            ret, frame = cap.read()
            if not ret:
                break

            # Resize current frame
            frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)

            # Perform frame comparison in parallel
            future = executor.submit(process_frame, reference_frame, frame, threshold)
            is_slide = future.result()

            if not is_slide:
                end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                duration = end_time - start_time
                slide_durations.append({
                    "start": format_time(start_time),
                    "end": format_time(end_time),
                    "duration": format_time(duration)
                })

                reference_frame = frame
                start_time = end_time

    cap.release()

    # Return the JSON data instead of writing to a file
    return {"Slide_durations_Test": slide_durations}

# Example usage
#video_path = '2min_output_clip.mp4'
# result_json = detect_slide_durations(video_path)

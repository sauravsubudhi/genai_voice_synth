from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import os
from utills import *

app = FastAPI()

def get_video_info(file_path):
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Error opening video file")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frames / fps
        result_json = detect_slide_durations(file_path)
        

        return {
            "duration": duration,
            "fps": fps,
            "frames": frames,
            "infernace": result_json["Slide_durations_Test"]
            
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cap.release()

@app.post("/upload/video")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as video_file:
            video_file.write(file.file.read())
        
        video_info = get_video_info(file_path)
        print(video_info)

        return JSONResponse(content=video_info, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optionally, you may want to delete the uploaded file after processing
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        #print("HIIIIII")

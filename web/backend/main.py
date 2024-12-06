from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import subprocess
import shutil
from pathlib import Path
from typing import List
import uuid

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = Path("tiktok_test_log/image_log")

@app.post("/upload/")
async def upload_files(
    source_image: UploadFile = File(...),
    pose_image: UploadFile = File(...)
):
    try:
        # Create unique session ID
        session_id = str(uuid.uuid4())
        session_dir = UPLOAD_DIR / session_id
        session_dir.mkdir(parents=True)

        # Save uploaded files
        source_path = session_dir / source_image.filename
        pose_path = session_dir / pose_image.filename
        
        with open(source_path, "wb") as f:
            shutil.copyfileobj(source_image.file, f)
        with open(pose_path, "wb") as f:
            shutil.copyfileobj(pose_image.file, f)

        # Prepare the command
        cmd = [
            "python", "test_any_image_pose.py",
            "--model_config", "model_lib/ControlNet/models/cldm_v15_reference_only_pose.yaml",
            "--num_train_steps", "1",
            "--img_bin_limit", "all",
            "--train_batch_size", "1",
            "--use_fp16",
            "--control_mode", "controlnet_important",
            "--control_type", "body+hand+face",
            "--train_dataset", "tiktok_video_arnold",
            "--v4",
            "--with_text",
            "--wonoise",
            "--local_image_dir", f"./tiktok_test_log/image_log/{session_id}/001/image",
            "--local_log_dir", f"./tiktok_test_log/tb_log/{session_id}/001/log",
            "--image_pretrain_dir", "./pretrained_weights/model_state-110000.th",
            "--local_pose_path", str(pose_path),
            "--local_cond_image_path", str(source_path)
        ]

        # Run the command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Processing failed: {stderr.decode()}")

        # Get the output images
        output_dir = OUTPUT_DIR / session_id / "001" / "image"
        output_images = list(output_dir.glob("*.png"))
        
        return {
            "session_id": session_id,
            "message": "Processing complete",
            "output_images": [str(img) for img in output_images]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{session_id}/{image_name}")
async def get_result_image(session_id: str, image_name: str):
    image_path = OUTPUT_DIR / session_id / "001" / "image" / image_name
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(str(image_path))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
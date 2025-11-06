from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil

app = FastAPI(title="School Data Upload API", version="1.0")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-school-data")
async def upload_school_data(file: UploadFile = File(...)):
    """
    Upload a school dataset (Excel/CSV) and save it for terminal AI usage.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return JSONResponse({
            "message": f"✅ File '{file.filename}' uploaded successfully!",
            "saved_path": file_path
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

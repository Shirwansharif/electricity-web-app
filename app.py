from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
import os
import json
import pickle
from typing import List, Optional
import base64
from pathlib import Path
import aiofiles
from datetime import datetime

app = FastAPI(title="Face Recognition System - Demo", version="1.0.0")

# Create necessary directories
UPLOAD_DIR = Path("uploads")
KNOWN_FACES_DIR = Path("known_faces")
ENCODINGS_FILE = Path("face_encodings.pkl")
DATA_DIR = Path("data")

for directory in [UPLOAD_DIR, KNOWN_FACES_DIR, DATA_DIR]:
    directory.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global storage for face data (simplified without face_recognition library)
known_faces = {}  # {name: [list of image paths]}

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def load_known_faces():
    """Load known faces from file"""
    global known_faces
    if ENCODINGS_FILE.exists():
        with open(ENCODINGS_FILE, 'rb') as f:
            known_faces = pickle.load(f)
    else:
        known_faces = {}

def save_known_faces():
    """Save known faces to file"""
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump(known_faces, f)

# Load on startup
load_known_faces()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    total = sum(len(paths) for paths in known_faces.values())
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_faces": total
    })

@app.post("/api/upload")
async def upload_face(name: str, file: UploadFile = File(...)):
    """Upload and train a face image - DEMO VERSION"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "هیچ دەموچاوێک نەدۆزرایەوە لە وێنەکەدا"}
            )
        
        if len(faces) > 1:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "فرە دەموچاو دۆزرایەوە. تکایە وێنەیەک بە یەک دەموچاو بنێرە"}
            )
        
        # Save the image
        file_path = KNOWN_FACES_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(str(file_path), image)
        
        # Add to known faces
        if name not in known_faces:
            known_faces[name] = []
        known_faces[name].append(str(file_path))
        
        # Save
        save_known_faces()
        
        total = sum(len(paths) for paths in known_faces.values())
        
        return JSONResponse(content={
            "success": True,
            "message": f"دەموچاوی '{name}' سەرکەوتووانە زیادکرا",
            "total_faces": total
        })
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"هەڵە: {str(e)}"}
        )

@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Recognize face from uploaded image - DEMO VERSION (Face Detection Only)"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        
        # Draw rectangles and labels
        for (x, y, w, h) in faces:
            # In demo mode, we just detect faces without recognizing
            # Use random name from known faces for demo
            if known_faces:
                import random
                name = random.choice(list(known_faces.keys()))
                confidence = round(random.uniform(75, 95), 2)  # Demo confidence
            else:
                name = "Unknown"
                confidence = 0
            
            results.append({
                "name": name,
                "confidence": confidence,
                "location": {"top": y, "right": x+w, "bottom": y+h, "left": x}
            })
            
            # Draw rectangle
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
            
            # Draw label
            label = f"{name} ({confidence:.1f}%)" if name != "Unknown" else "Detected Face"
            cv2.rectangle(image, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
            cv2.putText(image, label, (x+6, y+h-6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Convert processed image to base64
        _, buffer = cv2.imencode('.jpg', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "faces_detected": len(faces),
            "results": results,
            "image": f"data:image/jpeg;base64,{img_base64}",
            "demo_mode": True
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"هەڵە: {str(e)}"}
        )

@app.get("/api/faces")
async def get_known_faces():
    """Get list of all known faces"""
    face_counts = {name: len(paths) for name, paths in known_faces.items()}
    total = sum(face_counts.values())
    
    return JSONResponse(content={
        "success": True,
        "total_faces": total,
        "unique_people": len(known_faces),
        "faces": [{"name": name, "count": count} for name, count in face_counts.items()]
    })

@app.delete("/api/faces/{name}")
async def delete_face(name: str):
    """Delete a face from the database"""
    global known_faces
    
    if name not in known_faces:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": f"دەموچاوی '{name}' نەدۆزرایەوە"}
        )
    
    # Delete files
    for path in known_faces[name]:
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
    
    # Remove from dict
    del known_faces[name]
    
    # Save
    save_known_faces()
    
    total = sum(len(paths) for paths in known_faces.values())
    
    return JSONResponse(content={
        "success": True,
        "message": f"دەموچاوی '{name}' سڕایەوە",
        "total_faces": total
    })

@app.websocket("/ws/webcam")
async def webcam_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time webcam face detection - DEMO VERSION"""
    await websocket.accept()
    
    try:
        while True:
            # Receive image data from client
            data = await websocket.receive_text()
            
            # Decode base64 image
            img_data = base64.b64decode(data.split(',')[1])
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Resize for faster processing
            small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            
            # Find faces
            faces = face_cascade.detectMultiScale(small_gray, 1.3, 5)
            
            results = []
            
            for (x, y, w, h) in faces:
                # Scale back up
                x, y, w, h = x*2, y*2, w*2, h*2
                
                # Demo: use random known face or unknown
                if known_faces:
                    import random
                    name = random.choice(list(known_faces.keys()))
                    confidence = round(random.uniform(75, 95), 2)
                else:
                    name = "Unknown"
                    confidence = 0
                
                results.append({
                    "name": name,
                    "confidence": confidence,
                    "location": {"top": y, "right": x+w, "bottom": y+h, "left": x}
                })
            
            # Send results back
            await websocket.send_json({
                "faces": results,
                "demo_mode": True
            })
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")

@app.get("/api/demo-info")
async def demo_info():
    """Return demo mode information"""
    return JSONResponse(content={
        "demo_mode": True,
        "message": "ئەمە وەشانی Demo یە - تەنها دۆزینەوەی دەموچاو، بێ ناسینەوەی ڕاستەقینە",
        "message_en": "This is a DEMO version - Face detection only, without real recognition",
        "note": "بۆ ناسینەوەی ڕاستەقینە، dlib و face_recognition پێویستە"
    })

if __name__ == "__main__":
    import uvicorn
    print("🎯 Starting Face Recognition System - DEMO Mode")
    print("📝 Note: Using OpenCV face detection (without face_recognition library)")
    print("🌐 Access from: http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

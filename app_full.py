from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import face_recognition
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

app = FastAPI(title="Face Recognition System", version="1.0.0")

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

# Global storage for face encodings
known_face_encodings = []
known_face_names = []

def load_encodings():
    """Load face encodings from file"""
    global known_face_encodings, known_face_names
    if ENCODINGS_FILE.exists():
        with open(ENCODINGS_FILE, 'rb') as f:
            data = pickle.load(f)
            known_face_encodings = data.get('encodings', [])
            known_face_names = data.get('names', [])
        print(f"Loaded {len(known_face_names)} face encodings")
    else:
        known_face_encodings = []
        known_face_names = []

def save_encodings():
    """Save face encodings to file"""
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump({
            'encodings': known_face_encodings,
            'names': known_face_names
        }, f)
    print(f"Saved {len(known_face_names)} face encodings")

# Load encodings on startup
load_encodings()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_faces": len(known_face_names)
    })

@app.post("/api/upload")
async def upload_face(name: str, file: UploadFile = File(...)):
    """Upload and train a face image"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "No face detected in the image"}
            )
        
        if len(face_locations) > 1:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Multiple faces detected. Please upload image with single face"}
            )
        
        # Get face encoding
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if len(face_encodings) > 0:
            # Save the image
            file_path = KNOWN_FACES_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(str(file_path), image)
            
            # Add to known faces
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
            
            # Save encodings
            save_encodings()
            
            return JSONResponse(content={
                "success": True,
                "message": f"Face for '{name}' uploaded and trained successfully",
                "total_faces": len(known_face_names)
            })
        else:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Could not encode face"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )

@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Recognize face from uploaded image"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        results = []
        
        # Draw rectangles and labels on image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if face matches any known face
            if len(known_face_encodings) > 0:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"
                confidence = 0
                
                # Calculate face distances
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        confidence = (1 - face_distances[best_match_index]) * 100
                
                results.append({
                    "name": name,
                    "confidence": round(confidence, 2),
                    "location": {"top": top, "right": right, "bottom": bottom, "left": left}
                })
                
                # Draw rectangle
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(image, (left, top), (right, bottom), color, 2)
                
                # Draw label
                label = f"{name} ({confidence:.1f}%)" if name != "Unknown" else "Unknown"
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(image, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            else:
                results.append({
                    "name": "Unknown",
                    "confidence": 0,
                    "location": {"top": top, "right": right, "bottom": bottom, "left": left}
                })
        
        # Convert processed image to base64
        _, buffer = cv2.imencode('.jpg', image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "faces_detected": len(face_locations),
            "results": results,
            "image": f"data:image/jpeg;base64,{img_base64}"
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )

@app.get("/api/faces")
async def get_known_faces():
    """Get list of all known faces"""
    unique_names = list(set(known_face_names))
    face_counts = {name: known_face_names.count(name) for name in unique_names}
    
    return JSONResponse(content={
        "success": True,
        "total_faces": len(known_face_names),
        "unique_people": len(unique_names),
        "faces": [{"name": name, "count": count} for name, count in face_counts.items()]
    })

@app.delete("/api/faces/{name}")
async def delete_face(name: str):
    """Delete a face from the database"""
    global known_face_encodings, known_face_names
    
    # Find and remove all instances of this name
    indices_to_remove = [i for i, n in enumerate(known_face_names) if n == name]
    
    if not indices_to_remove:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": f"Face '{name}' not found"}
        )
    
    # Remove from lists (reverse order to maintain correct indices)
    for i in sorted(indices_to_remove, reverse=True):
        del known_face_encodings[i]
        del known_face_names[i]
    
    # Save updated encodings
    save_encodings()
    
    return JSONResponse(content={
        "success": True,
        "message": f"Deleted {len(indices_to_remove)} encoding(s) for '{name}'",
        "total_faces": len(known_face_names)
    })

@app.websocket("/ws/webcam")
async def webcam_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time webcam face recognition"""
    await websocket.accept()
    
    try:
        while True:
            # Receive image data from client
            data = await websocket.receive_text()
            
            # Decode base64 image
            img_data = base64.b64decode(data.split(',')[1])
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize for faster processing
            small_image = cv2.resize(rgb_image, (0, 0), fx=0.25, fy=0.25)
            
            # Find faces
            face_locations = face_recognition.face_locations(small_image)
            face_encodings = face_recognition.face_encodings(small_image, face_locations)
            
            results = []
            
            for face_encoding, face_location in zip(face_encodings, face_locations):
                name = "Unknown"
                confidence = 0
                
                if len(known_face_encodings) > 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            confidence = (1 - face_distances[best_match_index]) * 100
                
                # Scale back up face locations
                top, right, bottom, left = [v * 4 for v in face_location]
                
                results.append({
                    "name": name,
                    "confidence": round(confidence, 2),
                    "location": {"top": top, "right": right, "bottom": bottom, "left": left}
                })
            
            # Send results back
            await websocket.send_json({
                "faces": results
            })
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

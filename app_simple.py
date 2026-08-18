from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
from pathlib import Path
from datetime import datetime
import base64

app = FastAPI(title="Face Recognition System - UI Demo", version="1.0.0")

# Create necessary directories
UPLOAD_DIR = Path("uploads")
KNOWN_FACES_DIR = Path("known_faces")
DATA_DIR = Path("data")

for directory in [UPLOAD_DIR, KNOWN_FACES_DIR, DATA_DIR]:
    directory.mkdir(exist_ok=True)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

templates = Jinja2Templates(directory="templates")

# Simple storage
known_faces_db = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_faces": len(known_faces_db)
    })

@app.post("/api/upload")
async def upload_face(name: str = Form(...), file: UploadFile = File(...)):
    """Upload face - UI Demo"""
    try:
        # Save file
        file_path = KNOWN_FACES_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Add to database
        if name not in known_faces_db:
            known_faces_db[name] = []
        known_faces_db[name].append(str(file_path))
        
        return JSONResponse(content={
            "success": True,
            "message": f"✅ دەموچاوی '{name}' سەرکەوتووانە زیادکرا!",
            "total_faces": sum(len(v) for v in known_faces_db.values())
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"هەڵە: {str(e)}"}
        )

@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Recognize face - UI Demo"""
    try:
        import random
        
        # Read file
        contents = await file.read()
        
        # Demo: pretend we found faces
        img_base64 = base64.b64encode(contents).decode('utf-8')
        
        # Generate demo results
        results = []
        if known_faces_db:
            for i in range(random.randint(1, 2)):
                name = random.choice(list(known_faces_db.keys()))
                results.append({
                    "name": name,
                    "confidence": round(random.uniform(80, 95), 2),
                    "location": {"top": 100, "right": 300, "bottom": 300, "left": 100}
                })
        
        return JSONResponse(content={
            "success": True,
            "faces_detected": len(results),
            "results": results,
            "image": f"data:image/jpeg;base64,{img_base64}",
            "demo_mode": True,
            "message": "🎯 UI Demo Mode - بینینی ڕووکار"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"هەڵە: {str(e)}"}
        )

@app.get("/api/faces")
async def get_known_faces():
    """Get list of all known faces"""
    face_list = []
    for name, paths in known_faces_db.items():
        face_list.append({"name": name, "count": len(paths)})
    
    return JSONResponse(content={
        "success": True,
        "total_faces": sum(len(v) for v in known_faces_db.values()),
        "unique_people": len(known_faces_db),
        "faces": face_list
    })

@app.delete("/api/faces/{name}")
async def delete_face(name: str):
    """Delete a face"""
    if name in known_faces_db:
        # Delete files
        for path in known_faces_db[name]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
        del known_faces_db[name]
        
        return JSONResponse(content={
            "success": True,
            "message": f"✅ دەموچاوی '{name}' سڕایەوە",
            "total_faces": sum(len(v) for v in known_faces_db.values())
        })
    else:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": f"'{name}' نەدۆزرایەوە"}
        )

@app.websocket("/ws/webcam")
async def webcam_endpoint(websocket: WebSocket):
    """WebSocket for webcam - UI Demo"""
    await websocket.accept()
    import random
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # Demo: send back random detections
            results = []
            if known_faces_db and random.random() > 0.3:
                name = random.choice(list(known_faces_db.keys()))
                results.append({
                    "name": name,
                    "confidence": round(random.uniform(75, 95), 2),
                    "location": {"top": 50, "right": 250, "bottom": 250, "left": 50}
                })
            
            await websocket.send_json({
                "faces": results,
                "demo_mode": True
            })
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎯 Face Recognition System - UI DEMO")
    print("="*60)
    print("📱 Access from your mobile:")
    print("   http://0.0.0.0:8000")
    print("\n💡 Note: This is UI demo - showing interface only")
    print("   Full face recognition requires additional setup")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Face Recognition Web Application
سیستەمی ناسینەوەی دەموچاو - Web App

FastAPI backend for the face recognition system
"""

from fastapi import FastAPI, File, UploadFile, Form, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys
import cv2
import numpy as np
from PIL import Image
import io
import base64
import logging

# Add parent directory to path to import shared module
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.face_engine import FaceRecognitionEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Face Recognition System | سیستەمی ناسینەوەی دەموچاو")

# Setup directories
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize face recognition engine
try:
    engine = FaceRecognitionEngine(data_dir="data/faces")
    logger.info("✅ Face Recognition Engine initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize engine: {e}")
    engine = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    stats = {"total_faces": 0, "unique_people": 0, "database_size": 0}
    if engine:
        stats = engine.get_statistics()
    
    # FIXED: Use explicit parameter names to avoid Jinja2 cache issue
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=stats
    )


@app.post("/api/add-person")
async def add_person(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """Add a new person to the database"""
    try:
        if not engine:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Engine not initialized"}
            )
        
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid image file"}
            )
        
        # Add person to database
        success = engine.add_person(name, image)
        
        if success:
            stats = engine.get_statistics()
            return JSONResponse(content={
                "success": True,
                "message": f"✅ {name} added successfully | {name} زیادکرا بە سەرکەوتوویی",
                "stats": stats
            })
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "❌ No face detected in image | هیچ دەموچاوێک نەدۆزرایەوە"
                }
            )
    
    except Exception as e:
        logger.error(f"Error adding person: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )


@app.post("/api/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Recognize faces in uploaded image"""
    try:
        if not engine:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Engine not initialized"}
            )
        
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid image file"}
            )
        
        # Recognize faces
        results = engine.recognize_faces(image)
        
        if len(results) == 0:
            return JSONResponse(content={
                "success": True,
                "faces": [],
                "message": "⚠️ No faces detected | هیچ دەموچاوێک نەدۆزرایەوە"
            })
        
        # Draw results on image
        output_image = engine.draw_results(image, results)
        
        # Convert to base64 for display
        _, buffer = cv2.imencode('.jpg', output_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Format results
        faces_info = []
        for result in results:
            faces_info.append({
                "name": result["name"],
                "confidence": f"{result['confidence']:.2%}",
                "location": result["box"]
            })
        
        return JSONResponse(content={
            "success": True,
            "faces": faces_info,
            "image": f"data:image/jpeg;base64,{img_base64}",
            "message": f"✅ Found {len(results)} face(s) | {len(results)} دەموچاو دۆزرایەوە"
        })
    
    except Exception as e:
        logger.error(f"Error recognizing face: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )


@app.get("/api/people")
async def get_people():
    """Get list of all people in database"""
    try:
        if not engine:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Engine not initialized"}
            )
        
        people = engine.get_all_people()
        return JSONResponse(content={
            "success": True,
            "people": people,
            "count": len(people)
        })
    
    except Exception as e:
        logger.error(f"Error getting people: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )


@app.delete("/api/person/{name}")
async def delete_person(name: str):
    """Delete a person from database"""
    try:
        if not engine:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Engine not initialized"}
            )
        
        success = engine.delete_person(name)
        
        if success:
            stats = engine.get_statistics()
            return JSONResponse(content={
                "success": True,
                "message": f"✅ {name} deleted | {name} سڕایەوە",
                "stats": stats
            })
        else:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": f"Person {name} not found"}
            )
    
    except Exception as e:
        logger.error(f"Error deleting person: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )


@app.get("/api/stats")
async def get_stats():
    """Get database statistics"""
    try:
        if not engine:
            return JSONResponse(content={
                "success": True,
                "stats": {"total_faces": 0, "unique_people": 0, "database_size": 0}
            })
        
        stats = engine.get_statistics()
        return JSONResponse(content={
            "success": True,
            "stats": stats
        })
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )


@app.websocket("/ws/webcam")
async def webcam_recognition(websocket: WebSocket):
    """WebSocket endpoint for real-time webcam recognition"""
    await websocket.accept()
    logger.info("🎥 Webcam WebSocket connected")
    
    try:
        while True:
            # Receive frame from client
            data = await websocket.receive_json()
            
            if data.get("type") == "frame":
                try:
                    # Decode base64 image
                    img_data = base64.b64decode(data["image"].split(",")[1])
                    nparr = np.frombuffer(img_data, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if image is not None and engine:
                        # Recognize faces
                        results = engine.recognize_faces(image)
                        
                        # Send results back
                        await websocket.send_json({
                            "type": "results",
                            "faces": [{
                                "name": r["name"],
                                "confidence": f"{r['confidence']:.2%}",
                                "location": r["box"]
                            } for r in results]
                        })
                
                except Exception as e:
                    logger.error(f"Error processing frame: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
    
    except WebSocketDisconnect:
        logger.info("🎥 Webcam WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting Face Recognition Web Application")
    print("   سیستەمی ناسینەوەی دەموچاو")
    print("="*60)
    print("📱 Access at: http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

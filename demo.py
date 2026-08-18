from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Face Recognition Demo")

# Create directories
UPLOAD_DIR = Path("uploads")
KNOWN_FACES_DIR = Path("known_faces")
for directory in [UPLOAD_DIR, KNOWN_FACES_DIR]:
    directory.mkdir(exist_ok=True)

known_faces_db = {}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سیستەمی ناسینەوەی دەموچاو - Face Recognition</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        .card-header {
            border-radius: 15px 15px 0 0 !important;
            padding: 1rem 1.5rem;
            font-weight: bold;
        }
        .btn {
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 600;
        }
        .result {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .navbar {
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="bi bi-person-bounding-box"></i>
                سیستەمی ناسینەوەی دەموچاو
            </a>
            <span class="navbar-text text-white">
                <i class="bi bi-people-fill"></i>
                کەسی ناسراو: <span id="totalFaces" class="badge bg-light text-primary">0</span>
            </span>
        </div>
    </nav>

    <div class="container">
        <div class="row g-4">
            <!-- Upload Panel -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-cloud-upload"></i>
                            زیادکردنی دەموچاوی نوێ
                        </h5>
                    </div>
                    <div class="card-body">
                        <form id="uploadForm">
                            <div class="mb-3">
                                <label class="form-label">ناوی کەس:</label>
                                <input type="text" class="form-control" id="personName" placeholder="ناو بنووسە..." required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">وێنە هەڵبژێرە:</label>
                                <input type="file" class="form-control" id="uploadImage" accept="image/*" required>
                            </div>
                            <button type="submit" class="btn btn-success w-100">
                                <i class="bi bi-check-circle"></i>
                                زیادکردن
                            </button>
                        </form>
                        
                        <hr class="my-4">
                        
                        <h6 class="text-muted mb-3">دەموچاوە ناسراوەکان:</h6>
                        <div id="knownFacesList" class="list-group">
                            <div class="text-center text-muted py-3">
                                <i class="bi bi-inbox"></i>
                                هێشتا هیچ دەموچاوێک زیاد نەکراوە
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Info Panel -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-info-circle"></i>
                            زانیاری
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-success">
                            <h6><i class="bi bi-check-circle"></i> بەرنامە کار دەکات!</h6>
                            <p class="mb-0">UI Demo Mode - ڕووکاری جوان و کارا</p>
                        </div>
                        
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6 class="card-title">تایبەتمەندییەکان:</h6>
                                <ul class="mb-0">
                                    <li>✅ زیادکردنی دەموچاو</li>
                                    <li>✅ بینینی لیستی ناسراوەکان</li>
                                    <li>✅ سڕینەوەی دەموچاو</li>
                                    <li>✅ ڕووکاری جوان و مۆدێرن</li>
                                    <li>✅ پشتگیری کوردی</li>
                                </ul>
                            </div>
                        </div>

                        <div class="mt-3">
                            <h6>دۆخی سیستەم:</h6>
                            <div class="result">
                                <i class="bi bi-check-circle-fill"></i>
                                ✅ سێرڤەر کار دەکات
                                <br>
                                ✅ API ئامادەیە
                                <br>
                                ✅ UI باشە
                            </div>
                        </div>

                        <div class="alert alert-info mt-3">
                            <strong>تێبینی:</strong> بۆ تایبەتمەندیی تەواو (وێبکام، ناسینەوە)، پێویستی بە dlib هەیە.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="notificationToast" class="toast" role="alert">
            <div class="toast-header">
                <i class="bi bi-bell-fill me-2"></i>
                <strong class="me-auto">ئاگاداری</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body" id="toastMessage"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showNotification(message, type = 'info') {
            const toast = new bootstrap.Toast(document.getElementById('notificationToast'));
            const toastBody = document.getElementById('toastMessage');
            toastBody.textContent = message;
            toast.show();
        }

        function loadKnownFaces() {
            fetch('/api/faces')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('knownFacesList');
                    if (data.success && data.faces.length > 0) {
                        container.innerHTML = data.faces.map(face => `
                            <div class="list-group-item d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="bi bi-person-circle"></i>
                                    <strong>${face.name}</strong>
                                    <span class="badge bg-primary rounded-pill ms-2">${face.count}</span>
                                </div>
                                <button class="btn btn-sm btn-danger" onclick="deleteFace('${face.name}')">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        `).join('');
                    } else {
                        container.innerHTML = '<div class="text-center text-muted py-3"><i class="bi bi-inbox"></i> هیچ دەموچاوێک نییە</div>';
                    }
                    document.getElementById('totalFaces').textContent = data.total_faces || 0;
                });
        }

        async function deleteFace(name) {
            if (!confirm(`سڕینەوەی "${name}"?`)) return;
            const response = await fetch(`/api/faces/${encodeURIComponent(name)}`, { method: 'DELETE' });
            const data = await response.json();
            showNotification(data.message, data.success ? 'success' : 'danger');
            if (data.success) loadKnownFaces();
        }

        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('personName').value.trim();
            const file = document.getElementById('uploadImage').files[0];
            
            if (!name || !file) {
                showNotification('تکایە ناو و وێنە دابنێ!', 'warning');
                return;
            }
            
            const formData = new FormData();
            formData.append('name', name);
            formData.append('file', file);
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                showNotification(data.message, data.success ? 'success' : 'danger');
                if (data.success) {
                    document.getElementById('uploadForm').reset();
                    loadKnownFaces();
                }
            } catch (error) {
                showNotification('هەڵە: ' + error.message, 'danger');
            }
        });

        loadKnownFaces();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE

@app.post("/api/upload")
async def upload_face(name: str = Form(...), file: UploadFile = File(...)):
    try:
        file_path = KNOWN_FACES_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        if name not in known_faces_db:
            known_faces_db[name] = []
        known_faces_db[name].append(str(file_path))
        
        return JSONResponse(content={
            "success": True,
            "message": f"✅ دەموچاوی '{name}' زیادکرا!",
            "total_faces": sum(len(v) for v in known_faces_db.values())
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"هەڵە: {str(e)}"}
        )

@app.get("/api/faces")
async def get_known_faces():
    face_list = [{"name": name, "count": len(paths)} for name, paths in known_faces_db.items()]
    return JSONResponse(content={
        "success": True,
        "total_faces": sum(len(v) for v in known_faces_db.values()),
        "unique_people": len(known_faces_db),
        "faces": face_list
    })

@app.delete("/api/faces/{name}")
async def delete_face(name: str):
    if name in known_faces_db:
        for path in known_faces_db[name]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
        del known_faces_db[name]
        return JSONResponse(content={
            "success": True,
            "message": f"✅ '{name}' سڕایەوە",
            "total_faces": sum(len(v) for v in known_faces_db.values())
        })
    return JSONResponse(status_code=404, content={"success": False, "message": f"'{name}' نەدۆزرایەوە"})

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🎯 Face Recognition System - Working Demo")
    print("="*60)
    print("✅ Server starting...")
    print("📱 Open in browser: http://localhost:8000")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

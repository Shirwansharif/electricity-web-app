// Global variables
let webcamStream = null;
let websocket = null;
let webcamInterval = null;
let isRecognizing = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadKnownFaces();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Upload form
    document.getElementById('uploadForm').addEventListener('submit', handleUpload);
    
    // Image preview
    document.getElementById('uploadImage').addEventListener('change', function(e) {
        previewImage(e.target.files[0], 'previewImg', 'uploadPreview');
    });
    
    // Webcam controls
    document.getElementById('startWebcam').addEventListener('click', startWebcam);
    document.getElementById('stopWebcam').addEventListener('click', stopWebcam);
    
    // Recognize form
    document.getElementById('recognizeForm').addEventListener('submit', handleRecognition);
}

// Show notification
function showNotification(message, type = 'info') {
    const toast = new bootstrap.Toast(document.getElementById('notificationToast'));
    const toastBody = document.getElementById('toastMessage');
    toastBody.textContent = message;
    
    const toastHeader = document.querySelector('.toast-header');
    toastHeader.className = `toast-header bg-${type} text-white`;
    
    toast.show();
}

// Show/hide loading
function setLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

// Preview image
function previewImage(file, imgId, containerId) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(imgId).src = e.target.result;
            document.getElementById(containerId).style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Handle upload and training
async function handleUpload(e) {
    e.preventDefault();
    
    const name = document.getElementById('personName').value.trim();
    const fileInput = document.getElementById('uploadImage');
    const file = fileInput.files[0];
    
    if (!name || !file) {
        showNotification('تکایە ناو و وێنە دابنێ!', 'warning');
        return;
    }
    
    setLoading(true);
    
    const formData = new FormData();
    formData.append('name', name);
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            document.getElementById('uploadForm').reset();
            document.getElementById('uploadPreview').style.display = 'none';
            document.getElementById('totalFaces').textContent = data.total_faces;
            loadKnownFaces();
        } else {
            showNotification(data.message, 'danger');
        }
    } catch (error) {
        showNotification('هەڵەیەک ڕوویدا: ' + error.message, 'danger');
    } finally {
        setLoading(false);
    }
}

// Load known faces list
async function loadKnownFaces() {
    try {
        const response = await fetch('/api/faces');
        const data = await response.json();
        
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
            container.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="bi bi-inbox"></i>
                    هێشتا هیچ دەموچاوێک زیاد نەکراوە
                </div>
            `;
        }
        
        document.getElementById('totalFaces').textContent = data.total_faces || 0;
    } catch (error) {
        console.error('Error loading faces:', error);
    }
}

// Delete face
async function deleteFace(name) {
    if (!confirm(`دڵنیای لە سڕینەوەی دەموچاوی "${name}"?`)) {
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(`/api/faces/${encodeURIComponent(name)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            loadKnownFaces();
        } else {
            showNotification(data.message, 'danger');
        }
    } catch (error) {
        showNotification('هەڵەیەک ڕوویدا: ' + error.message, 'danger');
    } finally {
        setLoading(false);
    }
}

// Start webcam
async function startWebcam() {
    try {
        // Request webcam access
        webcamStream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        
        const video = document.getElementById('webcam');
        video.srcObject = webcamStream;
        
        // Show webcam container
        document.getElementById('webcamContainer').style.display = 'block';
        document.getElementById('startWebcam').style.display = 'none';
        document.getElementById('stopWebcam').style.display = 'inline-block';
        document.getElementById('webcamStatus').style.display = 'block';
        document.getElementById('webcamStatus').textContent = 'پەیوەندی بە سێرڤەرەوە...';
        
        // Connect to WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/webcam`;
        
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = function() {
            document.getElementById('webcamStatus').textContent = 'ناسینەوە کارایە - وێبکام چالاکە';
            document.getElementById('webcamStatus').className = 'alert alert-success mt-3';
            isRecognizing = true;
            startRecognitionLoop();
        };
        
        websocket.onerror = function(error) {
            console.error('WebSocket error:', error);
            document.getElementById('webcamStatus').textContent = 'هەڵە لە پەیوەندیکردن';
            document.getElementById('webcamStatus').className = 'alert alert-danger mt-3';
        };
        
        websocket.onclose = function() {
            document.getElementById('webcamStatus').textContent = 'پەیوەندی پچڕا';
            document.getElementById('webcamStatus').className = 'alert alert-warning mt-3';
            isRecognizing = false;
        };
        
        websocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            displayWebcamResults(data.faces);
        };
        
    } catch (error) {
        showNotification('دەستگەیشتن بە وێبکام سەرکەوتوو نەبوو: ' + error.message, 'danger');
        console.error('Webcam error:', error);
    }
}

// Stop webcam
function stopWebcam() {
    // Stop webcam stream
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    
    // Close WebSocket
    if (websocket) {
        websocket.close();
        websocket = null;
    }
    
    // Clear interval
    if (webcamInterval) {
        clearInterval(webcamInterval);
        webcamInterval = null;
    }
    
    isRecognizing = false;
    
    // Reset UI
    document.getElementById('webcamContainer').style.display = 'none';
    document.getElementById('startWebcam').style.display = 'inline-block';
    document.getElementById('stopWebcam').style.display = 'none';
    document.getElementById('webcamStatus').style.display = 'none';
    document.getElementById('webcamResults').style.display = 'none';
}

// Start recognition loop
function startRecognitionLoop() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const ctx = canvas.getContext('2d');
    
    webcamInterval = setInterval(() => {
        if (!isRecognizing || !video.videoWidth) return;
        
        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw video frame to canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get image data and send to server
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(imageData);
        }
    }, 500); // Process every 500ms
}

// Display webcam results
function displayWebcamResults(faces) {
    const canvas = document.getElementById('webcamCanvas');
    const ctx = canvas.getContext('2d');
    const video = document.getElementById('webcam');
    
    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw rectangles and labels
    faces.forEach(face => {
        const { top, right, bottom, left } = face.location;
        const color = face.name !== 'Unknown' ? '#00ff00' : '#ff0000';
        
        // Draw rectangle
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(left, top, right - left, bottom - top);
        
        // Draw label background
        ctx.fillStyle = color;
        ctx.fillRect(left, bottom, right - left, 35);
        
        // Draw label text
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 16px Arial';
        const label = face.name !== 'Unknown' 
            ? `${face.name} (${face.confidence.toFixed(1)}%)` 
            : 'Unknown';
        ctx.fillText(label, left + 6, bottom + 23);
    });
    
    // Update results list
    const resultsDiv = document.getElementById('webcamResults');
    const facesDiv = document.getElementById('webcamFaces');
    
    if (faces.length > 0) {
        resultsDiv.style.display = 'block';
        facesDiv.innerHTML = faces.map(face => {
            const cardClass = face.name !== 'Unknown' ? 'result-card' : 'result-card unknown';
            return `
                <div class="${cardClass}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="bi bi-person-fill"></i>
                            <strong>${face.name}</strong>
                        </div>
                        <div>
                            ${face.confidence > 0 ? `
                                <span class="badge bg-light text-dark">${face.confidence.toFixed(1)}%</span>
                            ` : ''}
                        </div>
                    </div>
                    ${face.confidence > 0 ? `
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${face.confidence}%"></div>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    } else {
        resultsDiv.style.display = 'none';
    }
}

// Handle image recognition
async function handleRecognition(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('recognizeImage');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('تکایە وێنەیەک هەڵبژێرە!', 'warning');
        return;
    }
    
    setLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/recognize', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecognitionResults(data);
            showNotification(`${data.faces_detected} دەموچاو دۆزرایەوە`, 'success');
        } else {
            showNotification(data.message, 'danger');
        }
    } catch (error) {
        showNotification('هەڵەیەک ڕوویدا: ' + error.message, 'danger');
    } finally {
        setLoading(false);
    }
}

// Display recognition results
function displayRecognitionResults(data) {
    const resultDiv = document.getElementById('recognitionResult');
    const imageDiv = document.getElementById('resultImage');
    const detailsDiv = document.getElementById('resultDetails');
    
    // Show processed image
    imageDiv.innerHTML = `<img src="${data.image}" class="img-fluid rounded border" style="max-height: 400px;">`;
    
    // Show details
    if (data.results.length > 0) {
        detailsDiv.innerHTML = `
            <div class="alert alert-info">
                <strong>تێبینی:</strong> ${data.faces_detected} دەموچاو دۆزرایەوە
            </div>
            ${data.results.map(result => {
                const cardClass = result.name !== 'Unknown' ? 'result-card' : 'result-card unknown';
                return `
                    <div class="${cardClass}">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <i class="bi bi-person-fill"></i>
                                <strong>${result.name}</strong>
                            </div>
                            <div>
                                ${result.confidence > 0 ? `
                                    <span class="badge bg-light text-dark">${result.confidence.toFixed(1)}%</span>
                                ` : ''}
                            </div>
                        </div>
                        ${result.confidence > 0 ? `
                            <div class="confidence-bar mt-2">
                                <div class="confidence-fill" style="width: ${result.confidence}%"></div>
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('')}
        `;
    } else {
        detailsDiv.innerHTML = `
            <div class="alert alert-warning">
                هیچ دەموچاوێک نەدۆزرایەوە
            </div>
        `;
    }
    
    resultDiv.style.display = 'block';
    
    // Reset form
    document.getElementById('recognizeForm').reset();
}

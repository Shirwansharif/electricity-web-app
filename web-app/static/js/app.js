// Face Recognition System - Client-side JavaScript

// Global variables
let webcamStream = null;
let webcamSocket = null;
let webcamInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Face Recognition System initialized');
    
    // Load initial data
    loadPeopleList();
    
    // Setup event listeners
    setupEventListeners();
});

// Setup all event listeners
function setupEventListeners() {
    // Add Person Form
    document.getElementById('addPersonForm').addEventListener('submit', handleAddPerson);
    document.getElementById('personImage').addEventListener('change', function(e) {
        previewImage(e, 'addPreview');
    });
    
    // Recognize Form
    document.getElementById('recognizeForm').addEventListener('submit', handleRecognize);
    document.getElementById('recognizeImage').addEventListener('change', function(e) {
        previewImage(e, 'recognizePreview');
    });
    
    // Webcam buttons
    document.getElementById('startWebcam').addEventListener('click', startWebcam);
    document.getElementById('stopWebcam').addEventListener('click', stopWebcam);
}

// Preview uploaded image
function previewImage(event, previewId) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            preview.src = e.target.result;
            preview.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
    }
}

// Handle Add Person form submission
async function handleAddPerson(e) {
    e.preventDefault();
    
    const name = document.getElementById('personName').value.trim();
    const fileInput = document.getElementById('personImage');
    const file = fileInput.files[0];
    
    if (!name || !file) {
        showResult('addResult', 'danger', 'Please enter a name and select an image');
        return;
    }
    
    // Show loading
    showResult('addResult', 'info', '<span class="spinner-border spinner-border-sm me-2"></span>چاوەڕوان... Processing...');
    
    // Prepare form data
    const formData = new FormData();
    formData.append('name', name);
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/add-person', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult('addResult', 'success', data.message);
            
            // Update statistics
            if (data.stats) {
                updateStats(data.stats);
            }
            
            // Reload people list
            loadPeopleList();
            
            // Reset form
            document.getElementById('addPersonForm').reset();
            document.getElementById('addPreview').classList.add('d-none');
        } else {
            showResult('addResult', 'danger', data.message);
        }
    } catch (error) {
        console.error('Error adding person:', error);
        showResult('addResult', 'danger', '❌ Error: ' + error.message);
    }
}

// Handle Recognize form submission
async function handleRecognize(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('recognizeImage');
    const file = fileInput.files[0];
    
    if (!file) {
        showResult('recognizeResult', 'danger', 'Please select an image');
        return;
    }
    
    // Show loading
    showResult('recognizeResult', 'info', '<span class="spinner-border spinner-border-sm me-2"></span>ناسینەوە... Recognizing...');
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/recognize', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.faces && data.faces.length > 0) {
                // Show recognized faces
                let resultHtml = `<div class="alert alert-success">${data.message}</div>`;
                
                // Display result image if available
                if (data.image) {
                    resultHtml += `<img src="${data.image}" class="result-image" alt="Result">`;
                }
                
                // Display face details
                resultHtml += '<div class="mt-3">';
                data.faces.forEach((face, index) => {
                    const isUnknown = face.name === 'Unknown';
                    resultHtml += `
                        <div class="face-result ${isUnknown ? 'unknown' : ''} fade-in">
                            <div class="face-name">
                                ${isUnknown ? '❌' : '✅'} ${face.name}
                            </div>
                            ${!isUnknown ? `<div class="face-confidence">دڵنیایی | Confidence: ${face.confidence}</div>` : ''}
                        </div>
                    `;
                });
                resultHtml += '</div>';
                
                document.getElementById('recognizeResult').innerHTML = resultHtml;
            } else {
                showResult('recognizeResult', 'warning', data.message);
            }
        } else {
            showResult('recognizeResult', 'danger', data.message);
        }
    } catch (error) {
        console.error('Error recognizing face:', error);
        showResult('recognizeResult', 'danger', '❌ Error: ' + error.message);
    }
}

// Load people list
async function loadPeopleList() {
    const listDiv = document.getElementById('peopleList');
    listDiv.innerHTML = '<p class="text-muted">چاوەڕوان... Loading...</p>';
    
    try {
        const response = await fetch('/api/people');
        const data = await response.json();
        
        if (data.success && data.people && data.people.length > 0) {
            let html = '';
            data.people.forEach(name => {
                html += `
                    <div class="person-item">
                        <span class="person-name">${name}</span>
                        <button class="btn btn-sm btn-danger btn-delete" onclick="deletePerson('${name}')">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;
            });
            listDiv.innerHTML = html;
        } else {
            listDiv.innerHTML = '<p class="text-muted">هیچ کەسایەتییەک نییە | No people added yet</p>';
        }
    } catch (error) {
        console.error('Error loading people:', error);
        listDiv.innerHTML = '<p class="text-danger">❌ Error loading people</p>';
    }
}

// Delete person
async function deletePerson(name) {
    if (!confirm(`دڵنیای لە سڕینەوەی ${name}؟\nAre you sure you want to delete ${name}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/person/${encodeURIComponent(name)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update statistics
            if (data.stats) {
                updateStats(data.stats);
            }
            
            // Reload people list
            loadPeopleList();
            
            // Show success message
            showResult('addResult', 'success', data.message);
        } else {
            showResult('addResult', 'danger', data.message);
        }
    } catch (error) {
        console.error('Error deleting person:', error);
        showResult('addResult', 'danger', '❌ Error: ' + error.message);
    }
}

// Start webcam recognition
async function startWebcam() {
    try {
        // Request webcam access
        webcamStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 }
            } 
        });
        
        const video = document.getElementById('webcam');
        video.srcObject = webcamStream;
        
        // Update button states
        document.getElementById('startWebcam').disabled = true;
        document.getElementById('stopWebcam').disabled = false;
        
        // Connect WebSocket
        connectWebSocket();
        
        // Start sending frames
        webcamInterval = setInterval(sendWebcamFrame, 1000); // Send frame every second
        
        showResult('webcamResults', 'success', '✅ وێبکام کارپێکرا | Webcam started');
        
    } catch (error) {
        console.error('Error accessing webcam:', error);
        showResult('webcamResults', 'danger', '❌ هیچ وێبکامێک نەدۆزرایەوە | No webcam found');
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
    if (webcamSocket) {
        webcamSocket.close();
        webcamSocket = null;
    }
    
    // Clear interval
    if (webcamInterval) {
        clearInterval(webcamInterval);
        webcamInterval = null;
    }
    
    // Clear video
    const video = document.getElementById('webcam');
    video.srcObject = null;
    
    // Update button states
    document.getElementById('startWebcam').disabled = false;
    document.getElementById('stopWebcam').disabled = true;
    
    // Clear results
    document.getElementById('webcamResults').innerHTML = '';
}

// Connect WebSocket for webcam recognition
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/webcam`;
    
    webcamSocket = new WebSocket(wsUrl);
    
    webcamSocket.onopen = function() {
        console.log('🎥 WebSocket connected');
    };
    
    webcamSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'results') {
            displayWebcamResults(data.faces);
        } else if (data.type === 'error') {
            console.error('WebSocket error:', data.message);
        }
    };
    
    webcamSocket.onerror = function(error) {
        console.error('WebSocket error:', error);
        showResult('webcamResults', 'danger', '❌ Connection error');
    };
    
    webcamSocket.onclose = function() {
        console.log('🎥 WebSocket disconnected');
    };
}

// Send webcam frame via WebSocket
function sendWebcamFrame() {
    if (!webcamSocket || webcamSocket.readyState !== WebSocket.OPEN) {
        return;
    }
    
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const context = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to base64 and send
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    
    webcamSocket.send(JSON.stringify({
        type: 'frame',
        image: imageData
    }));
}

// Display webcam recognition results
function displayWebcamResults(faces) {
    const resultsDiv = document.getElementById('webcamResults');
    
    if (faces && faces.length > 0) {
        let html = '<div class="alert alert-success">✅ دەموچاو دۆزرایەوە | Faces detected</div>';
        
        faces.forEach(face => {
            const isUnknown = face.name === 'Unknown';
            html += `
                <div class="face-result ${isUnknown ? 'unknown' : ''} fade-in">
                    <div class="face-name">
                        ${isUnknown ? '❌' : '✅'} ${face.name}
                    </div>
                    ${!isUnknown ? `<div class="face-confidence">دڵنیایی | Confidence: ${face.confidence}</div>` : ''}
                </div>
            `;
        });
        
        resultsDiv.innerHTML = html;
    } else {
        resultsDiv.innerHTML = '<div class="alert alert-warning">⚠️ هیچ دەموچاوێک نەدۆزرایەوە | No faces detected</div>';
    }
}

// Update statistics
function updateStats(stats) {
    if (stats.unique_people !== undefined) {
        document.getElementById('uniquePeople').textContent = stats.unique_people;
    }
    if (stats.total_faces !== undefined) {
        document.getElementById('totalFaces').textContent = stats.total_faces;
    }
    if (stats.database_size !== undefined) {
        const sizeKB = (stats.database_size / 1024).toFixed(2);
        document.getElementById('dbSize').textContent = sizeKB;
    }
}

// Show result message
function showResult(elementId, type, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="alert alert-${type} fade-in">${message}</div>`;
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopWebcam();
});

# 🎯 Face Recognition System - سیستەمی ناسینەوەی دەموچاو

A powerful and modern face recognition system built with FastAPI, OpenCV, and face_recognition library. This application supports real-time face recognition from webcam, uploaded images, and can work with surveillance cameras.

سیستەمێکی بەهێز و مۆدێرن بۆ ناسینەوەی دەموچاو کە بە FastAPI، OpenCV و کتێبخانەی face_recognition دروستکراوە. ئەم بەرنامەیە پشتگیری دەکات لە ناسینەوەی ڕاستەوخۆی دەموچاو لە وێبکام، وێنەی بارکراو، و دەتوانێت لەگەڵ کامێرای چاودێریدا کار بکات.

## ✨ Features / تایبەتمەندییەکان

### 🚀 Core Features

- ✅ **Real-time Webcam Recognition** - ناسینەوەی ڕاستەوخۆ لە وێبکام
- ✅ **Image Upload Recognition** - ناسینەوە لە وێنەی بارکراو
- ✅ **Face Training System** - سیستەمی فێربوونی دەموچاو
- ✅ **Multiple Face Detection** - ناسینەوەی فرە دەموچاو لە یەک کاتدا
- ✅ **Confidence Score** - ڕێژەی دڵنیایی بۆ هەر ناسینەوەیەک
- ✅ **Face Database Management** - بەڕێوەبردنی داتابەیسی دەموچاوەکان
- ✅ **Beautiful Modern UI** - ڕووکاری جوان و مۆدێرن
- ✅ **RTL Support** - پشتگیری زمانی کوردی (ڕاست بۆ چەپ)
- ✅ **Responsive Design** - دیزاینی گونجاو لەگەڵ هەموو ئامێرەکان

### 🎨 UI Features

- Modern gradient design with Bootstrap 5
- Real-time visual feedback
- Toast notifications
- Loading indicators
- Animated results display
- Kurdish and English language support

## 📋 Requirements / پێداویستییەکان

### System Requirements

- Python 3.8 or higher
- Webcam (for real-time recognition)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Python Packages

All required packages are listed in `requirements.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
opencv-python==4.8.1.78
face-recognition==1.3.0
dlib==19.24.2
numpy==1.24.3
Pillow==10.1.0
aiofiles==23.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
websockets==12.0
```

## 🛠️ Installation / دامەزراندن

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installing `dlib` and `face_recognition` may take some time and require build tools:

- **Windows:** Install Visual Studio Build Tools
- **macOS:** Install Xcode Command Line Tools: `xcode-select --install`
- **Linux:** Install cmake and build essentials:
  ```bash
  sudo apt-get update
  sudo apt-get install build-essential cmake
  ```

### Step 4: Run the Application

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at: **http://localhost:8000**

## 📖 Usage Guide / ڕێنمایی بەکارهێنان

### 1️⃣ Adding Faces (Training) - زیادکردنی دەموچاو

1. Navigate to the **"زیادکردنی دەموچاوی نوێ"** section (left panel)
2. Enter the person's name in Kurdish or English
3. Click **"وێنە هەڵبژێرە"** to select an image
4. Click **"زیادکردن و فێربوون"** to upload and train

**Tips:**
- Use clear, front-facing photos
- Ensure good lighting
- One face per image
- Multiple images of the same person improve accuracy

### 2️⃣ Real-time Webcam Recognition - ناسینەوە لە وێبکام

1. Go to the **"ناسینەوە لە وێبکام"** section (middle panel)
2. Click **"دەستپێکردن"** to start the webcam
3. Allow browser access to your webcam
4. The system will automatically detect and recognize faces
5. Click **"ڕاگرتن"** to stop

**Features:**
- Real-time face detection with bounding boxes
- Shows name and confidence percentage
- Green boxes for recognized faces
- Red boxes for unknown faces
- Updates every 500ms

### 3️⃣ Image Recognition - ناسینەوە لە وێنە

1. Go to the **"ناسینەوە لە وێنە"** section (right panel)
2. Click **"وێنە هەڵبژێرە بۆ ناسینەوە"** to select an image
3. Click **"ناسینەوە"** to process
4. View the results with annotated faces

**Features:**
- Detects multiple faces in one image
- Shows processed image with labels
- Displays confidence scores
- Works with photos containing multiple people

### 4️⃣ Managing Known Faces - بەڕێوەبردنی دەموچاوەکان

- View list of all trained faces in the left panel
- Each face shows count of trained images
- Click trash icon to delete a face from database
- Total count displayed in navigation bar

## 🏗️ Project Structure

```
face-recognition-system/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── app.js             # Frontend JavaScript
├── uploads/                    # Temporary upload folder
├── known_faces/               # Stored face images
├── data/                      # Application data
└── face_encodings.pkl         # Serialized face encodings
```

## 🔧 Configuration

### Changing Recognition Sensitivity

In `app.py`, adjust the `tolerance` parameter (default: 0.6):

```python
matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
```

- **Lower value (0.4-0.5):** More strict, fewer false positives
- **Higher value (0.7-0.8):** More lenient, more matches

### Changing Webcam Processing Speed

In `static/js/app.js`, modify the interval (default: 500ms):

```javascript
webcamInterval = setInterval(() => {
    // ... processing code
}, 500); // Change this value (milliseconds)
```

### Changing Server Port

In `app.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

## 🌐 API Endpoints

### Upload Face
```
POST /api/upload
Parameters: name (string), file (image)
Response: success, message, total_faces
```

### Recognize Face
```
POST /api/recognize
Parameters: file (image)
Response: success, faces_detected, results, image
```

### Get Known Faces
```
GET /api/faces
Response: success, total_faces, unique_people, faces
```

### Delete Face
```
DELETE /api/faces/{name}
Response: success, message, total_faces
```

### WebSocket Webcam
```
WebSocket: /ws/webcam
Send: base64 encoded image
Receive: JSON with detected faces
```

## 🐛 Troubleshooting / چارەسەرکردنی کێشەکان

### Issue: Cannot install dlib
**Solution:**
- Install CMake: `pip install cmake`
- Install Visual Studio Build Tools (Windows)
- Use pre-built wheels: `pip install dlib-binary`

### Issue: Webcam not working
**Solution:**
- Allow browser camera permissions
- Check if another application is using the camera
- Use HTTPS for webcam access (HTTP works on localhost)

### Issue: Face not recognized
**Solution:**
- Add more training images of the person
- Ensure good lighting in both training and recognition
- Adjust tolerance value in configuration
- Use clear, front-facing photos

### Issue: Slow performance
**Solution:**
- Reduce webcam resolution
- Increase processing interval
- Use smaller images for training
- Run on machine with better CPU/GPU

## 🔒 Security Notes

- This is a demonstration application
- Do not expose to public internet without authentication
- Implement proper user authentication for production use
- Secure your face database
- Follow data privacy regulations (GDPR, etc.)

## 📝 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

## 🎓 How It Works / چۆن کار دەکات

### Face Recognition Technology

This system uses the `face_recognition` library which implements:

1. **Face Detection:** Locates faces in images using HOG (Histogram of Oriented Gradients)
2. **Face Encoding:** Converts each face into a 128-dimensional vector
3. **Face Comparison:** Compares vectors using Euclidean distance
4. **Recognition:** Matches unknown faces against known encodings

### Workflow

```
1. Upload & Training:
   Image → Face Detection → Face Encoding → Save to Database

2. Recognition:
   Input → Face Detection → Face Encoding → Compare with Database → Result

3. Real-time Webcam:
   Video Frame → Face Detection → Face Encoding → Compare → Draw Results → Repeat
```

## 🚀 Future Enhancements

Potential features for future development:

- [ ] User authentication system
- [ ] PostgreSQL database support
- [ ] IP camera (RTSP) streaming
- [ ] Face attendance system
- [ ] Export recognition logs
- [ ] Multi-language support
- [ ] Mobile app
- [ ] API key authentication
- [ ] Docker deployment
- [ ] Cloud storage integration

---

**Made with ❤️ for Face Recognition**

**دروستکراوە بە ❤️ بۆ ناسینەوەی دەموچاو**

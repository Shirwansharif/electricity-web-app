# Face Recognition System | سیستەمی ناسینەوەی دەموچاو

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)

**Professional Face Recognition System with Web & Desktop Interfaces**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Kurdish Documentation](#-kurdish-documentation)

</div>

---

## 🌟 Features

### Core Capabilities
- ✅ **Multi-Face Recognition**: Detect and recognize multiple faces in images
- ✅ **Real-time Webcam Recognition**: Live recognition via WebSocket connection
- ✅ **Image Upload Recognition**: Process uploaded images (JPG, PNG, etc.)
- ✅ **Face Database Management**: Add, view, and delete people from database
- ✅ **High Accuracy**: Uses `face_recognition` library (built on dlib)
- ✅ **Bilingual Interface**: Kurdish (RTL) and English support

### Technical Features
- 🎯 **Modular Architecture**: Shared core engine for web and desktop apps
- 🚀 **FastAPI Backend**: High-performance async Python web framework
- 💾 **Persistent Storage**: Face encodings stored in pickle database
- 🎨 **Modern UI**: Bootstrap 5 with custom gradient design
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🔒 **Local Processing**: All face recognition happens locally (no cloud)

---

## 📁 Project Structure

```
face-recognition-system/
├── web-app/                    # Web application
│   ├── app.py                 # FastAPI backend
│   ├── templates/             # HTML templates
│   │   └── index.html        # Main interface
│   └── static/                # Static assets
│       ├── css/
│       │   └── style.css     # Custom styles
│       └── js/
│           └── app.js        # Client-side JavaScript
│
├── shared/                     # Shared modules
│   └── face_engine.py         # Core face recognition engine
│
├── data/                       # Data storage
│   ├── faces/                 # Face encodings database
│   │   └── faces_db.pkl      # Pickle database file
│   └── uploads/               # Uploaded images
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (for real-time recognition)
- Windows, Linux, or macOS

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
```

### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Installing `dlib` can be challenging on Windows. If you encounter errors:

**Option 1: Pre-built wheel (Windows)**
```bash
# For Python 3.8
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp38-cp38-win_amd64.whl

# For Python 3.10
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp310-cp310-win_amd64.whl
```

**Option 2: Build from source (requires CMake)**
```bash
pip install cmake
pip install dlib
```

---

## 💻 Usage

### Web Application

1. **Start the web server:**

```bash
cd web-app
python app.py
```

2. **Open your browser:**

Navigate to: `http://localhost:8000`

3. **Using the interface:**

   - **Add Person**: Upload a clear photo with one face and enter the person's name
   - **Webcam Recognition**: Click "Start" to enable real-time recognition
   - **Image Recognition**: Upload an image to recognize faces in it
   - **Manage People**: View and delete people from the database

### Desktop Application (Coming Soon)

```bash
cd desktop-app
python desktop_app.py
```

---

## 🔌 API Documentation

### Endpoints

#### `GET /`
Main web interface

#### `POST /api/add-person`
Add a new person to the database

**Form Data:**
- `name` (string): Person's name
- `file` (file): Image file containing the person's face

**Response:**
```json
{
  "success": true,
  "message": "Ahmed added successfully",
  "stats": {
    "total_faces": 5,
    "unique_people": 3,
    "database_size": 2048
  }
}
```

#### `POST /api/recognize`
Recognize faces in an uploaded image

**Form Data:**
- `file` (file): Image file to analyze

**Response:**
```json
{
  "success": true,
  "faces": [
    {
      "name": "Ahmed",
      "confidence": "95.23%",
      "location": {"top": 100, "right": 200, "bottom": 300, "left": 50}
    }
  ],
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "message": "Found 1 face(s)"
}
```

#### `GET /api/people`
Get list of all people in database

**Response:**
```json
{
  "success": true,
  "people": ["Ahmed", "Sara", "Omar"],
  "count": 3
}
```

#### `DELETE /api/person/{name}`
Delete a person from database

**Response:**
```json
{
  "success": true,
  "message": "Ahmed deleted",
  "stats": {
    "total_faces": 4,
    "unique_people": 2,
    "database_size": 1536
  }
}
```

#### `GET /api/stats`
Get database statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_faces": 5,
    "unique_people": 3,
    "database_size": 2048
  }
}
```

#### `WebSocket /ws/webcam`
Real-time webcam recognition

**Send:**
```json
{
  "type": "frame",
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

**Receive:**
```json
{
  "type": "results",
  "faces": [
    {
      "name": "Ahmed",
      "confidence": "95.23%",
      "location": {"top": 100, "right": 200, "bottom": 300, "left": 50}
    }
  ]
}
```

---

## 🎨 Customization

### Adjusting Recognition Tolerance

Edit `shared/face_engine.py`:

```python
# Lower tolerance = more strict (less false positives)
# Higher tolerance = more lenient (more false positives)
def recognize_faces(self, image: np.ndarray, tolerance: float = 0.6):
    # Default is 0.6, try values between 0.4 and 0.7
```

### Changing UI Colors

Edit `web-app/static/css/style.css`:

```css
/* Main gradient background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Change to your preferred colors */
body {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'face_recognition'"
**Solution:** Install dependencies: `pip install face-recognition`

### Issue: "dlib installation fails"
**Solution:** Use pre-built wheel (see Installation Step 3)

### Issue: "No webcam found"
**Solution:** 
- Check if webcam is connected and working
- Grant browser permission to access webcam
- Try a different browser

### Issue: "Template rendering error"
**Solution:** This has been fixed in the latest version. Make sure you're using the updated `web-app/app.py` with explicit template parameter names.

### Issue: "Face not recognized even though added"
**Solution:**
- Use clear, well-lit photos
- Ensure face is front-facing
- Try adjusting the tolerance parameter
- Add multiple photos of the same person

---

## 📚 Technical Details

### Face Recognition Process

1. **Face Detection**: Uses HOG (Histogram of Oriented Gradients) or CNN to detect faces
2. **Face Encoding**: Generates 128-dimensional face embedding using deep learning
3. **Face Comparison**: Compares encodings using Euclidean distance
4. **Recognition**: Matches against database with configurable tolerance

### Performance

- **Face Detection**: ~100-200ms per image (depending on size)
- **Face Encoding**: ~50-100ms per face
- **Face Recognition**: ~10-20ms per comparison
- **Webcam**: ~1 FPS (configurable)

### Database Format

Face encodings are stored in `data/faces/faces_db.pkl`:

```python
{
    "Person Name": {
        "encodings": [numpy.ndarray, ...],
        "metadata": {
            "date_added": "2024-08-19",
            "notes": "Optional info"
        }
    }
}
```

---

## 🔐 Security & Privacy

- ✅ **Local Processing**: All face recognition happens on your machine
- ✅ **No Cloud Upload**: Images are never sent to external servers
- ✅ **Local Storage**: Database stored locally in pickle format
- ⚠️ **Note**: This is a demo application without authentication. For production use, add user authentication and access control.

---

## 🛠️ Development

### Running in Development Mode

```bash
cd web-app
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Adding New Features

1. **Backend**: Edit `web-app/app.py` to add new API endpoints
2. **Core Logic**: Edit `shared/face_engine.py` to modify face recognition
3. **Frontend**: Edit `web-app/templates/index.html` and `web-app/static/js/app.js`
4. **Styling**: Edit `web-app/static/css/style.css`

---

## 📝 Kurdish Documentation

<div dir="rtl">

# سیستەمی ناسینەوەی دەموچاو

## تایبەتمەندییەکان

- ✅ **ناسینەوەی چەند دەموچاوێک**: دەتوانێت چەندین دەموچاو لە یەک وێنەدا بناسێتەوە
- ✅ **ناسینەوە لە ڕاستەوخۆ**: ناسینەوەی ڕاستەوخۆ لە ڕێگەی وێبکامەوە
- ✅ **ناسینەوە لە وێنە**: چاودێری وێنە بارکراوەکان بکە
- ✅ **بەڕێوەبردنی بنکەدراوە**: کەسایەتی زیادبکە، ببینە، و بسڕەوە
- ✅ **وردبینی بەرز**: بەکارهێنانی کتێبخانەی `face_recognition`
- ✅ **ڕووکاری دووزمانە**: پشتگیری کوردی و ئینگلیزی

## چۆنیەتی بەکارهێنان

### 1. دامەزراندنی پێداویستییەکان

```bash
pip install -r requirements.txt
```

### 2. کارپێکردنی بەرنامە

```bash
cd web-app
python app.py
```

### 3. کردنەوەی وێبگەڕ

`http://localhost:8000` بکەرەوە

### 4. زیادکردنی کەسایەتی

1. وێنەیەک هەڵبژێرە کە تەنها یەک دەموچاوی تێدابێت
2. ناوی کەسەکە بنووسە
3. دوگمەی "زیادکردن" کلیک بکە

### 5. ناسینەوە

**لە وێبکامەوە:**
- دوگمەی "دەستپێکردن" کلیک بکە
- ڕێگە بە وێبگەڕ بدە بۆ بەکارهێنانی وێبکام
- سیستەم بە خۆکاری دەموچاوەکان دەناسێتەوە

**لە وێنەوە:**
- وێنەیەک هەڵبژێرە
- دوگمەی "ناسینەوە" کلیک بکە
- ئەنجامەکان دەبینیت

## چارەسەری کێشەکان

### کێشە: هیچ دەموچاوێک نەدۆزرایەوە
**چارەسەر:**
- وێنەیەکی ڕوون بەکاربهێنە
- دڵنیابە کە دەموچاوەکە ڕووەو کامێرایە
- ڕووناکی باش بەکاربهێنە

### کێشە: دەموچاو نەناسرایەوە
**چارەسەر:**
- چەند وێنەی جیاواز لە هەمان کەس زیادبکە
- وێنەی باشترە بەکاربهێنە
- دڵنیابە کە وێنەکان هاوشێوەن (هاوچەشن، هاوڕەنگ، هتد)

## پشتگیری

بۆ هەر پرسیار یان کێشەیەک، Issue بکەرەوە لە GitHub.

</div>

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [dlib](http://dlib.net/) by Davis King
- [FastAPI](https://fastapi.tiangolo.com/) by Sebastián Ramírez
- [OpenCV](https://opencv.org/) community

---

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for the Kurdish community**

ئەم پرۆژەیە بۆ کۆمەڵگەی کوردی دروستکراوە

</div>

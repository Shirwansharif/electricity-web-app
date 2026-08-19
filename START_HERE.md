# 🚀 Quick Start Guide | ڕێنمایی خێرا

<div dir="rtl">

## بۆ بەکارهێنەرانی کوردی

### پێشمەرجەکان
- Python 3.8 یان زیاتر
- وێبکام (بۆ ناسینەوەی ڕاستەوخۆ)

### هەنگاوەکان

#### 1️⃣ داگرتنی پرۆژە
```bash
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
```

#### 2️⃣ دروستکردنی ژینگەی تایبەت
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

#### 3️⃣ دامەزراندنی کتێبخانەکان
```bash
pip install -r requirements.txt
```

**تێبینی بۆ Windows:** ئەگەر کێشەت هەبوو لە دامەزراندنی `dlib`:
```bash
pip install cmake
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp38-cp38-win_amd64.whl
```

#### 4️⃣ کارپێکردنی بەرنامە
```bash
cd web-app
python app.py
```

#### 5️⃣ کردنەوەی وێبگەڕ
بڕۆ بۆ: `http://localhost:8000`

### چۆنیەتی بەکارهێنان

1. **زیادکردنی کەسایەتی**
   - وێنەیەکی ڕوون هەڵبژێرە (تەنها یەک دەموچاو)
   - ناوی کەسەکە بنووسە
   - دوگمەی "زیادکردن" کلیک بکە

2. **ناسینەوە لە وێبکام**
   - دوگمەی "دەستپێکردن" کلیک بکە
   - ڕێگە بدە بە وێبگەڕ بۆ بەکارهێنانی وێبکام
   - سیستەم خۆکار دەموچاوەکان دەناسێتەوە

3. **ناسینەوە لە وێنە**
   - وێنەیەک هەڵبژێرە
   - دوگمەی "ناسینەوە" کلیک بکە

---

</div>

## For English Users

### Prerequisites
- Python 3.8 or higher
- Webcam (for real-time recognition)
- Git

### Steps

#### 1️⃣ Clone the Project
```bash
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
```

#### 2️⃣ Create Virtual Environment
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

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

**Note for Windows:** If you have issues installing `dlib`:
```bash
pip install cmake
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp38-cp38-win_amd64.whl
```

Replace `cp38` with your Python version:
- Python 3.8: `cp38`
- Python 3.10: `cp310`
- Python 3.11: `cp311`

#### 4️⃣ Start the Application
```bash
cd web-app
python app.py
```

#### 5️⃣ Open Browser
Navigate to: `http://localhost:8000`

### How to Use

1. **Add a Person**
   - Select a clear image (with only one face)
   - Enter the person's name
   - Click "Add" button

2. **Webcam Recognition**
   - Click "Start" button
   - Allow browser to access webcam
   - System will recognize faces automatically

3. **Image Recognition**
   - Select an image file
   - Click "Recognize" button
   - View results with face boxes and names

---

## 🐛 Common Issues

### Issue: ModuleNotFoundError: No module named 'jinja2'
**Solution:**
```bash
pip install jinja2
```

### Issue: dlib installation fails
**Solution (Windows):**
```bash
pip install cmake
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp38-cp38-win_amd64.whl
```

### Issue: "No webcam found"
**Solution:**
- Check if webcam is connected
- Grant browser permission to access webcam
- Try a different browser (Chrome recommended)

### Issue: "Internal Server Error"
**Solution:**
- Make sure you're in the `web-app` directory
- Check that all files are present: `app.py`, `templates/index.html`, `static/css/style.css`, `static/js/app.js`
- Verify the `shared/face_engine.py` file exists

---

## 📁 Project Structure

```
face-recognition-system/
├── web-app/                    ← Web application
│   ├── app.py                 ← Start this file
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── shared/
│   └── face_engine.py         ← Core logic
├── data/
│   ├── faces/                 ← Face database
│   └── uploads/               ← Uploaded images
└── requirements.txt           ← Dependencies
```

---

## 🎯 What This System Can Do

✅ **Detect Faces** - Find faces in images and video  
✅ **Recognize People** - Identify known people by their face  
✅ **Real-time Recognition** - Live recognition via webcam  
✅ **Manage Database** - Add, view, delete people  
✅ **High Accuracy** - Uses state-of-the-art face recognition  
✅ **Local Processing** - Everything runs on your computer (no cloud)  

---

## 🔒 Privacy & Security

- ✅ All processing happens locally on your machine
- ✅ No images are sent to the internet
- ✅ Face data is stored only on your computer
- ✅ You have full control over your data

---

## 📚 More Documentation

- **Full Documentation**: See `README_PROFESSIONAL.md`
- **API Documentation**: See API section in README_PROFESSIONAL.md
- **Troubleshooting**: See README_PROFESSIONAL.md

---

## 💡 Tips for Best Results

1. **Use Clear Photos**
   - Good lighting
   - Face looking at camera
   - High resolution

2. **Add Multiple Photos**
   - Add 2-3 photos per person
   - Different angles
   - Different expressions

3. **Avoid Common Mistakes**
   - Don't use group photos (only 1 face per image)
   - Don't use very old photos (if person's appearance changed)
   - Don't use blurry or dark photos

---

<div align="center">

**Ready to start? Just run:**

```bash
cd web-app
python app.py
```

Then open: **http://localhost:8000**

</div>

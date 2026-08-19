# 🚀 Quick Start Guide - ڕێنمایی خێرا

## بۆ کەسانێک کە Python-یان نییە

---

## ڕێگە 1: دامەزراندنی Python (پێشنیارکراو) ⭐

### Windows:
1. **دابگرە Python:**
   - بڕۆ: https://www.python.org/downloads/
   - کلیک لە "Download Python 3.12"
   
2. **دامەزرێنە:**
   - Run بکە .exe فایلەکە
   - ✅ **گرنگ:** تیک بکە لەسەر "Add Python to PATH"
   - کلیک لە "Install Now"
   - چاوەڕوان بە 2-3 خولەک

3. **پشتڕاست بکەرەوە:**
   ```cmd
   python --version
   ```

4. **پرۆژەکە بکەوە:**
   ```cmd
   cd path\to\project
   git checkout cursor/face-recognition-system-2d57
   pip install fastapi uvicorn python-multipart aiofiles websockets
   python app_simple.py
   ```

5. **بزوێنەر بکەوە:**
   ```
   http://localhost:8000
   ```

### Mac:
```bash
# دامەزراندنی Python
brew install python3

# یان لە python.org دایبگرە

# پرۆژەکە بکەوە
cd /path/to/project
git checkout cursor/face-recognition-system-2d57
pip3 install fastapi uvicorn python-multipart aiofiles websockets
python3 app_simple.py
```

---

## ڕێگە 2: GitHub Codespaces (ئۆنلاین، بێ دامەزراندن) 🌐

**هیچ شتێک نادەزرێنیت لەسەر کۆمپیوتەرەکەت!**

1. بڕۆ بۆ: https://github.com/Shirwansharif/electricity-web-app
2. کلیک لە دوگمەی سەوز **"< > Code"**
3. هەڵبژێرە تابی **"Codespaces"**
4. کلیک لە **"Create codespace on cursor/face-recognition-system-2d57"**
5. چاوەڕوان بە بۆ بار بوونی ژینگەکە (1-2 خولەک)

لە تێرمیناڵی Codespace:
```bash
pip install fastapi uvicorn python-multipart aiofiles websockets
python3 app_simple.py
```

کاتێک دەست پێدەکات، پۆرت 8000 خودکار دەکرێتەوە!

---

## ڕێگە 3: بینینی کۆد و UI لە GitHub 👀

**بینین تەنها، بێ کارپێکردن**

### بینینی HTML/CSS/JavaScript:
- HTML: https://github.com/Shirwansharif/electricity-web-app/blob/cursor/face-recognition-system-2d57/templates/index.html
- CSS: https://github.com/Shirwansharif/electricity-web-app/blob/cursor/face-recognition-system-2d57/static/css/style.css
- JS: https://github.com/Shirwansharif/electricity-web-app/blob/cursor/face-recognition-system-2d57/static/js/app.js

### بینینی Pull Request:
https://github.com/Shirwansharif/electricity-web-app/pull/1

---

## ڕێگە 4: Docker (ئەگەر Docker هەتە) 🐋

```bash
# Clone بکە
git clone https://github.com/Shirwansharif/electricity-web-app.git
cd electricity-web-app
git checkout cursor/face-recognition-system-2d57

# Build و Run
docker-compose up --build
```

بزوێنەر بکەوە: http://localhost:8000

---

## ڕێگە 5: Portable Python (بێ Install)

**Windows تەنها:**

1. دابگرە WinPython: https://winpython.github.io/
2. Extract بکە
3. Run بکە "WinPython Command Prompt.exe"
4. پرۆژەکە بکەوە وەک بەرتەسک

---

## چارەسەرکردنی کێشە 🔧

### کێشە: "python is not recognized"
**چارەسەر:**
- Python زیادبکە بۆ PATH
- یان بەکاربهێنە: `py` لە جێی `python`

### کێشە: "pip is not recognized"
**چارەسەر:**
```bash
python -m pip install ...
```

### کێشە: "Port 8000 already in use"
**چارەسەر:**
```bash
# گۆڕینی پۆرت
python app_simple.py --port 8001
```

یان لە `app_simple.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # گۆڕی بۆ 8001
```

---

## یارمەتی زیاتر 💬

ئەگەر کێشەت هەبوو:
1. ببینە README.md
2. کێشەکە بنووسە لە GitHub Issues
3. لینکی Pull Request: https://github.com/Shirwansharif/electricity-web-app/pull/1

---

## تێبینی گرنگ ⚠️

**وەشانی ئێستا:**
- ✅ UI تەواوە و کار دەکات
- ✅ Backend API ئامادەیە
- ⏳ Face recognition بە dlib پێویستی بە setup-ی زیاتر هەیە
- ✅ Demo mode بەردەستە (دۆزینەوەی دەموچاو)

**بۆ ناسینەوەی تەواو:**
```bash
pip install cmake dlib face-recognition
# ئینجا app.py-ی سەرەکی بەکاربهێنە
python app.py
```

---

**خۆشحاڵیت دەکەم! 🎉**

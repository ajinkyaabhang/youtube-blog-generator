# 📺 YouTube Blog Generator

## 🚀 Project Description
The **YouTube Blog Generator** is a Streamlit-powered application that automatically converts YouTube video transcripts into well-structured blog posts. It uses **LangChain**, **Groq AI**, and **YouTube Transcript API** to fetch video transcripts, generate engaging blog posts, analyze their quality, and improve them if necessary.

## 🛠️ Features
- 🎥 Fetches transcripts from YouTube videos.
- 📝 Converts transcripts into well-structured blog posts.
- 🤖 Uses AI to analyze blog quality (Pass/Fail criteria).
- 🔄 Improves blog quality if needed.
- 🌐 Streamlit-based UI for easy interaction.

## 📦 Tech Stack
- **Python** 🐍
- **Streamlit** 🎨
- **LangChain** 🔗
- **Groq AI** 🤖
- **YouTube Transcript API** 🎥

---

## 📌 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUTUBE-BLOG-GENERATOR.git
cd youtube-blog-generator
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a **.env** file and add your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key
```

### 5️⃣ Run the Application
```bash
streamlit run app.py
```

---

## 📜 Usage Guide
1. **Enter a YouTube Video URL** in the input field.
2. Click **"Generate Blog"** to start processing.
3. The app fetches the transcript, generates a blog, and evaluates its quality.
4. If needed, AI improves the blog before displaying it.
5. Copy or download the final blog post.

---

## 🤝 Contributing
Feel free to fork this repository, submit issues, or contribute via pull requests.

### Steps to Contribute:
1. Fork the repository 🍴
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch`
5. Open a Pull Request ✅

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 📬 Contact
- **GitHub:** https://github.com/ajinkyaabhang
- **Email:** ajinkyaabhang@gmail.com


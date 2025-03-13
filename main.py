
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Analyzer</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        :root {
            --primary: #0c8346;
            --secondary: #7fcc8c;
            --accent: #ffbd59;
            --dark: #1e3a2b;
            --light: #f5fff7;
        }
        
        html {
            height: 100%;
            scroll-behavior: smooth;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background-image: url('https://images.unsplash.com/photo-1587502537745-84b86da1204f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            margin: 0;
            padding: 0;
            color: var(--dark);
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(12, 131, 70, 0.4) 0%, rgba(0, 0, 0, 0.4) 100%);
            z-index: -1;
        }
        
        .container {
            width: 90%;
            max-width: 800px;
            background: rgba(255, 255, 255, 0.85);
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), 
                        0 0 20px rgba(12, 131, 70, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateY(0);
            animation: float 6s ease-in-out infinite;
            position: relative;
            z-index: 1;
            transition: animation 0.3s;
        }
        
        .container.typing {
            animation: none;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            color: var(--primary);
            text-align: center;
            margin-bottom: 30px;
            font-weight: 700;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            display: inline-block;
            width: 100%;
        }
        
        h1::after {
            content: "";
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 2px;
        }
        
        textarea {
            width: 100%;
            padding: 18px;
            border: 2px solid var(--secondary);
            border-radius: 15px;
            font-size: 16px;
            background-color: rgba(255, 255, 255, 0.9);
            resize: vertical;
            transition: all 0.4s ease;
            box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.05);
            color: var(--dark);
            font-family: 'Poppins', sans-serif;
        }
        
        textarea:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 4px rgba(12, 131, 70, 0.2), 
                        inset 0 2px 6px rgba(0, 0, 0, 0.05);
            transform: scale(1.005);
        }
        
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 25px;
            position: relative;
        }
        
        input[type="submit"] {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 14px 40px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.4s;
            box-shadow: 0 10px 20px rgba(12, 131, 70, 0.3);
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        input[type="submit"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 0%;
            height: 100%;
            background: linear-gradient(45deg, var(--secondary), var(--primary));
            transition: all 0.4s;
            z-index: -1;
            border-radius: 50px;
        }
        
        input[type="submit"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(12, 131, 70, 0.4);
        }
        
        input[type="submit"]:hover::before {
            width: 100%;
        }
        
        .results {
            margin-top: 35px;
            padding: 25px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 255, 240, 0.9) 100%);
            border-radius: 18px;
            border-left: 6px solid var(--primary);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            transform: translateY(0);
            transition: all 0.4s;
            position: relative;
            overflow: hidden;
        }
        
        .results::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 65%);
            opacity: 0;
            transition: opacity 1.5s;
            transform: rotate(30deg);
            pointer-events: none;
        }
        
        .results:hover::before {
            opacity: 1;
        }
        
        .results:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }
        
        .results h2 {
            color: var(--primary);
            margin-top: 0;
            font-weight: 600;
            position: relative;
            display: inline-block;
        }
        
        .results h2::after {
            content: "";
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 40px;
            height: 3px;
            background: var(--accent);
            border-radius: 2px;
        }
        
        .results p {
            font-size: 18px;
            margin: 15px 0;
            padding: 10px 15px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.6);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            border-left: 3px solid var(--secondary);
            transition: all 0.3s;
        }
        
        .results p:hover {
            transform: translateX(5px);
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        
        .nature-decoration {
            text-align: center;
            margin: 20px 0;
            font-size: 28px;
            line-height: 1.5;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            animation: breathe 4s ease-in-out infinite;
        }
        
        @keyframes breathe {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.9; }
        }
        
        .leaf {
            display: inline-block;
            transform-origin: center;
            animation: sway 3s ease-in-out infinite;
        }
        
        @keyframes sway {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(5deg); }
        }
        
        .leaf:nth-child(odd) {
            animation-duration: 3.5s;
            animation-direction: alternate;
        }
        
        .leaf:nth-child(3n) {
            animation-duration: 4s;
        }
        
        .firefly {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 100, 0.8);
            border-radius: 50%;
            box-shadow: 0 0 10px 2px rgba(255, 255, 100, 0.5);
            animation: fly 20s linear infinite, blink 2s ease-in-out infinite alternate;
            pointer-events: none;
        }
        
        @keyframes fly {
            0% { transform: translate(0, 0); }
            25% { transform: translate(100px, -50px); }
            50% { transform: translate(200px, 100px); }
            75% { transform: translate(100px, 200px); }
            100% { transform: translate(0, 0); }
        }
        
        @keyframes blink {
            0%, 100% { opacity: 0.1; }
            50% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 Text Analyzer 🌿</h1>
        
        <div class="nature-decoration">
            <span class="leaf">🌳</span> 
            <span class="leaf">🌻</span> 
            <span class="leaf">🍃</span> 
            <span class="leaf">🌷</span> 
            <span class="leaf">🌿</span>
        </div>
        
        <form method="post">
            <textarea name="text" rows="10" cols="30" placeholder="Type or paste your text here...">{{ text }}</textarea>
            <div class="button-container">
                <input type="submit" value="Analyze Text">
            </div>
        </form>
        
        {% if result %}
        <div class="results">
            <h2>✨ Analysis Results</h2>
            <p>📝 Total Characters: {{ result['total_characters'] }}</p>
            <p>🔤 Total Letters: {{ result['total_letters'] }}</p>
            <p>📚 Total Words: {{ result['total_words'] }}</p>
        </div>
        {% endif %}
        
        <div class="nature-decoration">
            <span class="leaf">🌿</span> 
            <span class="leaf">🌼</span> 
            <span class="leaf">🍂</span> 
            <span class="leaf">🌱</span> 
            <span class="leaf">🌳</span>
        </div>
        
        <!-- Animated fireflies -->
        <div class="firefly" style="top: 10%; left: 10%;"></div>
        <div class="firefly" style="top: 20%; left: 80%;"></div>
        <div class="firefly" style="top: 50%; left: 15%;"></div>
        <div class="firefly" style="top: 70%; left: 85%;"></div>
        <div class="firefly" style="top: 85%; left: 40%;"></div>
    </div>

    <script>
        // Create additional random fireflies
        document.addEventListener('DOMContentLoaded', function() {
            const container = document.querySelector('body');
            for (let i = 0; i < 15; i++) {
                const firefly = document.createElement('div');
                firefly.className = 'firefly';
                firefly.style.top = Math.random() * 100 + '%';
                firefly.style.left = Math.random() * 100 + '%';
                
                // Randomize animation properties
                firefly.style.animationDuration = (15 + Math.random() * 15) + 's, ' + 
                                                (1 + Math.random() * 3) + 's';
                firefly.style.animationDelay = Math.random() * 5 + 's, ' + 
                                              Math.random() * 1 + 's';
                
                container.appendChild(firefly);
            }
            
            // Add subtle text effects and stop container animation when typing
            const textarea = document.querySelector('textarea');
            const containerElement = document.querySelector('.container');
            
            if (textarea) {
                textarea.addEventListener('focus', function() {
                    this.style.transform = 'scale(1.01)';
                    // Stop container animation when typing
                    containerElement.classList.add('typing');
                });
                
                textarea.addEventListener('blur', function() {
                    this.style.transform = 'scale(1)';
                    // Resume container animation when not typing
                    containerElement.classList.remove('typing');
                });
            }
            
            // Add results animation
            const results = document.querySelector('.results');
            if (results) {
                setTimeout(() => {
                    results.style.opacity = '0';
                    results.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        results.style.transition = 'all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)';
                        results.style.opacity = '1';
                        results.style.transform = 'translateY(0)';
                    }, 100);
                }, 100);
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_form():
    template = Template(html_template)
    return template.render(result=None, text="")

@app.post("/", response_class=HTMLResponse)
def analyze_text(text: str = Form(...)):
    total_characters = len(text)
    total_letters = sum(c.isalpha() for c in text)
    total_words = len(text.split()) if text.strip() else 0
    result = {
        "total_characters": total_characters, 
        "total_letters": total_letters,
        "total_words": total_words
    }
    template = Template(html_template)
    return template.render(result=result, text=text)

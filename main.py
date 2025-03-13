
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
        body {
            font-family: 'Arial', sans-serif;
            background-image: url('https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            margin: 0;
            padding: 0;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            width: 90%;
            max-width: 800px;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2e7d32;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #a5d6a7;
            border-radius: 10px;
            font-size: 16px;
            background-color: rgba(255, 255, 255, 0.8);
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            border-color: #4caf50;
            outline: none;
            box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        input[type="submit"] {
            background-color: #4caf50;
            color: white;
            border: none;
            padding: 12px 35px;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        input[type="submit"]:hover {
            background-color: #2e7d32;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: rgba(230, 255, 230, 0.7);
            border-radius: 10px;
            border-left: 5px solid #4caf50;
        }
        .results h2 {
            color: #2e7d32;
            margin-top: 0;
        }
        .results p {
            font-size: 18px;
            margin: 10px 0;
        }
        .nature-decoration {
            text-align: center;
            margin: 20px 0;
            font-size: 24px;
            color: #4caf50;
        }
        html {
            height: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 Text Analyzer 🌿</h1>
        
        <div class="nature-decoration">
            🌳 🌻 🍃 🌷 🌿
        </div>
        
        <form method="post">
            <textarea name="text" rows="10" cols="30">{{ text }}</textarea>
            <div class="button-container">
                <input type="submit" value="Analyze">
            </div>
        </form>
        
        {% if result %}
        <div class="results">
            <h2>✨ Analysis Results:</h2>
            <p>📝 Total Characters: {{ result['total_characters'] }}</p>
            <p>🔤 Total Letters: {{ result['total_letters'] }}</p>
        </div>
        {% endif %}
        
        <div class="nature-decoration">
            🌿 🌼 🍂 🌱 🌳
        </div>
    </div>
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
    result = {"total_characters": total_characters, "total_letters": total_letters}
    template = Template(html_template)
    return template.render(result=result, text=text)

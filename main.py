from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Analyzer</title>
</head>
<body>
    <h1>Text Analyzer</h1>
    <form method="post">
        <textarea name="text" rows="10" cols="30"></textarea><br>
        <input type="submit" value="Analyze">
    </form>
    {% if result %}
    <h2>Results:</h2>
    <p>Total Characters: {{ result['total_characters'] }}</p>
    <p>Total Letters: {{ result['total_letters'] }}</p>
    {% endif %}
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_form():
    template = Template(html_template)
    return template.render(result=None)

@app.post("/", response_class=HTMLResponse)
def analyze_text(text: str = Form(...)):
    total_characters = len(text)
    total_letters = sum(c.isalpha() for c in text)
    result = {"total_characters": total_characters, "total_letters": total_letters}
    template = Template(html_template)
    return template.render(result=result)

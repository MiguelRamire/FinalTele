from flask import Flask, render_template_string, request

app = Flask(__name__)

# Página HTML integrada en el archivo Python
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juego Clicker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        h1 {
            margin-top: 20px;
        }
        .score {
            font-size: 24px;
            margin: 20px 0;
        }
        button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Juego Clicker</h1>
    <div class="score">Puntuación: {{ score }}</div>
    <form method="POST">
        <button type="submit" name="action" value="click">¡Haz clic aquí!</button>
        <button type="submit" name="action" value="reset">Reiniciar</button>
    </form>
</body>
</html>
"""

# Variable global para almacenar la puntuación
score = 0

@app.route("/", methods=["GET", "POST"])
def game():
    global score
    if request.method == "POST":
        action = request.form.get("action")
        if action == "click":
            score += 1  # Incrementa la puntuación
        elif action == "reset":
            score = 0  # Reinicia la puntuación
    return render_template_string(html_template, score=score)

if __name__ == "__main__":
    app.run(debug=True)
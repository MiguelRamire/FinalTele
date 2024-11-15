from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flappy Bird</title>
        <style>
            body {
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            canvas {
                border: 2px solid black;
                background-color: white;
            }
        </style>
    </head>
    <body>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");

            const bird = { x: 50, y: canvas.height / 2, width: 30, height: 30, velocity: 0 };
            const gravity = 1;
            const jumpStrength = -10;

            const pipes = [];
            const pipeWidth = 60;
            const pipeGap = 150;
            let pipeFrequency = 90; // Frames entre tubos
            let frame = 0;
            let score = 0;

            function createPipe() {
                const pipeHeight = Math.random() * (canvas.height - pipeGap - 100) + 50;
                pipes.push({ x: canvas.width, topHeight: pipeHeight, bottomY: pipeHeight + pipeGap });
            }

            function drawBird() {
                ctx.fillStyle = "blue";
                ctx.fillRect(bird.x, bird.y, bird.width, bird.height);
            }

            function drawPipes() {
                ctx.fillStyle = "green";
                pipes.forEach(pipe => {
                    ctx.fillRect(pipe.x, 0, pipeWidth, pipe.topHeight);
                    ctx.fillRect(pipe.x, pipe.bottomY, pipeWidth, canvas.height - pipe.bottomY);
                });
            }

            function updatePipes() {
                pipes.forEach(pipe => pipe.x -= 4);
                pipes.filter(pipe => pipe.x + pipeWidth > 0);
                if (frame % pipeFrequency === 0) createPipe();
            }

            function drawScore() {
                ctx.fillStyle = "black";
                ctx.font = "20px Arial";
                ctx.fillText("Score: " + score, 10, 30);
            }

            function gameOver() {
                ctx.fillStyle = "black";
                ctx.font = "40px Arial";
                ctx.fillText("Game Over", canvas.width / 4, canvas.height / 2);
                cancelAnimationFrame(animationId);
            }

            let animationId;

            function gameLoop() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                bird.velocity += gravity;
                bird.y += bird.velocity;

                drawBird();
                updatePipes();
                drawPipes();
                drawScore();

                // Detectar colisiones
                if (bird.y < 0 || bird.y + bird.height > canvas.height) {
                    gameOver();
                    return;
                }
                pipes.forEach(pipe => {
                    if (
                        bird.x < pipe.x + pipeWidth &&
                        bird.x + bird.width > pipe.x &&
                        (bird.y < pipe.topHeight || bird.y + bird.height > pipe.bottomY)
                    ) {
                        gameOver();
                        return;
                    }
                });

                frame++;
                animationId = requestAnimationFrame(gameLoop);
            }

            // Control del pájaro
            document.addEventListener("keydown", event => {
                if (event.code === "Space") {
                    bird.velocity = jumpStrength;
                }
            });

            // Iniciar el juego
            gameLoop();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)

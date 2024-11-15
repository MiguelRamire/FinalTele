import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Configuración de la pantalla
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Variables del juego
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_width = 30
bird_height = 30
gravity = 1
bird_velocity = 0
jump_strength = -10

pipe_width = 60
pipe_gap = 150
pipe_velocity = 4
pipe_frequency = 1500  # Tiempo en milisegundos entre nuevos tubos

# Variables de puntuación
score = 0
high_score = 0

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Grupo de tubos
pipes = []
last_pipe = pygame.time.get_ticks() - pipe_frequency  # Tiempo del último tubo

# Función para dibujar al pájaro
def draw_bird(bird_y):
    pygame.draw.rect(screen, BLUE, [bird_x, bird_y, bird_width, bird_height])

# Función para crear tubos
def create_pipe():
    pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

# Función para mover y dibujar tubos
def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= pipe_velocity
    return [pipe for pipe in pipes if pipe.x + pipe_width > 0]  # Filtra tubos fuera de la pantalla

# Función para mostrar la puntuación
def show_score(score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, [10, 10])

# Función principal del juego
def game_loop():
    global bird_y, bird_velocity, score, pipes, last_pipe, high_score
    
    # Variables de inicio
    game_over = False
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipes = []
    
    while not game_over:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength  # Saltar con la barra espaciadora
        
        # Gravedad y movimiento del pájaro
        bird_velocity += gravity
        bird_y += bird_velocity
        
        # Generación de nuevos tubos
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now
        
        # Movimiento de tubos y detección de colisiones
        pipes = move_pipes(pipes)
        for pipe in pipes:
            if pipe.colliderect(pygame.Rect(bird_x, bird_y, bird_width, bird_height)):
                game_over = True
        
        # Comprobar si el pájaro toca el suelo o el techo
        if bird_y < 0 or bird_y > SCREEN_HEIGHT - bird_height:
            game_over = True
        
        # Comprobar si se pasa un tubo y actualizar puntuación
        for pipe in pipes:
            if pipe.x + pipe_width == bird_x:  # Al pasar el tubo, se suma un punto
                score += 1
                high_score = max(score, high_score)

        # Dibujar elementos del juego
        screen.fill(WHITE)
        draw_bird(bird_y)
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe)
        show_score(score)
        
        pygame.display.flip()
        clock.tick(60)  # Control de FPS

    # Mensaje de Game Over
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render("Game Over", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3])
    show_score(score)
    pygame.display.flip()
    
    pygame.time.delay(2000)  # Retraso de 2 segundos para reiniciar
    game_loop()  # Reiniciar el juego

# Ejecutar el juego
game_loop()
import pygame
import random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 43)
BLUE = (92, 225, 230)
PURPLE = (129, 0, 154)


GREEN = (0, 255, 0)
RED = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)


# Global variables for snake color and sound state
SNAKE_COLOR = WHITE
SOUND_ENABLED = True
CURRENT_COLOR_INDEX = 0
AVAILABLE_COLORS = [WHITE, GREEN, RED, ORANGE, PINK, BLACK] 


# Helper functions
def on_grid_random():
    x = random.randint(0, 23)
    y = random.randint(0, 22)  # Ajustando para eliminar o espaço extra no final da tela
    return (x * 25, y * 25)

def collision(c1, c2_list):
    for c2 in c2_list:
        if c1[0] == c2[0] and c1[1] == c2[1]:
            return True
    return False

# Macro definition for snake movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def draw_button(screen, color, x, y, width, height, text, text_color):
    rect = pygame.Rect(x, y, width, height)
    font = pygame.font.Font('freesansbold.ttf', 18)
    if rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, color,(x, y, width, height), border_radius=15)
    else:
        pygame.draw.rect(screen, BLUE, (x, y, width, height), border_radius=15)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)

def draw_hud(screen, score):
    font = pygame.font.Font('freesansbold.ttf', 24)
    
    # Draw score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
def generate_equation(screen):
    font = pygame.font.Font('freesansbold.ttf', 24)
    # Gera uma equação matemática com operações de soma e multiplicação
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    op1 = random.randint(0, 3)
    op2 = random.randint(0, 3)
    operations = ['+','-','+','-']
    equation = f"{a} {operations[op1]} {b} {operations[op2]} {c}" #{operations[op1]}{c}
    result = eval(equation)
    return equation, result

def generate_incorrect_results(correct_result, num_results):
    incorrect_results = []
    for _ in range(num_results):
        incorrect_result = correct_result
        while incorrect_result == correct_result or incorrect_result in incorrect_results:
            incorrect_result += random.choice([-1, 1])
        incorrect_results.append(incorrect_result)
    return incorrect_results

def main_menu(screen):
    click_sound = pygame.mixer.Sound('audios/click-sound.mp3')

    background_image = pygame.image.load('img/menu-background.png')  # Carregar imagem de fundo
    background_rect = background_image.get_rect()
    
    running = True
    while running:
        screen.blit(background_image, background_rect)  # Desenhar imagem de fundo
        
        # Desenhar título do menu
        font = pygame.font.Font('freesansbold.ttf', 36)
        title_text = font.render('Snake Game', True, WHITE)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 130))
        screen.blit(title_text, title_rect)
        
        # Desenhar botão "Iniciar"
        draw_button(screen, YELLOW, 200, 370, 200, 50, "Iniciar", WHITE)
        
        # Desenhar botão "Configurações"
        draw_button(screen, YELLOW, 200, 440, 200, 50, "Configurações", WHITE)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 200 <= mouse_pos[0] <= 400 and 370 <= mouse_pos[1] <= 420:
                    if SOUND_ENABLED:
                        click_sound.play()
                    return True  # Retorna True para indicar que o jogo deve ser iniciado
                elif 200 <= mouse_pos[0] <= 400 and 440 <= mouse_pos[1] <= 490:
                    if SOUND_ENABLED:
                        click_sound.play()
                    config_menu(screen)  # Abrir tela de configurações

    return False  # Retorna False se o jogo não foi iniciado

def config_menu(screen):
    global SOUND_ENABLED, SNAKE_COLOR, CURRENT_COLOR_INDEX
    click_sound = pygame.mixer.Sound('audios/click-sound.mp3')

    background_image = pygame.image.load('img/game-over2.png')  # Carregar imagem de fundo
    background_rect = background_image.get_rect()
    
    running = True

    while running:
        screen.blit(background_image, background_rect)  # Desenhar imagem de fundo
        
        # Desenhar título do menu
        font = pygame.font.Font('freesansbold.ttf', 36)
        title_text = font.render('Configurações', True, WHITE)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 130))
        screen.blit(title_text, title_rect)
        
        # Desenhar opção de cor da cobrinha
        draw_button(screen, YELLOW, 200, 370, 200, 50, "Cor da Cobrinha", AVAILABLE_COLORS[CURRENT_COLOR_INDEX])
        
        # Desenhar opção de som
        sound_text = "Som: Ligado" if SOUND_ENABLED else "Som: Desligado"
        draw_button(screen, YELLOW, 200, 440, 200, 50, sound_text, WHITE)
        
        # Desenhar botão "Voltar"
        draw_button(screen, YELLOW, 200, 510, 200, 50, "Voltar", WHITE)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 200 <= mouse_pos[0] <= 400 and 370 <= mouse_pos[1] <= 420:
                    # Alterar cor da cobrinha ao clicar na opção
                    if SOUND_ENABLED:
                        click_sound.play()
                    
                    CURRENT_COLOR_INDEX = (CURRENT_COLOR_INDEX + 1) % len(AVAILABLE_COLORS)
                    SNAKE_COLOR = AVAILABLE_COLORS[CURRENT_COLOR_INDEX]
                elif 200 <= mouse_pos[0] <= 400 and 440 <= mouse_pos[1] <= 490:
                    # Alternar estado do som ao clicar na opção
                    if SOUND_ENABLED:
                        click_sound.play()
                    SOUND_ENABLED = not SOUND_ENABLED
                elif 200 <= mouse_pos[0] <= 400 and 510 <= mouse_pos[1] <= 560:
                    if SOUND_ENABLED:
                        click_sound.play()
                    return  # Voltar para o menu principal

def run(screen):
    global SNAKE_COLOR
    # Defina as variáveis de tempo
    initial_speed = 5  # Intervalo de tempo inicial em milissegundos
    max_speed = 15  # Intervalo de tempo mínimo em milissegundos
    speed_factor = 0.01  # Fator de redução do intervalo de tempo

    click_sound = pygame.mixer.Sound('audios/click-sound.mp3')
    eat_sound = pygame.mixer.Sound('audios/eat-sound.mp3')
    eat_wrong_sound = pygame.mixer.Sound('audios/eat-wrong-sound.mp3')
    game_over_sound = pygame.mixer.Sound('audios/game-over-sound.mp3')

    snake = [(200, 200)]  # Increase snake size to 25 pixels each segment
    snake_skin = pygame.Surface((25, 25))
    snake_skin.fill(SNAKE_COLOR)  # White

    my_direction = LEFT

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 18)
    score = 0

    game_over = False
    apple_pos = on_grid_random()
    correct_equation, correct_result = generate_equation(screen)
    incorrect_results = generate_incorrect_results(correct_result, 3)
    all_apple_pos = [apple_pos] + [on_grid_random() for _ in range(3)]
    while not game_over:
        clock.tick(initial_speed)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_UP and my_direction != DOWN:
                    my_direction = UP
                if event.key == K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT
                if event.key == K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT

        if collision(snake[0], all_apple_pos):
            collided_apple_index = None
            for i, apple in enumerate(all_apple_pos):
                if collision(snake[0], [apple]):
                    collided_apple_index = i
                    break
            
            if collided_apple_index is not None:
                if 0 != collided_apple_index:
                    if SOUND_ENABLED:
                        eat_wrong_sound.play()
                    snake = snake[:-1]
                    score -= 1
                else:
                    if SOUND_ENABLED:
                        eat_sound.play()
                    apple_pos = on_grid_random()
                    snake.append((0, 0))
                    score += 1

            correct_equation, correct_result = generate_equation(screen)
            incorrect_results = generate_incorrect_results(correct_result, 3)
            all_apple_pos = [apple_pos] + [on_grid_random() for _ in range(3)]

        # Check if snake collided with boundaries
        if len(snake) > 0 and (snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0):
            if SOUND_ENABLED:
                game_over_sound.play()
            game_over = True
            break

        if len(snake) <= 0:
            if SOUND_ENABLED:
                game_over_sound.play()
            game_over = True
            break

        # Check if the snake has hit itself
        for i in range(1, len(snake) - 1):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                if SOUND_ENABLED:
                    game_over_sound.play()
                game_over = True
                break

        if game_over:
            print("game over")
            if SOUND_ENABLED:
                game_over_sound.play()
            break

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])

        # Actually make the snake move.
        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 25)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 25)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 25, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 25, snake[0][1])

        background_image = pygame.image.load('img/game.png')  # Carregar imagem de fundo
        background_rect = background_image.get_rect()
        screen.blit(background_image, background_rect)

        # Desenhar maçã com a resposta correta
        apple_correct = pygame.Surface((25, 25))
        apple_correct.fill((255, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 15)
        text_surface_correct = font.render(str(correct_result), True, WHITE)
        screen.blit(apple_correct, apple_pos)
        screen.blit(text_surface_correct, (apple_pos[0] + 7, apple_pos[1] + 7))

        # Desenhar maçãs com as respostas incorretas
        for i, pos in enumerate(all_apple_pos[1:]):
            apple_incorrect = pygame.Surface((25, 25))
            apple_incorrect.fill((255, 0, 0))
            font = pygame.font.Font('freesansbold.ttf', 15)
            text_surface_incorrect = font.render(str(incorrect_results[i]), True, WHITE)
            screen.blit(apple_incorrect, pos)
            screen.blit(text_surface_incorrect, (pos[0] + 7, pos[1] + 7))

        # Desenhar HUD
        draw_hud(screen, score)

        # Desenhar grade
        for x in range(0, 600, 25):  # Desenhar linhas verticais
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
        for y in range(0, 600, 25):  # Desenhar linhas horizontais
            pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

        # Desenhar cobrinha
        for pos in snake:
            screen.blit(snake_skin, pos)

        # Exibir equação
        font = pygame.font.Font('freesansbold.ttf', 24)
        equation_text = font.render(f'Equation: {correct_equation}', True, (255, 255, 255))
        equation_rect = equation_text.get_rect(center=(screen.get_width()//2, 30))
        screen.blit(equation_text, equation_rect)

        initial_speed = min(max_speed, initial_speed + speed_factor)
        pygame.display.update()

    while True:

        background_image = pygame.image.load('img/game-over2.png')  # Carregar imagem de fundo
        background_rect = background_image.get_rect()
        screen.blit(background_image, background_rect)

        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, 170)
        screen.blit(game_over_screen, game_over_rect)

        # Desenhar botão "Jogar Novamente"
        draw_button(screen, YELLOW, 200, 370, 200, 50, "Jogar Novamente", (255, 255, 255))

        draw_button(screen, YELLOW, 200, 440, 200, 50, "Voltar", (255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 200 <= mouse_pos[0] <= 400 and 370 <= mouse_pos[1] <= 420:
                    if SOUND_ENABLED:
                        click_sound.play()
                    run(screen)
                elif 200 <= mouse_pos[0] <= 400 and 440 <= mouse_pos[1] <= 490:
                    if SOUND_ENABLED:
                        click_sound.play()
                    main()


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((600, 625))  # Ajustando a altura da tela para eliminar o espaço extra
    pygame.display.set_caption('Snake')

    if main_menu(screen):  # Verifica se o jogo deve ser iniciado
        run(screen)

if __name__ == "__main__":
    main()

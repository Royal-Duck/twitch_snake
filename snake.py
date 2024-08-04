import pygame, time, random

CELL_SIZE : int = 35
WINDOW_SIZE : int = 700
BACKGROUND_COLOR : tuple[int,int,int] = (218,255,182)
GRID_SIZE : int = int(WINDOW_SIZE / CELL_SIZE)

APPLE_TYPES : list[tuple[int,int,int,int]] = [(90,255,0,0), (5,0,200,255), (5,255,0,200)]

pygame.init()

game_over_screen : pygame.Surface = pygame.image.load("./game_over.png")
pixel_font : pygame.font.Font = pygame.font.Font("pixel.ttf", 5)
score_render : pygame.Surface = pixel_font.render("0", False, (0,0,0))

snake_color : tuple[int,int,int] = (0,255,0)
elapse_time : float = 0.2

screen : pygame.Surface = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock : pygame.time.Clock = pygame.time.Clock()

def get_cell_rect(x : int, y : int) -> pygame.Rect:
    return pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)

def draw_cell(x : int, y : int, color : tuple[int,int,int], image : pygame.Surface | None = None, image_orientation : int = 0) -> None:
    global screen
    pygame.draw.rect(screen, color, get_cell_rect(x, y))
    if image:
        final_image : pygame.Surface = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        final_image = pygame.transform.rotate(final_image, 90*image_orientation)
        screen.blit(final_image, (round(x)*CELL_SIZE, round(y)*CELL_SIZE))

snake : list[tuple[int,int]] = [(0,0),(1,0)]
direction : tuple[int,int] = (1,0)
score : int = 0
apple : tuple[int,int] = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
apple_type : int = 0
pwups : dict[str,bool] = {
    "noclip" : False,
    "noselfcollision" : False
}
def draw_frame() -> None:
    i : int = 0
    cell : tuple[int,int] = (0,0)
    for i, cell in enumerate(snake[:-1]):
        body_part_direction : tuple[int,int] = cell[0] + snake[i+1][0], cell[1]+snake[i+1][1]
        body_part_orientation : int = (2 if body_part_direction[1] == 1 else 0) -body_part_direction[0]
        draw_cell(cell[0], cell[1], snake_color, pygame.image.load("./snake_body.png"), body_part_orientation)
    head_orientation : int = (2 if direction[1] == 1 else 0) -direction[0]
    draw_cell(snake[-1][0], snake[-1][1], snake_color, pygame.image.load("./snake_head.png"), head_orientation)
    draw_cell(apple[0], apple[1], APPLE_TYPES[apple_type][1:], pygame.image.load("./apple.png"))

def process_frame() -> int:
    global snake, score, apple, apple_type, snake_color
    snake.append((snake[-1][0]+direction[0], snake[-1][1]+direction[1]))
    del snake[0]
    #time.sleep(elapse_time)
    if snake[-1][0] not in range(0, GRID_SIZE) or snake[-1][1] not in range(0, GRID_SIZE):
        if pwups["noclip"]:
            pwups["noclip"] = False
            snake_color = (0,255,0)
            pos : tuple[int, int] = (snake[-1][0] % GRID_SIZE, snake[-1][1] % GRID_SIZE)
            del snake[-1]
            snake.append(pos)
        else :
            return 1
    if snake[-1] in snake[:-1]:
        if pwups["noselfcollision"]:
            pwups["noselfcollision"] = False
            snake_color = (0,255,0)
        else :
            return 1
    if snake[-1] == apple:
        match apple_type:
            case 1:
                pwups["noselfcollision"] = True
                snake_color = APPLE_TYPES[1][1:]
            case 2:
                pwups["noclip"] = True
                snake_color = APPLE_TYPES[2][1:]
        score += 1
        apple_type = random.choices(list(range(len(APPLE_TYPES))), [a_type[0] for a_type in APPLE_TYPES])[0]
        apple = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        snake.append(snake[-1])
    clock.tick(1/elapse_time)
    return 0

def process_events() -> int:
    if pygame.event.get(pygame.QUIT):
        return 2
    event : pygame.event.Event = pygame.event.Event(0)
    for event in pygame.event.get():
        if event.type != pygame.KEYDOWN:
            continue
        global direction
        direction_pressed : bool = True
        if event.key == pygame.K_LEFT and direction != (1,0):
            direction = (-1,0)
        elif event.key == pygame.K_RIGHT and direction != (-1,0):
            direction = (1,0)
        elif event.key == pygame.K_UP and direction != (0,1):
            direction = (0,-1)
        elif event.key == pygame.K_DOWN and direction != (0,-1):
            direction = (0,1)
        else:
            direction_pressed = False
        if direction_pressed :
            break
    return 0

def update() -> int:
    return_code : int = process_events()
    screen.fill(BACKGROUND_COLOR)
    draw_frame()
    pygame.display.flip()
    if process_frame(): 
        return 1 
    return return_code

def game_over() -> None:
    global snake, direction, score, apple, game_over_screen, score_render, pixel_font
    pixel_font = pygame.font.Font("./pixel.ttf", 5)
    score_render = pygame.Surface((len(str(score))*5, 5))
    score_render = pixel_font.render(str(score), False, (0,0,0))
    game_over_screen.blit(score_render, (82, 124))
    game_over_screen = pygame.transform.scale(game_over_screen, (WINDOW_SIZE, WINDOW_SIZE))
    screen.blit(game_over_screen, (0,0))
    pygame.display.flip()
    while 1:
        event : pygame.event.Event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            snake = [(0,0), (1,0)]
            direction = (1,0)
            score = 0
            apple = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            break

while 1:
    while 1:
        match update():
            case 1:
                break
            case 2:
                pygame.quit()
                exit(0)
    game_over()

pygame.quit()
exit(0)

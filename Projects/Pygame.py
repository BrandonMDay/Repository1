import pygame
import random
from pygame import time
pygame.init()
base = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 20, 147)
base_blue = (0, 0, 255)
screen_width = 600
screen_height = 800
use_font = pygame.font.get_default_font()
font = pygame.font.SysFont(use_font, 75)


def setup_screen(screen_width, screen_height):
    display = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("First Game")
    return display


screen = setup_screen(screen_width, screen_height)


def game_start():
    waiting = True
    while waiting:
        screen.fill(black)
        title_txt = font.render("Dodge Rocks!", True, white)
        game_start_txt = font.render("Press 'space' to start", True, white)
        screen.blit(title_txt, ((screen_width * 0.25), (screen_height * 0.5)))
        screen.blit(game_start_txt, ((screen_width * 0.07), (screen_height * 0.7)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def get_random_colour():
    for num in range(255):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
    return (red, green, blue)


def draw_ladder(y_lines):
    interval = y_lines
    while interval < screen_height:
        pygame.draw.line(screen, black, (0, interval), (screen_width, interval), 3)
        interval += 50
    if y_lines < 50:
        return y_lines + 1
    else:
        return 0


def draw_squares_left(y_squares):
    left = 20
    top = y_squares
    width = 20
    height = 20
    while top <= screen_height:
        square = pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, pink, square)
        top += 200
    if y_squares < 200:
        return y_squares + 1
    else:
        return 0


def draw_squares_right(y_squares):
    left = screen_width - 40
    top = y_squares
    width = 20
    height = 20
    while top <= screen_height:
        square = pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, pink, square)
        top += 200
    if y_squares < 200:
        return y_squares + 1
    else:
        return 0


def get_player(car_x, car_y):
    car_image = pygame.image.load('car_image_transparent.png').convert_alpha()
    car_rect = car_image.get_rect()
    car_rect.center = (car_x, car_y)
    screen.blit(car_image, car_rect)
    return car_rect


def get_rock(rock_x, rock_y, car_rect):
    rock_fall = 5
    rock_image = pygame.image.load('rock_image.png').convert_alpha()
    rock_image = pygame.transform.scale(rock_image, (75, 75))
    rock_rect = rock_image.get_rect()
    rock_rect.center = rock_x, rock_y
    screen.blit(rock_image, rock_rect)
    collide = rock_rect.colliderect(car_rect)
    if rock_y == 0:
        rock_x = random.randint(75, screen_width - 75)
        return rock_x, rock_y + rock_fall, collide
    if rock_y < screen_height:
        return rock_x, rock_y + rock_fall, collide
    else:
        return rock_x, 0, collide


def restart_game(hp):
    hp = 100
    timer = 0
    return hp, timer


def play_game():
    run = True
    y_lines = 0
    y_squares = 0
    rock_cords = [100, 0]
    rock_x = rock_cords[0]
    rock_y = rock_cords[1]
    car_x = screen_width * 0.5
    car_y = screen_height * 0.8
    velocity = 5
    hp = 100
    timer = 0
    while run:
        ig_time = round(timer, 2)
        screen.fill(white)
        y_squares = draw_squares_left(y_squares)
        y_squares = draw_squares_right(y_squares)
        y_lines = draw_ladder(y_lines)
        car_rect = get_player(car_x, car_y)
        rock_x, rock_y, collide = get_rock(rock_x, rock_y, car_rect)
        img = font.render(f"Life: {hp}", True, base_blue)
        screen.blit(img, ((screen_width * 0.5), 20))
        clock = font.render(f"Time: {ig_time}", True, base_blue)
        screen.blit(clock, ((screen_width * 0.05), 20))
        if hp > 0:
            timer += 0.01
        if collide:
            hp -= 1
        if hp <= 0:
            screen.fill(black)
            game_over_txt = font.render("GAME OVER", True, white)
            restart_text = font.render("Press 'r' to restart", True, white)
            score = round(ig_time * 100)
            score_txt = font.render(f"Score: {score} points!", True, white)
            screen.blit(game_over_txt, ((screen_width*0.25), (screen_height*0.5)))
            screen.blit(score_txt, ((screen_width * 0.13), (screen_height * 0.7)))
            screen.blit(restart_text, ((screen_width*0.13), (screen_height*0.9)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and hp <= 0:
                    hp, timer = restart_game(hp)

        keys = pygame.key.get_pressed()
        change_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * velocity
        if 0 <= (car_x + change_x) <= (screen_width - 102):
            car_x += change_x

        pygame.display.update()

        time.wait(10)


game_start()
play_game()
pygame.quit()

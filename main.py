import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape Catcher")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

BG_COLOR = (20, 20, 35)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
COLORS = [(255, 60, 60), (60, 255, 120), (60, 150, 255),
          (255, 220, 60), (255, 80, 255), (60, 255, 255), (255, 140, 40)]
SHAPES = ["circle", "square", "triangle"]


def draw_shape(kind, x, y, color):
    if kind == "circle":
        pygame.draw.circle(screen, color, (x, y), 20)
    elif kind == "square":
        pygame.draw.rect(screen, color, (x - 20, y - 20, 40, 40))
    else:
        pygame.draw.polygon(screen, color, [(x, y - 22), (x - 22, y + 18), (x + 22, y + 18)])


def draw_hearts(lives):
    for i in range(lives):
        x = WIDTH - 150 + i * 45
        pygame.draw.circle(screen, RED, (x - 8, 22), 8)
        pygame.draw.circle(screen, RED, (x + 8, 22), 8)
        pygame.draw.polygon(screen, RED, [(x - 16, 25), (x + 16, 25), (x, 42)])


def run_game():
    basket = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 70, 120, 24)
    basket_color = random.choice(COLORS)
    shapes = []
    score = 0
    lives = 3
    spawn_timer = 0

    while lives > 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # التحكم بالكيبورد
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            basket.x -= 8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            basket.x += 8

        # التحكم باللمس أو الفأرة: السلة تتبع الإصبع أو المؤشر
        if pygame.mouse.get_pressed()[0]:
            mouse_x, _ = pygame.mouse.get_pos()
            basket.centerx = mouse_x

        basket.clamp_ip(screen.get_rect())

        # إنشاء أشكال جديدة
        spawn_timer += 1
        if spawn_timer >= max(15, 45 - score):
            spawn_timer = 0
            shapes.append({
                "kind": random.choice(SHAPES),
                "x": random.randint(30, WIDTH - 30),
                "y": -20,
                "color": random.choice(COLORS),
                "speed": random.uniform(2, 4) + score * 0.05,
            })

        # تحريك الأشكال والتحقق من الالتقاط أو السقوط
        for s in shapes[:]:
            s["y"] += s["speed"]
            shape_rect = pygame.Rect(s["x"] - 20, s["y"] - 20, 40, 40)
            if basket.colliderect(shape_rect):
                shapes.remove(s)
                score += 1
                basket_color = s["color"]
            elif s["y"] > HEIGHT:
                shapes.remove(s)
                lives -= 1

        # الرسم
        screen.fill(BG_COLOR)
        for s in shapes:
            draw_shape(s["kind"], s["x"], s["y"], s["color"])
        pygame.draw.rect(screen, basket_color, basket, border_radius=10)
        pygame.draw.rect(screen, WHITE, basket, 2, border_radius=10)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (15, 12))
        draw_hearts(lives)
        pygame.display.flip()

    return score


def game_over_screen(score):
    screen.fill(BG_COLOR)
    lines = [
        (big_font, "GAME OVER", RED, -90),
        (font, f"Score: {score}", WHITE, -10),
        (font, "Tap or click to play again", WHITE, 40),
        (font, "R = restart    Q = quit", WHITE, 80),
    ]
    for f, text, color, dy in lines:
        surf = f.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + dy)))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(30)


def main():
    while True:
        score = run_game()
        game_over_screen(score)


if __name__ == "__main__":
    main()
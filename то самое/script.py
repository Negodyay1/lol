import pygame, random, time
pygame.init()

def load_best():
    try:
        with open('best_score.txt', 'r') as f:
            return int(f.read.strip())
    except:
        return 0

def save_best(score):
    with open('best_score.txt', 'w') as f:
        f.write(str(score))


w = 700
h = 700
p = pygame.Rect(300, 100, 40, 40)
SPEED = 5

s = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
run = True

pygame.mixer.init()
coin_sound =  pygame.mixer.Sound('coin1.mp3')
hit_sound = pygame.mixer.Sound('hit.mp3')
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

best_score = load_best()

f = pygame.font.Font('ofont.ru_Zeitmax.ttf', 36)

enemy = pygame.Rect(100, 100, 40, 40)
ex, ey = 4, 3

TIME_LIMIT = 75
end_time = time.time() + TIME_LIMIT

COIN_TYPES = [
    ((255, 215, 0), +1),
    ((0, 200, 0),   +3),
    ((0, 250, 250), +5),
    ((200, 50, 50), -2),
    ((50, 0, 0), -5)]


def new_coin():
    (r, g, b), value = random.choice(COIN_TYPES)
    x = random.randint(20, w - 20)
    y = random.randint(20, h - 20)
    return {"pos": (x, y), "color": (r, g, b), "value": value}

def show_menu():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return
        s.fill((67,157,247))
        title = f.render("METAL PIPE COINS", True, (255,255,255))
        subtitle = f.render("press ENTER to start", True, (255,150,150))
        s.blit(title, (150,150))
        s.blit(subtitle, (105,300))
        pygame.display.flip()
        clock.tick(30)

def run_game():
    global score,lives,ex,ey
    coins = [new_coin() for _ in range(15)]
    score = 0
    lives = 5
    run = True
    best_score = load_best()


    score = 0
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        k = pygame.key.get_pressed()
        if k[pygame.K_a]:
            p.x -= SPEED
        if k[pygame.K_d]:
            p.x += SPEED
        if k[pygame.K_w]:
            p.y -= SPEED
        if k[pygame.K_s]:
            p.y += SPEED

        p.x = max(0, min(w - p.w, p.x))
        p.y = max(0, min(h - p.h, p.y))

        enemy.x += ex;
        enemy.y += ey
        if enemy.left <= 0 or enemy.right >= w: ex *= -1
        if enemy.top <= 0 or enemy.bottom >= h: ey *= -1

        if p.colliderect(enemy):
            lives -= 1
            pygame.mixer.Sound.play(hit_sound)
            p.x, p.y = w // 2 - p.w // 2, h - 60
            pygame.time.wait(300)
            if lives <= 0:
                reason = 'lives'
                break

        for c in coins:
            if p.collidepoint(c["pos"]):
                pygame.mixer.Sound.play(coin_sound)
                score += c["value"]
                nc = new_coin()
                c["pos"], c["color"], c["value"] = nc["pos"], nc["color"], nc["value"]

        s.fill((67, 157, 247))
        pygame.draw.rect(s, (200, 150, 50), p)
        pygame.draw.rect(s, (255, 80, 80,), enemy)
        for c in coins:
            pygame.draw.circle(s, c["color"], c["pos"], 10)

        t_left = max(0, int(end_time - time.time()))
        s.blit(f.render(f"Очки: {score}", True, (255, 255, 255)), (10, 10))
        s.blit(f.render(f"Время: {t_left}", True, (200, 220, 255)), (10, 40))
        s.blit(f.render(f"Жизни: {lives}", True, (255, 180, 180)), (10, 70))

        pygame.display.flip()
        clock.tick(60)  # fps

        if t_left == 0:
            reason = "time"
            break

    s.fill((20, 20, 20))
    msg = "GAME OVER (жизни кончились)"
    if reason == "lives":
        pass
    else:
        msg = "Время вышло!"
    s.blit(f.render(msg, True, (255, 120, 120)), (40, 160))
    s.blit(f.render(f'Итоговый счёт: {score}', True, (255, 255, 255)), (110, 200))

    if score > best_score:
        save_best(score)
        best_score = score
        s.blit(f.render("НОВЫЙ РЕКОРД", True, (255, 255, 0)), (100, 230))


    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

show_menu()
while True:
    run_game()




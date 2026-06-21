import pygame
import sys
import random
import math

# --- PHYSIQUE & CALCULS INSA (DM CONTEXT) ---
PCI, G, K_SAFE, K_TO, V_CRUISE = 43e6, 9.81, 1.15, 4.5, 250
WHITE, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, ADV_COLOR, RED = (255,255,255), (0,255,255), (255,0,255), (50,255,50), (170,255,0), (255, 50, 50)

def solver_avion(npax, dist, fin, eta, adv):
    """Calculateur de performance thermodynamique"""
    m_cellule = (485 * npax - 35000) * (0.85 if adv else 1.0)
    rend = eta + (0.05 if adv else 0)
    m_payload = npax * 100
    m_fuel, m_moteurs, m_totale = 5000, 2000, 0
    for _ in range(15):
        old_m = m_totale
        m_totale = m_cellule + m_payload + m_moteurs + m_fuel
        poussee_cr = (m_totale * G) / fin # PFD: F = mg/f
        e_tot = (poussee_cr * dist * 1000) + (m_totale * G * 10000)
        m_fuel = K_SAFE * (e_tot / (PCI * rend))
        poussee_max_kn = (poussee_cr * K_TO) / 1000
        m_moteurs = 20 * poussee_max_kn
        if abs(m_totale - old_m) < 1: break
    
    moteurs_data = [("CFM56", 110, "RAPID"), ("LEAP-1A", 145, "SPREAD"), ("GEnx", 320, "BEAM"), ("GE9X", 470, "MEGA_BEAM")]
    moteur_final = moteurs_data[0]
    for m in moteurs_data:
        if m[1] >= (poussee_max_kn / 2): moteur_final = m; break
    
    target = 10000 if dist > 10000 else (6000 if npax > 300 else 4000)
    return {"mtow": m_totale, "fuel": m_fuel, "moteur": moteur_final, "target": target}

# --- CLASSES DU JEU ---
class Player(pygame.sprite.Sprite):
    def __init__(self, is_adv):
        super().__init__()
        self.image = pygame.Surface((70, 35), pygame.SRCALPHA)
        self.color = ADV_COLOR if is_adv else WHITE
        pygame.draw.rect(self.image, self.color, (0, 15, 60, 15), border_radius=5)
        pygame.draw.polygon(self.image, self.color, [(30, 15), (10, 0), (25, 15)])
        self.rect = self.image.get_rect(center=(150, 350))
        self.lives = 3
        self.shield = 0

    def update(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 700: self.rect.y += speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type_m, is_enemy=False):
        super().__init__()
        w, h = (100, 20) if "BEAM" in type_m else (25, 8)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        col = RED if is_enemy else (NEON_MAGENTA if "BEAM" in type_m else NEON_CYAN)
        pygame.draw.rect(self.image, col, (0, 0, w, h), border_radius=3)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -15 if is_enemy else 25
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1200 or self.rect.x < 0: self.kill()

class Creature(pygame.sprite.Sprite):
    def __init__(self, mult):
        super().__init__()
        self.image = pygame.Surface((45, 45), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (22, 22), 18)
        self.rect = self.image.get_rect(x=1200, y=random.randint(50, 650))
        self.speed = random.randint(5, 10) * mult
        self.offset = random.random() * 10
    def update(self):
        self.rect.x -= self.speed
        self.rect.y += int(6 * math.sin(pygame.time.get_ticks() * 0.008 + self.offset))
        if self.rect.x < -50: self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, diff_name, mult):
        super().__init__()
        self.image = pygame.Surface((200, 300), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, NEON_MAGENTA, (0, 0, 200, 300), 5)
        self.rect = self.image.get_rect(x=1200, y=200)
        self.hp_max = 80 * mult
        self.hp = self.hp_max
        self.attack_timer = 0
    def update(self):
        if self.rect.x > 900: self.rect.x -= 2
        self.rect.y += int(4 * math.sin(pygame.time.get_ticks() * 0.003))
        self.attack_timer += 1

# --- INITIALISATION ---
pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
font = pygame.font.SysFont("Consolas", 24)
font_huge = pygame.font.SysFont("Consolas", 60, bold=True)

def select_difficulty():
    levels = [("CADET (FACILE)", 0.8, NEON_GREEN), ("PILOTE (MOYEN)", 1.2, NEON_CYAN), ("TOP GUN (DUR)", 2.0, NEON_MAGENTA)]
    sel = 1
    while True:
        screen.fill((2, 5, 15))
        for i, (name, mult, col) in enumerate(levels):
            c = col if sel == i else (100, 100, 100)
            txt = font.render(("> " if sel == i else "  ") + name, True, c)
            screen.blit(txt, (W//2 - 150, 300 + i*60))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: sel = (sel-1)%3
                if e.key == pygame.K_DOWN: sel = (sel+1)%3
                if e.key == pygame.K_RETURN: return levels[sel]

def menu_config():
    pax, dist, fin, eta, adv = 200, 5000, 18.0, 0.40, False
    while True:
        screen.fill((5, 10, 25))
        txts = ["=== ANALYSE AVANT-PROJET AVION ===", f"Passagers (Npax) : {pax}", f"Distance (L) : {dist} km", f"Finesse (f) : {fin:.1f}", f"Matériaux : {'ADV' if adv else 'STD'}", "", "[ENTRÉE] VALIDER"]
        for i, t in enumerate(txts): screen.blit(font.render(t, True, NEON_CYAN), (100, 100 + i*40))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: pax += 20
                if e.key == pygame.K_DOWN: pax = max(50, pax-20)
                if e.key == pygame.K_RIGHT: dist += 1000
                if e.key == pygame.K_LEFT: dist = max(500, dist-1000)
                if e.key == pygame.K_m: adv = not adv
                if e.key == pygame.K_RETURN: return solver_avion(pax, dist, fin, eta, adv), adv

# --- Lancement ---
res, is_adv = menu_config()
diff_name, diff_mult, diff_col = select_difficulty()
player = Player(is_adv)
bullets, enemy_bullets, monsters, boss_grp = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

score, running, boss_active, screen_shake = 0, True, False, 0
clock = pygame.time.Clock()

while running:
    offset = (random.randint(-screen_shake, screen_shake), random.randint(-screen_shake, screen_shake))
    screen.fill((2, 5, 20))
    if screen_shake > 0: screen_shake -= 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            bullets.add(Bullet(player.rect.right, player.rect.centery, res['moteur'][2]))
            screen_shake = 4

    # Physique d'inertie liée à la masse
    player_speed = max(4, 16 - (res['mtow']/70000))
    player.update(player_speed)

    # Boss Attack Logic (Riposte)
    if not boss_active:
        if random.random() < 0.06 * diff_mult: monsters.add(Creature(diff_mult))
        if score >= res['target'] - 1000:
            boss_active = True
            boss_obj = Boss(diff_name, diff_mult)
            boss_grp.add(boss_obj)
    else:
        # Le Boss tire toutes les 40 frames
        if boss_obj.attack_timer % 40 == 0:
            enemy_bullets.add(Bullet(boss_obj.rect.left, boss_obj.rect.centery, "RAPID", True))

    # Collisions
    if pygame.sprite.groupcollide(bullets, monsters, True, True): score += 100
    if pygame.sprite.spritecollide(player, monsters, True): player.lives -= 1; screen_shake = 15
    if pygame.sprite.spritecollide(player, enemy_bullets, True): player.lives -= 1; screen_shake = 15
    
    if boss_active:
        if pygame.sprite.groupcollide(bullets, boss_grp, True, False): 
            boss_obj.hp -= 1
            if boss_obj.hp <= 0: score += 3000; boss_obj.kill()

    bullets.update(); enemy_bullets.update(); monsters.update(); boss_grp.update()
    
    # Rendu
    temp_surf = pygame.Surface((W, H), pygame.SRCALPHA)
    bullets.draw(temp_surf); enemy_bullets.draw(temp_surf); monsters.draw(temp_surf); boss_grp.draw(temp_surf)
    temp_surf.blit(player.image, player.rect)
    screen.blit(temp_surf, offset)
    
    if boss_active and boss_obj.alive():
        pygame.draw.rect(screen, RED, (W//2-200, 20, int(400 * (boss_obj.hp/boss_obj.hp_max)), 15))

    # HUD avec moteur affiché
    screen.blit(font.render(f"SCORE: {score}/{res['target']} | VIES: {player.lives}", True, NEON_CYAN), (20, 20))
    screen.blit(font.render(f"MOTEUR INSTALLÉ : {res['moteur'][0]}", True, NEON_GREEN), (20, H-40))

    if score >= res['target']:
        msg = font_huge.render("VICTOIRE !", True, NEON_GREEN)
        screen.blit(msg, (W//2-msg.get_width()//2, H//2)); pygame.display.flip(); pygame.time.wait(3000); running = False
    
    if player.lives <= 0:
        msg = font_huge.render("CRASH - GAME OVER", True, RED)
        screen.blit(msg, (W//2-msg.get_width()//2, H//2)); pygame.display.flip(); pygame.time.wait(2000); running = False

    pygame.display.flip(); clock.tick(60)
pygame.quit()
import pygame
import sys
import random

# --- PHYSIQUE INSA ---
PCI, G, K_SAFE, K_TO, V_CRUISE = 43e6, 9.81, 1.15, 4.5, 250

def solver_avion(npax, dist, fin, eta, adv):
    m_cellule = (485 * npax - 35000) * (0.85 if adv else 1.0)
    rend = eta + (0.05 if adv else 0)
    m_payload = npax * 100
    m_fuel, m_moteurs, m_totale = 5000, 2000, 0
    for _ in range(15):
        old_m = m_totale
        m_totale = m_cellule + m_payload + m_moteurs + m_fuel
        poussee_cr = (m_totale * G) / fin # F = mg/f
        e_tot = (poussee_cr * dist * 1000) + (m_totale * G * 10000)
        m_fuel = K_SAFE * (e_tot / (PCI * rend))
        poussee_max_kn = (poussee_cr * K_TO) / 1000
        m_moteurs = 20 * poussee_max_kn
        if abs(m_totale - old_m) < 1: break
    
    moteurs_data = [("CFM56", 110, "RAPID"), ("LEAP-1A", 145, "SPREAD"), 
                    ("GEnx", 320, "BEAM"), ("Trent XWB", 370, "BEAM"), ("GE9X", 470, "MEGA_BEAM")]
    moteur_final = moteurs_data[0]
    for m in moteurs_data:
        if m[1] >= (poussee_max_kn / 2): moteur_final = m; break
    
    # Objectif dynamique
    if dist > 10000: obj = "SURVIE LONG COURRIER : Atteindre 5000 pts"
    elif npax > 300: obj = "SÉCURITÉ MAXIMALE : Ne perdez aucune vie"
    else: obj = "EFFICIENCE : Détruire 20 ennemis"

    return {"mtow": m_totale, "fuel": m_fuel, "moteur": moteur_final, "pwr": (poussee_cr * V_CRUISE) / 1e6, "obj": obj}

# --- INITIALISATION ---
pygame.init()
W, H = 1200, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 22)
font_huge = pygame.font.SysFont("Consolas", 40, bold=True)

NEON_CYAN, NEON_MAGENTA, NEON_GREEN, ADV_COLOR = (0, 255, 255), (255, 0, 255), (50, 255, 50), (170, 255, 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type_m):
        super().__init__()
        w, h = (60, 20) if type_m in ["BEAM", "MEGA_BEAM"] else (20, 5)
        self.image = pygame.Surface((w, h))
        self.image.fill(NEON_MAGENTA if "BEAM" in type_m else NEON_CYAN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > W: self.kill()

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill((255, 50, 50))
        pygame.draw.rect(self.image, (150, 0, 0), (5, 5, 35, 35))
        self.rect = self.image.get_rect(x=W, y=random.randint(50, H-50))
        self.speed = random.randint(4, 8)
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -50: self.kill()

def draw_hud(lives, score, res, is_adv):
    screen.blit(font.render(f"VIES: {'♥' * lives}", True, (255, 50, 50)), (20, 20))
    screen.blit(font.render(f"SCORE: {score} | MTOW: {int(res['mtow'])} kg", True, NEON_CYAN), (20, 50))
    screen.blit(font.render(f"OBJECTIF: {res['obj']}", True, NEON_GREEN), (20, H-40))

# --- ÉCRANS ---
def menu_config():
    pax, dist, fin, eta, adv = 200, 5000, 18.0, 0.40, False
    while True:
        screen.fill((5, 10, 25))
        txts = ["=== CONFIGURATION AVANT-PROJET INSA ===", f"[HAUT/BAS] Passagers : {pax}", f"[GAUCHE/DROITE] Distance : {dist} km",
                f"[F/G] Finesse : {fin:.1f}", f"[M] Matériaux : {'ADV' if adv else 'STD'}", "", "APPUYEZ SUR [ENTRÉE] POUR VALIDER"]
        for i, t in enumerate(txts): screen.blit(font.render(t, True, NEON_CYAN), (100, 100 + i*40))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: pax += 10
                if e.key == pygame.K_DOWN: pax -= 10
                if e.key == pygame.K_RIGHT: dist += 500
                if e.key == pygame.K_LEFT: dist -= 500
                if e.key == pygame.K_f: fin += 0.5
                if e.key == pygame.K_g: fin -= 0.5
                if e.key == pygame.K_m: adv = not adv
                if e.key == pygame.K_RETURN: return solver_avion(pax, dist, fin, eta, adv), adv

def presentation(res, is_adv):
    while True:
        screen.fill((2, 5, 15))
        txts = ["=== ANALYSE DU BUREAU D'ÉTUDES ===", f"MOTEUR RETENU : {res['moteur'][0]}", f"CLASSE DE TIR  : {res['moteur'][2]}",
                f"PUISSANCE MAX : {res['pwr']:.2f} MW", f"MASSE CARBURANT: {int(res['fuel'])} kg", "", f"MISSION : {res['obj']}", "", "APPUYEZ SUR [ESPACE] POUR LANCER LE TEST"]
        for i, t in enumerate(txts): screen.blit(font.render(t, True, NEON_GREEN if "MOTEUR" in t or "MISSION" in t else WHITE), (W//2-250, 150 + i*40))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: return
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

# --- BOUCLE DE JEU ---
res, is_adv = menu_config()
presentation(res, is_adv)

player_y, score, lives = H // 2, 0, 3
bullets, monsters = pygame.sprite.Group(), pygame.sprite.Group()
running = True

while running:
    screen.fill((2, 5, 15))
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            m_type = res['moteur'][2]
            if m_type == "RAPID": bullets.add(Bullet(160, player_y+10, m_type))
            elif m_type == "SPREAD": 
                for a in [-15, 0, 15]: bullets.add(Bullet(160, player_y+10+a, m_type))
            else: bullets.add(Bullet(160, player_y+10, m_type))

    keys = pygame.key.get_pressed()
    speed = max(3, 12 - (res['mtow']/80000)) # Inertie liée à la masse
    if keys[pygame.K_UP] and player_y > 0: player_y -= speed
    if keys[pygame.K_DOWN] and player_y < H-40: player_y += speed

    if random.random() < 0.04: monsters.add(Monster())
    
    # Collisions
    if pygame.sprite.groupcollide(monsters, bullets, True, res['moteur'][2] != "MEGA_BEAM"): score += 100
    for m in monsters:
        if m.rect.colliderect(pygame.Rect(100, player_y, 60, 20)):
            m.kill(); lives -= 1

    bullets.update(); monsters.update()
    p_color = ADV_COLOR if is_adv else (220, 220, 220)
    pygame.draw.rect(screen, p_color, (100, player_y, 60, 20), border_radius=5)
    pygame.draw.polygon(screen, p_color, [(120, player_y), (100, player_y-25), (110, player_y)])
    bullets.draw(screen); monsters.draw(screen)
    draw_hud(lives, score, res, is_adv)

    if lives <= 0:
        screen.blit(font_huge.render("CRASH - MISSION ÉCHOUÉE", True, (255, 0, 0)), (W//2-250, H//2)); pygame.display.flip()
        pygame.time.wait(2000); running = False
    
    pygame.display.flip(); clock.tick(60)
pygame.quit()
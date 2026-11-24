import json
import os
import random
import time
import pygame
from src.settings import (
    WIDTH, HEIGHT, FPS, BG_COLOR, GRID_COLOR, WHITE,
    NEON_GREEN, NEON_CYAN, NEON_RED, NEON_PURPLE, GOLD,
    INITIAL_LIVES, INITIAL_SPAWN_DELAY, BASE_FALL_SPEED,
    WORD_LIST, POWERUP_WORDS, HIGHSCORE_FILE
)
from src.entities import FallingWord, LaserBeam, Particle

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"score": 0, "wpm": 0}

def save_highscore(score, wpm):
    current = load_highscore()
    updated = False
    if score > current["score"]:
        current["score"] = score
        updated = True
    if wpm > current["wpm"]:
        current["wpm"] = wpm
        updated = True
    if updated:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f)
    return current

def spawn_explosion(particles, x, y, color=NEON_GREEN, count=22):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyType Pro | Arcade Klavye & Refleks Arenasi")
    clock = pygame.time.Clock()

    word_font = pygame.font.SysFont("consolas", 26, bold=True)
    hud_font = pygame.font.SysFont("consolas", 18, bold=True)
    small_font = pygame.font.SysFont("consolas", 15, bold=True)
    big_font = pygame.font.SysFont("consolas", 48, bold=True)

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 1.2)] for _ in range(45)]
    highscore = load_highscore()

    def reset_game():
        return {
            "words": [],
            "lasers": [],
            "particles": [],
            "active_word": None,
            "score": 0,
            "lives": INITIAL_LIVES,
            "level": 1,
            "combo": 0,
            "correct_chars": 0,
            "total_keystrokes": 0,
            "start_time": time.time(),
            "last_spawn": pygame.time.get_ticks(),
            "slow_until": 0,
            "game_over": False
        }

    state = reset_game()
    ship_pos = (WIDTH // 2, HEIGHT - 32)

    running = True
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        slow_active = now < state["slow_until"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state["game_over"]:
                    if event.key == pygame.K_RETURN:
                        state = reset_game()
                    continue

                if event.key == pygame.K_ESCAPE and state["active_word"]:
                    state["active_word"].locked = False
                    state["active_word"].typed = ""
                    state["active_word"] = None
                    continue

                char = event.unicode.lower()
                if not char.isalpha():
                    continue

                state["total_keystrokes"] += 1

                def handle_word_destroyed(target):
                    multiplier = 1 + (state["combo"] // 15)
                    state["score"] += len(target.word) * 10 * multiplier
                    state["words"].remove(target)
                    state["active_word"] = None
                    state["level"] = (state["score"] // 200) + 1

                    if target.powerup_type == "BOMB":
                        for other in state["words"][:]:
                            spawn_explosion(state["particles"], other.x + 30, other.y + 10, GOLD, 18)
                            state["score"] += len(other.word) * 5
                        state["words"].clear()
                        spawn_explosion(state["particles"], WIDTH // 2, HEIGHT // 2, GOLD, 50)
                    elif target.powerup_type == "SLOW":
                        state["slow_until"] = now + 5000
                        spawn_explosion(state["particles"], target.x + 30, target.y + 10, NEON_PURPLE, 30)
                    elif target.powerup_type == "HEAL":
                        state["lives"] = min(INITIAL_LIVES + 2, state["lives"] + 1)
                        spawn_explosion(state["particles"], target.x + 30, target.y + 10, NEON_CYAN, 30)
                    else:
                        spawn_explosion(state["particles"], target.x + 35, target.y + 12, NEON_GREEN, 22)

                if state["active_word"]:
                    target = state["active_word"]
                    if target.remaining.startswith(char):
                        target.typed += char
                        state["correct_chars"] += 1
                        state["combo"] += 1
                        laser_color = GOLD if target.powerup_type else NEON_CYAN
                        state["lasers"].append(LaserBeam(ship_pos, (target.x + 25, target.y + 15), laser_color))
                        if target.remaining == "":
                            handle_word_destroyed(target)
                    else:
                        state["combo"] = 0
                else:
                    candidates = [w for w in state["words"] if w.word.startswith(char)]
                    if candidates:
                        target = max(candidates, key=lambda w: w.y)
                        target.locked = True
                        target.typed += char
                        state["active_word"] = target
                        state["correct_chars"] += 1
                        state["combo"] += 1
                        laser_color = GOLD if target.powerup_type else NEON_CYAN
                        state["lasers"].append(LaserBeam(ship_pos, (target.x + 25, target.y + 15), laser_color))
                        if target.remaining == "":
                            handle_word_destroyed(target)
                    else:
                        state["combo"] = 0

        # Arka plan ve kayan yildizlari ciz
        screen.fill(BG_COLOR)
        for s in stars:
            s[1] += s[2] * (0.4 if slow_active else 1.0)
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, (90, 110, 160), (int(s[0]), int(s[1])), 1)

        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

        line_color = NEON_PURPLE if slow_active else NEON_RED
        pygame.draw.line(screen, line_color, (0, HEIGHT - 62), (WIDTH, HEIGHT - 62), 2)

        if not state["game_over"]:
            spawn_delay = max(650, INITIAL_SPAWN_DELAY - (state["level"] - 1) * 160)
            fall_speed = BASE_FALL_SPEED + (state["level"] - 1) * 0.22

            if now - state["last_spawn"] > spawn_delay:
                used_first = {w.word[0] for w in state["words"]}
                
                if random.random() < 0.15:
                    avail_pw = [w for w in POWERUP_WORDS if w[0] not in used_first]
                    if avail_pw:
                        chosen = random.choice(avail_pw)
                        state["words"].append(FallingWord(chosen, fall_speed * 1.15, word_font, POWERUP_WORDS[chosen]))
                        state["last_spawn"] = now
                else:
                    avail = [w for w in WORD_LIST if w[0] not in used_first]
                    if avail:
                        chosen = random.choice(avail)
                        state["words"].append(FallingWord(chosen, fall_speed, word_font))
                        state["last_spawn"] = now

            for w in state["words"][:]:
                w.update(slow_active)
                w.draw(screen)
                if w.y > HEIGHT - 68:
                    spawn_explosion(state["particles"], w.x + 30, HEIGHT - 65, NEON_RED, 25)
                    state["words"].remove(w)
                    if state["active_word"] == w:
                        state["active_word"] = None
                    state["lives"] -= 1
                    state["combo"] = 0
                    if state["lives"] <= 0:
                        state["game_over"] = True
                        elapsed_min = max((time.time() - state["start_time"]) / 60.0, 0.01)
                        final_wpm = int((state["correct_chars"] / 5) / elapsed_min)
                        highscore = save_highscore(state["score"], final_wpm)

            for laser in state["lasers"][:]:
                laser.update()
                laser.draw(screen)
                if laser.timer <= 0:
                    state["lasers"].remove(laser)

            for p in state["particles"][:]:
                p.update()
                p.draw(screen)
                if p.life <= 0:
                    state["particles"].remove(p)

            pygame.draw.polygon(screen, NEON_CYAN, [
                (ship_pos[0], ship_pos[1] - 20),
                (ship_pos[0] - 18, ship_pos[1] + 12),
                (ship_pos[0] + 18, ship_pos[1] + 12)
            ])

        # Istatistikler ve Ust HUD Paneli
        elapsed_minutes = max((time.time() - state["start_time"]) / 60.0, 0.01)
        wpm = int((state["correct_chars"] / 5) / elapsed_minutes)
        accuracy = int((state["correct_chars"] / max(1, state["total_keystrokes"])) * 100)
        multiplier = 1 + (state["combo"] // 15)

        pygame.draw.rect(screen, (15, 20, 38), (0, 0, WIDTH, 48))
        pygame.draw.line(screen, GRID_COLOR, (0, 48), (WIDTH, 48), 2)

        hud_left = f"SKOR: {state['score']} ({multiplier}x) | LVL: {state['level']} | HIZ: {wpm} WPM | ISABET: %{accuracy}"
        hud_right = f"REKOR: {highscore['score']} | CAN: {'*' * state['lives']}"
        
        screen.blit(hud_font.render(hud_left, True, GOLD), (15, 14))
        right_surf = hud_font.render(hud_right, True, NEON_GREEN)
        screen.blit(right_surf, (WIDTH - right_surf.get_width() - 15, 14))

        if slow_active:
            slow_surf = small_font.render("ZAMAN YAVASLATILDI!", True, NEON_PURPLE)
            screen.blit(slow_surf, (WIDTH // 2 - slow_surf.get_width() // 2, 56))

        if state["game_over"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 8, 18, 190))
            screen.blit(overlay, (0, 0))

            over_surf = big_font.render("OYUN BITTI!", True, NEON_RED)
            stat_surf = hud_font.render(f"Skor: {state['score']}  |  Hiz: {wpm} WPM  |  Isabet: %{accuracy}", True, WHITE)
            rec_surf = hud_font.render(f"En Yuksek Rekor: {highscore['score']} Puan ({highscore['wpm']} WPM)", True, GOLD)
            restart_surf = hud_font.render("Tekrar oynamak icin ENTER tusuna bas", True, NEON_GREEN)

            screen.blit(over_surf, (WIDTH // 2 - over_surf.get_width() // 2, HEIGHT // 2 - 90))
            screen.blit(stat_surf, (WIDTH // 2 - stat_surf.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(rec_surf, (WIDTH // 2 - rec_surf.get_width() // 2, HEIGHT // 2 + 20))
            screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

        

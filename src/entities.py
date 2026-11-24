import random
import pygame
from src.settings import WIDTH, WHITE, NEON_GREEN, NEON_CYAN, GOLD, NEON_PURPLE

class FallingWord:
    def __init__(self, word, speed, font, powerup_type=None):
        self.word = word
        self.typed = ""
        self.speed = speed
        self.font = font
        self.locked = False
        self.powerup_type = powerup_type  # None, "BOMB", "SLOW", "HEAL"
        
        text_width = self.font.size(self.word)[0]
        self.x = random.randint(45, WIDTH - text_width - 45)
        self.y = -35

    def update(self, slow_active=False):
        """Zaman yavaşlatma aktifse yarı hızda düşer."""
        current_speed = self.speed * 0.45 if slow_active else self.speed
        self.y += current_speed

    @property
    def remaining(self):
        return self.word[len(self.typed):]

    def draw(self, screen):
        # Güçlendirme kelimesiyse kalan harfler altın rengi görünür
        base_color = GOLD if self.powerup_type else WHITE
        typed_surface = self.font.render(self.typed, True, NEON_GREEN)
        rem_surface = self.font.render(self.remaining, True, base_color)
        
        total_width = typed_surface.get_width() + rem_surface.get_width()
        height = rem_surface.get_height()

        if self.locked or self.powerup_type:
            padding = 6
            rect = pygame.Rect(
                self.x - padding, 
                self.y - padding, 
                total_width + padding * 2, 
                height + padding * 2
            )
            border_color = GOLD if self.powerup_type else NEON_CYAN
            fill_color = (45, 38, 15) if self.powerup_type else (20, 45, 65)
            pygame.draw.rect(screen, fill_color, rect, border_radius=6)
            pygame.draw.rect(screen, border_color, rect, width=2, border_radius=6)

        screen.blit(typed_surface, (self.x, self.y))
        screen.blit(rem_surface, (self.x + typed_surface.get_width(), self.y))


class LaserBeam:
    def __init__(self, start_pos, end_pos, color=NEON_CYAN):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.timer = 6

    def update(self):
        self.timer -= 1

    def draw(self, screen):
        if self.timer > 0:
            pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 3)


class Particle:
    """Kelime patladığında etrafa saçılan neon kıvılcımlar."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4.5, 4.5)
        self.vy = random.uniform(-4.5, 4.5)
        self.life = random.randint(18, 32)
        self.color = color
        self.size = random.randint(3, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

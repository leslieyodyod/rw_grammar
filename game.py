import pygame
import random
import sys

pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kinyarwanda Matching Game")
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (144, 238, 144)
BLACK = (0, 0, 0)

# Levels: each level has its own pairs
levels = [
    [  # Level 1
        ("umuntu", "abantu"),
        ("umwana", "abana"),
    ],
    [  # Level 2
        ("igiti", "ibiti"),
        ("ikirenge", "ibirenge"),
        ("igitabo", "ibitabo"),
    ],
    [  # Level 3
        ("inka", "inka"),
        ("ihene", "ihene"),
        ("intama", "intama"),
    ]
]

# Layout
CARD_W, CARD_H = 150, 80
PADDING = 20
cols = 4

# Game state
current_level = 0
card_rects = []
selected = []
clock = pygame.time.Clock()

# --- Functions ---
def load_level(level_pairs):
    """Setup cards for a given level"""
    global card_rects, selected
    selected = []
    cards = [word for pair in level_pairs for word in pair]
    random.shuffle(cards)

    card_rects = []
    for i, word in enumerate(cards):
        x = (i % cols) * (CARD_W + PADDING) + 100
        y = (i // cols) * (CARD_H + PADDING) + 100
        rect = pygame.Rect(x, y, CARD_W, CARD_H)
        card_rects.append({"rect": rect, "word": word, "matched": False})

def draw_cards():
    """Draw all cards"""
    for card in card_rects:
        color = GREEN if card["matched"] else GRAY
        pygame.draw.rect(screen, color, card["rect"])
        pygame.draw.rect(screen, BLACK, card["rect"], 2)
        text = font.render(card["word"], True, BLACK)
        text_rect = text.get_rect(center=card["rect"].center)
        screen.blit(text, text_rect)

def check_match(pairs):
    """Check if selected cards form a valid pair"""
    global selected
    if len(selected) == 2:
        w1, w2 = selected[0]["word"], selected[1]["word"]
        # Is it a valid pair?
        if any(w1 in p and w2 in p for p in pairs):
            selected[0]["matched"] = True
            selected[1]["matched"] = True
        pygame.display.flip()
        pygame.time.delay(500)
        selected = []

def check_level_complete():
    """Return True if all cards are matched"""
    return all(card["matched"] for card in card_rects)

def show_message(message, duration=1500):
    """Display a message in the center of the screen"""
    screen.fill(WHITE)
    text = big_font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(duration)

# --- Start Game ---
load_level(levels[current_level])

while True:
    screen.fill(WHITE)
    draw_cards()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for card in card_rects:
                if card["rect"].collidepoint(event.pos) and not card["matched"]:
                    if card not in selected and len(selected) < 2:
                        selected.append(card)
                    if len(selected) == 2:
                        check_match(levels[current_level])

    # After each frame, check if the level is complete
    if check_level_complete():
        show_message(f"Level {current_level + 1} Complete!")
        current_level += 1
        if current_level < len(levels):
            load_level(levels[current_level])
        else:
            show_message("🎉 Congratulations! You finished all levels!", 2500)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)

import pickle
from typing import List, Tuple, Optional

import pygame

from colors import BLACK, WHITE, PURPLE, BLUE, ORANGE
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, HIGH_SCORE_FILE, STATE_DIR

ScoreEntry = Tuple[str, int]


def load_scores() -> List[ScoreEntry]:
    if not HIGH_SCORE_FILE.exists():
        return []
    try:
        with HIGH_SCORE_FILE.open("rb") as f:
            data = pickle.load(f)
        if isinstance(data, list):
            return [(str(n), int(s)) for n, s in data][:10]
    except Exception:
        return []
    return []


def save_scores(scores: List[ScoreEntry]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with HIGH_SCORE_FILE.open("wb") as f:
        pickle.dump(scores, f)


def qualifies(scores: List[ScoreEntry], score: int) -> bool:
    if score < 0:
        return False
    if len(scores) < 10:
        return True
    return score > min(scores, key=lambda s: s[1])[1]


def add_score(scores: List[ScoreEntry], name: str, score: int) -> List[ScoreEntry]:
    updated = scores + [(name, score)]
    updated.sort(key=lambda s: s[1], reverse=True)
    return updated[:10]


def prompt_for_name(screen: pygame.Surface, score: int) -> str:
    clock = pygame.time.Clock()
    name = ""
    font = pygame.font.SysFont("Courier New", 36)
    prompt = f"New High Score: {score}! Enter your name:"
    prompt_surf = font.render(prompt, True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()[:12]
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode and event.unicode.isprintable():
                    name += event.unicode

        screen.fill(BLACK)
        screen.blit(prompt_surf, ((SCREEN_WIDTH - prompt_surf.get_width()) // 2, SCREEN_HEIGHT // 3))
        entry_surf = font.render(name or "_", True, ORANGE)
        screen.blit(entry_surf, ((SCREEN_WIDTH - entry_surf.get_width()) // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        clock.tick(FRAME_RATE)


def show_high_scores(screen: pygame.Surface, score: Optional[int]) -> None:
    scores = load_scores()
    new_score = score if score is not None else 0
    if score is not None and qualifies(scores, score):
        name = prompt_for_name(screen, score)
        scores = add_score(scores, name, score)
        save_scores(scores)

    font = pygame.font.SysFont("Courier New", 36)
    title_font = pygame.font.SysFont("Courier New", 48)
    title = title_font.render("Top 10 Scores", True, WHITE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break

        screen.fill(BLUE)
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 60))

        y = 150
        for idx in range(10):
            entry = scores[idx] if idx < len(scores) else ("---", 0)
            line = f"{idx + 1:2}. {entry[0]:12}  {entry[1]:5}"
            line_surf = font.render(line, True, WHITE)
            screen.blit(line_surf, (SCREEN_WIDTH // 4, y))
            y += 40

        note = font.render("Press any key to continue", True, PURPLE)
        screen.blit(note, ((SCREEN_WIDTH - note.get_width()) // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()
        clock.tick(FRAME_RATE)

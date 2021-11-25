import pygame
from db import *
from Games.game_settings import *
from Games.Mugunghwa.Mugunghwa_Game import start_game as start_mugunghwa_game
from Games.Dalgona.dalgona_game import start_game as start_dalgona_game
from Games.MarbleGame.marble_game import start_game as start_marble_game
from Games.TugOfWar.TugOfWar import start_game as start_tug_game
from Games.game_menu import main_menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
LEVEL_UP_STEP = 1


if __name__ == "__main__":
    SCORE = 0
    LEVEL = 1
    selected = main_menu()

    if selected == INFINITE or selected == BEST_RECORD:
        while True:
            top_five = get_score(selected)
            mugunghwa_score = start_mugunghwa_game(LEVEL, SCORE)
            if mugunghwa_score:
                SCORE += mugunghwa_score
            else:
                break
            dalgona_score = start_dalgona_game(LEVEL, SCORE)
            if dalgona_score:
                SCORE += dalgona_score
            else:
                break
            tug_score = start_tug_game(LEVEL, SCORE)
            if tug_score:
                SCORE += tug_score
            else:
                break
            marble_score = start_marble_game(LEVEL, SCORE)
            if marble_score:
                SCORE += marble_score
            else:
                break
            if selected == BEST_RECORD:
                break
            LEVEL += LEVEL_UP_STEP
    elif selected == SELECT_MUGUNGHWA:
        while True:
            mugunghwa_score = start_mugunghwa_game(LEVEL, SCORE)
            if mugunghwa_score:
                SCORE += mugunghwa_score
            else:
                break
            LEVEL += LEVEL_UP_STEP
    elif selected == SELECT_DALGONA:
        while True:
            dalgona_score = start_dalgona_game(LEVEL, SCORE)
            if dalgona_score:
                SCORE += dalgona_score
            else:
                break
            LEVEL += LEVEL_UP_STEP
    elif selected == SELECT_TUG:
        while True:
            tug_score = start_tug_game(LEVEL, SCORE, best_record_mode=False, select_mode=True)
            if tug_score:
                SCORE += tug_score
            else:
                break
            LEVEL += LEVEL_UP_STEP
    elif selected == SELECT_MARBLE:
        while True:
            marble_score = start_marble_game(LEVEL, SCORE, best_record_mode=False, select_mode=True)
            if marble_score:
                SCORE += marble_score
            else:
                break
            LEVEL += LEVEL_UP_STEP

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ref_w, ref_h = screen.get_size()
    RUNNING = True
    ticks = pygame.time.get_ticks()
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
        screen.fill(PINK)
        message_to_screen_center(screen, '게임 종료', WHITE, korean_font,
                                 SCREEN_WIDTH / 3,
                                 ref_w,
                                 ref_h)
        message_to_screen_center(screen, f'점수는 {round(SCORE)} 점입니다. ', WHITE, korean_font,
                                 SCREEN_WIDTH / 2,
                                 ref_w,
                                 ref_h)
        elapsed_time = (pygame.time.get_ticks() - ticks) / 1000
        pygame.display.update()
        clock.tick(60)
        timer = 4 - elapsed_time
        if timer <= 0:
            break

    if selected == INFINITE or selected == BEST_RECORD:
        # 5 위 안에 들었는 지 계산.
        for record in top_five:
            # top_five 는 db.py 에서 sort 되어 있음.
            if int(record['score']) < SCORE:
                record_score(selected, {"user": "hanum", "score": SCORE}, record)
                break

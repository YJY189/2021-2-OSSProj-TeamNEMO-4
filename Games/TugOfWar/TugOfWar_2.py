import  pygame
import sys
import random
from Games.game_settings import *


class Game:
    def main(self):
        time = 30
        self.game_over_timer = GameOverTimer(time)
        tmr = 0
        level = 0
        click = 0
        click_n = 15

        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 메세지 배치하는 함수
        def message_to_screen_topLeft(surface, msg, color, font):
            textSurf, textRect = text_objects(msg, color, font)
            surface.blit(textSurf, (0, 0))

        def message_to_screen_topCenter(surface, msg, color, font):
            textSurf, textRect = text_objects(msg, color, font)
            surface.blit(textSurf, (200, 0))



        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tmr += 1
            imgBG = pygame.image.load("Images/TugOfWarBack.png")
            char_1 = pygame.image.load("Images/char1.png")
            char_2 = pygame.image.load("Images/char2.png")

            key = pygame.key.get_pressed()

            # 시작 화면
            if idx == 0:
                screen.fill(WHITE)
                screen.blit(imgBG, [0, 0])
                message_to_screen_center(screen, '줄다리기 게임', WHITE, korean_font, SCREEN_HEIGHT / 4)
                message_to_screen_left(screen, '[조작법]', WHITE, korean_font_small_size, 150, 320)
                message_to_screen_left(screen, 'A 클릭하여 줄 당기기', WHITE, korean_font_small_size, 150, 370)
                message_to_screen_left(screen, 'D 클릭하여 버티기', WHITE, korean_font_small_size, 150, 420)
                message_to_screen_left(screen, 'E 로 시작, Q로 종료', WHITE, korean_font_small_size, 150, 520)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            idx = 1
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            # 게임 화면 1단계
            if idx == 1:
                level = idx
                click_num = click_n*level
                screen.fill(BLACK)
                screen.blit(imgBG, [0, 0])
                # 캐릭터 놓기
                for i in range(0, 151, 50):
                    screen.blit(char_1, (i, 260))
                for i in range(760, 609, -50):
                    screen.blit(char_2, (i, 260))
                # LEVEL 표시
                message_to_screen_topLeft(screen, 'LEVEL {}'.format(level), WHITE, level_font)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            click += 1
                        elif event.key == pygame.K_d:
                            click += 1
                message_to_screen_topCenter(screen, '남은 클릭횟수 : {}'.format((click_num - click)), WHITE, korean_font)
                pygame.display.update()
                if click == click_num:
                    idx = 22

            # 게임 화면 2단계
            if idx == 2:
                level = idx
                click_num = click_n*level
                screen.fill(BLACK)
                screen.blit(imgBG, [0, 0])
                # 캐릭터 놓기
                for i in range(0, 151, 50):
                    screen.blit(char_1, (i, 260))
                for i in range(760, 609, -50):
                    screen.blit(char_2, (i, 260))
                # LEVEL 표시
                message_to_screen_topLeft(screen, 'LEVEL {}'.format(level), WHITE, level_font)
                # 키 입력 받음
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            click += 1
                        elif event.key == pygame.K_d:
                            click += 1
                message_to_screen_topCenter(screen, '남은 클릭횟수 : {}'.format(click_num - click), WHITE, korean_font)
                pygame.display.update()
                if click == click_num:
                    idx = 22

            # 게임 화면 3단계
            if idx == 3:
                level = idx
                click_num = click_n * level
                screen.fill(BLACK)
                screen.blit(imgBG, [0, 0])
                # 캐릭터 놓기
                for i in range(0, 151, 50):
                    screen.blit(char_1, (i, 260))
                for i in range(760, 609, -50):
                   screen.blit(char_2, (i, 260))
                # LEVEL 표시
                message_to_screen_topLeft(screen, 'LEVEL {}'.format(level), WHITE, level_font)
                # 키 입력 받음
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            click += 1
                        elif event.key == pygame.K_d:
                            click += 1
                message_to_screen_topCenter(screen, '남은 클릭횟수 : {}'.format(click_num - click), WHITE, korean_font)
                pygame.display.update()
                if click == click_num:
                    idx = 33

            # 통과화면
            if idx == 22:
                click = 0
                screen.fill(BLACK)
                message_to_screen_center(screen, '통과하셨습니다', BLUE, korean_font, 200)
                message_to_screen_center(screen, '다음 Level로 이동 : C', BLUE, korean_font, 300)
                message_to_screen_center(screen, '게임 종료 : Q', BLUE, korean_font, 400)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            idx = level + 1
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            # 종료함수
            if idx == 33:
                screen.fill(BLACK)
                message_to_screen_center(screen, '줄 다리기 게임을 통과했습니다', BLUE, korean_font, 200)
                message_to_screen_center(screen, '시작화면으로 이동 : R', BLUE, korean_font, 300)
                message_to_screen_center(screen, '게임 종료 : Q', BLUE, korean_font, 400)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            idx = 0
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            # 실패 화면
            if idx == 44:
                screen.fill(BLACK)
                message_to_screen_center(screen, '탈 락 하 셨 습 니 다', RED, korean_font, 200)
                message_to_screen_center(screen, '시작화면으로 이동 : R', RED, korean_font, 300)
                message_to_screen_center(screen, '게임 종료 : Q', RED, korean_font, 400)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            idx = 0
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()


new_game = Game()
new_game.main()




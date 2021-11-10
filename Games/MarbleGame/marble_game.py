import sys
import random
from Games.game_settings import *

class MarbleGame:
    TITLE=0
    MARBLE_GAME=1
    CLEAR=12
    MARBLE_GAME_INTRO=7
    GGANBU=6
    LEVEL_UP=11
    GAME_OVER=13
    TRUE_FALSE=14

    # 변수 선언
    idx = TITLE  # 화면 전환 관리 변수 idx 이 변수를 통해 화면 전환이 일어난다
    player_marbles = 10 #처음 플레이어가 가진 구슬 개수
    player_betting = 1 #처음 플레이어가 배팅하는 구슬 개수
    computer_marbles = 10 #처음 컴퓨터가 가진 구슬 개수
    computer_betting = random.randint(1, 2) #처음 컴퓨터는 1개, 2개 중 배팅을 하고 marble_game_level이 올라가면 그만큼 증가됨
    marble_game_level = 0 #플레이어가 가진 구슬 개수에 관여하는 변수로 이후 +1 해서 레벨을 나타냄
    betting_success = True
    betting_button_pressed = False
    screen_buffer = 0  # 화면 대기 구현 변수
    marble_game_timer = 0 #게임 루프문을 통해 이후 계속 1이 더해진다. 화면 대기 변수와 비교문을 통해 이미지 효과를 사용할 때 이용
    fail_eff = 0 #게임 이펙트 화면에서 게임 루프문을 통해 계속 -1이 되는데 이때 양수 값을 주면 0이 될때까지 이펙트 효과를 사용할 때 이용
    fail_eff_x = 0 #random.randint(-20, 20)
    fail_eff_y = 0 #random.randint(-10, 10)
    score=0 #게임의 점수를 저장하는 변수
    hint = 5 #hint 사용 가능 수
    # 이미지 로딩
    imgBG = pygame.image.load("bg/bg.png")  # 배경 이미지
    imgBGbase=pygame.image.load("bg/bgbase.png")
    imgTrue = pygame.image.load("imgs/True.png")  # 배팅 성공 이미지
    imgFalse = pygame.image.load("imgs/False.png")  # 배팅 실패 이미지
    imgStart = pygame.image.load("imgs/gamestart.png")
    imgHand1 = pygame.image.load("imgs/hand1.png")
    imgHand2 = pygame.image.load("imgs/hand2.png")
    imgHand3 = pygame.image.load("imgs/hand3.png")
    imgHand4 = pygame.image.load("imgs/hand4.png")
    imgHand5 = pygame.image.load("imgs/hand5.png")
    imgNPC=pygame.image.load("imgs/NPC.png")
    gganbuplay=False

    def __init__(self,width,height):
        pygame.display.set_caption(SCREEN_TITLE)
        self.width = width
        self.height = height
        # Screen set-up
        self.game_screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        self.ref_w, self.ref_h = self.game_screen.get_size()
        self.game_screen.fill(PINK)

    def reset_variable(self):
        self.player_marbles = 10
        self.player_betting = 1
        self.computer_marbles = 10
        self.computer_betting = random.randint(1,2+self.marble_game_level)
        self.marble_game_level = 0
        self.marble_game_timer = 0
        self.idx = self.TITLE  # 초기 화면으로
        self.hint=5 #힌트 5개로 초기화

    def draw_title(self):
        self.game_screen.fill(PINK)
        message_to_screen_center(self.game_screen, '홀짝 게임', WHITE, korean_font, self.game_screen.get_height() / 4,
                                     self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '[ 조작법 ]', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 3, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '↑↓ 방향키로 구슬 선택', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 2, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, '←→ 방향키로 홀짝 선택', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 1.7, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Enter&Return 키로 홀짝 힌트', WHITE, korean_font_small_size,
                                 self.game_screen.get_height() / 1.5, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Press Space Key', WHITE, korean_font_small_size,
                                     self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
        self.score = 0
    def draw_game_over(self):
        self.game_screen.fill(BLACK)
        self.imgNPC = pygame.transform.scale(self.imgNPC,(self.game_screen.get_width(), self.game_screen.get_height()))
        self.game_screen.blit(self.imgNPC, [0, 0])
        if self.screen_buffer <= self.marble_game_timer - 20:
            self.game_screen.fill(BLACK)
            if self.screen_buffer <= self.marble_game_timer - 30:
                pygame.mixer.music.stop()
                message_to_screen_center(self.game_screen, "GAME OVER", WHITE, korean_font,self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
                message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
                message_to_screen_left(self.game_screen, "SCORE : " + str(self.score), WHITE, korean_font,self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                                           self.ref_h)
    def level_up(self,score=0):
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, 'YOU WIN! LEVEL UP!', WHITE, korean_font,self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        if self.screen_buffer <= self.marble_game_timer - 20:
            self.marble_game_timer = 0
            self.marble_game_level += 1
            self.player_marbles = 10 - self.marble_game_level
            self.player_betting = 1
            self.computer_marbles = 10
            self.computer_betting = random.randint(1,2+self.marble_game_level)
            self.idx = self.MARBLE_GAME
            self.score += int(score)
        if self.player_marbles <= 5:  # 플레이어 구슬이 5개 이하라면
            self.score += int(score)
            self.idx = self.CLEAR  # 12 클리어 화면으로
    def draw_true_false(self):
        self.game_screen.fill(BLACK)
        if self.screen_buffer <= self.marble_game_timer - 20:
            if self.betting_success:
                self.imgTrue = pygame.transform.scale(self.imgTrue, (
                self.game_screen.get_width(), self.game_screen.get_height()))
                self.game_screen.blit(self.imgTrue, [0, 0])
                if self.screen_buffer <= self.marble_game_timer - 30:
                    self.player_betting = 1
                    self.idx = self.MARBLE_GAME
                    if self.player_marbles <= 0:
                        self.marble_game_timer=0
                        self.screen_buffer = self.marble_game_timer
                        self.idx = self.GAME_OVER
                    if self.computer_marbles <= 0:
                        self.marble_game_timer = 0
                        self.screen_buffer = self.marble_game_timer
                        self.idx = self.LEVEL_UP
            else:
                self.imgFalse = pygame.transform.scale(self.imgFalse, (
                self.game_screen.get_width(), self.game_screen.get_height()))
                self.game_screen.blit(self.imgFalse, [0, 0])
                if self.fail_eff > 0:
                    self.fail_eff_x = random.randint(-20, 20)
                    self.fail_eff_y = random.randint(-10, 10)
                    self.fail_eff = self.fail_eff - 1
                self.game_screen.blit(self.imgFalse, [self.fail_eff_x, self.fail_eff_y])
                if self.screen_buffer <= self.marble_game_timer - 30:
                    self.player_betting = 1
                    self.idx = self.MARBLE_GAME
                    if self.player_marbles <= 0:
                        self.marble_game_timer = 0
                        self.screen_buffer = self.marble_game_timer
                        self.idx = self.GAME_OVER
                    if self.computer_marbles <= 0:
                        self.marble_game_timer = 0
                        self.screen_buffer = self.marble_game_timer
                        self.idx = self.LEVEL_UP
    def draw_clear(self):
        pygame.mixer.music.stop()
        self.game_screen.fill(BLACK)
        message_to_screen_center(self.game_screen, "THANK YOU FOR PLAYING", WHITE, korean_font,
                                 self.game_screen.get_height() / 4, self.ref_w, self.ref_h)
        message_to_screen_center(self.game_screen, 'Press Enter or Return Key', WHITE, korean_font_small_size,
                                 self.game_screen.get_height() / 1.25, self.ref_w, self.ref_h)
        message_to_screen_left(self.game_screen, "SCORE : " + str(self.score), WHITE, korean_font,
                               self.game_screen.get_width() / 2, self.game_screen.get_height() / 2, self.ref_w,
                               self.ref_h)

    def draw_gganbu(self):
        self.game_screen.fill(BLACK)
        gganbu = pygame.mixer.Sound("sound/gganbu.mp3")
        if self.screen_buffer <= self.marble_game_timer - 20:
            if self.gganbuplay == False:
                gganbu.play()
                self.gganbuplay =True
            if self.screen_buffer <= self.marble_game_timer - 40:
                self.player_marbles = 6
                self.gganbuplay =False
                self.marble_game_timer = 0
                self.screen_buffer=0
                self.idx = self.LEVEL_UP
    def draw_hand(self):
        self.imgBGbase = pygame.transform.scale(self.imgBGbase,(self.game_screen.get_width(), self.game_screen.get_height()))
        self.game_screen.blit(self.imgBGbase, [0, 0])
        self.imgHand1 = pygame.transform.scale(self.imgHand1,(self.game_screen.get_width(), self.game_screen.get_height()))
        self.game_screen.blit(self.imgHand1, [0, 0])
        if self.screen_buffer <= self.marble_game_timer - 10:
            self.game_screen.blit(self.imgBGbase, [0, 0])
            self.imgHand3 = pygame.transform.scale(self.imgHand3,(self.game_screen.get_width(), self.game_screen.get_height()))
            self.game_screen.blit(self.imgHand3, [0, 0])
            if self.screen_buffer <= self.marble_game_timer - 15:
                self.game_screen.blit(self.imgBGbase, [0, 0])
                self.imgHand4 = pygame.transform.scale(self.imgHand4,(self.game_screen.get_width(), self.game_screen.get_height()))
                if self.fail_eff > 0:
                    self.fail_eff_x = random.randint(-10, 10)
                    self.fail_eff = self.fail_eff - 1
                self.game_screen.blit(self.imgHand4, [self.fail_eff_x, 0])
                if self.screen_buffer <= self.marble_game_timer - 35:
                    self.game_screen.blit(self.imgBGbase, [0, 0])
                    self.game_screen.blit(self.imgHand4, [0, 0])
                    if self.screen_buffer <= self.marble_game_timer - 40:
                        self.imgStart = pygame.transform.scale(self.imgStart,(self.game_screen.get_width(),self.game_screen.get_height()))
                        self.game_screen.blit(self.imgStart, [0, 0])
                        if self.screen_buffer <= self.marble_game_timer - 50:
                            game_over_timer = GameOverTimer(60)
                            self.fail_eff = 0
                            self.idx=self.MARBLE_GAME
    def start_marble_game(self):
        #배경 음악 로딩
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
        except:
            print("sound/bgm.mp3 파일이 존재하지 않습니다")
        try:
            marblesound=pygame.mixer.Sound("sound/marblesound.mp3")
            marblesound2=pygame.mixer.Sound("sound/marblesound2.mp3")
            marblesound3=pygame.mixer.Sound("sound/marblesound3.mp3")
            marblesound4=pygame.mixer.Sound("sound/marblesound4.mp3")
            marblesound5=pygame.mixer.Sound("sound/marblesound5.mp3")
        except:
            print("해당 파일이 존재하지 않습니다")

        #게임 루프
        while True:
            self.marble_game_timer+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.VIDEORESIZE:
                    self.game_screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

            key = pygame.key.get_pressed() #모든 키 입력 감지
            if self.idx==self.TITLE: #0은 타이틀 화면
                self.draw_title()
                if key[pygame.K_SPACE] == 1:
                    #game_over_timer = GameOverTimer(60)
                    self.screen_buffer = self.marble_game_timer
                    self.idx = self.MARBLE_GAME_INTRO  # 스페이스키 입력시 1번 화면으로 이동

            if self.idx==self.MARBLE_GAME_INTRO:
                self.fail_eff = 10
                self.draw_hand()
                game_over_timer = GameOverTimer(60)
            if self.idx==self.MARBLE_GAME:
                # 타이머
                left_time = game_over_timer.time_checker()
                self.imgBG=pygame.transform.scale(self.imgBG,(self.game_screen.get_width(),self.game_screen.get_height()))
                self.game_screen.blit(self.imgBG,[0,0])
                self.imgHand5 = pygame.transform.scale(self.imgHand5,(self.game_screen.get_width(), self.game_screen.get_height()))
                if pygame.mixer.music.get_busy() == False: #bgm 재생 정지 상태라면
                    try:
                        pygame.mixer.music.play(-1) #bgm 재생
                    except:
                        pass
                if left_time<=0 :
                    self.marble_game_timer = 0
                    self.screen_buffer = self.marble_game_timer
                    self.idx = self.GAME_OVER
                if key[pygame.K_UP] and self.player_betting < self.player_marbles and self.player_betting<self.computer_marbles: self.player_betting += 1
                if key[pygame.K_DOWN] and self.player_betting > 0: self.player_betting -= 1
                if self.betting_button_pressed == True and self.computer_marbles > 1:
                    if self.computer_marbles>6:
                        self.computer_betting=random.randint(1,2+self.marble_game_level)
                    else :self.computer_betting = random.randint(1,self.computer_marbles)
                    self.player_betting = 1
                    self.betting_button_pressed = False
                elif self.betting_button_pressed == True and self.computer_marbles ==1:
                    self.computer_betting = 1
                    self.player_betting = 1
                    self.betting_button_pressed = False
                if key[pygame.K_LEFT]: #홀 버튼 누름&배팅
                    if self.computer_betting % 2 == 0: #컴퓨터 배팅이 짝이면
                        self.betting_success = False
                        self.player_marbles -= self.player_betting
                        self.computer_marbles += self.player_betting
                    else:
                        self.betting_success = True
                        self.player_marbles += self.player_betting
                        self.computer_marbles -= self.player_betting
                        self.score+=self.player_betting
                    self.screen_buffer = self.marble_game_timer
                    self.idx = self.TRUE_FALSE
                    self.fail_eff = 5
                    self.betting_button_pressed = True
                    if self.player_marbles == 1:
                        if random.randint(0, 99) < 40 - self.marble_game_level * 5: #40%확률로 깐부 발동
                            self.score += 10
                            self.idx = self.GGANBU #6

                if key[pygame.K_RIGHT]:
                    if self.computer_betting % 2 == 1:
                        self.betting_success = False
                        self.player_marbles -= self.player_betting
                        self.computer_marbles += self.player_betting
                    else:
                        self.betting_success = True
                        self.player_marbles += self.player_betting
                        self.computer_marbles -= self.player_betting
                        self.score += self.player_betting
                    self.screen_buffer = self.marble_game_timer
                    self.idx = self.TRUE_FALSE
                    self.fail_eff=5
                    self.betting_button_pressed = True
                    if self.player_marbles == 1:
                        if random.randint(0, 99) < 40 - self.marble_game_level * 5: #40%확률로 깐부 발동
                            self.score+=10
                            self.idx = self.GGANBU
                if key[pygame.K_RETURN]:
                    self.fail_eff=5
                    if self.hint>0:
                        if self.computer_betting == 2:  # 구슬이 2개일 때 1번 부딪치는 소리 재생
                            marblesound.play()
                        elif self.computer_betting == 3:
                            marblesound2.play()
                        elif self.computer_betting == 4:
                            marblesound3.play()
                        elif self.computer_betting == 5:
                            marblesound4.play()
                        elif self.computer_betting == 6:
                            marblesound5.play()
                        self.hint-=1
                if self.fail_eff > 0:
                    self.fail_eff_x = random.randint(-10, 10)
                    self.fail_eff = self.fail_eff - 1
                self.game_screen.blit(self.imgHand5, [self.fail_eff_x, 0])


                if left_time>=30:
                    message_to_screen_left(self.game_screen, str(left_time), WHITE, korean_font,
                                           self.game_screen.get_width() / 2.05, self.game_screen.get_height() / 20, self.ref_w,
                                           self.ref_h)
                else:
                    message_to_screen_left(self.game_screen, str(left_time), RED, korean_font,
                                           self.game_screen.get_width() / 2.05, self.game_screen.get_height() / 20,
                                           self.ref_w,
                                           self.ref_h)
                message_to_screen_left(self.game_screen, "구슬 개수 : " + str(self.player_marbles), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 10, self.game_screen.get_height() / 17, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "상대 구슬 개수 : " + str(self.computer_marbles), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 1.2, self.game_screen.get_height() / 40, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "배팅 : "+str(self.player_betting), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 1.25, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "SCORE : " + str(self.score), WHITE, korean_font_small_size,
                                       self.game_screen.get_width() / 10, self.game_screen.get_height() / 40, self.ref_w,
                                       self.ref_h)
                message_to_screen_left(self.game_screen, "남은 힌트 : " + str(self.hint), WHITE,korean_font_small_size,
                                       self.game_screen.get_width() / 1.2, self.game_screen.get_height() /17,self.ref_w,self.ref_h)
                '''
                message_to_screen_left(self.game_screen, "컴퓨터 배팅 test : " + str(self.computer_betting), WHITE, korean_font,
                                       self.game_screen.get_width() / 2, self.game_screen.get_height() / 7, self.ref_w,
                                       self.ref_h)
                '''
            if self.idx == self.LEVEL_UP:
                self.level_up(left_time)
                game_over_timer.__init__(60)
            if self.idx == self.CLEAR: #클리어 화면
                self.draw_clear()
                game_over_timer.__init__(60)
                if key[pygame.K_RETURN] == 1: #엔터 또는 return 키가 눌리면
                    self.reset_variable()
            if self.idx == self.GAME_OVER: #게임 오버 화면
                self.draw_game_over()
                if key[pygame.K_RETURN] == 1:
                    game_over_timer.__init__(60)
                    self.score = 0
                    self.reset_variable()
            if self.idx == self.TRUE_FALSE: # 홀짝 판정 화면으로
                self.draw_true_false()
            if self.idx == self.GGANBU:
                self.draw_gganbu()
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    pygame.init()
    new_game = MarbleGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.start_marble_game()

    pygame.quit()
    quit()


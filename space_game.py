import pygame
import sys
import time
import os

pygame.init()

screen_width = 1600
screen_height = int(screen_width*9/16)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("우주게임")

# 초당 프레임 설정
clock = pygame.time.Clock()
FPS = 60

# 글 폰트
font = pygame.font.SysFont("malgungothic", 30)
loading_font = pygame.font.SysFont("malgungothic", 50)
game_over_font = pygame.font.SysFont("malgungothic", 130, bold=True)
game_clear_font = pygame.font.SysFont("malgungothic", 130, bold=True)
last_font = pygame.font.SysFont("malgungothic", 70)
# 점
dot_count = 1
dot_timer = 0

# 플레이어 액션
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# 상태창 설정
food = 10
fuel = 100.0
day = 1

# 우주선 속도
speed = 10
# 우주선 오브젝트 생성
x = 1
y = 900
scale = 0.2
# ?? #
base_path = os.path.dirname(__file__)
img_path = os.path.join(base_path, "space_ship.png")
img = pygame.image.load(img_path)
# ?? #
img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
rect = img.get_rect()    # 이미지 위치
rect.center = (x, y)

# 화성 생성 & 화성에서의 시간 & 화성탐사횟수
mars_rect = pygame.Rect(700, 700, 75, 75)
mars_time = 0
mars_count = 0
# 목성 생성 & 목성에서의 시간 % 목성탐사횟수
jupiter_rect = pygame.Rect(300, 200, 175, 175)
jupiter_time = 0
jupiter_count = 0
# 토성 생성 & 토성에서의 시간 % 토성탐사횟수
saturn_rect = pygame.Rect(1200, 600, 150, 150)
saturn_time = 0
saturn_count = 0
# 천왕성 생성 & 천왕성에서의 시간 % 천왕성탐사횟수
uranus_rect = pygame.Rect(900, 100, 100, 100)
uranus_time = 0
uranus_count = 0
# 해왕성(클리어) 생성 & 해왕성에서의 시간 % 해왕성탐사횟수
neptune_rect = pygame.Rect(1400, 75, 100, 100)
neptune_time = 0
neptune_count = 0

# 탐험 완료 후 텍스트
reward_text = ""
reward_time = 0

# 플레이 장소
game_stage = "lobby"

# 로비 버튼
start_button = pygame.Rect(screen_width // 2 - 180, 350, 360, 90)
explain_button = pygame.Rect(screen_width // 2 - 180, 480, 360, 90)
back_button = pygame.Rect(screen_width - 260, screen_height - 110, 220, 70)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

running = True
while running:
    clock.tick(FPS)    # 초당 프레임 설정

    for event in pygame.event.get():
        # 게임 종료
        if event.type == pygame.QUIT:
            running = False
        # 마우스 작동
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_stage == "lobby":
                if start_button.collidepoint(event.pos):
                    game_stage = "space"
                    # 타이머 초기화
                    food_timer = pygame.time.get_ticks()
                    day_time = pygame.time.get_ticks()
                    
                if explain_button.collidepoint(event.pos):
                    game_stage = "explain"

            elif game_stage == "explain":
                if back_button.collidepoint(event.pos):
                    game_stage = "lobby"
        # 키보드 작동(누르기)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                running = False
        # 키보드 작동(떼기)
        if food > 0 and fuel > 0:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False

        # 이미지 생성을 위한 좌표. 나중에 없애야함.
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)

    # 회전 이미지 생성
    angle = 0
    if moving_up and moving_left:    # 대각선이 wasd보다 밑에있으면 wasd의 조건 또한 충족시키므로 더 위에 적어서 우선순위 변경
        angle = 0
    elif moving_down and moving_left:
        angle = 90
    elif moving_down and moving_right:
        angle = 180
    elif moving_up and moving_right:   
        angle = 270
    elif moving_left:
        angle = 45
    elif moving_down:
        angle = 135
    elif moving_right:                 
        angle = 225
    elif moving_up:                    
        angle = 315

    # 우주선 무빙
    if game_stage == "space":
        if food > 0 and fuel > 0:
            if moving_left:
                rect.x -= speed
                fuel -= 0.1
                now_time = pygame.time.get_ticks()
                if now_time - food_timer > 4000:
                    food -= 2
                    food_timer = now_time
            if moving_right:
                rect.x += speed
                fuel -= 0.1
                now_time = pygame.time.get_ticks()
                if now_time - food_timer > 4000:
                    food -= 2
                    food_timer = now_time
            if moving_up:
                rect.y -= speed
                fuel -= 0.1
                now_time = pygame.time.get_ticks()
                if now_time - food_timer > 4000:
                    food -= 2
                    food_timer = now_time
            if moving_down:
                rect.y += speed
                fuel -= 0.1
                now_time = pygame.time.get_ticks()
                if now_time - food_timer > 4000:
                    food -= 2
                    food_timer = now_time

    # 게임창 경계 넘는지 안넘는지 판단
    if rect.left < 0:
        rect.left = 0
    if rect.right > screen_width:
        rect.right = screen_width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > screen_height:
        rect.bottom = screen_height

    if game_stage == "space":
        now_time = pygame.time.get_ticks()
        if now_time - day_time > 5000:
            day += 1
            day_time = now_time

    # 화성 접촉 및 상태
    if game_stage == "space" and rect.colliderect(mars_rect):
        game_stage = "mars"
        mars_time = pygame.time.get_ticks()
    if game_stage == "mars":
        now_time = pygame.time.get_ticks()
        if now_time - mars_time > 5000:
            rect.center = (1, 900)
            game_stage = "space"
            mars_count += 1
            fuel += 12
            speed += 1
            food += 2
            reward_text = "식량 2개와 연료 12L를 얻었다!"
            reward_time = pygame.time.get_ticks()
        if now_time - dot_timer > 500:  # ... 변화
            dot_timer = now_time
            dot_count += 1
        if dot_count > 4:
            dot_count = 1
    # 목성 접촉 및 상태
    if game_stage == "space" and rect.colliderect(jupiter_rect):
        game_stage = "jupiter"
        jupiter_time = pygame.time.get_ticks()
    if game_stage == "jupiter":
        now_time = pygame.time.get_ticks()
        if now_time - jupiter_time > 5000:
            rect.center = (1, 900)
            game_stage = "space"
            jupiter_count += 1
            fuel += 17
            speed += 1.5
            food += 3
            reward_text = "식량 3개와 연료 17L를 얻었다!"
            reward_time = pygame.time.get_ticks()
        if now_time - dot_timer > 500:  # ... 변화
            dot_timer = now_time
            dot_count += 1
        if dot_count > 4:
            dot_count = 1
    # 토성 접촉 및 상태
    if game_stage == "space" and rect.colliderect(saturn_rect):
        game_stage = "saturn"
        saturn_time = pygame.time.get_ticks()
    if game_stage == "saturn":
        now_time = pygame.time.get_ticks()
        if now_time - saturn_time > 5000:
            rect.center = (1, 900)
            game_stage = "space"
            saturn_count += 1
            fuel += 25
            speed += 2.5
            food += 5
            reward_text = "식량 5개와 연료 25L를 얻었다!"
            reward_time = pygame.time.get_ticks()
        if now_time - dot_timer > 500:  # ... 변화
            dot_timer = now_time
            dot_count += 1
        if dot_count > 4:
            dot_count = 1
    # 천왕성 접촉 및 상태
    if game_stage == "space" and rect.colliderect(uranus_rect):
        game_stage = "uranus"
        uranus_time = pygame.time.get_ticks()
    if game_stage == "uranus":
        now_time = pygame.time.get_ticks()
        if now_time - uranus_time > 5000:
            rect.center = (1, 900)
            game_stage = "space"
            uranus_count += 1
            fuel += 20
            speed += 2
            food += 4
            reward_text = "식량 4개와 연료 20L를 얻었다!"
            reward_time = pygame.time.get_ticks()
        if now_time - dot_timer > 500:  # ... 변화
            dot_timer = now_time
            dot_count += 1
        if dot_count > 4:
            dot_count = 1
    # 해왕성 접촉 및 상태
    if game_stage == "space" and rect.colliderect(neptune_rect):
        game_stage = "neptune"
        neptune_time = pygame.time.get_ticks() 
    if game_stage == "neptune":
        now_time = pygame.time.get_ticks()
        # if now_time - neptune_time > 5000:
        game_stage = "clear"
    
    if food < 0:
        food = 0
    if fuel < 0:
        fuel = 0
    if game_stage == "space" and (food <= 0 or fuel <= 0):
        game_stage = "game_over"
        moving_left = False
        moving_right = False
        moving_up = False
        moving_down = False

    #게임 클리어 화면 출력
    elif game_stage == "clear":
        screen.fill((0, 0, 0))
        # 탐사 횟수 계산
        total_explore = mars_count + jupiter_count + saturn_count + uranus_count + neptune_count
        # 점수 계산
        if total_explore == 0 or day == 0:
            score = 0
        else:
            score = (food * fuel) / (total_explore * day)

        # 제목
        clear_title = game_clear_font.render("게임 클리어!", True, (255,255,10))
        # 결과 표시
        food_result = last_font.render(f"남은 식량 : {food}", True, (255,255,255))
        fuel_result = last_font.render(f"남은 연료 : {fuel:.1f}", True, (255,255,255))
        explore_result = last_font.render(f"총 탐사 횟수 : {total_explore}", True, (255,255,255))
        day_result = last_font.render(f"보낸 일 수 : {day}", True, (255,255,255))
        score_result = game_clear_font.render(f"총 점수 : {score:.2f}", True, (255,255,0))

        # 제목
        clear_title_rect = clear_title.get_rect(center=(screen_width // 2, 130))
        # 결과
        food_result_rect = food_result.get_rect(center=(screen_width // 2, 300))
        fuel_result_rect = fuel_result.get_rect(center=(screen_width // 2, 380))
        explore_result_rect = explore_result.get_rect(center=(screen_width // 2, 460))
        day_result_rect = day_result.get_rect(center=(screen_width // 2, 540))
        # 점수
        score_result_rect = score_result.get_rect(center=(screen_width // 2, 700))

        screen.blit(clear_title, clear_title_rect)
        screen.blit(food_result, food_result_rect)
        screen.blit(fuel_result, fuel_result_rect)
        screen.blit(explore_result, explore_result_rect)
        screen.blit(day_result, day_result_rect)
        screen.blit(score_result, score_result_rect)

        # 종료 안내
        exit_text = font.render("ESC를 누르면 종료할 수 있습니다.",True, (255,255,255))
        exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height - 40))
        screen.blit(exit_text, exit_rect)

    # 게임 오버 화면 출력
    elif game_stage == "game_over":
        screen.fill((0, 0, 0))

        game_over_title = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_title.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(game_over_title, game_over_rect)

        if food <= 0:
            reason_text = last_font.render("식량이 부족합니다.",True,(255, 0, 0))
            reason_rect = reason_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(reason_text, reason_rect)
        
        elif fuel <= 0:
            reason_text = last_font.render("연료가 부족합니다.",True,(255, 0, 0))
            reason_rect = reason_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(reason_text, reason_rect)

        exit_text = font.render("ESC를 누르면 종료할 수 있습니다.",True,(255, 255, 255))
        exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(exit_text, exit_rect)

    # 화면 내 이미지 저장 및 생성
    rotated_img = pygame.transform.rotate(img, angle)
    rotated_rect = rotated_img.get_rect(center=rect.center)

    # 로비 그리기
    if game_stage == "lobby":
        screen.fill((0, 0, 0))

        title = game_clear_font.render("우주 탐사 게임", True, (255, 255, 0))
        title_rect = title.get_rect(center=(screen_width // 2, 180))
        screen.blit(title, title_rect)

        pygame.draw.rect(screen, (255, 220, 0), start_button, border_radius=20)
        pygame.draw.rect(screen, (255, 220, 0), explain_button, border_radius=20)

        start_text = loading_font.render("시작", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        explain_text = loading_font.render("설명", True, (0, 0, 0))
        explain_text_rect = explain_text.get_rect(center=explain_button.center)
        screen.blit(explain_text, explain_text_rect)

    #설명창 그리기
    elif game_stage == "explain":
        screen.fill((0, 0, 0))

        explain_title = loading_font.render("게임 설명", True, (255, 255, 0))
        explain_title_rect = explain_title.get_rect(center=(screen_width // 2, 100))
        screen.blit(explain_title, explain_title_rect)

        #설명
        explain_lines = [
            "목표 : 해왕성에 도착하여 게임을 클리어하세요.",
            "",
            "조작법",
            "W A S D : 이동",
            "ESC : 게임 종료",
            "",
            "식량과 연료를 관리하며 탐사하세요.",
            "식량 또는 연료가 0이 되면 게임 오버입니다."
        ]
        # 설명 리스트를 한줄씩 내려가며 반복
        y = 180
        for line in explain_lines:
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (100, y))
            y += 40

        pygame.draw.rect(screen, (255, 220, 0), back_button, border_radius=15)

        back_text = font.render("돌아가기", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        # 플레이 장소
    elif game_stage == "space":
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (180, 60, 40), mars_rect.center, 50)
        screen.blit(rotated_img, rotated_rect)
         # 화성 생성
        pygame.draw.circle(screen, (180, 60, 40), mars_rect.center, 50)
        mars_text = font.render("화성", True, (255,255,255))
        mars_text_rect = mars_text.get_rect(center=mars_rect.center)
        screen.blit(mars_text, mars_text_rect)
        # 목성 생성
        pygame.draw.circle(screen, (180, 60, 40), jupiter_rect.center, 150)
        jupiter_text = font.render("목성", True, (255,255,255))
        jupiter_text_rect = jupiter_text.get_rect(center=jupiter_rect.center)
        screen.blit(jupiter_text, jupiter_text_rect)
        # 토성 생성
        pygame.draw.circle(screen, (180, 60, 40), saturn_rect.center, 125)
        saturn_text = font.render("토성", True, (255,255,255))
        saturn_text_rect = saturn_text.get_rect(center=saturn_rect.center)
        screen.blit(saturn_text, saturn_text_rect)
        # 천왕성 생성
        pygame.draw.circle(screen, (180, 60, 40), uranus_rect.center, 75)
        uranus_text = font.render("천왕성", True, (255,255,255))
        uranus_text_rect = uranus_text.get_rect(center=uranus_rect.center)
        screen.blit(uranus_text, uranus_text_rect)
        # 해왕성 생성
        pygame.draw.circle(screen, (180, 60, 40), neptune_rect.center, 75)
        neptune_text = font.render("해왕성", True, (255,255,255))
        neptune_text_rect = neptune_text.get_rect(center=neptune_rect.center)
        screen.blit(neptune_text, neptune_text_rect)
        # 보상 획득 텍스트
        if pygame.time.get_ticks() - reward_time < 3000:
            reward_surface = font.render(reward_text,True,(255,255,255))
            reward_rect = reward_surface.get_rect(center=(500, 25))
            screen.blit(reward_surface, reward_rect)

        # 화성
    elif game_stage == "mars":
        screen.fill((50, 20, 20))

        mars_title = loading_font.render("화성 도착!", True, (255,255,255))
        mars_title_rect = mars_title.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

        exploring_text = "탐험중" + "." * dot_count
        exploring = loading_font.render(exploring_text, True, (255,255,255))
        exploring_rect = exploring.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        screen.blit(mars_title, mars_title_rect)
        screen.blit(exploring, exploring_rect)

    # 목성
    elif game_stage == "jupiter":
        screen.fill((50, 20, 20))

        jupiter_title = loading_font.render("목성 도착!", True, (255,255,255))
        jupiter_title_rect = jupiter_title.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

        exploring_text = "탐험중" + "." * dot_count
        exploring = loading_font.render(exploring_text, True, (255,255,255))
        exploring_rect = exploring.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        screen.blit(jupiter_title, jupiter_title_rect)
        screen.blit(exploring, exploring_rect)

    # 토성
    elif game_stage == "saturn":
        screen.fill((50, 20, 20))

        saturn_title = loading_font.render("토성 도착!", True, (255,255,255))
        saturn_title_rect = saturn_title.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

        exploring_text = "탐험중" + "." * dot_count
        exploring = loading_font.render(exploring_text, True, (255,255,255))
        exploring_rect = exploring.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        screen.blit(saturn_title, saturn_title_rect)
        screen.blit(exploring, exploring_rect)

    # 천왕성
    elif game_stage == "uranus":
        screen.fill((50, 20, 20))

        uranus_title = loading_font.render("천왕성 도착!", True, (255,255,255))
        uranus_title_rect = uranus_title.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

        exploring_text = "탐험중" + "." * dot_count
        exploring = loading_font.render(exploring_text, True, (255,255,255))
        exploring_rect = exploring.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        screen.blit(uranus_title, uranus_title_rect)
        screen.blit(exploring, exploring_rect)

    # # 해왕성
    # elif game_stage == "neptune":
    #     screen.fill((50, 20, 20))

    #     neptune_title = loading_font.render("해왕성 도착!", True, (255,255,255))
    #     neptune_title_rect = neptune_title.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

    #     exploring_text = "탐험중" + "." * dot_count
    #     exploring = loading_font.render(exploring_text, True, (255,255,255))
    #     exploring_rect = exploring.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    #     screen.blit(neptune_title, neptune_title_rect)
    #     screen.blit(exploring, exploring_rect)

    # 기본 화면 글자 생성
    if game_stage != "clear" and game_stage != "game_over" and game_stage != "lobby" and game_stage != "explain":
        food_text = font.render(f"식량 : {food}", True, (255,255,255))
        screen.blit(food_text, (20,20))
        fuel_text = font.render(f"연료 : {fuel:.1f}", True, (255,255,255))    # 소수점 1자리수까지만 출력
        screen.blit(fuel_text, (20,60))
        speed_text = font.render(f"속도 : {speed:.1f}", True, (255,255,255))    # 소수점 1자리수까지만 출력
        screen.blit(speed_text, (20,100))
        day_text = font.render(f"일 : {day}", True, (255,255,255))    # 소수점 1자리수까지만 출력
        screen.blit(day_text, (20,140))

    pygame.display.update()    # 화면 업데이트
    
pygame.quit()

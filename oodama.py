import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("大玉転がしゲーム")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)      
PURPLE = (128, 0, 128)   
PINK = (255, 192, 203)  
YELLOW = (255, 255, 0)     

OBSTACLE_COLORS = [ORANGE, GREEN, PURPLE, PINK, YELLOW]

# ボールの設定
class Ball:
    def __init__(self):
        self.radius = 30
        self.x = SCREEN_WIDTH // 6
        self.y = SCREEN_HEIGHT - self.radius
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 0.5
        self.friction = 0.98
        self.can_jump = True  # ジャンプ可能かを判定
        

    def move(self):
        self.speed_y += self.acceleration
        
        self.x += self.speed_x
        self.y += self.speed_y
        
        self.speed_x *= self.friction
        self.speed_y *= self.friction

        if self.y + self.radius > SCREEN_HEIGHT:
            self.can_jump = True
        
        # 画面端での挙動
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -0.7
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.speed_x *= -0.7
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.speed_y *= -0.7
        elif self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.speed_y *= -0.7

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# ゴールの設定
class Goal:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = SCREEN_WIDTH - 150
        self.y = SCREEN_HEIGHT - self.height
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
    
    def check_collision(self, ball):
        return (ball.x > self.x and 
                ball.x < self.x + self.width and 
                ball.y + ball.radius > self.y)

# 障害物の設定
class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = random.choice(OBSTACLE_COLORS)
        self.original_y = y  # 初期座標を記憶しておく
        self.original_x = x  # 初期座標を記憶しておく
        self.move_speed = 3  
        self.moving_up = True  
        self.original_width = width
        self.original_height = height
        self.size_change_speed = 2
        self.growing = True
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    
    
    def handle_collision(self, ball):
        # 左からの衝突
        if ball.speed_x > 0 and ball.x + ball.radius >= self.x and ball.x < self.x:
            ball.x = self.x - ball.radius
            ball.speed_x *= -0.7
        # 右からの衝突
        elif ball.speed_x < 0 and ball.x - ball.radius <= self.x + self.width and ball.x > self.x + self.width:
            ball.x = self.x + self.width + ball.radius
            ball.speed_x *= -0.7
        # 上からの衝突
        if ball.speed_y > 0 and ball.y + ball.radius >= self.y and ball.y < self.y:
            ball.y = self.y - ball.radius
            ball.speed_y *= -0.7
            ball.can_jump = True  
        # 下からの衝突
        elif ball.speed_y < 0 and ball.y - ball.radius <= self.y + self.height and ball.y > self.y + self.height:
            ball.y = self.y + self.height + ball.radius
            ball.speed_y *= -0.7

    def update(self):
        #緑
        if self.color == GREEN:
            if self.moving_up:
                self.y -= self.move_speed
                if self.y < self.original_y - 150: 
                    self.moving_up = False
            else:
                self.y += self.move_speed
                if self.y > self.original_y + 30:
                    self.moving_up = True
        #紫
        elif self.color == PURPLE:
            if self.moving_up:  
                self.x -= self.move_speed
                if self.x < self.original_x - 100:
                    self.moving_up = False
            else:
                self.x += self.move_speed
                if self.x > self.original_x + 100:
                    self.moving_up = True
        #オレンジ
        elif self.color == ORANGE:
            if self.growing:
                self.width += self.size_change_speed
                self.height += self.size_change_speed
                self.x -= self.size_change_speed / 2
                self.y -= self.size_change_speed / 2
                
                if self.width > self.original_width * 1.5:
                    self.growing = False
            else:
                self.width -= self.size_change_speed
                self.height -= self.size_change_speed
                self.x += self.size_change_speed / 2
                self.y += self.size_change_speed / 2
            
            if self.width < self.original_width * 0.5:
                self.growing = True
        #黄色

    def check_collision(self, ball):
        if (ball.x + ball.radius > self.x and 
            ball.x - ball.radius < self.x + self.width and 
            ball.y + ball.radius > self.y and 
            ball.y - ball.radius < self.y + self.height):
            self.handle_collision(ball)
            return True
        return False


def create_stage_obstacles(stage_num):
    obstacles.clear()
    num_obstacles = min(stage_num, 8)
    
    for _ in range(num_obstacles):
        width = random.randint(30, 100)
        height = random.randint(100, 200)

        base_distance = random.randint(-20, 180) 

        x = random.randint(width, SCREEN_WIDTH - width - 150)
        y = SCREEN_HEIGHT - height - base_distance
        
        obstacles.append(Obstacle(x, y, width, height))

# 表示
ball = Ball()
goal = Goal()
stage = 0
font = pygame.font.Font(None, 36)
obstacles = [] 

# ゲームループ
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_r:  # Rキーが押されたとき
                ball = Ball()
                create_stage_obstacles(stage)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if reset_rect.inflate(20, 10).collidepoint(mouse_pos):
                ball = Ball()
                create_stage_obstacles(stage)
    
    # キー入力処理
    keys = pygame.key.get_pressed()
    move_speed = 0.3 if ball.can_jump else 0.1 
    if keys[pygame.K_LEFT]:
        ball.speed_x -= move_speed
    if keys[pygame.K_RIGHT]:
        ball.speed_x += move_speed
    if keys[pygame.K_SPACE] and ball.can_jump: 
        ball.speed_y = -16  
        ball.can_jump = False  
    
    ball.move()

    # 障害物との衝突判定
    for obstacle in obstacles:
        obstacle.check_collision(ball) 
    
    # ゴールとの衝突判定
    if goal.check_collision(ball):
        stage += 1
        ball = Ball()
        create_stage_obstacles(stage) 

    for obstacle in obstacles:
        obstacle.update() 
    
    # 画面描画
    screen.fill(WHITE)
    for obstacle in obstacles:
        obstacle.draw()
    ball.draw()
    goal.draw()
    stage_text = font.render(f"Stage: {stage}", True, (0, 0, 0))

    reset_text = font.render("Reset Stage (R)", True, (0, 0, 0))
    reset_rect = reset_text.get_rect()
    reset_rect.topright = (SCREEN_WIDTH - 10, 10)  
    screen.blit(reset_text, reset_rect)
    pygame.draw.rect(screen, (220, 220, 220), reset_rect.inflate(20, 10)) 
    screen.blit(reset_text, reset_rect)  

    screen.blit(stage_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
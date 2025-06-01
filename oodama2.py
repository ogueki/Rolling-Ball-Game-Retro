import pyxel
import random
import pygame

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
WORLD_WIDTH = 640  

class Ball:
    def __init__(self):
        self.radius = 8
        self.x = 20
        self.y = 100
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 0.3
        self.friction = 0.98
        self.can_jump = True
        self.anim_frame = 0
        self.anim_timer = 0

    def move(self):
        self.speed_y += self.acceleration
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_x *= self.friction
        self.speed_y *= self.friction

        if abs(self.speed_x) > 0.05:
            self.anim_timer += 1
            if self.anim_timer > 3:
                self.anim_frame = (self.anim_frame + 1) % 4
                self.anim_timer = 0

        if self.y + self.radius > SCREEN_HEIGHT:
            self.can_jump = True

        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x *= -0.7
        elif self.x + self.radius > WORLD_WIDTH:
            self.x = WORLD_WIDTH - self.radius
            self.speed_x *= -0.7

        if self.y - self.radius < 0:
            self.y = self.radius
            self.speed_y *= -0.7
        elif self.y + self.radius > 104:
            self.y = 104 - self.radius
            self.speed_y *= -0.7
            self.can_jump = True

    def draw(self, cam_x):
        u = self.anim_frame * 16
        pyxel.blt(int(self.x - 8 - cam_x), int(self.y - 8), 0, u, 0, 16, 16, 0)

class Goal:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.x = WORLD_WIDTH - 40
        self.y = 88

    def draw(self, cam_x):
        pyxel.blt(int(self.x - cam_x), int(self.y), 0, 0, 16, self.width, self.height, 0)

    def check_collision(self, ball):
        return (
            ball.x > self.x and 
            ball.x < self.x + self.width and 
            ball.y + ball.radius > self.y
        )

class Obstacle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.original_x = x
        self.original_y = y
        self.move_speed = 1
        self.moving_positive = True

    def draw(self, cam_x):
        pyxel.rect(self.x - cam_x, self.y, self.width, self.height, self.color)

    def update(self):
        if self.color in [10, 11]:
            if self.moving_positive:
                self.y -= self.move_speed
                if self.y < self.original_y - 20:
                    self.moving_positive = False
            else:
                self.y += self.move_speed
                if self.y > self.original_y + 20:
                    self.moving_positive = True
        elif self.color in [5, 13]:
            if self.moving_positive:
                self.x -= self.move_speed
                if self.x < self.original_x - 20:
                    self.moving_positive = False
            else:
                self.x += self.move_speed
                if self.x > self.original_x + 20:
                    self.moving_positive = True

    def check_collision(self, ball):
        if (ball.x + ball.radius > self.x and 
            ball.x - ball.radius < self.x + self.width and 
            ball.y + ball.radius > self.y and 
            ball.y - ball.radius < self.y + self.height):

            if ball.speed_x > 0 and ball.x < self.x:
                ball.x = self.x - ball.radius
                ball.speed_x *= -0.7
            elif ball.speed_x < 0 and ball.x > self.x + self.width:
                ball.x = self.x + self.width + ball.radius
                ball.speed_x *= -0.7
            if ball.speed_y > 0 and ball.y < self.y:
                ball.y = self.y - ball.radius
                ball.speed_y *= -0.7
                ball.can_jump = True
            elif ball.speed_y < 0 and ball.y > self.y + self.height:
                ball.y = self.y + self.height + ball.radius
                ball.speed_y *= -0.7
            return True
        return False

def create_stage_obstacles(stage_num):
    obstacles = []
    num_obstacles = min(stage_num + 2, 6)
    for _ in range(num_obstacles):
        width = random.randint(10, 20)
        height = random.randint(5, 10)
        x = random.randint(10, WORLD_WIDTH - 30)
        y = random.randint(30, 100)
        color = random.choice([3, 5, 10, 11, 13])
        obstacles.append(Obstacle(x, y, width, height, color))
    return obstacles

class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x -= self.speed
        if self.x < -24:
            self.x = WORLD_WIDTH
            self.y = random.randint(5, 40)

    def draw(self, cam_x):
        pyxel.blt(int(self.x - cam_x), int(self.y), 0, 0, 32, 24, 16, 0)

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="大玉転がし")
        pyxel.load("my_resources.pyxres")
        pyxel.playm(0, loop=True) 

        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound("jump.wav") 
        self.collision_sound = pygame.mixer.Sound("collision.wav") 
        self.jump_sound.set_volume(0.3)
        self.collision_sound.set_volume(0.3)

        self.stage = 1
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.ball = Ball()
        self.goal = Goal()
        self.obstacles = create_stage_obstacles(self.stage)
        self.clouds = [Cloud(random.randint(0, 640), random.randint(5, 40), random.uniform(0.2, 0.6)) for _ in range(8)]

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ball.speed_x -= 0.2 if self.ball.can_jump else 0.1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ball.speed_x += 0.2 if self.ball.can_jump else 0.1
        if pyxel.btnp(pyxel.KEY_SPACE) and self.ball.can_jump:
            self.ball.speed_y = -4
            self.ball.can_jump = False
            self.jump_sound.play()

        self.ball.move()

        for obs in self.obstacles:
            obs.update()
            if obs.check_collision(self.ball):
                self.collision_sound.play()

        for cloud in self.clouds:
            cloud.update()

        if self.goal.check_collision(self.ball):
            self.stage += 1
            self.reset()

        self.camera_x = max(0, min(int(self.ball.x - SCREEN_WIDTH // 2), WORLD_WIDTH - SCREEN_WIDTH))

    def draw(self):
        pyxel.cls(12)
        pyxel.blt(130, 10, 0, 0, 48, 16, 16, 0)

        for cloud in self.clouds:
            cloud.draw(self.camera_x)

        # 地面
        for x in range(0, WORLD_WIDTH, 16):
            pyxel.blt(x - self.camera_x, 104, 1, 0, 0, 16, 16, 0)

        # プレイヤー・障害物・ゴール
        self.ball.draw(self.camera_x)
        self.goal.draw(self.camera_x)
        for obs in self.obstacles:
            obs.draw(self.camera_x)

        # ステージ情報
        pyxel.text(5, 5, f"Stage: {self.stage}", 0)

Game()

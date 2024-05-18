import math
import pygame

# Constants
MAP_WIDTH = 16
MAP_HEIGHT = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOV = math.pi / 4
DEPTH = 16.0
SPEED = 0.25
PROJECTILE_SPEED = 0.2

world_map = [
    "################",
    "#..............#",
    "#.......########",
    "#..............#",
    "#.......##.....#",
    "#.......##.....#",
    "#..............#",
    "###............#",
    "##.............#",
    "#......####..###",
    "#......#.......#",
    "#......#.......#",
    "#..............#",
    "#......#########",
    "#..............#",
    "################",
]

# Player
player_x = 8.0
player_y = 10.0
player_angle = 0.0
projectiles = []


class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self):
        self.x += math.sin(self.angle) * PROJECTILE_SPEED
        self.y += math.cos(self.angle) * PROJECTILE_SPEED

    def is_colliding(self):
        if world_map[int(self.y)][int(self.x)] == "#":
            return True
        return False


def cast_rays(screen):
    global projectiles

    for x in range(SCREEN_WIDTH):
        ray_angle = (player_angle - FOV / 2.0) + (x / SCREEN_WIDTH) * FOV
        distance_to_wall = 0.0
        hit_wall = False
        boundary = False

        eye_x = math.sin(ray_angle)
        eye_y = math.cos(ray_angle)

        while not hit_wall and distance_to_wall < DEPTH:
            distance_to_wall += 0.1
            test_x = int(player_x + eye_x * distance_to_wall)
            test_y = int(player_y + eye_y * distance_to_wall)

            if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                hit_wall = True
                distance_to_wall = DEPTH
            else:
                if world_map[test_y][test_x] == "#":
                    hit_wall = True
                    boundary = True  # Simple boundary check

        ceiling = int(SCREEN_HEIGHT / 2.0 - SCREEN_HEIGHT / distance_to_wall)
        floor = SCREEN_HEIGHT - ceiling

        for y in range(SCREEN_HEIGHT):
            if y < ceiling:
                color = (0, 0, 0)  # Sky
            elif y >= ceiling and y < floor:
                shade = 255 if boundary else 255 - int(distance_to_wall * 15)
                color = (shade, 0, 0)  # Wall
            else:
                color = (50, 50, 50)  # Ground

            screen.set_at((x, y), color)

    # Draw projectiles
    for proj in projectiles:
        print(proj.x)
        proj_screen_x = (
            int((proj.x - player_x) / DEPTH * SCREEN_WIDTH / 2) + SCREEN_WIDTH // 2
        )
        proj_screen_y = (
            int((proj.y - player_y) / DEPTH * SCREEN_HEIGHT / 2) + SCREEN_HEIGHT // 2
        )
        if 0 <= proj_screen_x < SCREEN_WIDTH and 0 <= proj_screen_y < SCREEN_HEIGHT:
            screen.set_at((proj_screen_x, proj_screen_y), (255, 0, 0))


def game_loop():
    global player_x, player_y, player_angle, projectiles

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raycaster")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectiles.append(Projectile(player_x, player_y, player_angle))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_x += math.sin(player_angle) * SPEED
            player_y += math.cos(player_angle) * SPEED
            if world_map[int(player_y)][int(player_x)] == "#":
                player_x -= math.sin(player_angle) * SPEED
                player_y -= math.cos(player_angle) * SPEED
        if keys[pygame.K_s]:
            player_x -= math.sin(player_angle) * SPEED
            player_y -= math.cos(player_angle) * SPEED
            if world_map[int(player_y)][int(player_x)] == "#":
                player_x += math.sin(player_angle) * SPEED
                player_y += math.cos(player_angle) * SPEED
        if keys[pygame.K_a]:
            player_angle -= SPEED
        if keys[pygame.K_d]:
            player_angle += SPEED

        # Update projectiles and remove if colliding
        for proj in projectiles:
            proj.update()
            if proj.is_colliding():
                projectiles.remove(proj)

        screen.fill((0, 0, 0))
        cast_rays(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()

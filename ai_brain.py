import random
import math
import pygame

PATROL_SPEED = 0.4
ATTACK_SPEED = 1.2
EVADE_SPEED = 1.6
BULLET_EVADE_DIST = 120
ATTACK_RANGE_X = 200
LOW_HEALTH_THRESHOLD = 1

def distance(a_x, a_y, b_x, b_y):
    return math.sqrt((a_x - b_x)**2 + (a_y - b_y)**2)

def initialize_enemies(num, enemy_path):
    """Creates enemy attributes + default states"""

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    enemy_health = []
    enemy_state = []
    enemy_speed = []

    for i in range(num):
        enemyImg.append(pygame.image.load(enemy_path))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(PATROL_SPEED)
        enemyY_change.append(40)
        enemy_health.append(3)
        enemy_state.append("patrol") 
        enemy_speed.append(PATROL_SPEED)

    return {
        "img": enemyImg,
        "x": enemyX,
        "y": enemyY,
        "x_change": enemyX_change,
        "y_change": enemyY_change,
        "hp": enemy_health,
        "state": enemy_state,
        "speed": enemy_speed
    }

def update_enemy(i, enemies, playerX, playerY, bulletX, bulletY, bullet_state):
    """Updates 1 enemy using ONLY finite-state logic."""

    x = enemies["x"]
    y = enemies["y"]
    x_change = enemies["x_change"]
    y_change = enemies["y_change"]
    hp = enemies["hp"]
    state = enemies["state"]
    speed = enemies["speed"]

    # ---------------------------
    # STATE CHECK & TRANSITIONS
    # ---------------------------
    if state[i] == "dead":
        y[i] = 2000  
        return

    if hp[i] <= 0:
        state[i] = "dead"
        return

    player_dx = abs(playerX - x[i])
    bullet_dist = distance(x[i], y[i], bulletX, bulletY)

    if hp[i] <= LOW_HEALTH_THRESHOLD:
        state[i] = "evade"
        speed[i] = EVADE_SPEED

    elif bullet_state == "fire" and bullet_dist < BULLET_EVADE_DIST:
        state[i] = "evade"
        speed[i] = EVADE_SPEED

    elif player_dx < ATTACK_RANGE_X and playerY > y[i]:
        state[i] = "attack"
        speed[i] = ATTACK_SPEED

    else:
        state[i] = "patrol"
        speed[i] = PATROL_SPEED

    # ---------------------------
    # MOVEMENT PER STATE
    # ---------------------------
    if state[i] == "patrol":
        x[i] += x_change[i]
        if x[i] <= 0:
            x_change[i] = abs(speed[i])
            y[i] += y_change[i]
        elif x[i] >= 736:
            x_change[i] = -abs(speed[i])
            y[i] += y_change[i]

    elif state[i] == "attack":
        if playerX > x[i]:
            x[i] += speed[i]
        else:
            x[i] -= speed[i]

        y[i] += 0.25 * speed[i]

    elif state[i] == "evade":
        if bullet_state == "fire":
            if bulletX > x[i]:
                x[i] -= speed[i] * 1.2
            else:
                x[i] += speed[i] * 1.2

            y[i] -= speed[i] * 0.8
        else:
            if random.random() < 0.5:
                x[i] += speed[i]
            else:
                x[i] -= speed[i]
            y[i] -= 0.2 * speed[i]

    # ---------------------------
    # SCREEN LIMITS
    # ---------------------------
    x[i] = max(0, min(736, x[i]))
    if y[i] > 440:
        y[i] = 440

    return enemies
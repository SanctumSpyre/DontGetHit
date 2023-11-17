

#Imports
import pygame, sys
import random

#Constants
WIDTH, HEIGHT = 1536, 864
TITLE = "Dont Get Hit!"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#Classes
class Parent:
    def __init__(self, x1, y1, x2, y2, level, tier=0,color=(0,0,0)):
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2
        self.level = level
        self.tier = tier
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.x2, self.y2)
    def appear(self):
        pygame.draw.rect(win, self.color, self.rect)
    def update(self):
        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(self.x,self.y, self.x2, self.y2)
class Barrier(Parent):
    def __init__(self, x1, y1, x2, y2, level, blocking_direction):
        super().__init__(x1,y1,x2,y2,level,color=(0,150,60))
        self.block = blocking_direction
class Gate(Parent):
    def __init__(self, x1, y1, x2, y2,level,tier, blocking_direction,binary):
        color =(2,2,2)
        super().__init__(x1,y1,x2,y2,level,tier,(128,128,128))
        self.open = bool(binary)
        self.block = blocking_direction
class Enemy(Parent):
    def __init__(self, x1, y1, x2, y2,level, enemy_speed_x, enemy_speed_y):
        super().__init__(x1,y1,x2,y2,level,color=(8, 143, 143))
        self.velX = enemy_speed_x
        self.velY = enemy_speed_y
class Checkpoint(Parent):
    def __init__(self, x1, y1, x2, y2,level,tier):
        super().__init__(x1,y1,x2,y2,level,tier,color=(128, 0, 128))
class Objective(Parent):
    def __init__(self, x1, y1, x2, y2, level,ToF):
        super().__init__(x1,y1,x2,y2,level,color=(0, 255, 255))
        self.menu_choice = ToF
class Key(Parent):
    def __init__(self, x1,y1,x2,y2,level,tier,ToF):
        super().__init__(x1,y1,x2,y2,level,tier,(255, 255, 0))
        self.obtained = ToF
class Player(Parent):
    def __init__(self, x1,y1,x2,y2,level,tier):
        super().__init__(x1,y1,x2,y2,level,tier,(250, 120, 60))
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2
    def reset(self, spawnpoint_x, spawnpoint_y):
        self.x = spawnpoint_x
        self.y = spawnpoint_y
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        super().update()
objectives = []
barriers = []
gates = []
gates2 = []
enemies = []
enemies2 = []
keys = []
keys2 = []
checkpoints = []
def EntityAppender():
    file = open('general_appendments.txt','r')
    appendments_list = file.readlines()
    file.close()
    for item in appendments_list:
        sl = item.strip().split(',')
        if sl[0][0] == '#':
            continue
        else:
            if sl[0] == 'Objective':
                objectives.append(Objective(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6])))
            if sl[0] == 'Barrier':
                barriers.append(Barrier(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),str(sl[6])))
            if sl[0] == 'Enemy':
                if int(sl[5]) == 1:
                    enemies.append(Enemy(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
                if int(sl[5]) == 2:
                    enemies2.append(Enemy(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
            if sl[0] == 'Gate':
                if int(sl[5]) == 1:
                    gates.append(Gate(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),str(sl[7]),int(sl[8])))
                if int(sl[5]) == 2:
                    gates2.append(Gate(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),str(sl[7]),int(sl[8])))
            if sl[0] == 'Key':
                if int(sl[5]) == 1:
                    keys.append(Key(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
                if int(sl[5]) == 2:
                    keys2.append(Key(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
            if sl[0] == 'Checkpoint':
                checkpoints.append(Checkpoint(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6])))
EntityAppender()
player = Player(WIDTH/2,HEIGHT/2+100,24,24,0,0)
#main menu screen
while player.level == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_w:
                player.up_pressed = True
            if event.key == pygame.K_s:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_s:
                player.down_pressed = False
    win.fill((12, 24, 36))  
    player.appear()
    '''objective section'''
    for objective in objectives:
        if objective.menu_choice == 1:
            objective.appear()
            #this spawns you in each level respective to the tier of the objective
            if pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 1:
                newest_spawn_point_x = 100
                newest_spawn_point_y = HEIGHT-100
                player.reset(newest_spawn_point_x,newest_spawn_point_y)
                player.level = 1
            elif pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 2:
                newest_spawn_point_x = WIDTH-70
                newest_spawn_point_y = 55
                player.reset(newest_spawn_point_x,newest_spawn_point_y)
                player.level = 2
            elif pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 3:
                newest_spawn_point_x = 100
                newest_spawn_point_y = HEIGHT-100
                player.reset(newest_spawn_point_x,newest_spawn_point_y)
                player.level = 3
    player.appear()
    player.update()
    pygame.display.flip()
    clock.tick(120)
################################
#Level 1
while player.level == 1:
    #barrier collison lists
    left_barrier_collision =  []
    right_barrier_collision = []  
    top_barrier_collision =  [] 
    bottom_barrier_collision = []
    #gates collision list
    left_gate_collision =  []
    right_gate_collision = []  
    top_gate_collision =  [] 
    bottom_gate_collision = []
    #enemy collision list
    enemy_collision = []
    #checkpoint collision list
    checkpoint_collision = []
    #key collision list
    key_collision = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_w:
                player.up_pressed = True
            if event.key == pygame.K_s:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_s:
                player.down_pressed = False
    win.fill((12, 24, 36))
    '''barriers section'''
    for barrier in barriers:
        if barrier.level == 1:
            if barrier.block == 'A':
                left_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'D':
                right_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'W':
                top_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'S':
                bottom_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
    for barrier in barriers:
        if barrier.level == 1:
            barrier.appear()
        if any(left_barrier_collision) == True:
            player.left_pressed = False
        if any(right_barrier_collision) == True:
            player.right_pressed = False
        if any(top_barrier_collision) == True:
            player.up_pressed = False
        if any(bottom_barrier_collision) == True:
            player.down_pressed = False
    '''key section'''
    for key in keys:
        if key.level == 1:
            if  pygame.Rect.colliderect(player.rect, key.rect) == True:
                key.obtained = True
            if key.obtained == True:
                continue
            else:
                key.appear()
    '''enemies section'''
    for enemy in enemies:
        if enemy.level == 1:
            enemy.appear()
            enemy_collision.append(pygame.Rect.colliderect(player.rect, enemy.rect))
            if  pygame.Rect.colliderect(player.rect, enemy.rect) == True and enemy.level == 1:
                player.reset(newest_spawn_point_x,newest_spawn_point_y)
                for key in keys:
                    if key.level == 1:
                        if key.tier-1 < player.tier:
                            continue
                        else:
                            key.obtained = False
    #first corridor level 1
    if enemies[0].y == 831:
        for enemy in enemies[0:6]:
            enemy.velY = -enemy.velY
    if enemies[0].y == 708:
        for enemy in enemies[0:6]:
            enemy.velY = -enemy.velY
    #swirly squares section
    if enemies[6].x == 1350 and enemies[6].y == 602:
        for enemy in enemies[6:11]:
            enemy.velX = -2
            enemy.velY = 0
        for enemy in enemies[11:]:
            enemy.velX = 0
            enemy.velY = 2
    if enemies[6].x == 1350 and enemies[6].y == 650:
        for enemy in enemies[6:11]:
            enemy.velX = 0
            enemy.velY = -2
        for enemy in enemies[11:]:
            enemy.velX = 2
            enemy.velY = 0
    if enemies[6].x == 1302 and enemies[6].y == 650:
        for enemy in enemies[6:11]:
            enemy.velX = 2
            enemy.velY = 0
        for enemy in enemies[11:]:
            enemy.velX = 0
            enemy.velY = -2
    if enemies[6].x == 1302 and enemies[6].y == 602:
        for enemy in enemies[6:11]:
            enemy.velX = 0
            enemy.velY = 2
        for enemy in enemies[11:]:
            enemy.velX = -2
            enemy.velY = 0
    for enemy in enemies:
        enemy.update()
    '''checkpoints section'''
    for checkpoint in checkpoints:
        if checkpoint.level == 1:
            checkpoint.appear()
            checkpoint_collision.append(pygame.Rect.colliderect(player.rect, checkpoint.rect))
            if pygame.Rect.colliderect(player.rect, checkpoint.rect) == True:
                newest_spawn_point_x = ((checkpoint.x + checkpoint.x + checkpoint.x2)/2)-12 #centers yourself in checkpoint
                newest_spawn_point_y = ((checkpoint.y + checkpoint.y + checkpoint.y2)/2)-12
                player.tier = checkpoint.tier
    player.appear()
    '''gates section'''
    for gate in gates:
        if gate.level == 1:
            for key in keys:
                if key.level == 1:
                    if key.obtained == True and key.tier == gate.tier:
                       gate.open = True
                    else:
                        gate.appear()
                        gate.open = False
    for gate in gates:
        if gate.level == 1:
            if gate.open == False:
                if gate.block == 'A':
                    left_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'D':
                    right_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'W':
                    top_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'S':
                    bottom_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
    for gate in gates:
        if gate.level == 1:
            if any(left_gate_collision) == True and gate.open == False:
                player.left_pressed = False
            if any(right_gate_collision) == True and gate.open == False:
                player.right_pressed = False
            if any(top_gate_collision) == True and gate.open == False:
                player.up_pressed = False
            if any(bottom_gate_collision) == True and gate.open == False:
                player.down_pressed = False
            '''objective section'''
    for objective in objectives:
        if objective.menu_choice == 0:
            if objective.level == 1:
                objective.appear()
                if pygame.Rect.colliderect(player.rect, objective.rect):
                    newest_spawn_point_x = WIDTH-70
                    newest_spawn_point_y = 55
                    player.reset(newest_spawn_point_x,newest_spawn_point_y)
                    player.tier = 0
                    player.level = 2
    player.appear()
    player.update()
    pygame.display.flip()
    clock.tick(120)
 ##########################
#Level 2
while player.level == 2:
    #barrier collison lists
    left_barrier_collision =  []
    right_barrier_collision = []  
    top_barrier_collision =  [] 
    bottom_barrier_collision = []
    #gates collision list
    left_gate_collision =  []
    right_gate_collision = []  
    top_gate_collision =  [] 
    bottom_gate_collision = []
    #enemy collision list
    enemy_collision = []
    #checkpoint collision list
    checkpoint_collision = []
    #key collision list
    key_collision = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_w:
                player.up_pressed = True
            if event.key == pygame.K_s:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_s:
                player.down_pressed = False
    win.fill((12, 24, 36))  
    '''barriers section'''
    for barrier in barriers:
        if barrier.level == 2:
            if barrier.block == 'A':
                left_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'D':
                right_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'W':
                top_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'S':
                bottom_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
    for barrier in barriers:
        if barrier.level == 2:
            barrier.appear()
        if any(left_barrier_collision) == True:
            player.left_pressed = False
        if any(right_barrier_collision) == True:
            player.right_pressed = False
        if any(top_barrier_collision) == True:
            player.up_pressed = False
        if any(bottom_barrier_collision) == True:
            player.down_pressed = False
    '''key section'''
    for key in keys2:
        if key.level == 2:
            key_collision.append(pygame.Rect.colliderect(player.rect, key.rect))
            if  pygame.Rect.colliderect(player.rect, key.rect) == True:
                key.obtained = True
            if key.obtained == True:
                continue
            else:
                key.appear()
    '''enemies section'''
    for enemy in enemies2:
        enemy.appear()
        #enemy_collision.append(pygame.Rect.colliderect(player.rect, enemy.rect))
        if  pygame.Rect.colliderect(player.rect, enemy.rect) == True and enemy.level == 2:
            player.reset(newest_spawn_point_x,newest_spawn_point_y)
            for key in keys2:
                if key.level == 2:
                    if key.tier < player.tier:
                        continue
                    else:
                        key.obtained = False
    for enemy in enemies2[0:12]:
        if enemy.level == 2:
            if enemies2[0].x == 1503 and enemies2[0].y == 286:
                enemy.velX = -enemy.velX
                enemy.velY = -enemy.velY
            if enemies2[0].x == 1430 and enemies2[0].y == 359:
                enemy.velX = -enemy.velX
                enemy.velY = -enemy.velY
    for enemy in enemies2[12:]:
        if enemy.x >= WIDTH-150:
            enemy.velX = -enemy.velX
        if enemy.x <= 150:
            enemy.velX = -enemy.velX
        if enemy.y <= 130:
            enemy.velY = -enemy.velY
        if enemy.y >= HEIGHT-154:
            enemy.velY = -enemy.velY
    #first corridor level 2
    for enemy in enemies2:
        enemy.update()
    '''checkpoints section'''
    for checkpoint in checkpoints:
        if checkpoint.level == 2:
            checkpoint.appear()
            checkpoint_collision.append(pygame.Rect.colliderect(player.rect, checkpoint.rect))
            if pygame.Rect.colliderect(player.rect, checkpoint.rect) == True:
                newest_spawn_point_x = ((checkpoint.x + checkpoint.x + checkpoint.x2)/2)-12 #centers yourself in checkpoint
                newest_spawn_point_y = ((checkpoint.y + checkpoint.y + checkpoint.y2)/2)-12
                player.tier = checkpoint.tier
    player.appear()
    '''gates section'''
    for gate in gates2[0:2]:
        if gate.level == 2:
            for key in keys2[0:1]:
                if key.level == 2:
                    if key.obtained == True and key.tier == gate.tier:
                       gate.open = True
                    else:
                        gate.appear()
                        gate.open = False
    for gate in gates2[2:4]:
        if gate.level == 2:
            for key in keys2[1:2]:
                if key.level == 2:
                    if key.obtained == True and key.tier == gate.tier:
                       gate.open = True
                    else:
                        gate.appear()
                        gate.open = False
    for gate in gates2[4:6]:
        if gate.level == 2:
            for key in keys2[2:3]:
                if key.level == 2:
                    if key.obtained == True and key.tier == gate.tier:
                       gate.open = True
                    else:
                        gate.appear()
                        gate.open = False
    for gate in gates2[6:]:
        if gate.level == 2:
            for key in keys2[3:]:
                if key.level == 2:
                    if key.obtained == False or key.tier != gate.tier:
                        gate.appear()
                        gate.open = False
                        break
                    else:
                        gate.open = True
                    break
    for gate in gates2:
        if gate.level == 2:
            if gate.open == False:
                if gate.block == 'A':
                    left_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'D':
                    right_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'W':
                    top_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
                if gate.block == 'S':
                    bottom_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
    for gate in gates2:
        if gate.level == 2:
            if any(left_gate_collision) == True and gate.open == False:
                if gate.open == False:
                    player.left_pressed = False
            if any(right_gate_collision) == True and gate.open == False:
                if gate.open == False:
                    player.right_pressed = False
            if any(top_gate_collision) == True and gate.open == False:
                if gate.open == False:
                    player.up_pressed = False
            if any(bottom_gate_collision) == True and gate.open == False:
                if gate.open == False:
                    player.down_pressed = False
        '''objective section'''
    for objective in objectives:
        if objective.menu_choice == 0:
            if objective.level == 2:
                objective.appear()
                if pygame.Rect.colliderect(player.rect, objective.rect):
                    newest_spawn_point_x = WIDTH-70
                    newest_spawn_point_y = 55
                    player.reset(newest_spawn_point_x,newest_spawn_point_y)
                    player.tier = 1
                    player.level = 3
    player.appear()
    player.update()
    pygame.display.flip()
    clock.tick(120)

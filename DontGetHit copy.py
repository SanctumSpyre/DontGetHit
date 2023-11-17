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
    def __init__(self, x1, y1, x2, y2, level, tier=None,color=(0,0,0)):
        self.x = x1
        self.y = y1
        self.x2 = x2
        self.y2 = y2
        self.level = level
        if tier != None:
            self.tier = tier
        else:
            self.tier = 0
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
        self.open = binary
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
        self.spawnpoint_x = 0
        self.spawnpoint_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2
    def reset(self):
        self.x = self.spawnpoint_x
        self.y = self.spawnpoint_y
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
gatesUltimate = []
enemiesUltimate = []
keysUltimate = []
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
                    enemiesUltimate.append(Enemy(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
                if int(sl[5]) == 2:
                    enemiesUltimate.append(Enemy(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
            if sl[0] == 'Gate':
                if int(sl[5]) == 1:
                    gatesUltimate.append(Gate(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),str(sl[7]),int(sl[8])))
                if int(sl[5]) == 2:
                    gatesUltimate.append(Gate(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),str(sl[7]),int(sl[8])))
            if sl[0] == 'Key':
                if int(sl[5]) == 1:
                    keysUltimate.append(Key(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
                if int(sl[5]) == 2:
                    keysUltimate.append(Key(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6]),int(sl[7])))
            if sl[0] == 'Checkpoint':
                checkpoints.append(Checkpoint(int(sl[1]),int(sl[2]),int(sl[3]),int(sl[4]),int(sl[5]),int(sl[6])))

def LevelCreator(level):
    for gate in gatesUltimate:
            if gate.level == player.level:
                temp_gates.append(gate)
    if level == 0:
        for objective in objectives:
            if objective.menu_choice == 1:
                objective.appear()
            #this spawns you in each level respective to the tier of the objective
            if pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 1:
                player.spawnpoint_x = 100
                player.spawnpoint_y = HEIGHT-100
                player.reset()
                player.level = 1
            elif pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 2:
                player.spawnpoint_x = WIDTH-70
                player.spawnpoint_y = 55
                player.reset()
                player.level = 2
            elif pygame.Rect.colliderect(player.rect, objective.rect) and objective.level == 3:
                player.spawnpoint_x = 100
                player.spawnpoint_y = HEIGHT-100
                player.reset()
                player.level = 3
    if level == 1:
        if temp_enemies[0].y == 831:
            for enemy in temp_enemies[0:6]:
                enemy.velY = -enemy.velY
        if temp_enemies[0].y == 708:
            for enemy in temp_enemies[0:6]:
                enemy.velY = -enemy.velY
    #swirly squares section
        if temp_enemies[6].x == 1350 and temp_enemies[6].y == 602:
            for enemy in temp_enemies[6:11]:
                enemy.velX = -2
                enemy.velY = 0
            for enemy in temp_enemies[11:]:
                enemy.velX = 0
                enemy.velY = 2
        if temp_enemies[6].x == 1350 and temp_enemies[6].y == 650:
            for enemy in temp_enemies[6:11]:
                enemy.velX = 0
                enemy.velY = -2
            for enemy in temp_enemies[11:]:
                enemy.velX = 2
                enemy.velY = 0
        if temp_enemies[6].x == 1302 and temp_enemies[6].y == 650:
            for enemy in temp_enemies[6:11]:
                enemy.velX = 2
                enemy.velY = 0
            for enemy in temp_enemies[11:]:
                enemy.velX = 0
                enemy.velY = -2
        if temp_enemies[6].x == 1302 and temp_enemies[6].y == 602:
            for enemy in temp_enemies[6:11]:
                enemy.velX = 0
                enemy.velY = 2
            for enemy in temp_enemies[11:]:
                enemy.velX = -2
                enemy.velY = 0
        for gate in temp_gates:
            for key in temp_keys:
                if key.obtained == True and key.tier == gate.tier:
                    gate.open = True
                else:
                    gate.appear()
                    gate.open = False        
    if level == 2:
        for enemy in temp_enemies[0:12]:
            if temp_enemies[0].x == 1503 and temp_enemies[0].y == 286:
                enemy.velX = -enemy.velX
                enemy.velY = -enemy.velY
            if temp_enemies[0].x == 1430 and temp_enemies[0].y == 359:
                enemy.velX = -enemy.velX
                enemy.velY = -enemy.velY
        for enemy in temp_enemies[12:26]:
            if enemy.x >= WIDTH-150:
                enemy.velX = -enemy.velX
            if enemy.x <= 150:
                enemy.velX = -enemy.velX
            if enemy.y <= 130:
                enemy.velY = -enemy.velY
            if enemy.y >= HEIGHT-154:
                enemy.velY = -enemy.velY
        for enemy in temp_enemies[26:28]:
            if enemy.x >= 86:
                enemy.velX = -enemy.velX
            if enemy.x <= 10:
                enemy.velX = -enemy.velX
            if enemy.y <= 230:
                enemy.velY = -enemy.velY
            if enemy.y >= 732:
                enemy.velY = -enemy.velY
        for enemy in temp_enemies[28:30]:
            if enemy.x >= 1166:
                enemy.velX = -enemy.velX
            if enemy.x <= 110:
                enemy.velX = -enemy.velX
        for enemy in temp_enemies[30:]:
            if enemy.x >= 1166:
                enemy.velX = -enemy.velX
            if enemy.x <= 230:
                enemy.velX = -enemy.velX
        for gate in temp_gates[0:2]:
            for key in temp_keys[0:1]:
                if key.obtained == True and key.tier == gate.tier:
                    gate.open = True
                else:
                    gate.appear()
                    gate.open = False
        for gate in temp_gates[2:4]:
            for key in temp_keys[1:2]:
                if key.obtained == False or key.tier != gate.tier:
                    gate.appear()
                    gate.open = False
                if key.obtained == False and key.tier == gate.tier:
                    gate.appear()
                    gate.open = False
                    break
                else:
                    gate.open = True
        for gate in temp_gates[4:6]:
            for key in temp_keys[2:3]:
                if key.obtained == True and key.tier == gate.tier:
                    gate.open = True
                else:
                    gate.appear()
                    gate.open = False
        for gate in temp_gates[6:]:
            for key in temp_keys[3:]:
                if key.obtained == False or key.tier != gate.tier:
                    gate.appear()
                    gate.open = False
                if key.obtained == False and key.tier == gate.tier:
                    gate.appear()
                    gate.open = False
                    break
                else:
                    gate.open = True
    #first corridor level 2
    for enemy in temp_enemies:
        enemy.update()
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)
EntityAppender()
player = Player(WIDTH/2,HEIGHT/2+100,24,24,0,0)
menu = False
Running = True
while Running == True:
    #temp lists
    temp_keys = []
    temp_enemies= []
    temp_gates = []
    left_barrier_collision =  []
    right_barrier_collision = []  
    top_barrier_collision =  [] 
    bottom_barrier_collision = []
    left_gate_collision =  []
    right_gate_collision = []  
    top_gate_collision =  [] 
    bottom_gate_collision = []
    enemy_collision = []
    checkpoint_collision = []
    key_collision = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                menu = True
            if event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
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
    #this is for when game is 3 levels have been completed!
    if player.level == 4:
        PLAY_TEXT = get_font(45).render("YOU'VE BEATEN DONT GET HIT!!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(int(640*1.2), int(1.2*260)))
        PLAY_TEXT2 = get_font(40).render("Press M to go back to replay levels!", True, "white")
        PLAY_RECT2 = PLAY_TEXT2.get_rect(center=(int(640*1.2), int(1.2*260+50)))
        win.blit(PLAY_TEXT,PLAY_RECT)
        win.blit(PLAY_TEXT2,PLAY_RECT2)
    for barrier in barriers:
       if barrier.level == player.level:
            if barrier.block == 'A':
                left_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'D':
                right_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'W':
                top_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
            if barrier.block == 'S':
                bottom_barrier_collision.append(pygame.Rect.colliderect(player.rect, barrier.rect))
    for barrier in barriers:
        if barrier.level == player.level:
            barrier.appear()
        if any(left_barrier_collision) == True:
            player.left_pressed = False
        if any(right_barrier_collision) == True:
            player.right_pressed = False
        if any(top_barrier_collision) == True:
            player.up_pressed = False
        if any(bottom_barrier_collision) == True:
            player.down_pressed = False
    for key1 in keysUltimate:
        if key1.level == player.level:
            temp_keys.append(key1)
        for key2 in temp_keys:
            if  pygame.Rect.colliderect(player.rect, key2.rect) == True and key1.x == key2.x and key1.y == key2.y:
                key1.obtained = True
                key2.obtained = True
            if key2.obtained == True:
                continue
            else:
                key2.appear()
    for enemy in enemiesUltimate:
        if enemy.level == player.level:
            temp_enemies.append(enemy)
        for enemy in temp_enemies:
            enemy.appear()
            if  pygame.Rect.colliderect(player.rect, enemy.rect) == True:
                player.reset()
                for key in temp_keys:
                    if key.tier-1 < player.tier:
                        continue
                    else:
                        key.obtained = False
    for checkpoint in checkpoints:
        if checkpoint.level == player.level:
            checkpoint.appear()
            if pygame.Rect.colliderect(player.rect, checkpoint.rect) == True:
                player.spawnpoint_x = ((checkpoint.x + checkpoint.x + checkpoint.x2)/2)-12 #centers yourself in checkpoint
                player.spawnpoint_y = ((checkpoint.y + checkpoint.y + checkpoint.y2)/2)-12
                player.tier = checkpoint.tier
    for objective in objectives:
        if objective.menu_choice == 0:
            if objective.level == player.level:
                objective.appear()
                if pygame.Rect.colliderect(player.rect, objective.rect):
                    player.spawnpoint_x = ((objective.x + objective.x + objective.x2)/2)-12
                    player.spawnpoint_y = ((objective.y + objective.y + objective.y2)/2)-12
                    player.reset()
                    player.tier = 1
                    player.level += 1
    '''for gate in gatesUltimate:
            if gate.level == player.level:
                temp_gates.append(gate)
                
    for gate in temp_gates:
        for key in temp_keys:
            if key.obtained == True and key.tier == gate.tier:
                       gate.open = True
                    else:
                        gate.appear()
                        gate.open = False'''
    LevelCreator(player.level)
    for gate in temp_gates:
        if gate.open == False:
            if gate.block == 'A':
                left_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
            if gate.block == 'D':
                right_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
            if gate.block == 'W':
                top_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
            if gate.block == 'S':
                bottom_gate_collision.append(pygame.Rect.colliderect(player.rect, gate.rect))
    for gate in temp_gates:
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
    if menu == True:
        player.reset()
        player.level = 0
        player.x = WIDTH/2
        player.y = HEIGHT/2+100
        player.level = 0
        for key in keysUltimate:
            key.obtained = False
        player.tier = 0
        menu = False

    player.appear()
    player.update()
    pygame.display.flip()
    clock.tick(120)
            





        

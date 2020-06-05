import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *
pygame.init()
pygame.mixer.init()
bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')
background = pygame.image.load('images/background2.png').convert()
ice_bg = pygame.image.load('images/ice_bg.png').convert_alpha()
# 设置一些颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
# 加载背景音乐及音效
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
get_heart_sound = pygame.mixer.Sound("sound/get_heart.wav")
get_heart_sound.set_volume(0.2)
get_ice_sound = pygame.mixer.Sound("sound/get_ice.wav")
get_ice_sound.set_volume(0.2)
lose_ice_sound = pygame.mixer.Sound("sound/lose_ice.wav")
lose_ice_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
# 定义生成小型敌机函数
def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
# 定义生成中型敌机函数
def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
# 定义生成大型敌机函数
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
# 定义改变敌机速度函数
def inc_speed(target, inc):
    for each in target:
        each.speed += inc
# 主程序
def main():
    # 循环播放背景音乐
    pygame.mixer.music.play(-1)
    # 生成我方飞机
    me = myplane.MyPlane(bg_size)
    # 创建敌机组
    enemies = pygame.sprite.Group()
    # 生成小型敌机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    # 生成中型敌机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,4)
    # 生成大型敌机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)
    # 初始化子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    # 初始化超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
    # 初始化四层子弹
    bullet3 = []
    bullet3_index = 0
    bullet3_num = 16
    for i in range(bullet3_num // 4):
        bullet3.append(bullet.Bullet3((me.rect.centerx - 63, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx - 23, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx + 23, me.rect.centery)))
        bullet3.append(bullet.Bullet3((me.rect.centerx + 63, me.rect.centery)))
    # 初始化延时器
    clock = pygame.time.Clock()
    # 定义绘制飞机索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    # 初始化得分
    score = 0
    score_font = pygame.font.Font('font/font.ttf',36)
    # 初始化暂停按钮和状态
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width - paused_rect.width - 10,10
    paused_image = pause_nor_image
    # 初始化禁音按钮和状态
    silence = False
    volume_on_pressed_image = pygame.image.load('images/sound_open.png').convert_alpha()
    volume_on_image = pygame.image.load('images/sound_open_not.png').convert_alpha()
    volume_off_pressed_image = pygame.image.load('images/sound_close.png').convert_alpha()
    volume_off_image = pygame.image.load('images/sound_close_not.png').convert_alpha()
    volume_rect = volume_on_image.get_rect()
    volume_rect.left, volume_rect.top = width - paused_rect.width - 10, 65
    volume_image = volume_on_image
    # 初始化等级
    level = 1
    # 初始化全屏炸弹显示
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3
    # 初始化补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    heart_supply = supply.Heart_Supply(bg_size)
    ice_supply = supply.Ice_Supply(bg_size)
    fire_supply = supply.Fire_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,30 * 1000)
    DOUBLE_BULLET_TIME = USEREVENT + 1
    is_double_bullet = False
    is_super_bullet = False
    # 初始化无敌状态
    INVINCIBLE_TIME = USEREVENT + 2
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3
    # 避免反复读取文件
    recorded = False
    # 初始化游戏结束元素
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    flozen = False
    FLOZEN_TIME = USEREVENT + 3
    bg_posy = -700
    switch_image = True
    delay = 100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    # 暂停或开始
                    paused = not paused
                    if paused:
                        # 停止发放补给
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        # 停止播放音乐
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    elif not paused and not silence:
                        # 设置发放补给
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        # 继续播放音乐
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if event.button == 1 and volume_rect.collidepoint(event.pos):
                    silence = not silence
                    if silence:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    elif not paused and not silence:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                # 如果用户点击了暂停按钮
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
                # 如果用户点击了禁音按钮
                if volume_rect.collidepoint(event.pos):
                    if silence:
                        volume_image = volume_off_pressed_image
                    else:
                        volume_image = volume_on_pressed_image
                else:
                    if silence:
                        volume_image = volume_off_image
                    else:
                        volume_image = volume_on_image
            elif event.type == KEYDOWN:
                # 用户使用了全屏炸弹
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        if not silence:
                            bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                # 发放补给
                if not silence:
                    supply_sound.play()
                # 随机的补给内容
                choose = choice([1,2,3,4,5])
                if choose == 1:
                    bomb_supply.reset()
                elif choose == 2:
                    bullet_supply.reset()
                elif choose == 3:
                    fire_supply.reset()
                elif choose == 4:
                    ice_supply.reset()
                elif choose == 5:
                    heart_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                # 结束超级子弹的使用
                is_double_bullet = False
                is_super_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)
            elif event.type == FLOZEN_TIME:
                if not silence:
                    lose_ice_sound.play()
                flozen = False
                pygame.time.set_timer(FLOZEN_TIME, 0)
        # 级别上升
        if level == 1 and score > 50000:
            level = 2
            if not silence:
                upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            inc_speed(small_enemies,1)
        # 级别上升
        elif level == 1 and score > 300000:
            level = 2
            if not silence:
                upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        # 级别上升
        elif level == 3 and score > 600000:
            level = 4
            if not silence:
                upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        # 级别上升
        elif level == 4 and score > 1000000:
            level = 5
            if not silence:
                upgrade_sound.play()
            add_small_enemies(small_enemies,enemies,5)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        # 绘制背景
        if bg_posy >= 0 and not paused and not flozen:
            bg_posy = -700
        if not paused and not flozen:
            bg_posy += 0.5
        screen.blit(background, (0, bg_posy))
        if life_num and not paused:
            if not flozen:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_w] or key_pressed[K_UP]:
                    me.moveUp()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    me.moveDown()
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    me.moveLeft()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    me.moveRight()
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    if not silence:
                        get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    if not silence:
                        get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False
            if heart_supply.active:
                heart_supply.move()
                screen.blit(heart_supply.image, heart_supply.rect)
                if pygame.sprite.collide_mask(heart_supply, me):
                    if not silence:
                        get_heart_sound.play()
                    if life_num < 3 and life_num > 0:
                        life_num += 1
                    heart_supply.active = False
            if ice_supply.active:
                ice_supply.move()
                screen.blit(ice_supply.image, ice_supply.rect)
                if pygame.sprite.collide_mask(ice_supply, me):
                    if not silence:
                        get_ice_sound.play()
                    pygame.time.set_timer(FLOZEN_TIME, 5 * 1000)
                    flozen = True
                    ice_supply.active = False
            if fire_supply.active:
                fire_supply.move()
                screen.blit(fire_supply.image, fire_supply.rect)
                if pygame.sprite.collide_mask(fire_supply, me):
                    if not silence:
                        get_bullet_sound.play()
                    is_super_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    fire_supply.active = False
            if not(delay % 10) and not flozen:
                if not silence:
                    bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx+30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                elif is_super_bullet:
                    bullets = bullet3
                    bullets[bullet3_index].reset((me.rect.centerx - 63, me.rect.centery))
                    bullets[bullet3_index + 1].reset((me.rect.centerx - 23, me.rect.centery))
                    bullets[bullet3_index + 2].reset((me.rect.centerx + 23, me.rect.centery))
                    bullets[bullet3_index + 3].reset((me.rect.centerx + 63, me.rect.centery))
                    bullet3_index = (bullet3_index + 4) % bullet3_num
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            for b in bullets:
                if b.active and not flozen:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            for each in big_enemies:
                if each.active:
                    each.move(flozen)
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)
                    pygame.draw.line(screen,BLACK,\
                        (each.rect.left,each.rect.top - 5),\
                        (each.rect.right,each.rect.top - 5),\
                        2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,\
                        (each.rect.left,each.rect.top - 5),\
                        (each.rect.left + each.rect.width * energy_remain,\
                            each.rect.top - 5),2)
                    if each.rect.bottom == -50 and not silence:
                        enemy3_fly_sound.play(-1)
                else:
                    if not (delay % 3):
                        if e3_destroy_index == 0 and not silence:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()
            for each in mid_enemies:
                if each.active:
                    each.move(flozen)
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image,each.rect)
                    pygame.draw.line(screen,BLACK,\
                        (each.rect.left,each.rect.top - 5),\
                        (each.rect.right,each.rect.top - 5),\
                        2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,\
                        (each.rect.left,each.rect.top - 5),\
                        (each.rect.left + each.rect.width * energy_remain,\
                            each.rect.top - 5),2)
                else:
                    if not (delay % 3):
                        if e2_destroy_index == 0 and not silence:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()
            for each in small_enemies:
                if each.active:
                    each.move(flozen)
                    screen.blit(each.image,each.rect)
                else:
                    if not (delay % 3):
                        if e1_destroy_index == 0 and not silence:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            if me.active:
                if not me.invincible:
                    if delay // 5 % 2 and not flozen:
                        screen.blit(me.image1, me.rect)
                    else:
                        screen.blit(me.image2, me.rect)
                else:
                    if delay % 10 < 7:
                        screen.blit(me.image1, me.rect)
            else:
                if not silence:
                    me_down_sound.play()
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index],me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3 * 1000)
            if flozen:
                screen.blit(ice_bg,(0,0))
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))
            score_text = score_font.render('Score : %s'% str(score),True,WHITE)
            screen.blit(score_text,(10,5))
        elif life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recorded:
                recorded = True
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)
            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)
            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                    again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()
        screen.blit(paused_image,paused_rect)
        screen.blit(volume_image, volume_rect)
        if not(delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

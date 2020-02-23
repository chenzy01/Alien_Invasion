import sys

import pygame
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """下面使用elif代码块，是因为每个事件都只与一个键关联
    """
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()  # 按"q"退出游戏


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


def check_events(ai_settings, screen, ship, bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():  # 事件循环，来管理屏幕更新的代码
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, alien, bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()  # 每次执行循环时都绘制一个空屏幕，并擦去旧屏幕


def update_bullets(bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    bullets.update()  # 更新子弹位置

    # 删除未消失的子弹，为何删除：子弹在到达屏幕顶端后并没有消失，而是因为无法绘制所以无法看到，但
    # y坐标变成负值，会越来越小，将继续消耗内存和处理能力。
    for bullet in bullets.copy():  # 使用了浅拷贝
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    """
    1、直接赋值：其实就是对象的引用（别名）。
    2、浅拷贝(copy)：拷贝父对象，不会拷贝对象的内部的子对象。
    3、深拷贝(deepcopy)： copy 模块的 deepcopy 方法，完全拷贝了父对象及其子对象。
    参考：https://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html
    """


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:  # 限制了发射子弹时，屏幕中只能有三颗子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
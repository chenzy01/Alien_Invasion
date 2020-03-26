import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


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


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():  # 事件循环，来管理屏幕更新的代码
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # 返回一个元组，包含玩家单机时鼠标的x和y坐标
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家点击 Play 按钮时开始游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):  # 检查点击时鼠标的坐标是否落在Play按钮rect内
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        # 仅当玩家单击了 Play 按钮且游戏当前处于非活跃状态时，游戏才重新开始
        if button_clicked and not stats.game_active:
            # 重置游戏设置
            ai_settings.initialize_dynamic_settings()
            # 影藏光标
            pygame.mouse.set_visible(False)
            # 重置游戏统计信息
            stats.reset_stats()
            stats.game_active = True

            # 清空外星人和子弹列表
            aliens.empty()
            bullets.empty()

            # 创建一群新的外星人，并让飞船居中
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # aliens.blitme()
    aliens.draw(screen)  # 访问外星人编组，并绘制每个外星人
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()  # 每次执行循环时都绘制一个空屏幕，并擦去旧屏幕


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
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
    # 检查子弹与外星人的碰撞
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 检查是否有子弹击中了外星人，是将每颗子弹的rect同外星人的rect进行比较
    # 若击中，就删除相应的子弹和外星人
    # sprite.groupcollide 返回的是一个字典{"子弹":"外星人"}
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)  # 每次发生碰撞则记录一次
            sb.prep_score()  # 更新记分

    if len(aliens) == 0:
        # 当外星人为空时，清空子弹,加快游戏节奏，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:  # 限制了发射子弹时，屏幕中只能有三颗子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """

    :param ai_settings:设置类的对象，获取外星人的属性
    :param alien_width:外星人编组
    :return:number_alienx_x ,每行可容纳的数量
    外星人之间的间距是外星人图像的宽度
    屏幕两边都留下间距，为外星人的宽度
    """
    avaible_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaible_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """
    :param ai_settings: 设置类的对象，获取外星人的属性
    :param ship_height: 飞船的高度
    :param alien_height:  外星人的高度
    :return: 可容纳的行数
    """
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)  # 计算有多少可用的垂直空间
    number_rows = int(available_space_y / (2 * alien_height))  # 计算可容纳的行数
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    :param ai_settings: 设置类的对象，获取外星人的属性
    :param screen: 屏幕对象，为了获取屏幕的属性
    :param aliens: 外星人编组，每生成一个，及加入到编组中
    :param alien_number: 一行中，第 alien_number 个外星人
    :param row_number: 垂直方向上，第 row_number 行的外星人，存储行号
    :return:
    """
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width  # 外星人的宽
    alien.x = alien_width + 2 * alien_width * alien_number  # 外星人的X坐标
    alien.rect.x = alien.x  # 一个外星人在一行上要占用的空间，包括最左边的间距，本身的宽度，外星人之间的间隔
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    :param ship:  飞船对象，获取飞船属性
    :param ai_settings: 设置类的对象，获取外星人的属性
    :param screen: 屏幕对象，为了获取屏幕的属性
    :param aliens: 外星人编组
    创建外星人群
    创建一个外星人，并计算一行可以容纳多少外星人
    """
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人处于屏幕边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查外星人和飞船之间的碰撞
    # spritecollideany()函数接受一个精灵和一个编组，遍历编组，找与精灵碰撞的成员，找到就返回该成员，找不到返回None
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Ship hit!!! GAME OVER")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():  # sprites在抽象类AbstractGroup中，Group()继承了AbstractGroup，aliens是Group()的对象
        if alien.check_edges():  # 返回了True，说明到达屏幕边缘
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed   # 遍历所有外星人，将y坐标下移（增加，因为0坐标在左上角）
    ai_settings.fleet_direction *= -1  # 方向标志位


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将 ships_left 的值减1
        stats.ships_left -= 1
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放置到屏幕中央底部
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

















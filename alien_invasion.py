import pygame
from pygame.sprite import Group

# from alien import Alien
from settings.settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    """初始化游戏并创建一个屏幕对象"""
    # 初始化背景pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()  # Settings() 是设置类
    # 创建一个显示窗口,宽1200,高800，是窗口大小，元组，这是整个游戏的窗口
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_hight))
    pygame.display.set_caption("Alien Invasion")  # 窗口的标题

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人
    # alien = Alien(ai_settings, screen)
    # 创建一个外星人编组,存储外星人群
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens)



    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)
        # 更新飞船位置
        ship.update()
        # 更新子弹位置和删除未消失的子弹
        gf.update_bullets(bullets)
        # 每次循环重新绘制屏幕,让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()



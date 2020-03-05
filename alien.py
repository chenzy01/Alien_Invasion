import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen, *groups):
        super(Alien, self).__init__(*groups)
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()  # 获取屏幕的属性
        if self.rect.right >= screen_rect.right:  # rect:外星人图像的对象,若外星人的right大于或等于屏幕的right，则位于屏幕右边缘
            return True
        elif self.rect.left <= 0:  # 若外星人的left小于或等于屏幕的left，则位于屏幕左边缘
            return True

    def update(self):
        """向右或向左移动外星人"""
        # 通过 fleet_direction 改变移动的方向，alien_speed_fector 是移动的速度
        self.x += (self.ai_settings.alien_speed_fector * self.ai_settings.fleet_direction)
        self.rect.x = self.x


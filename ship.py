import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()  # 获取图像(飞船)的属性，是一个矩形
        self.screen_rect = screen.get_rect()  # 获取屏幕的属性

        # 将每膄飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx  # 屏幕中央，以X轴为坐标
        self.rect.bottom = self.screen_rect.bottom  # 屏幕底部

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.move_right = False
        self.move_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        """
        这里使用if，而不使用elif代码块的区别：
        if：玩家同时按下左右两个方向箭头，将先增大rect.centerx的值，再降低这个值，从而保持位置不变
        elif：右箭头会始终处于优先地位
        """
        # 更新飞船center的值，而不是rect
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)
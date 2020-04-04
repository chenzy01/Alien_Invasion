import pygame.font
from pygame .sprite import Group

from ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_image()

    def prep_image(self):
        # 准备初始化当前得分、最高得分和等级图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

        # 剩余飞船数量
        self.prep_ships()

    def show_score(self):
        """在屏幕上显示当前得分、最高得分和等级"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        self.ships.draw(self.screen)

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        """round()用法：对浮点数取近似值，保留几位小数
        round( x [, n])，参数 x:数字表达式，n,表示从小数点后保留n位数，默认值为 0
        特殊情况：round(2.675, 2) >2.67，这跟浮点数的精度有关。在机器中浮点数不一定能精确表达，
        因为换算成一串 1 和 0 后可能是无限位数的，机器已经做出了截断处理。
        那么在机器中保存的2.675这个数字就比实际数字要小那么一点点。这一点点就导致了它离 2.67 要更近一点点，
        所以保留两位小数时就近似到了 2.67。
        
        format()用法：该函数把字符串当成一个模板，通过传入的参数进行格式化，并且使用大括号‘{}’作为特殊字符代替‘%’
        位置匹配：
        （1）不带编号，即“{}”
　　    （2）带数字编号，可调换顺序，即“{1}”、“{2}”
　　    （3）带关键字，即“{a}”、“{tom}”
        具体用法参考：https://www.cnblogs.com/fat39/p/7159881.html#tag2
        """
        round_score = round(self.stats.score, -1)
        score_str = "{:,}".format(round_score)  # 将数字值 stats.score 装换为字符串

        # 创建图像函数 font.render()，返回了一个 Surface
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # 得分的图像距离屏幕右边缘20像素
        self.score_rect.top = 20  # 得分的图像距离屏幕上边缘20像素

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩余多少艘飞船"""
        self.ships = Group()  # 存储飞船实例
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


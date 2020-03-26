class Settings():
    """存储 外星人入侵 的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""

        # 屏幕设置
        self.screen_width = 1200  # 屏幕的宽
        self.screen_height = 700  # 屏幕的高
        # 设置背景色
        """
        颜色是以RGB值指定，这种颜色由红色、绿色、蓝色值组成，其中每个值的取值范围都在 0~255.通
        通过组合成不同的RGB值，可创建1600万种颜色
        红色(255,0,0)
        绿色(0,255,0)
        蓝色(0,0,255)
        """
        self.bg_color = (230, 230, 230)  # 用浅灰色填充屏幕

        # 飞船的数量
        self.ship_limit = 3

        # 子弹设置:宽，高，颜色
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # 外星人设置
        self.fleet_drop_speed = 25  # 向下移动的速度

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        # 飞船的速度
        self.ship_speed_factor = 1.5
        # 子弹的速速
        self.bullet_speed_factor = 4
        # 移动的速度
        self.alien_speed_fector = 1
        # fleet_direction为1表示向右，-1表示向左
        self.fleet_direction = 1
        # 记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_fector *= self.speedup_scale
        # 让点数变成整数
        self.alien_points = int(self.alien_points * self.score_scale)  # 提高点数，加快节奏






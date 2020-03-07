class Settings():
    """存储 外星人入侵 的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""

        # 屏幕设置
        self.screen_width = 1100  # 屏幕的宽
        self.screen_height = 600  # 屏幕的高
        # 设置背景色
        """
        颜色是以RGB值指定，这种颜色由红色、绿色、蓝色值组成，其中每个值的取值范围都在 0~255.通
        通过组合成不同的RGB值，可创建1600万种颜色
        红色(255,0,0)
        绿色(0,255,0)
        蓝色(0,0,255)
        """
        self.bg_color = (230, 230, 230)  # 用浅灰色填充屏幕

        # 飞船的位置
        self.ship_speed_factor = 1.5

        # 子弹设置:速度，宽，高，颜色
        self.bullet_speed_factor = 2
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # 外星人设置
        self.alien_speed_fector = 1  # 移动的速度
        self.fleet_drop_speed = 10  # 向下移动的速度
        # fleet_direction为1表示向右，-1表示向左
        self.fleet_direction = 1




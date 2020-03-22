import pygame.font  # 将文本渲染到屏幕上


class Button():

    def __init__(self, ai_settings, screen, msg):  # msg 是要在按钮中显示的文本
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # 指定渲染文本的字体，None 使用默认字体，48 指定文本字号

        # 创建按钮的rec对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次，把字符串渲染为图像来处理文本
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将 msg 渲染为图像，并使其在按钮上居中"""
        '''
        font.render()
        msg:将存储在 msg 中的文本转换为图像，将图像保存在对象 msg_image 中
        True:指定开启还是关闭反锯齿功能（反锯齿让文本边缘更平滑）
        '''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



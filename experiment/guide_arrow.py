from kivy.app import Widget
from kivy.graphics.vertex_instructions import (Line, Triangle)
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from config import appearance


class GuideArrow(Widget):
    def __init__(self, direction, arrow_color, arrow_length, **kwargs):
        super(GuideArrow, self).__init__(**kwargs)
        self.direction = direction
        self.arrow_length = arrow_length
        self.arrow_tip_size = 0.02
        self.arrow_color = arrow_color
        self.draw()

    def generate_line_position(self):
        width, height = Window.width, Window.height
        x_mid = width / 2
        y_mid = height / 2
        if self.direction == 'TOP' or self.direction == 'BOTTOM':
            line = (
                x_mid, y_mid * (1 + self.arrow_length),
                x_mid, y_mid * (1 - self.arrow_length)
            )
            return line
        if self.direction == 'LEFT' or self.direction == 'RIGHT':
            line = (
                x_mid * (1 + self.arrow_length), y_mid,
                x_mid * (1 - self.arrow_length), y_mid
            )
            return line

    def generate_arrow_tip_position(self):
        width, height = Window.width, Window.height
        x_mid = width / 2
        y_mid = height / 2
        pos_offset = (1 + self.arrow_tip_size)
        neg_offset = (1 - self.arrow_tip_size)
        if self.direction == 'TOP':
            tip_pos = (x_mid, y_mid * (1 + self.arrow_length))
            triangle = (
                tip_pos[0], tip_pos[1],
                tip_pos[0] * pos_offset, tip_pos[1] * neg_offset,
                tip_pos[0] * neg_offset, tip_pos[1] * neg_offset,
            )
            return triangle
        if self.direction == 'BOTTOM':
            tip_pos = (x_mid, y_mid * (1 - self.arrow_length))
            triangle = (
                tip_pos[0], tip_pos[1],
                tip_pos[0] * pos_offset, tip_pos[1] * pos_offset,
                tip_pos[0] * neg_offset, tip_pos[1] * pos_offset,
            )
            return triangle
        if self.direction == 'RIGHT':
            tip_pos = (x_mid * (1 + self.arrow_length), y_mid)
            triangle = (
                tip_pos[0], tip_pos[1],
                tip_pos[0] * neg_offset, tip_pos[1] * pos_offset,
                tip_pos[0] * neg_offset, tip_pos[1] * neg_offset
            )
            return triangle
        if self.direction == 'LEFT':
            tip_pos = (x_mid * (1 - self.arrow_length), y_mid)
            triangle = (
                tip_pos[0], tip_pos[1],
                tip_pos[0] * pos_offset, tip_pos[1] * pos_offset,
                tip_pos[0] * pos_offset, tip_pos[1] * neg_offset
            )
            return triangle

    def get_pos(self):
        line = self.generate_line_position()
        triangle = self.generate_arrow_tip_position()
        return line, triangle

    def draw(self):
        line, triangle = self.get_pos()
        with self.canvas:
            self.canvas.clear()
            Color(*appearance.COLOR[self.arrow_color])
            Line(points=line, width=1)
            Triangle(points=triangle)

    def finish(self):
        with self.canvas:
            self.canvas.clear()

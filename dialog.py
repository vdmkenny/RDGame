import arcade

TEXT_PADDING = 10
FONT_SIZE = 18


class DialogMessage:
    def __init__(
        self, game, message=["test!"], name=None, coords=[0, 0], size=[100, 100]
    ):
        self.offset_x = game.view_left
        self.offset_y = game.view_bottom
        self.index = 0
        self.active = False
        self.full_message = message
        self.current_message = message[self.index]
        if name:
            self.name = name
        else:
            self.name = ""
        self.coords = coords

        if not size:
            self.size = [game.SCREEN_WIDTH, game.SCREEN_HEIGHT // 5]
        else:
            self.size = size

    def setMessage(self, message=[], name=None):
        self.index = 0
        if name:
            self.name = name
        else:
            self.name = None
        self.full_message = message
        self.current_message = self.full_message[self.index]
        self.active = True

    def nextMessage(self):
        self.index += 1
        if self.index >= len(self.full_message):
            self.active = False
            return

        self.current_message = self.message[self.index]

    def update(self, game):
        self.offset_x = game.view_left
        self.offset_y = game.view_bottom

    def draw(self):
        if self.active:
            arcade.draw_xywh_rectangle_outline(
                self.coords[0] + self.offset_x,
                self.coords[1] + self.offset_y,
                self.size[0],
                self.size[1],
                [128, 128, 128, 128],
                5,
            )
            arcade.draw_xywh_rectangle_filled(
                self.coords[0] + self.offset_x,
                self.coords[1] + self.offset_y,
                self.size[0],
                self.size[1],
                [0, 0, 64, 128],
            )

            name_start = [
                self.coords[0] + self.offset_x + TEXT_PADDING,
                self.coords[1]
                + self.offset_y
                + self.size[1]
                - FONT_SIZE
                - (TEXT_PADDING * 2),
            ]

            message_start = [
                self.coords[0] + self.offset_x + TEXT_PADDING,
                self.coords[1]
                + self.offset_y
                + self.size[1]
                - (FONT_SIZE * 2)
                - (TEXT_PADDING * 4),
            ]

            if self.name:
                arcade.draw_text(
                    f"{self.name}:",
                    name_start[0],
                    name_start[1],
                    arcade.color.WHITE,
                    FONT_SIZE,
                )
            arcade.draw_text(
                self.current_message,
                message_start[0],
                message_start[1],
                arcade.color.WHITE,
                FONT_SIZE,
            )

import arcade

import player, maps

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "R&D Game"

TILE_SCALING = 1

MOVEMENT_SPEED = 4

#Facing constants
DOWN_FACING = 0
UP_FACING = 1
LEFT_FACING = 2
RIGHT_FACING = 3

class IntroView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        #self.texture = arcade.load_texture("game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("R&D Game",
                         0, SCREEN_HEIGHT - 100, arcade.color.WHITE, 32, SCREEN_WIDTH, align="center")
        arcade.draw_text("You're a classic nerd which has been transported to an anime world.\nWith this sudden teleportation come sudden powers. Try to survive!\n\nPress any Key to start.",
                         0, SCREEN_HEIGHT - 300, arcade.color.WHITE, 16, SCREEN_WIDTH, align="center")


    def on_key_press(self, key, modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        # Keep track of held keys
        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False

        # viewport offset
        self.view_left = 0
        self.view_bottom = 0

        # Speed of the world moving around the player
        self.move_x = 0
        self.move_y = 0

        self.player = None
        self.physics_engine = None

        self.default_map_dir = "pipoya/SampleMap/"
        self.default_map = "samplemap"

        self.active_map = None

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT


    def setup(self):
        self.player = player.PlayerCharacter(SCREEN_WIDTH,
                                            SCREEN_HEIGHT, 
                                            self.view_left, 
                                            self.view_bottom)

        self.activemap = maps.GameMap(mapname=self.default_map, basepath=self.default_map_dir)
        self.activemap.LoadMap(self)

        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left - 1,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom - 1)
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_layers)


    # Check if any arrow key is currently held down
    def iskeyheld(self):
        return self.key_up or self.key_down or self.key_left or self.key_right


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.key_up = True
            self.player.player_moving = True
            self.player.character_face_direction = UP_FACING
            self.move_y=-MOVEMENT_SPEED
            self.move_x=0
        elif key == arcade.key.DOWN:
            self.key_down = True
            self.player.player_moving = True
            self.player.character_face_direction = DOWN_FACING
            self.move_y=MOVEMENT_SPEED
            self.move_x=0
        elif key == arcade.key.LEFT:
            self.key_left = True
            self.player.player_moving = True
            self.player.character_face_direction = LEFT_FACING
            self.move_x=MOVEMENT_SPEED
            self.move_y=0
        elif key == arcade.key.RIGHT:
            self.key_right = True
            self.player.player_moving = True
            self.player.character_face_direction = RIGHT_FACING
            self.move_x=-MOVEMENT_SPEED
            self.move_y=0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.key_up = False
            self.move_y=0
            if not self.iskeyheld():
                self.player.player_moving = False
        elif key == arcade.key.DOWN:
            self.move_y=0
            self.key_down = False
            if not self.iskeyheld():
                self.player.player_moving = False
        elif key == arcade.key.LEFT:
            self.move_x=0
            self.key_left = False
            if not self.iskeyheld():
                self.player.player_moving = False
        elif key == arcade.key.RIGHT:
            self.move_x=0
            self.key_right = False
            if not self.iskeyheld():
                self.player.player_moving = False

    def on_draw(self):
        arcade.start_render()

        self.ground_layers.draw()
        self.collision_layers.draw()
        self.bridge_layers.draw()
        self.player.draw()
        self.top_layers.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.player.update()
        self.player.update_animation()

        # Center character
        if self.player.player_moving:
            self.player.center_x -= self.move_x
            self.player.center_y -= self.move_y

        if self.player.collides_with_list(self.collision_layers):
            self.physics_engine.update()
            self.player.center_x = SCREEN_WIDTH / 2 + self.view_left
            self.player.center_y = SCREEN_HEIGHT / 2 + self.view_bottom
            return

        self.view_left -= self.move_x
        self.view_bottom -= self.move_y

        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_vsync(True)
    start_view = IntroView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

import threading
import time
import random

import arcade

MAIN_PATH="images/sprites/"
CHARACTER_SCALING = 2
CHARACTER_RESOLUTION = 32
UPDATES_PER_FRAME = 10
MOVEMENT_SPEED = 1

#Facing constants
DOWN_FACING = 0
UP_FACING = 1
LEFT_FACING = 2
RIGHT_FACING = 3

#Character constants
NERD = 0
OLD_MAN = 1
YOUNG_GIRL = 2

def sort_spritelist(sprite_list, key=None):
    sprite_list.sprite_list = sorted(sprite_list.sprite_list, key=key, reverse=True)
#    for idx, sprite in enumerate(sprite_list.sprite_list):
#        sprite_list.sprite_idx[sprite] = idx
#    sprite_list._vao1 = None


def load_character_textures(filename, character, facing):
    if facing == DOWN_FACING:
        return [
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 0,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 3,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 0,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 7,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=False)
        ]
    if facing == UP_FACING:
        return [
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 1,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 4,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 1,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 4,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=True)
        ]
    if facing == LEFT_FACING:
        return [
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 2,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 5,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 2,
                                y=CHARACTER_RESOLUTION * (character * 2)),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 6,
                                y=CHARACTER_RESOLUTION * (character * 2)),
        ]
    if facing == RIGHT_FACING:
        return [
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 2,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=True),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 5,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=True),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 2,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=True),
            arcade.load_texture(file_name=filename,
			 	width=CHARACTER_RESOLUTION,
				height=CHARACTER_RESOLUTION * 2,
				x=CHARACTER_RESOLUTION * 6,
                                y=CHARACTER_RESOLUTION * (character * 2),
				flipped_horizontally=True)
        ]


class GameCharacter(arcade.Sprite):
    def character_action(self):
        while True:
            action_dict = {
                'rotate': self.set_facing,
                'wander': self.set_moving,
            }
            action = action_dict.get(self.properties.get('movement', None), None)
            if action:
                action()
            time.sleep(random.randint(2,10))


    def set_facing(self, facing=None):
        if facing==None:
            facing = random.randint(0,3)

        if 0 <= facing <= 3:
            self.character_face_direction = facing
        else:
            self.character_face_direction = DOWN_FACING

    def set_moving(self, direction=None):
        if not direction:
            direction = random.randint(0,3)

        self.character_moving = True
        self.set_facing(facing=direction)

        if direction == DOWN_FACING:
            self.change_x = 0
            self.change_y = -MOVEMENT_SPEED
        elif direction == UP_FACING:
            self.change_x = 0
            self.change_y = MOVEMENT_SPEED
        elif direction == LEFT_FACING:
            self.change_x = -MOVEMENT_SPEED
            self.change_y = 0
        elif direction == RIGHT_FACING:
            self.change_x = MOVEMENT_SPEED
            self.change_y = 0
           
        time.sleep(random.randint(0,1))
        self.character_moving = False
        self.change_x = 0
        self.change_y = 0


    def __init__(self, character, properties={}):
        # Set up parent class
        super().__init__()

        self.properties=properties
        self.timer = threading.Timer(random.randint(0,3), self.character_action)
        self.timer.start()

        self.character_moving = False

        # Select character model
        self.character = character

        # Used for flipping between image sequences
        self.cur_texture = 1

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        #self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        self.textures_down   = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, DOWN_FACING)
        self.textures_up     = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, UP_FACING)
        self.textures_left   = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, LEFT_FACING)
        self.textures_right  = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, RIGHT_FACING)

        self.facingdict = {
            DOWN_FACING: self.textures_down,
            UP_FACING: self.textures_up,
            LEFT_FACING: self.textures_left,
            RIGHT_FACING: self.textures_right,
        }

        # Default to face-down
        self.character_face_direction = int(self.properties.get('facing', DOWN_FACING))

        # Default texture
        self.texture = self.textures_down[0]

        #self.set_hit_box(self.texture.hit_box_points)
        self.set_hit_box([
                         [-(CHARACTER_RESOLUTION // 2 -4),-(CHARACTER_RESOLUTION // 2)],
                         [(CHARACTER_RESOLUTION // 2  -4),-(CHARACTER_RESOLUTION // 2)], 
                         [(CHARACTER_RESOLUTION // 2  -4),-(CHARACTER_RESOLUTION)], 
                         [-(CHARACTER_RESOLUTION // 2 -4),-(CHARACTER_RESOLUTION)]
                         ])

        # Action Sprite is used for interactions with the world
        #self.action_sprite = arcade.Sprite(image_width=CHARACTER_RESOLUTION ,
        #                                   image_height=CHARACTER_RESOLUTION)
        
        self.action_sprite = arcade.Sprite()
                                           

        self.action_sprite.alpha = 128
        self.action_sprite.color = arcade.color.RED
        self.action_sprite.scale = CHARACTER_SCALING
        self.action_sprite.texture   = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, DOWN_FACING)[0]
        self.action_sprite.width = CHARACTER_RESOLUTION * CHARACTER_SCALING
        self.action_sprite.height = CHARACTER_RESOLUTION * CHARACTER_SCALING
        self.action_sprite.set_hit_box([
                         [-(CHARACTER_RESOLUTION // CHARACTER_SCALING // 2),-(CHARACTER_RESOLUTION // CHARACTER_SCALING// 2)],
                         [(CHARACTER_RESOLUTION // CHARACTER_SCALING // 2),-(CHARACTER_RESOLUTION // CHARACTER_SCALING // 2)], 
                         [(CHARACTER_RESOLUTION // CHARACTER_SCALING // 2),-(CHARACTER_RESOLUTION // CHARACTER_SCALING)], 
                         [-(CHARACTER_RESOLUTION // CHARACTER_SCALING // 2),-(CHARACTER_RESOLUTION // CHARACTER_SCALING)]
                         ])
        

    def check_for_collision(self, game):
        collision_list = game.activemap.map_dict.get('collision_layers', arcade.SpriteList())
        if self.collides_with_list(collision_list):
            self.character_moving=False
            self.center_x -= self.change_x
            self.center_y -= self.change_y


    def update_animation(self, delta_time: float = 1/60):
        # Position action sprite
        #self.switch_action = {
        #    DOWN_FACING:  [self.left, self.bottom - (CHARACTER_RESOLUTION * CHARACTER_SCALING)],
        #    UP_FACING:    [self.left, self.bottom + (CHARACTER_RESOLUTION * CHARACTER_SCALING)],
        #    LEFT_FACING:  [self.left - (CHARACTER_RESOLUTION * CHARACTER_SCALING), self.bottom],
        #    RIGHT_FACING: [self.left + (CHARACTER_RESOLUTION * CHARACTER_SCALING), self.bottom],
        #}
        self.switch_action = {
            DOWN_FACING:  [self.left, self.bottom - (CHARACTER_RESOLUTION // CHARACTER_SCALING) - 16],
            UP_FACING:    [self.left, self.top + 16],
            LEFT_FACING:  [self.left - (CHARACTER_RESOLUTION // CHARACTER_SCALING) - 16, self.bottom],
            RIGHT_FACING: [self.right + 16, self.bottom],
        }
        self.action_sprite.left   = self.switch_action.get(int(self.character_face_direction))[0]
        self.action_sprite.bottom = self.switch_action.get(int(self.character_face_direction))[1]

        # Idle animation
        if not self.character_moving:
            self.texture = self.facingdict.get(self.character_face_direction)[0]
            return

        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.facingdict.get(self.character_face_direction)[frame]

        # Walking animation
        framecount = 4 * UPDATES_PER_FRAME - 1
        if self.cur_texture >= framecount:
            self.cur_texture = 0

        self.cur_texture += 1

    def interact(self, game):
        #TODO: make this less shitcode
        interactions = self.action_sprite.collides_with_list(game.active_characters)    
        if interactions:
            switch_face = {
                DOWN_FACING:  UP_FACING,
                UP_FACING:    DOWN_FACING,
                LEFT_FACING:  RIGHT_FACING,
                RIGHT_FACING: LEFT_FACING,
            }
            interactions[0].character_face_direction =  switch_face.get(self.character_face_direction)

        interactions += self.action_sprite.collides_with_list(game.activemap.map_dict.get("message_layer"))
        if interactions:
            game.dialog.setMessage(name=interactions[0].properties.get('display_name', None),
                                   message=[interactions[0].properties.get('text', "")
                                       ])


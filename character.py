import arcade

MAIN_PATH="images/sprites/"
CHARACTER_SCALING = 1
CHARACTER_RESOLUTION = 32
UPDATES_PER_FRAME = 10

#Facing constants
DOWN_FACING = 0
UP_FACING = 1
LEFT_FACING = 2
RIGHT_FACING = 3

#Character constants
NERD = 0
OLD_MAN = 1
YOUNG_GIRL = 2

def get_y_value(npc):
    return npc.center_y

def order_npc(npc_list):
    if len(npc_list) <=1:
        return npc_list

    ordered_spritelist = arcade.SpriteList(use_spatial_hash=False)

    ordered_list = []

    for npc in npc_list:
        ordered_list.append(npc)
    print(len(ordered_list))

    ordered_list.sort(key=get_y_value)

    for npc in ordered_list:
        ordered_spritelist.append(npc)

    return ordered_spritelist

def sort_spritelist(sprite_list, key=None):
    sprite_list.sprite_list = sorted(sprite_list.sprite_list, key=key, reverse=True)
    for idx, sprite in enumerate(sprite_list.sprite_list):
        sprite_list.sprite_idx[sprite] = idx
    sprite_list._vao1 = None


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
    def __init__(self, character):

        # Set up parent class
        super().__init__()

        # Default to face-down
        self.character_face_direction = DOWN_FACING
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
        self.action_sprite = arcade.Sprite(image_width=CHARACTER_RESOLUTION,
                                           image_height=CHARACTER_RESOLUTION)

        self.action_sprite.alpha = 128
        self.action_sprite.color = arcade.color.RED
        self.action_sprite.scale = CHARACTER_SCALING
        self.action_sprite.texture   = load_character_textures(f"{MAIN_PATH}/spritemap.png", self.character, DOWN_FACING)[0]
        self.action_sprite.set_hit_box([
                         [-(CHARACTER_RESOLUTION // 2),-(CHARACTER_RESOLUTION // 2)],
                         [(CHARACTER_RESOLUTION // 2),-(CHARACTER_RESOLUTION // 2)], 
                         [(CHARACTER_RESOLUTION // 2),-(CHARACTER_RESOLUTION)], 
                         [-(CHARACTER_RESOLUTION // 2),-(CHARACTER_RESOLUTION)]
                         ])


    def update_animation(self, delta_time: float = 1/60):
        # Position action sprite
        self.switch_action = {
            DOWN_FACING:  [self.left, self.bottom - CHARACTER_RESOLUTION],
            UP_FACING:    [self.left, self.bottom + CHARACTER_RESOLUTION],
            LEFT_FACING:  [self.left - CHARACTER_RESOLUTION, self.bottom],
            RIGHT_FACING: [self.left + CHARACTER_RESOLUTION, self.bottom],
        }
        self.action_sprite.left   = self.switch_action.get(self.character_face_direction)[0]
        self.action_sprite.bottom = self.switch_action.get(self.character_face_direction)[1]

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
#        interactions = self.action_sprite.collides_with_list(game.activemap.map_dict.get("npc_layer"))    
        interactions = self.action_sprite.collides_with_list(game.active_characters)    
        interactions += self.action_sprite.collides_with_list(game.activemap.map_dict.get("message_layer"))
        if interactions:
            game.dialog.setMessage(name=interactions[0].properties.get('display_name', None),
                                   message=[interactions[0].properties.get('text', "")
                                       ])

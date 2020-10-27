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


class PlayerCharacter(arcade.Sprite):
    def __init__(self, width, height, view_left, view_bottom):

        # Set up parent class
        super().__init__()

        # Center character
        self.center_x = width / 2 + view_left
        self.center_y = height / 2 + view_bottom

        # Default to face-down
        self.character_face_direction = DOWN_FACING
        self.player_moving = False

        # Select character model
        self.character = NERD

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

    def update_animation(self, delta_time: float = 1/60):
        # Idle animation
        if not self.player_moving:
            self.texture = self.facingdict.get(self.character_face_direction)[0]
            return

        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.facingdict.get(self.character_face_direction)[frame]
        #self.set_hit_box(self.texture.hit_box_points)
        self.set_hit_box([
                         [-(CHARACTER_RESOLUTION // 2 -4),-(CHARACTER_RESOLUTION // 2)],
                         [(CHARACTER_RESOLUTION // 2  -4),-(CHARACTER_RESOLUTION // 2)], 
                         [(CHARACTER_RESOLUTION // 2  -4),-(CHARACTER_RESOLUTION)], 
                         [-(CHARACTER_RESOLUTION // 2 -4),-(CHARACTER_RESOLUTION)]
                         ])

        # Walking animation
        framecount = 4 * UPDATES_PER_FRAME - 1
        if self.cur_texture >= framecount:
            self.cur_texture = 0

        self.cur_texture += 1

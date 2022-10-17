import arcade

import character

TILE_SCALING=2

def create_npc_layer(npc_layer):
    npc_rendered = arcade.SpriteList()
    for npc in npc_layer:
        character_sprite = int(npc.properties.get('sprite'))
        npc_character = character.GameCharacter(character_sprite, npc.properties)
        npc_character.center_x = npc.center_x
        npc_character.center_y = npc.center_y
        npc_rendered.append(npc_character)

    return npc_rendered

class GameMap():

    def __init__(self, mapname, basepath="maps/", custom_spawn=None):
        self.ground_layers = arcade.SpriteList()
        self.collision_layers = arcade.SpriteList()
        self.bridge_layers = arcade.SpriteList()
        self.top_layers = arcade.SpriteList()
        self.warp_layer = arcade.SpriteList()
        self.spawn_layer = arcade.SpriteList()
        self.npc_layer = arcade.SpriteList()
        npc_rendered = arcade.SpriteList()
        self.message_layer = arcade.SpriteList()

        self.map_dict = {}

        full_map_name = f'{basepath}{mapname}.tmx'
        #tmx_map = arcade.tilemap.read_tmx(full_map_name)

        layer_options = {
            "ground": {"use_spatial_hash": False},
            "grass": {"use_spatial_hash": False},
            "farm": {"use_spatial_hash": True},
            "farm_up": {"use_spatial_hash": False},
            "water": {"use_spatial_hash": True},
            "water_grass": {"use_spatial_hash": False},
            "building": {"use_spatial_hash": True},
            "building_up": {"use_spatial_hash": False},
            "building_tree": {"use_spatial_hash": True},
        }

        self.tile_map = arcade.load_tilemap(full_map_name, TILE_SCALING, layer_options)

        # Define different types of map layers
        ground_list = ["ground", "grass"]
        collision_list = ["farm", "water", "building"]
        bridge_list = ["water_grass"]
        top_list = ["farm_up", "building_up", "tree"]


        for layer in ground_list:
            maplayer = self.tile_map.sprite_lists.get(layer)
            if maplayer:
                self.ground_layers.extend(maplayer)
        for layer in collision_list:
            maplayer = self.tile_map.sprite_lists.get(layer)
            if maplayer:
                self.collision_layers.extend(maplayer)
        for layer in bridge_list:
            maplayer = self.tile_map.sprite_lists.get(layer)
            if maplayer:
                self.bridge_layers.extend(maplayer)
        for layer in top_list:
            maplayer = self.tile_map.sprite_lists.get(layer)
            if maplayer:
                self.top_layers.extend(maplayer)


        maplayer = self.tile_map.sprite_lists.get("warp")
        if maplayer:
                self.warp_layer.extend(maplayer)

        maplayer = self.tile_map.sprite_lists.get("spawn")
        if maplayer:
                self.spawn_layer.extend(maplayer)

        maplayer = self.tile_map.sprite_lists.get("npc")
        if maplayer:
                self.npc_layer.extend(maplayer)

        ncp_rendered = create_npc_layer(npc_layer=self.npc_layer)

        maplayer = self.tile_map.sprite_lists.get("message")
        if maplayer:
                self.message_layer.extend(maplayer)


        if custom_spawn:
            self.spawnpoint = custom_spawn
        else:
            self.spawnpoint = [self.spawn_layer[0].center_x, self.spawn_layer[0].center_y]

        self.map_dict.update({
            'ground_layers': self.ground_layers,
            'collision_layers': self.collision_layers,
            'bridge_layers': self.bridge_layers,
            'top_layers': self.top_layers,
            'warp_layer': self.warp_layer,
            'npc_layer': create_npc_layer(npc_layer=self.npc_layer),
            'message_layer': self.message_layer,
            'spawn': self.spawnpoint,
  		})

    def LoadMap(self, game):

        game.view_left   = self.spawnpoint[0] - game.SCREEN_WIDTH / 2
        game.view_bottom = self.spawnpoint[1] - game.SCREEN_HEIGHT / 2

        arcade.set_viewport(game.view_left,
                            game.SCREEN_WIDTH + game.view_left - 1,
                            game.view_bottom,
                            game.SCREEN_HEIGHT + game.view_bottom - 1)

        game.player.center_x = game.SCREEN_WIDTH / 2 + game.view_left
        game.player.center_y = game.SCREEN_HEIGHT / 2 + game.view_bottom
        
        game.physics_engine = arcade.PhysicsEngineSimple(game.player, self.collision_layers)

        game.active_characters = self.map_dict.get("npc_layer")
        game.active_characters.append(game.player)


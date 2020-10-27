import arcade

TILE_SCALING=1


class GameMap():

    def __init__(self, mapname, basepath="maps/"):
        self.ground_layers = arcade.SpriteList()
        self.collision_layers = arcade.SpriteList()
        self.bridge_layers = arcade.SpriteList()
        self.top_layers = arcade.SpriteList()
        self.warp_layer = arcade.SpriteList()
        self.spawn_layer = arcade.SpriteList()

        self.map_dict = {}

        full_map_name = f'{basepath}{mapname}.tmx'
        tmx_map = arcade.tilemap.read_tmx(full_map_name)

        # Define different types of map layers
        ground_list = ["ground", "grass"]
        collision_list = ["farm", "water", "building"]
        bridge_list = ["water_grass"]
        top_list = ["farm_up", "building_up", "tree"]


        for layer in ground_list:
            self.ground_layers.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                      layer_name=layer,
                                                      scaling=TILE_SCALING))
        for layer in collision_list:
            self.collision_layers.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                      layer_name=layer,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True))
        for layer in bridge_list:
            self.bridge_layers.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                      layer_name=layer,
                                                      scaling=TILE_SCALING))
        for layer in top_list:
            self.top_layers.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                      layer_name=layer,
                                                      scaling=TILE_SCALING))
        self.warp_layer.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                  layer_name="warp",
                                                  scaling=TILE_SCALING))
        self.spawn_layer.extend(arcade.tilemap.process_layer(map_object=tmx_map,
                                                  layer_name="spawn",
                                                  scaling=TILE_SCALING))

        spawnpoint = [self.spawn_layer[0].center_x, self.spawn_layer[0].center_y]

        self.map_dict.update({'ground_layers': 	self.ground_layers,
			'collision_layers': 	self.collision_layers,
			'bridge_layers': 	self.bridge_layers,
			'top_layers': 		self.top_layers,
			'warp_layer': 		self.warp_layer,
			'spawn':		spawnpoint,
			})

    def LoadMap(self, game):

        arcade.set_viewport(game.view_left,
                            game.SCREEN_WIDTH + game.view_left - 1,
                            game.view_bottom,
                            game.SCREEN_HEIGHT + game.view_bottom - 1)
        
        return arcade.PhysicsEngineSimple(game.player, self.collision_layers)

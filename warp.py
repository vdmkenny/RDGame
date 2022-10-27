import arcade

import maps


def doWarp(game, mapname, basepath=None, warp_x=None, warp_y=None):
    if not basepath:
        basepath = "maps/"
    if warp_x and warp_y:
        custom_spawn = [float(warp_x), float(warp_y)]
    else:
        custom_spawn = None

    next_map = maps.GameMap(
        mapname=mapname, basepath=basepath, custom_spawn=custom_spawn
    )
    next_map.LoadMap(game)
    game.activemap = next_map

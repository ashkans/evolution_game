SETTING = dict()


SETTING['DISPLAY'] = dict(
    DOMAIN_SIZE=(100, 100),
    PARTICL_BASE_SIZE=1,
    SCALE=dict(SPEED=1, SPACE=1),
    WINDOW_RES=dict(WIDTH=840, HEIGHT=640),
    MAIN_SCREEN_RES=dict(WIDTH=600, HEIGHT=600, TOP=20, LEFT=20),
    DETAILS_SCREEN_RES=dict(WIDTH=180, HEIGHT=600, TOP=20, LEFT=640),
    FPS=60
)

SETTING['WORLD'] = dict(WIDTH=400, HEIGHT=400)

SETTING['FOOD'] = dict(APPLE=dict(INIT=100, RATE=100, ENERGY_CONTENT=10, SIZE=10))

SETTING['LOGGER'] = dict(FOLDER='log_file', ACTIVE=False)

# TODO Scale control - make self.origImage resolution updating with scale change
# TODO Add radar and rendering partially
# TODO Make it online with the ability of submitting new creature
# TODO Ability of moving objects for creatures
# TODO Add food size to config - Multiple food types
# TODO animation action list for each creature like born/eat/rotate/jump(?)
# TODO make add_food (in food.py) generic to add all the types accordingly
# TODO make game better to initialize the game based on the config file.
# TODO change the config file usage in the world.py and make it more consistent with others.
# TODO make a spawn agent to generate creature based on a user define rule. <hard>
# TODO move it to frontend / backend structure to enable change the frontend to JS in future.

# TODO IMPORTANT: Make all the foods (not moving objects) a subsurface of a new surface and just update it when (is
#  eaten/dies/changes). When something is eaten or changed, just a radious around that should be redrawn.




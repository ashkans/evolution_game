from config import SETTING
from world import World
import cProfile


w = World(setting=SETTING)

if __name__ == "__main__":
    cProfile.run('w.run()')
    #w.run()

import os


class Logger:
    def __init__(self, save_dir=None):
        if save_dir is None:
            save_dir = "./log"
        self.save_dir = save_dir

        if os.path.exists(self.save_dir):
            os.makedirs(save_dir)
        self.pop_log_var = []
        self.food_log_var = []

    def log(self, dt, pop, foods):
        self.log_food(dt, foods)
        self.log_pop(dt, pop)

    def log_food(self, dt, foods):

        pass

    def log_pop(self, dt, pop):
        pass

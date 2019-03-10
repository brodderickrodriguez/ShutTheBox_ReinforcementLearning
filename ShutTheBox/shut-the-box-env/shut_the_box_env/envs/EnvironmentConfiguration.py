# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


class EnvironmentConfiguration:
    def __init__(self):
        self.tile_range, self.number_of_dice, self.dice_sum_range, self.dice_range = None, None, None, (1, 6)
        self.type = 'NAN'


class NormalEnvironmentConfiguration(EnvironmentConfiguration):
    def __init__(self):
        super().__init__()
        self.tile_range = (1, 12)
        self.number_of_dice = 2
        self.dice_sum_range = (2, 12)
        self.type = 'normal'


class SimpleEnvironmentConfiguration(EnvironmentConfiguration):
    def __init__(self):
        super().__init__()
        self.tile_range = (1, 6)
        self.number_of_dice = 1
        self.dice_sum_range = (1, 6)
        self.type = 'simple'


env_config = SimpleEnvironmentConfiguration()
print('env config is {t}'.format(t=env_config.type))

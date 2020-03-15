from thing import Thing, Things


class Food(Thing):

    def __init__(self, **kwargs):
        print(kwargs.keys())
        if 'imgName' not in kwargs.keys():
            kwargs['imgName'] = 'square'
        Thing.__init__(self, **kwargs)

    def otherUpdates(self, dt):
        self.rotate(0.0005, dt)


class Foods(Things):
    pass


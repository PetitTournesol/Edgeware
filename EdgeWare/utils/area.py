from turtle import width


class Area:  # Area class for containing monitor info
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

    def dump(self):
        return (self.x, self.y, self.width, self.height)

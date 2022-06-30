class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, direction, length, x, y):
        self.direction = direction
        self.length =    length
        self.x =         x
        self.y =         y

    def __hash__(self):  # dictionary
        return hash((self.direction, self.length, self.x, self.y))

    def __eq__(self, other):  # intersection
        equality_bool = False

        if ((self.direction == other.direction) and
                (self.length == other.length) and
                (self.x == other.x) and
                (self.y == other.y)):
            equality_bool = True

        return equality_bool

    def __str__(self):
        return f"{self.direction} : {self.length}; {self.x}, {self.y}"

    def __repr__(self):
        direction = self.direction
        return f"Variable({direction}, {self.length}, {self.x}, {self.y})"


class Crossword():
    def __init__(self, word_dict, grid_horz, grid_vert):
        self.word_dict = word_dict
        self.grid_horz = grid_horz
        self.grid_vert = grid_vert

    def __hash__(self):
        pass




# word class / streak - start location, length, direction

# int start row, start col
# constraint - relationship between words

# intersection - constraint (letter needs to be the same)

# domain - list of strings

# create word objects
# create constraint objects

# then do constraint satisfaction

# make Variable (word class)
# store number - like 0, 1, 2
# down/across
# bool /
#

# constraint
# intersection letters
# if intersection works between variable objects - consistent
# else fails

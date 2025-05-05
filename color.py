class Colors:
    """Class for storing color constants"""
    BLACK = (0, 26, 51)
    BLUE = (51, 153, 255)
    ORANGE = (255, 153, 0)
    YELLOW = (255, 255, 77)
    RED = (230, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 179, 89)


class GameObject:
    """Base class for all game objects"""
    def __init__(self, position, radius, color):
        self.position = list(position)
        self.radius = radius
        self.color = color
    
    def draw(self, surface):
        """Draw method to be implemented by subclasses"""
        pass
    
    def update(self, dt):
        """Update method to be implemented by subclasses"""
        pass
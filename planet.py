import random
import pygame

from color import Colors, GameObject
import config


class Planet(GameObject):
    """Class representing a planet with gravity"""
    def __init__(self, position=None):
        position = position or [400, 300]
        super().__init__(position, 40, Colors.GREEN)
        self.mass = 1600
        self.active = False
    
    def draw(self, surface):
        """Draw the planet if active"""
        if self.active:
            pygame.draw.circle(surface, self.color, 
                              (int(self.position[0]), int(self.position[1])), 
                              self.radius)
    
    def activate(self, position):
        """Activate the planet at a specific position"""
        self.position = list(position)
        self.active = True
    
    def deactivate(self):
        """Deactivate the planet"""
        self.active = False


class Star:
    """Class representing background stars"""
    def __init__(self, position, is_big=False):
        self.position = position
        self.is_big = is_big
        self.lifetime = random.randint(5, 20)  # Random lifetime for twinkling effect
        self.visible = True
    
    def update(self):
        """Update star visibility to create twinkling effect"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.visible = not self.visible  # Toggle visibility
            self.lifetime = random.randint(5, 20)  # Reset lifetime
    
    @staticmethod
    def generate_stars(count, window_size):
        """Generate a list of random stars"""
        stars = []
        for _ in range(count):
            x = random.random() * window_size[0]
            y = random.random() * window_size[1]
            is_big = int(random.random() * 7) == 0
            stars.append(Star((x, y), is_big))
        return stars
    
    @staticmethod
    def update_all_stars(stars):
        """Update all stars and replace some randomly to create movement illusion"""
        window_size = config.Config.WINDOW_SIZE
        
        # Randomly replace some stars to create movement
        for i in range(len(stars)):
            # 1% chance to replace a star with a new one
            if random.random() < 0.01:
                x = random.random() * window_size[0]
                y = random.random() * window_size[1]
                is_big = int(random.random() * 7) == 0
                stars[i] = Star((x, y), is_big)
            else:
                # Update existing star
                stars[i].update()
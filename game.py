import sys
import pygame

from color import Colors
import config
from planet import Planet, Star
from spaceship import Spaceship


class Game:
    """Main game class that manages the game loop and objects"""
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode(config.Config.WINDOW_SIZE)
        pygame.display.set_caption("Space Game OOP")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.game_over_font = pygame.font.SysFont('impact, fantasy', 80, True, True)
        self.star_font = pygame.font.SysFont('impact, fantasy', 12, True, True)
        self.star_text = self.star_font.render("*", True, Colors.WHITE)
        
        # Initialize game objects
        self.ship = Spaceship([100, 200])
        self.planets = [Planet()]
        self.stars = Star.generate_stars(40, config.Config.WINDOW_SIZE)
        
        self.running = True
        self.previous_time = pygame.time.get_ticks()
    
    def process_events(self):
        """Process pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.ship.handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.planets[0].activate(event.pos)
                if event.button == 3:  # Right click
                    self.planets[0].deactivate()
    
    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        
        # Update ship position
        self.ship.update(dt, self.planets)
        
        # Update stars
        Star.update_all_stars(self.stars)
        
        # Check for collisions
        if self.ship.check_collisions(self.planets):
            self._handle_game_over()
    
    def _handle_game_over(self):
        """Handle game over state"""
        title = self.game_over_font.render("Game over", True, Colors.RED)
        self.screen.blit(title, (230, 300))
        pygame.display.flip()
        pygame.time.wait(1000)
        sys.exit()
    
    def render(self):
        """Render game objects"""
        self.screen.fill(Colors.BLACK)
        
        # Draw background stars
        for star in self.stars:
            if star.is_big and star.visible:
                self.screen.blit(self.star_text, star.position)
        
        # Draw planets and ship
        for planet in self.planets:
            planet.draw(self.screen)
        
        self.ship.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        pygame.key.set_repeat(10, 10)
        
        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(config.Config.FPS)
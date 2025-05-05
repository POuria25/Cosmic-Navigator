import math
import pygame

from color import Colors, GameObject
import config


class Spaceship(GameObject):
    """Class representing the player's spaceship"""
    def __init__(self, position):
        super().__init__(position, 15, Colors.BLUE)
        self.orientation = 0
        self.propulsion_counter = 0
        self.rotation_counter = 0
        self.mass = 1
        self.velocity = [0, 0]
        self.previous_time = 0
    
    def draw(self, surface):
        # Draw propulsion flames if active
        if self.propulsion_counter > 0 and pygame.time.get_ticks() % 2 == 0:
            self._draw_triangle(surface, Colors.YELLOW, 38, 
                               self.orientation + 21 * config.Config.PI / 20, config.Config.PI / 30)
            self._draw_triangle(surface, Colors.YELLOW, 38, 
                               self.orientation + 19 * config.Config.PI / 20, config.Config.PI / 30)
        
        # Draw ship body
        self._draw_triangle(surface, Colors.ORANGE, 23, 
                           self.orientation + config.Config.PI, config.Config.PI / 7)
        pygame.draw.circle(surface, self.color, 
                          (int(self.position[0]), int(self.position[1])), 
                          self.radius)
    
    def _draw_triangle(self, surface, color, r, a, b):
        """Helper method to draw triangular parts of the ship"""
        p = self.position
        p1 = self._polar_move(p, r, (a + b))
        p2 = self._polar_move(p, r, (a - b))
        polygon = [p, p1, p2]
        pygame.draw.polygon(surface, color, polygon)
    
    def _polar_move(self, point, distance, orientation):
        """Move a point using polar coordinates"""
        x, y = point
        x = math.cos(orientation) * distance + x
        y = math.sin(orientation) * distance + y
        return (x, y)
    
    def handle_key(self, key):
        """Handle keyboard input"""
        if key == pygame.K_RIGHT:
            self.orientation += config.Config.PI / 20
        elif key == pygame.K_LEFT:
            self.orientation -= config.Config.PI / 20
        elif key == pygame.K_UP:
            self.propulsion_counter = 3
        elif key == pygame.K_DOWN and self.rotation_counter == 0:
            self.rotation_counter = 10
            self.orientation += config.Config.PI
    
    def update(self, dt, planets):
        """Update ship position based on physics"""
        if self.propulsion_counter > 0:
            force = 0.0003
            self.propulsion_counter -= 1
        else:
            force = 0
        
        if self.rotation_counter > 0:
            self.rotation_counter -= 1
        
        force_x = force * math.cos(self.orientation)
        force_y = force * math.sin(self.orientation)
        
        # Calculate gravitational forces from all planets
        grav_force_x = 0
        grav_force_y = 0
        
        for planet in planets:
            if planet.active:
                dx = self.position[0] - planet.position[0]
                dy = self.position[1] - planet.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Apply gravitational force
                if distance > 0:  # Avoid division by zero
                    grav_force = config.Config.GRAVITY_CONSTANT * ((planet.mass * self.mass) / (distance**3))
                    grav_force_x -= grav_force * dx
                    grav_force_y -= grav_force * dy
        
        # Calculate acceleration and velocity
        ax = (force_x + grav_force_x) / self.mass
        ay = (force_y + grav_force_y) / self.mass
        
        self.velocity[0] += dt * ax
        self.velocity[1] += dt * ay
        
        # Update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        
        # Handle screen wrapping
        self._handle_borders()
    
    def _handle_borders(self):
        """Handle screen borders - wrap around effect"""
        if self.position[0] > config.Config.WINDOW_SIZE[0]:
            self.position[0] = 1
        if self.position[0] < 0:
            self.position[0] = config.Config.WINDOW_SIZE[0]
        if self.position[1] > config.Config.WINDOW_SIZE[1]:
            self.position[1] = 1
        if self.position[1] < 0:
            self.position[1] = config.Config.WINDOW_SIZE[1]
    
    def check_collisions(self, planets):
        """Check collisions with planets"""
        for planet in planets:
            if not planet.active:
                continue
                
            dx = self.position[0] - planet.position[0]
            dy = self.position[1] - planet.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if (self.radius + planet.radius) > distance:
                return True
        return False
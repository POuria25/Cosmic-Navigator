import pygame
import sys
from game import Game

def main():
    """Main entry point for the space game"""
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Create and run game
    game = Game()
    game.run()
    
    # Clean up pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
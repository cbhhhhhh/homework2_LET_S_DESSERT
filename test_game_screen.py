import pygame
import sys
from game_screen import game_screen

def main():
    pygame.init()
    
    # 设置屏幕
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Screen Test")

    # 运行游戏屏幕函数
    result = game_screen(screen, difficulty='easy')

    if result == 'game_menu':
        print("Returning to game menu.")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

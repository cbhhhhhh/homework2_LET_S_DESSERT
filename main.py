import pygame
from game_menu import game_menu
from difficulty_screen import difficulty_screen
from game_screen import game_screen
from win_screen import win_screen
from lose_screen import lose_screen
from rank_list import rank_list

def main():
    pygame.init()
    pygame.mixer.init()  # 初始化音频
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("LET'S DESSERT!")

    # 加载并播放背景音乐，-1 表示无限循环播放
    pygame.mixer.music.load("background_music.mp3")  # 替换为你的背景音乐文件路径
    pygame.mixer.music.play(-1)

    running = True
    current_screen = "game_menu"

    while running:
        if current_screen == "game_menu":
            next_screen = game_menu(screen)
            if next_screen == "start_game":
                current_screen = "difficulty_screen"
            elif next_screen == "leaderboard":
                current_screen = "rank_list"
            elif next_screen == "quit_game":
                running = False

        elif current_screen == "difficulty_screen":
            difficulty = difficulty_screen(screen)
            if difficulty:
                current_screen = game_screen(screen, difficulty)
            else:
                current_screen = "game_menu"  # 如果没有选择难度，返回主菜单

        elif current_screen == "game_screen":
            next_screen = game_screen(screen)  # 确保 `game_screen` 函数有正确的返回值
            current_screen = next_screen

        elif current_screen == "win":
            next_screen = win_screen(screen)
            if next_screen == "game_menu":
                current_screen = "win_screen"

        elif current_screen == "lose":
            next_screen = lose_screen(screen)
            if next_screen == "game_menu":
                current_screen = "lose_screen"

        elif current_screen == "rank_list":
            next_screen = rank_list(screen)
            if next_screen == "game_menu":
                current_screen = "game_menu"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()

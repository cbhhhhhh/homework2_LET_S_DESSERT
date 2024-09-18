import pygame

def game_menu(screen):
    menu_running = True
    screen_width, screen_height = screen.get_size()

    # Load the background image and scale it to fit the screen size
    menu_background = pygame.image.load('menu_background.png')
    menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

    font_background = pygame.image.load('font_background.png')

    title_font = pygame.font.Font('FascinateInline-Regular.ttf', 70)
    play_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)
    leaderboard_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)
    quit_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)

    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 100)

    BACKGROUND_WIDTH = 150
    BACKGROUND_HEIGHT = 100

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return "quit_game"  # 退出游戏
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"Clicked at: ({x}, {y})")  # 输出点击位置，用于调试
                # Check button regions
                if (screen_width // 2 - BACKGROUND_WIDTH // 2 <= x <= screen_width // 2 + BACKGROUND_WIDTH // 2 and 
                    300 <= y <= 300 + BACKGROUND_HEIGHT):
                    print("Start Game button clicked")
                    return "start_game"
                elif (screen_width // 2 - BACKGROUND_WIDTH // 2 <= x <= screen_width // 2 + BACKGROUND_WIDTH // 2 and 
                      400 <= y <= 400 + BACKGROUND_HEIGHT):
                    print("Leaderboard button clicked")
                    return "leaderboard"
                elif (screen_width // 2 - BACKGROUND_WIDTH // 2 <= x <= screen_width // 2 + BACKGROUND_WIDTH // 2 and 
                      500 <= y <= 500 + BACKGROUND_HEIGHT):
                    print("Quit Game button clicked")
                    return "quit_game"

        screen.blit(menu_background, (0, 0))

        title_text = title_font.render("LET'S DESSERT!", True, (139, 69, 19))
        play_text = play_font.render("GO!", True, (255, 192, 203))
        leaderboard_text = leaderboard_font.render("Rank", True, (255, 192, 203))
        quit_text = quit_font.render("BYE!", True, (255, 192, 203))

        play_background = pygame.transform.scale(font_background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        leaderboard_background = pygame.transform.scale(font_background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        quit_background = pygame.transform.scale(font_background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

        screen.blit(play_background, (screen_width // 2 - BACKGROUND_WIDTH // 2, 300))
        screen.blit(leaderboard_background, (screen_width // 2 - BACKGROUND_WIDTH // 2, 400))
        screen.blit(quit_background, (screen_width // 2 - BACKGROUND_WIDTH // 2, 500))

        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 300))
        screen.blit(leaderboard_text, (screen_width // 2 - leaderboard_text.get_width() // 2, 400))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 500))

        pygame.display.flip()

import pygame

def difficulty_screen(screen):
    difficulty_running = True
    screen_width, screen_height = screen.get_size()

    # Load background image
    bg_image = pygame.image.load('menu_background.png')

    # Set fonts
    title_font = pygame.font.Font('PixelifySans-Bold.ttf', 64)
    easy_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)
    hard_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)

    WHITE = (255, 255, 255)

    while difficulty_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                difficulty_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check button clicks
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and 300 <= y <= 350:
                    return "easy"
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and 400 <= y <= 450:
                    return "hard"

        # Draw background
        screen.blit(bg_image, (0, 0))

        # Render texts
        title_text = title_font.render("Select Difficulty", True, (255, 192, 203))
        easy_text = easy_font.render("Easy", True, (139, 69, 19), (255, 192, 203))
        hard_text = hard_font.render("Hard", True, (139, 69, 19), (255, 192, 203))

        # Draw texts
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(easy_text, (screen_width // 2 - easy_text.get_width() // 2, 300))
        screen.blit(hard_text, (screen_width // 2 - hard_text.get_width() // 2, 400))

        pygame.display.flip()

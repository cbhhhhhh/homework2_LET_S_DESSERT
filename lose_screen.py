import pygame

def lose_screen(screen):
    running = True
    clock = pygame.time.Clock()

    # Load your background image (make sure this is the correct image for the lose screen)
    background_image = pygame.image.load('win_screen.png').convert()  # Use a 'lose_screen' image

    # Load a custom font
    font_size = 84
    custom_font = pygame.font.Font('PixelifySans-Bold.ttf', font_size)

    # Define the Back button rectangle
    screen_width, screen_height = screen.get_size()
    back_button_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 50)
    button_font = pygame.font.Font('PixelifySans-Bold.ttf', 36)
    BUTTON_COLOR = (139, 69, 19)  # Brown color for the button
    WHITE = (255, 255, 255)

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit_game"  # Optionally handle quitting the game

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if the Back button is clicked
                if back_button_rect.collidepoint(x, y):
                    return "game_menu"  # Transition to the main menu

        # Display the background image
        screen.blit(background_image, (0, 0))

        # Display the lose message
        text = custom_font.render("GAME OVER!", True, (255, 0, 0), (255, 192, 203))  # Red text on a pink background
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        # Draw Back button
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_button_text = button_font.render("Back", True, WHITE)
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text, back_button_text_rect)

        pygame.display.flip()

    return "game_menu"  # Ensure to return to the main menu

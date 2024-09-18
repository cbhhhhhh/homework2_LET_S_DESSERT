import pygame

def win_screen(screen):
    running = True
    clock = pygame.time.Clock()

    # Load your background image
    background_image = pygame.image.load('win_screen.png').convert()

    # Load a custom font (replace 'your_font.ttf' with the actual font file path)
    font_size = 84  # Modify this to change the font size
    custom_font = pygame.font.Font('PixelifySans-Bold.ttf', font_size)  # Use custom font file, or None for default

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
                return "quit_game"  # Modify to handle quitting the game

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if the Back button is clicked
                if back_button_rect.collidepoint(x, y):
                    print("Back button clicked.")  # Debugging line
                    return "game_menu"  # Change to the identifier of your main menu screen

        # Display the background image
        screen.blit(background_image, (0, 0))  # Adjust the position as needed

        # Display the win message with black text on a pink background
        text = custom_font.render("YOU WIN!", True, (139, 69, 19), (255, 192, 203))  # Black text with pink background

        # Get the rectangle of the text and center it
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        # Draw Back button
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_button_text = button_font.render("Back", True, WHITE)
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text, back_button_text_rect)

        pygame.display.flip()

    return "game_menu"  # Return to the main menu

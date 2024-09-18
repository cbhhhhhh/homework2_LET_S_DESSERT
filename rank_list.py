import pygame

def rank_list(screen):
    list_running = True
    screen_width, screen_height = screen.get_size()

    # Load background and fonts
    list_background = pygame.image.load('rank_list_background.png')
    list_background = pygame.transform.scale(list_background, (screen_width, screen_height))

    title_font = pygame.font.Font('PixelifySans-Bold.ttf', 70)
    entry_font = pygame.font.Font('PixelifySans-Bold.ttf', 48)
    button_font = pygame.font.Font('PixelifySans-Bold.ttf', 36)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (139, 69, 19)  # Brown color for the button

    BACKGROUND_WIDTH = 150
    BACKGROUND_HEIGHT = 100

    # Load and sort the leaderboard
    entries = load_rank_list()
    entries.sort()  # Sort times in ascending order

    # Only keep the top 5 entries
    top_entries = entries[:5]

    # Define buttons rectangles
    back_button_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 50)
    clear_button_rect = pygame.Rect(screen_width - 240, screen_height - 60, 100, 50)  # Position for clear button

    while list_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                list_running = False
                return "quit_game"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if the Back button is clicked
                if back_button_rect.collidepoint(x, y):
                    return "game_menu"

                # Check if the Clear button is clicked
                if clear_button_rect.collidepoint(x, y):
                    clear_rank_list()
                    entries = load_rank_list()  # Reload to show that it's cleared
                    entries.sort()
                    top_entries = entries[:5]

        screen.blit(list_background, (0, 0))

        # Draw leaderboard title
        title_text = title_font.render("Leaderboard", True, (139, 69, 19))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 80))

        # Draw leaderboard entries
        start_y = 174  # Starting position for entries
        for i, entry in enumerate(top_entries):
            entry_text = entry_font.render(f"Rank {i + 1}: {entry:.2f}s", True, BLACK)
            screen.blit(entry_text, (screen_width // 2 - entry_text.get_width() // 2, start_y + i * 50))

        # Draw Back button
        pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_button_text = button_font.render("Back", True, WHITE)
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text, back_button_text_rect)

        # Draw Clear button
        pygame.draw.rect(screen, BUTTON_COLOR, clear_button_rect)
        clear_button_text = button_font.render("Clear", True, WHITE)
        clear_button_text_rect = clear_button_text.get_rect(center=clear_button_rect.center)
        screen.blit(clear_button_text, clear_button_text_rect)

        pygame.display.flip()

def load_rank_list():
    """Load leaderboard entries from the file."""
    try:
        with open('rank_list.csv', 'r') as f:
            lines = f.readlines()
            return [float(line.strip()) for line in lines]
    except FileNotFoundError:
        return []

def clear_rank_list():
    """Clear the leaderboard file."""
    with open('rank_list.csv', 'w') as f:
        # Just opening the file in write mode will clear its contents
        pass
    print("Leaderboard cleared.")

#game_screen.py
import pygame
import random

from win_screen import win_screen
from lose_screen import lose_screen
# 常量定义
TILE_SIZE = 70  # 图案的尺寸
MARGIN = 10  # 图案之间的间距
LAYERS = 3  # 层数
GRID_SIZE = 6  # 每层图案的网格大小
OFFSET_LAYER_1 = 0
OFFSET_LAYER_2 = 10
OFFSET_LAYER_3 = 15
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30
BG_COLOR = (255, 255, 255)
BACKGROUND_IMAGE_PATH = "game_screen_background.png"  # 背景图片路径
TIMER_DURATION = 360 # 倒计时时间
HIGHLIGHT_COLOR = (255, 255, 0)  # 发光的颜色
REARRANGE_COLOR = (139, 69, 19)  # 重排按钮的颜色
REARRANGE_RECT = pygame.Rect(20, SCREEN_HEIGHT - 70 - 10, 150, 50)  # 距离屏幕左边10像素，距离屏幕底部10像素
SHUFFLE_LIMIT = 3  # 最大重排次数
PAUSE_BUTTON_IMAGE_PATH = "pause_button.png"  # 暂停按钮图片路径
END_GAME_BUTTON_IMAGE_PATH = "exit_button.PNG"  # 结束游戏按钮图片路径

BUTTON_SIZE = 32  # 按钮的尺寸，假设为12x12像素

# 偏移量
OFFSET_Y = 20  # 调整按钮的垂直位置
LEFT_OFFSET = 40  # 调整按钮的水平位置，向左移动20像素

# 计算按钮位置
PAUSE_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - BUTTON_SIZE - 32 - LEFT_OFFSET, SCREEN_HEIGHT - BUTTON_SIZE - OFFSET_Y-20, BUTTON_SIZE, BUTTON_SIZE)
END_GAME_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - BUTTON_SIZE - 32 - LEFT_OFFSET, SCREEN_HEIGHT - 2 * BUTTON_SIZE - 58 - OFFSET_Y, BUTTON_SIZE, BUTTON_SIZE)

def load_patterns():
    """加载并返回图案"""
    patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
    return [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

def generate_layer_patterns(patterns, num_tiles):
    """为每层生成不同的图案"""
    num_patterns = len(patterns)
    num_each_pattern = max(3, (num_tiles // num_patterns) - (num_tiles // num_patterns) % 3)
    tiles = [pattern for pattern in patterns for _ in range(num_each_pattern)]
    random.shuffle(tiles)
    return tiles

def create_layer(start_x, start_y, offset_x, offset_y, tiles):
    """根据偏移量创建一层图案"""
    layer = []
    x = start_x + offset_x
    y = start_y + offset_y
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if tiles:
                tile = tiles.pop()
                rect = pygame.Rect(x + col * (TILE_SIZE + MARGIN), y + row * (TILE_SIZE + MARGIN), TILE_SIZE, TILE_SIZE)
                layer.append((tile, rect, False))
    return layer

def generate_layers(patterns):
    """生成三层卡牌排列"""
    layers = [[] for _ in range(LAYERS)]

    # 计算每层图案的总数
    num_tiles = GRID_SIZE * GRID_SIZE

    # 生成每层的卡牌图案
    all_tiles = [generate_layer_patterns(patterns, num_tiles) for _ in range(LAYERS)]

    # 计算第一层的起始位置
    start_x = (SCREEN_WIDTH - (GRID_SIZE * (TILE_SIZE + MARGIN) - MARGIN)) // 2
    start_y = (SCREEN_HEIGHT - (GRID_SIZE * (TILE_SIZE + MARGIN) - MARGIN)) // 2

    # 生成每一层的卡牌
    layers[0] = create_layer(start_x, start_y, OFFSET_LAYER_1, OFFSET_LAYER_1, all_tiles[0])
    layers[1] = create_layer(start_x, start_y, OFFSET_LAYER_2, OFFSET_LAYER_2, all_tiles[1])
    layers[2] = create_layer(start_x, start_y, OFFSET_LAYER_3, OFFSET_LAYER_3, all_tiles[2])

    return layers

def draw_buttons(screen):
    """绘制暂停和结束游戏按钮"""
    try:
        pause_button_image = pygame.image.load(PAUSE_BUTTON_IMAGE_PATH)
        end_game_button_image = pygame.image.load(END_GAME_BUTTON_IMAGE_PATH)
    except pygame.error as e:
        print(f"Error loading images: {e}")
        return
    
    screen.blit(pause_button_image, PAUSE_BUTTON_RECT.topleft)
    screen.blit(end_game_button_image, END_GAME_BUTTON_RECT.topleft)

def draw_layers(screen, layers):
    """绘制所有层次的图案"""
    for layer in layers:
        for tile, rect, is_selected in layer:
            if tile is not None:
                screen.blit(tile, rect.topleft)
                if is_selected:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 5)

def draw_rearrange_button(screen, shuffles_remaining):
    """绘制重排按钮并显示剩余重排次数"""
    pygame.draw.rect(screen, REARRANGE_COLOR, REARRANGE_RECT)  # Draw button with brown color

    # Load a custom font (replace 'custom_font.ttf' with your actual font file)
    font_size = 26 # Modify this to change the font size
    custom_font = pygame.font.Font('PixelifySans-Bold.ttf', font_size)  # Use custom font file, or None for default

    # Create the text surface with pink color
    text_surf = custom_font.render(f'Refresh ({shuffles_remaining})', True, (255,205,180))
    
    # Center the text within the button
    text_rect = text_surf.get_rect(center=REARRANGE_RECT.center)
    screen.blit(text_surf, text_rect)

def is_blocked(layers, row, col, rect):
    """检查是否被上层遮挡"""
    for upper_layer in layers[row + 1:]:
        for _, upper_rect, _ in upper_layer:
            if isinstance(upper_rect, pygame.Rect):
                if upper_rect.colliderect(rect):
                    return True
            else:
                print(f"Invalid upper_rect: {upper_rect}")
    return False

def update_blocking_status(layers):
    """更新每个图案的遮挡状态"""
    for row in range(LAYERS):
        for col in range(len(layers[row])):
            tile, rect, is_selected = layers[row][col]
            if tile is not None:
                blocked = is_blocked(layers, row, col, rect)
                layers[row][col] = (tile, rect, is_selected and not blocked)

def check_match(layers, selected):
    """检查选中的三个图案是否相同且没有被遮挡"""
    if len(selected) == 3:
        r1, c1, rect1 = selected[0]
        r2, c2, rect2 = selected[1]
        r3, c3, rect3 = selected[2]
        if (layers[r1][c1][0] == layers[r2][c2][0] == layers[r3][c3][0] and
                not is_blocked(layers, r1, c1, rect1) and
                not is_blocked(layers, r2, c2, rect2) and
                not is_blocked(layers, r3, c3, rect3)):
            # 移除选中的图案并清除发光
            for r, c in [(r1, c1), (r2, c2), (r3, c3)]:
                layers[r][c] = (None, layers[r][c][1], False)
            check_and_clear_layers(layers)
        else:
            # 如果不能消除，取消发光特效
            for r, c, _ in selected:
                tile, rect, _ = layers[r][c]
                layers[r][c] = (tile, rect, False)
        selected.clear()

def check_and_clear_layers(layers):
    """检查每一层，清除所有空图案，并更新遮挡状态"""
    for row in range(LAYERS):
        layers[row] = [t for t in layers[row] if t[0] is not None]
        for tile, rect, _ in layers[row]:
            if tile is None:
                pygame.draw.rect(screen, BG_COLOR, rect)

    update_blocking_status(layers)

def check_board_clear(layers):
    """检查游戏是否已经胜利（所有图案消除完毕）"""
    return all(tile is None for layer in layers for tile, _, _ in layer)

def handle_click(x, y, layers, selected):
    """处理鼠标点击事件，找到最下层可以被点击的图案"""
    for row in range(LAYERS - 1, -1, -1):
        for col, (tile, rect, is_selected) in enumerate(layers[row]):
            if isinstance(rect, pygame.Rect):
                if rect.collidepoint(x, y) and not is_selected and not is_blocked(layers, row, col, rect):
                    layers[row][col] = (tile, rect, True)
                    selected.append((row, col, rect))
                    check_match(layers, selected)
                    return

def shuffle_tiles(layers):
    """重排剩余图案"""
    remaining_tiles = []

    # 收集所有剩余的图案
    for row in layers:
        for tile, rect, is_selected in row:
            if tile is not None:
                remaining_tiles.append((tile, rect))  # 只收集 (tile, rect)

    random.shuffle(remaining_tiles)

    # 将重排后的图案重新分配到各层
    for row in layers:
        for i in range(len(row)):
            if row[i][0] is not None:
                # 获取一个重排后的图案
                tile, rect = remaining_tiles.pop()
                # 重新分配图案，is_selected 设为 False
                row[i] = (tile, rect, False)

    # 更新遮挡状态
    update_blocking_status(layers)

    
def game_screen(screen, difficulty='easy'):
    """游戏主循环"""
    patterns = load_patterns()
    layers = generate_layers(patterns)

    clock = pygame.time.Clock()

    try:
        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 用白色填充的背景
        background.fill(BG_COLOR)

    selected = []
    shuffle_count = SHUFFLE_LIMIT if difficulty == 'easy' else 0  # Set shuffle count based on difficulty
    countdown = TIMER_DURATION if difficulty == 'easy' else 120  # Set countdown based on difficulty
    running = True
    paused = False  # 是否暂停

    # Load a custom font (replace 'custom_font.ttf' with your actual font file)
    font_size = 36  # Modify this to change the font size
    custom_font = pygame.font.Font('PixelifySans-Bold.ttf', font_size)  # Use custom font file, or None for default

    start_time = pygame.time.get_ticks()  # 记录开始时间

    while running:
        screen.blit(background, (0, 0))  # 显示背景

        # 绘制按钮
        draw_buttons(screen)
        draw_rearrange_button(screen, shuffle_count)  # Pass the shuffle count

        # 倒计时处理
        if not paused:
            countdown -= 1 / FPS
            if countdown <= 0:
                # 计算完成时间并记录到排行榜
                end_time = pygame.time.get_ticks()
                completion_time = (end_time - start_time) / 1000  # 以秒为单位
                # 保存完成时间到排行榜文件（假设保存到一个 CSV 文件）
                save_time_to_rank_list(completion_time)
                lose_screen(screen)
                return

        # Create the countdown text with the custom font
        countdown_text = f"Time: {int(countdown)}"
        text_surf = custom_font.render(countdown_text, True, (139, 69, 19))  # Change color here
        screen.blit(text_surf, (10, 10))  # 在屏幕左上角绘制倒计时

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if REARRANGE_RECT.collidepoint(event.pos) and shuffle_count > 0:
                    shuffle_tiles(layers)
                    shuffle_count -= 1
                elif PAUSE_BUTTON_RECT.collidepoint(event.pos):
                    paused = not paused  # 切换暂停状态
                elif END_GAME_BUTTON_RECT.collidepoint(event.pos):
                    return 'game_menu'
                elif not paused:
                    handle_click(*event.pos, layers, selected)

        # 绘制图层
        draw_layers(screen, layers)

        # 检查胜利条件
        if check_board_clear(layers):
            end_time = pygame.time.get_ticks()
            completion_time = (end_time - start_time) / 1000  # 以秒为单位
            # 保存完成时间到排行榜文件（假设保存到一个 CSV 文件）
            save_time_to_rank_list(completion_time)
            win_screen(screen)
            return

        pygame.display.flip()
        clock.tick(FPS)

def save_time_to_rank_list(completion_time):
    """将完成时间保存到排行榜文件"""
    with open('rank_list.csv', 'a') as f:
        f.write(f"{completion_time}\n")

# 'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'

SCREEN_COLOR = 'gray0'
PLAYER_COLOR = 'LightGray'
SHIELD_STAGES = ['gray100', 'gray90', 'gray80', 'gray70', 'gray60', 'gray50',
                 'gray40', 'gray30', 'gray20', 'gray10']
TURTLE_COLORS = ['LightSteelBlue', 'DarkSeaGreen', 'CadetBlue', 'CornflowerBlue',
                 'MediumPurple', 'Orchid', 'IndianRed', 'Tomato', 'Chocolate',
                 'DarkOrange', 'SandyBrown', 'DarkSalmon', 'DarkKhaki']

# Method will add round number to determine color dict index:
TURTLE_COLOR_INDEX_DICT = {
    range(0, 21, 4): -1,  # Bottom row
    range(1, 22, 4): 0,  # Second row from bottom
    range(2, 23, 4): 1,  # Second row from top
    range(3, 24, 4): 2,  # Top row
}

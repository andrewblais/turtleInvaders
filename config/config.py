# 'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'

PLAYER_COLOR = 'LightGray'
SHIELD_ONE_COLOR = 'LightSlateGray'
SHIELD_TWO_COLOR = 'SlateGray'
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

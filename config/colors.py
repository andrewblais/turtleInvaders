# This module defines color constants used throughout the game for easy theme management.

# Background color for the game screen:
SCREEN_COLOR = 'gray0'

# Primary color for player elements:
PLAYER_COLOR = 'LightGray'

# Progressive damage stages for shields, represented by decreasing lightness:
SHIELD_STAGES = ['gray100', 'gray90', 'gray80', 'gray70', 'gray60', 'gray50',
                 'gray40', 'gray30', 'gray20', 'gray10']

# Colors used for different invader types, which might change per game round:
TURTLE_COLORS = ['LightSteelBlue', 'DarkSeaGreen', 'CadetBlue', 'CornflowerBlue',
                 'MediumPurple', 'Orchid', 'IndianRed', 'Tomato', 'Chocolate',
                 'DarkOrange', 'SandyBrown', 'DarkSalmon', 'DarkKhaki']

# Maps invader positions to color indices, facilitating changes in invader
#  color by game round:
TURTLE_COLOR_INDEX_DICT = {
    range(0, 21, 4): -1,  # Bottom row
    range(1, 22, 4): 0,  # Second row from bottom
    range(2, 23, 4): 1,  # Second row from top
    range(3, 24, 4): 2,  # Top row
}


def invader_get_row_index(number, game_round_current):
    """
    Determines the color index for an invader based on its position and current game round.

    :param number: The position number of the invader in its formation.
    :type number: int
    :param game_round_current: The current round of the game, affecting color selection.
    :type game_round_current: int
    :return: An index to the TURTLE_COLORS list, cycling through colors as rounds advance.
    :rtype: int
    """
    try:
        for key, value in TURTLE_COLOR_INDEX_DICT.items():
            if number in key:
                return (value + game_round_current) % len(TURTLE_COLORS)
    except (Exception, ValueError):
        return 0  # Default to the first color if any error occurs.

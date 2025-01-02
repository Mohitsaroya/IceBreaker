# ICEBREAKER
This is a game I made as a project in my CMPT 103 course. 
Brief Description and Rules of the Game:

	description:

		The icebreaker game involves participants taking turns introducing themselves to the group. This often includes sharing specific information or answering predetermined questions. The game may also incorporate group activities or challenges to promote collaboration and communication among participants. Time limits are commonly set for each interaction, maintaining a brisk pace and ensuring equal participation. The primary objective is to facilitate introductions and create a dynamic and engaging atmosphere within the group.

	Rules:
		The game commences with one player making a move on the board. Players are allowed to move in vertical, horizontal, or diagonal directions on the grid by one box. After each move, the player must "break the ice" by making one box on the grid inaccessible. Subsequently, the second player takes their turn and similarly breaks the ice following their move. The game progresses until one player becomes trapped, signifying that they are surrounded by broken ice and cannot execute a valid move. In such a scenario, the player who can still make a move is declared the winner.


GameWindow Class:
    The GameWindow class represents the main game window where the game is displayed.

    Attributes:

        BOX_SIZE: Constant representing the size of each game box.
        GAP: Constant representing the gap between game boxes.
    
    Methods:

        __init__(self, title, width, height, x_location=50, y_location=50): Initializes the game window with a specified title, width, height, and optional initial location.
        wait_until_close(self): Waits until the user closes the game window.
        draw_boxes(self): Draws the game grid with white boxes.
        get_clicked_box(self, mouse_x, mouse_y): Returns the coordinates of the clicked box based on mouse coordinates.
        is_player_trapped(self, player_index): Checks if the player is trapped or not.
	handle_click(self, click_point): Handles mouse clicks, updates the display, checks if the quit button or reset button is clicked, controls the players' moves on the board, and closes the game when one of the players gets trapped.
        message_display(self, message): Writes message at the bottom left corner
	player_info_message(self, message, col, row): Displays the player's co-ordinates and the message to move when it's their turn to move, otherwise any other message
	handle_quit_button(self): Handles the quit button click, prompting the user for confirmation and closing the window.
        is_player_overlap(self, position): Checks if the player is overlapping or not
	display_message(self, message): Displays a message at the bottom of the game window.
        reset_game(self): Resets the game state and displays a "Reset" message.

Player Class:
    The Player class represents a player in the game.

    Attributes:

        game_win: Reference to the GameWindow instance.
        position: Player's current position on the game grid.
        radius: Radius of the player's circle.
        color: Color of the player's circle.
        circle: Graphics circle representing the player on the game window.
    
    Methods:

        __init__(self, game_win, position, color): Initializes a player with a specified game window, position, and color.
        get_center(self): Computes the center coordinates for the player's circle on the game window.
	can_move_to(self, position): Checks if the player can move to the specified position on the game grid.
	move_to(self, position): Moves the player's circle to the specified position on the game window.
	

Button Class:
    The Button class represents a clickable button in the game window.

    Attributes:

        game_win: Reference to the GameWindow instance.
        label: Text label for the button.
        width, height: Dimensions of the button.
        center: Center coordinates of the button.
        rectangle: Graphics rectangle representing the button.
        labelText: Text label for the button.
    
    Methods:

        __init__(self, game_win, label, width, height, center, callback): Initializes a button with a specified game window, label, dimensions, center, and callback function.
        is_clicked(self, click_point): Checks if the button is clicked based on mouse coordinates.
        perform_action_if_clicked(self, click_point): Calls the callback function if the button is clicked.


StartWindow (GraphWin) class:
    Represents the starting window of the game.

    Attributes:

        title (str): The title of the window.
        width (int): The width of the window.
        height (int): The height of the window.

    Methods:

        __init__(self, title, width, height): Initializes a StartWindow object.
        draw_decorations(self): Draws decorative elements on the StartWindow.
        start_game(self): Closes the StartWindow to start the game.
        exit_game(self): Closes the StartWindow to exit the game.
        

EndWindow(StartWindow):
    Represents the ending window of the game, inheriting from StartWindow.
    
    __init__(self, title, width, height, scoreboard): Initializes an EndWindow object.
    draw_scoreboard(self): Draws the scoreboard on the EndWindow.
    get_scoreboard_text(self): Generates the text for the scoreboard.



Global variables:

    start_win (StartWindow):

        Type: Start Window
        Purpose: Represents an instance of the StartWindow class, serving as the starting window where the start game and exit game buttons are displayed under the heading of the game.

    start_button (Button):
    
        Type: Button
        Purpose: Represents an instance of the Button class for the start button in the start game window.

    exit_button (Button):
    
        Type: Button
        Purpose: Represents an instance of the Button class for the exit button in the start game window.

    game_win (GameWindow):

        Type: Game Window
        Purpose: Represents an instance of the GameWindow class, serving as the main game window where the game is displayed.
    
    reset_button (Button):

        Type: Button
        Purpose: Represents an instance of the Button class for the reset button in the game window.
    
    quit_button (Button):

        Type: Button
        Purpose: Represents an instance of the Button class for the quit button in the game window.

    end_win (EndWindow):

        Type: End Window
        Purpose: Represents an instance of the EndWindow class, serving as the ending window where the play again and exit game buttons are displayed under the scoreboard of the game.

    play_again_button (Button):
    
        Type: Button
        Purpose: Represents an instance of the Button class for the play again button in the end game window.

    exit_button (Button):
    
        Type: Button
        Purpose: Represents an instance of the Button class for the exit button in the end-game window.


Program Constants:
    BOX_SIZE:

        Type: int
        Purpose: Represents the size of each game box on the grid.

    GAP:

        Type: int
        Purpose: Signifies the gap between game boxes in the grid.

    QUIT_BUTTON_CLICK_COUNT:

        Type: int
        Purpose: Tracks the number of times the quit button is clicked, used for handling quitting confirmation.

    DEFAULT_PLAYER_POSITIONS:

        Type: tuple
        Purpose: Contains the default starting positions for the players on the game grid.

    PLAYER_COLORS:

        Type: list of str
        Purpose: Holds the colors assigned to each player in the game.

    BUTTON_WIDTH:

        Type: int
        Purpose: Specify the width of the buttons in the game window.

    BUTTON_HEIGHT:

        Type: int
        Purpose: Specifies the height of the buttons in the game window.

    BUTTON_RESET_POSITION:

        Type: Point (from graphics module)
        Purpose: Represents the position of the reset button on the game window.

    BUTTON_QUIT_POSITION:

        Type: Point (from graphics module)
        Purpose: Represents the position of the quit button on the game window.

Main Execution:

	The main execution part of the script creates an instance of the GameWindow class named game_win along with buttons (reset_button and quit_button) using the Button class. The script then enters a loop waiting for user input and calls methods to handle the input. The program implements a simple interactive game window with buttons and player objects, organized using object-oriented principles.

REFERENCES:

	Graphics.py version 5: http://mcsp.wartburg.edu/zelle/python/

	Graphics Reference pdf: http://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf
 
	Graphics Reference online: http://mcsp.wartburg.edu/zelle/python/graphics/graphics/index.html
 
	Geeks for Geeks: https://www.geeksforgeeks.org/python-programming-language/?ref=shm_outind
	

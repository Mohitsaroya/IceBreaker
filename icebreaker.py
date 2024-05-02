import time
from graphics import *

class GameWindow(GraphWin):
    """
    Represents the main game window for the Icebreaker game.

    Attributes:
    - BOX_SIZE (int): Size of each box in the game grid.
    - GAP (int): Gap between boxes in the game grid.
    """
    BOX_SIZE = 70
    GAP = 10

    def __init__(self, title, width, height, x_location=50, y_location=50):
        """
        Initializes the game window.

        Parameters:
        - title (str): Title of the game window.
        - width (int): Width of the game window.
        - height (int): Height of the game window.
        - x_location (int, optional): X-coordinate of the initial window location. Defaults to 50.
        - y_location (int, optional): Y-coordinate of the initial window location. Defaults to 50.
        """
        super().__init__(title, width, height)
        self.master.geometry(f"{width}x{height}+{x_location}+{y_location}")
        self.setBackground("white")

        self.last_coordinates = None
        self.grid = self.draw_boxes()
        self.current_player = 0
        self.players = [Player(self, (0, 2), "red"), Player(self, (5, 2), "blue")]
        self.ice_boxes = set()
        
        self.player_info_text = Text(Point(100, self.getHeight() - 100), "PLAYER 0 : [0, 2]\nMOVE")
        self.player_info_text.setSize(14)
        self.player_info_text.draw(self)

        self.bottom_left_text = Text(Point(100, self.getHeight() - 40), "Mouse")
        self.bottom_left_text.setSize(14)
        self.bottom_left_text.draw(self)

        self.quit_button_click_count = 0


    def wait_until_close(self):
        """
        Enters a loop waiting for the user to close the game window.
        """
        try:
            while True:
                self.checkMouse()
        except GraphicsError:
            pass

    def draw_boxes(self):
        """
        Draws the game grid with white boxes.

        Returns:
        - grid (list of list of Rectangle): The grid of box elements.
        """
        total_width = 6 * self.BOX_SIZE + 5 * self.GAP
        start_x = (self.getWidth() - total_width) // 2
        start_y = 10

        grid = []
        for row in range(5):
            row_boxes = []
            for col in range(6):
                box = Rectangle(
                    Point(start_x + col * (self.BOX_SIZE + self.GAP), start_y + row * (self.BOX_SIZE + self.GAP)),
                    Point(start_x + (col + 1) * self.BOX_SIZE + col * self.GAP,
                          start_y + (row + 1) * self.BOX_SIZE + row * self.GAP)
                )
                row_boxes.append(box)
                box.setOutline("black")
                box.setFill(color_rgb(200, 255, 255))
                box.draw(self)
            grid.append(row_boxes)

        return grid

    def get_clicked_box(self, mouse_x, mouse_y):
        """
        Returns the coordinates of the clicked box based on mouse coordinates.

        Parameters:
        - mouse_x (float): X-coordinate of the mouse click.
        - mouse_y (float): Y-coordinate of the mouse click.

        Returns:
        - box_coordinates (tuple or None): Tuple containing the coordinates of the clicked box, or None if not clicked on a box.
        """
        for row_index, row in enumerate(self.grid):
            for col_index, box in enumerate(row):
                if box.getP1().getX() <= mouse_x <= box.getP2().getX() and \
                   box.getP1().getY() <= mouse_y <= box.getP2().getY():
                    return col_index, row_index
        return None

    def is_player_trapped(self, player_index):
        """
        Checks if the player is trapped or not
        
        Parameters:
        - player_index (point): 
        Returns:
        - bool: True if the player is trapped, False otherwise.
        """
        player = self.players[player_index]
        x, y = player.position
        surrounded_by_blocks = all(
            (x + dx, y + dy) in self.ice_boxes or (x + dx, y + dy) == player.position or not player.can_move_to((x + dx, y + dy))
            for dx in [-1, 0, 1] for dy in [-1, 0, 1]
            if (dx, dy) != (0, 0) and 0 <= x + dx < 6 and 0 <= y + dy < 5
        )
        return surrounded_by_blocks

    def handle_click(self, click_point):
        """
         Handles mouse clicks, updates the display, and checks if the quit button or reset button is clicked, controls the players' moves on the board and closes the game when one of the players gets trapped.

        Parameters:
        - click_point (Point): The point representing the mouse click.
        """
        if click_point:
            self.bottom_left_text.undraw()
            box_coordinates = self.get_clicked_box(click_point.getX(), click_point.getY())

            if box_coordinates:
                col, row = box_coordinates

                if self.last_coordinates is None:
                    self.last_coordinates = (col, row)

                    if not self.players[self.current_player].can_move_to((col, row)):
                        self.message_display("INVALID")
                        self.last_coordinates = None
                        return

                    self.players[self.current_player].move_to((col, row))
                    self.player_info_message("BREAK ICE", col, row)

                else:
                    if (col, row) in self.ice_boxes or (col, row) == self.last_coordinates or self.is_player_overlap((col, row)):
                        self.message_display('INVALID')

                    else:
                        self.ice_boxes.add((col, row))
                        self.grid[row][col].setFill(color_rgb(0, 255, 255))
                        self.current_player = 1 - self.current_player

                        if not self.is_player_trapped(self.current_player):
                            self.message_display(f"ice broken at ({col}, {row})")

                        if self.is_player_trapped(self.current_player):
                            
                            self.message_display(f"PLAYER {self.current_player} TRAPPED!!")
                            time.sleep(2)
                            self.close()
                            return

                        self.last_coordinates = None
                        player = self.players[self.current_player]
                        col, row = player.position
                        self.player_info_message("MOVE", col, row)

            elif quit_button.is_clicked(click_point):
                self.handle_quit_button()

    def message_display(self, message):
        """
        Writes messsage at the bottom left corner
        
        Parameters:
        - message (str): the message that the players may want to see.
        """
        self.bottom_left_text = Text(self.bottom_left_text.getAnchor(), message)
        self.bottom_left_text.setSize(14)
        self.bottom_left_text.draw(self)

    def player_info_message(self, message, col, row):
        """
        Displays the player's co-ordinates and the message to move when its their turn to move, otherwise any other message
        
        Parameters:
        - message (str): the message that the players may want to see.
        - col (int): the column number
        - row (int): the row number
        """
        self.player_info_text.undraw()
        if message == 'MOVE':
            self.player_info_text = Text(Point(100, self.getHeight() - 100), f"PLAYER {self.current_player}: [{col},{row}]\n{message}")
        else:
            self.player_info_text = Text(Point(100, self.getHeight() - 100), f"PLAYER {self.current_player}\n{message}")

        self.player_info_text.setSize(14)
        self.player_info_text.draw(self)

    def handle_quit_button(self):
        """
        Handles the quit button click, initiating a confirmation process.
        """
        self.quit_button_click_count += 1

        if self.quit_button_click_count == 1:
            self.message_display("Are you sure?")
        elif self.quit_button_click_count == 2:
            self.message_display("Bye")
            time.sleep(1)
            self.close()

    def is_player_overlap(self, position):
        '''
        Checks if the player is overlapping or not
        
        Parameters:
        - position (point): the location of the player on the grid
        
        Returns:
        - bool: True if the player is trapped, else False
        '''
        x, y = position
        for player in self.players:
            if (x, y) == player.position:
                return True
        return False

    def reset_game(self):
        """
        Resets the game state and displays a "Reset" message.
        """

        self.message_display("RESET")
        self.players[0].move_to((0, 2))
        self.players[1].move_to((5, 2))
        self.current_player = 0
        self.player_info_message("MOVE", 0, 2)

        for row in self.grid:
            for box in row:
                box.setFill(color_rgb(200, 255, 255))

        self.ice_boxes = set()

        self.quit_button_click_count = 0
        self.last_coordinates = None


class Player:
    """
    Represents a player in the Icebreaker game.

    Attributes:
    - game_win (GameWindow): The game window instance.
    - position (tuple): The initial position of the player on the game grid.
    - radius (int): Radius of the player's circle.
    - color (str): The color of the player's circle.
    - circle (Circle): Graphical representation of the player.

    Methods:
    - get_center(): Computes the center coordinates for the player's circle on the game window.
    - can_move_to(position): Checks if the player can move to the specified position on the game grid.
    - move_to(position): Moves the player's circle to the specified position on the game window.
    """
    def __init__(self, game_win, position, color):
        """
        Initializes a player.

        Parameters:
        - game_win (GameWindow): The game window instance.
        - position (tuple): The initial position of the player on the game grid.
        - color (str): The color of the player's circle.
        """
        self.game_win = game_win
        self.position = position
        self.radius = 25
        self.color = color
        self.circle = Circle(self.get_center(), self.radius)
        self.circle.setFill(self.color)
        self.circle.draw(game_win)

    def get_center(self):
        """
        Computes the center coordinates for the player's circle on the game window.

        Returns:
        - center (Point): The center coordinates.
        """
        x, y = self.position
        start_x = (self.game_win.getWidth() - (6 * self.game_win.BOX_SIZE + 5 * self.game_win.GAP)) // 2
        start_y = 10
        center_x = start_x + (x + 0.45) * (self.game_win.BOX_SIZE + self.game_win.GAP)
        center_y = start_y + (y + 0.45) * (self.game_win.BOX_SIZE + self.game_win.GAP)
        return Point(center_x, center_y)

    def can_move_to(self, position):
        """
        Checks if the player can move to the specified position on the game grid.

        Parameters:
        - position (tuple): The target position (x, y) to check for movement.

        Returns:
        - bool: True if the player can move to the specified position, False otherwise.
        """
        x, y = position
        current_x, current_y = self.position
        new_position = (x, y)

        if self.game_win.is_player_overlap(new_position):
            return False

        return (
            (abs(x - current_x) == 1 and abs(y - current_y) == 0) or
            (abs(x - current_x) == 0 and abs(y - current_y) == 1) or
            (abs(x - current_x) == 1 and abs(y - current_y) == 1)
        ) and position not in self.game_win.ice_boxes

    def move_to(self, position):
        """
        Moves the player's circle to the specified position on the game window.

        Parameters:
        - position (tuple): The target position (x, y) to move the player's circle to.
        """
        self.circle.undraw()
        self.position = position
        self.circle = Circle(self.get_center(), self.radius)
        self.circle.setFill(self.color)
        self.circle.draw(self.game_win)
        

class Button:
    """
    Represents a button in the Icebreaker game.

    Attributes:
    - game_win (GameWindow): The game window instance.
    - label (str): Text label for the button.
    - center (Point): Center coordinates of the button.
    - width (int): Width of the button.
    - height (int): Height of the button.
    - rectangle (Rectangle): Graphical representation of the button.
    - labelText (Text): Text label for the button.
    - callback (function): Callback function to be executed when the button is clicked.

    Methods:
    - is_clicked(click_point): Checks if the button is clicked.
    - perform_action_if_clicked(click_point): Calls the callback function if the button is clicked.
    """
    def __init__(self, game_win, label, width, height, center, callback):
        """
        Initializes a button.

        Parameters:
        - game_win (GameWindow): The game window instance.
        - label (str): Text label for the button.
        - width (int): Width of the button.
        - height (int): Height of the button.
        - center (Point): Center coordinates of the button.
        - callback (function): Callback function to be executed when the button is clicked.
        """
        self.game_win = game_win
        self.label = label
        self.center = center
        self.width = width
        self.height = height
        self.rectangle = Rectangle(Point(center.x - width/2, center.y - height/2),
                                   Point(center.x + width/2, center.y + height/2))
        self.rectangle.setFill("lightgray")
        self.labelText = Text(center, label)
        self.labelText.setSize(12)
        self.rectangle.draw(game_win)
        self.labelText.draw(game_win)
        self.callback = callback

    def is_clicked(self, click_point):
        """
        Checks if the button is clicked.

        Parameters:
        - click_point (Point): The point representing the mouse click.

        Returns:
        - clicked (bool): True if the button is clicked, False otherwise.
        """
        return (self.center.x - self.width/2 <= click_point.getX() <= self.center.x + self.width/2 and
                self.center.y - self.height/2 <= click_point.getY() <= self.center.y + self.height/2)

    def perform_action_if_clicked(self, click_point):
        """
        Calls the callback function if the button is clicked.

        Parameters:
        - click_point (Point): The point representing the mouse click.
        """
        if self.is_clicked(click_point):
            if self.callback.__name__ != 'close':
                self.callback()


class StartWindow(GraphWin):
    """
    Represents the starting window of the game.

    Attributes:
    - title (str): The title of the window.
    - width (int): The width of the window.
    - height (int): The height of the window.
    """
    def __init__(self, title, width, height):
        """
        Initializes a StartWindow object.

        Parameters:
        - title (str): The title of the window.
        - width (int): The width of the window.
        - height (int): The height of the window.
        """
        super().__init__(title, width, height)
        self.setBackground(color_rgb(200, 255, 255))
        self.draw_decorations()

    def draw_decorations(self):
        """
        Draws decorative elements on the StartWindow.
        """
        rectangle = Rectangle(Point(50, 200), Point(self.getWidth() - 50, self.getHeight() - 200))
        rectangle.setOutline("black")
        rectangle.setWidth(2)
        rectangle.draw(self)

    def start_game(self):
        """
        Closes the StartWindow to start the game.
        """
        self.close()

    def exit_game(self):
        """
        Closes the StartWindow to exit the game.
        """
        self.close()
        
        
class EndWindow(StartWindow):
    """
    Represents the ending window of the game, inheriting from StartWindow.

    Attributes:
    - title (str): The title of the window.
    - width (int): The width of the window.
    - height (int): The height of the window.
    - scoreboard (list): A list containing scores for players.
    """
    def __init__(self, title, width, height, scoreboard):
        """
        Initializes an EndWindow object.

        Parameters:
        - title (str): The title of the window.
        - width (int): The width of the window.
        - height (int): The height of the window.
        - scoreboard (list): A list containing scores for players.
        """
        super().__init__(title, width, height)
        self.setBackground(color_rgb(0, 255, 255))
        self.scoreboard = scoreboard
        self.scoreboard_text = Text(Point(self.getWidth() / 2, 100), "")
        self.scoreboard_text.setSize(16)
        self.scoreboard_text.draw(self)
        self.draw_scoreboard()

    def draw_scoreboard(self):
        """
        Draws the scoreboard on the EndWindow.
        """
        self.scoreboard_text.setText(self.get_scoreboard_text())

    def get_scoreboard_text(self):
        """
        Generates the text for the scoreboard.

        Returns:
        - str: The text representation of the scoreboard.
        """
        return f"Player 0: {self.scoreboard[0]}\nPlayer 1: {self.scoreboard[1]}"


if __name__ == "__main__":
    """
    Main script to run the Icebreaker Game.

    This script initializes the game windows, handles user interactions,
    and manages the game loop, including starting, playing, and ending the game.
    """
    
    
    # Initialize scoreboard
    scoreboard = [0, 0]

    # Initialize StartWindow
    start_win = StartWindow("Start Game Window", 500, 600)

    # Display welcome text on StartWindow
    welcome_text = Text(Point(250, 150), "Welcome to Icebreaker Game!")
    welcome_text.setSize(20)
    about_text = Text(Point(250, 500), 'CMPT103 Milestone 3\nMade by Mohit Saroya\nstudent ID:3132683')
    about_text.setSize(15)
    about_text.setTextColor("black")
    welcome_text.setStyle("bold")
    welcome_text.setTextColor("black")
    welcome_text.draw(start_win)
    about_text.draw(start_win)

    # Initialize buttons on StartWindow
    start_button = Button(start_win, 'Start Game', 100, 40, Point(250, 270), start_win.start_game)
    exit_button = Button(start_win, 'Exit Game', 100, 40, Point(250, 350), start_win.exit_game)

    # Main loop for StartWindow interactions
    while not start_win.isClosed():
        click_point = start_win.getMouse()
        start_button.perform_action_if_clicked(click_point)
        exit_button.perform_action_if_clicked(click_point)

    # Check if the "Start Game" button is clicked
    if start_button.is_clicked(click_point):
        start_win.close()

        # Game loop for playing the game
        while True:
            game_win = GameWindow("GameWin", 500, 600)

            # Initialize buttons on GameWindow
            reset_button = Button(game_win, "Reset", 80, 30, Point(450, 450), game_win.reset_game)
            quit_button = Button(game_win, "Quit", 80, 30, Point(450, 500), game_win.close)

            # Main loop for GameWindow interactions
            while not game_win.isClosed():
                click_point = game_win.getMouse()
                game_win.handle_click(click_point)
                reset_button.perform_action_if_clicked(click_point)
                quit_button.perform_action_if_clicked(click_point)

            # Determine the winner and initialize EndWindow
            winner = game_win.wait_until_close()
            end_win = EndWindow("End Window", 500, 600, scoreboard)

            # Update scoreboard and display winner information
            if winner is not None:
                scoreboard[winner] += 1
                end_win.draw_scoreboard()
                winner_text = Text(Point(250, 500), f"Player {winner} wins!")
                winner_text.setSize(20)
                winner_text.draw(end_win)

            # Initialize buttons on EndWindow
            play_again_button = Button(end_win, 'Play Again', 100, 40, Point(250, 270), end_win.start_game)
            exit_button = Button(end_win, 'Exit Game', 100, 40, Point(250, 350), end_win.exit_game)

            # Main loop for EndWindow interactions
            while not end_win.isClosed():
                click_point = end_win.getMouse()
                play_again_button.perform_action_if_clicked(click_point)
                exit_button.perform_action_if_clicked(click_point)

            # Check if the "Exit Game" button is clicked
            if exit_button.is_clicked(click_point):
                break

    # Check if the "Exit Game" button is clicked on the StartWindow
    elif exit_button.is_clicked(click_point):
        start_win.close()

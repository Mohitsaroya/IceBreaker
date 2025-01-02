from graphics import *  # Assuming an external "graphics.py" is provided as in your code
import time


# ----------------------
# Main Game Structures
# ----------------------

class GameWindow(GraphWin):
    """
    Represents the main game window for the Icebreaker game.

    Key Responsibilities:
      - Handling rendering of the primary 5-row x 6-column grid.
      - Tracking 'ice' boxes, player positions, and movement logic.
      - Managing user interaction (clicks) and delegating to appropriate handling methods.

    Enhanced / Additional suggestions:
      1. Separated out certain logic (like tile-based movement rules) into standalone functions or
         smaller methods, for clarity.
      2. Avoided using Magic Numbers (like 5 or 6) inline, giving them meaningful constants.
      3. Provided more robust checks for invalid moves or out-of-bounds conditions.
    """

    BOX_SIZE = 70
    GAP = 10
    # Board dimension constants:
    NUM_ROWS = 5
    NUM_COLS = 6

    def __init__(self, title, width, height, x_location=50, y_location=50):
        """
        Initializes the game window and sets up the grid, players, and relevant UI text.
        """
        super().__init__(title, width, height)
        self.master.geometry(f"{width}x{height}+{x_location}+{y_location}")
        self.setBackground("white")

        # State variables
        self.last_coordinates = None
        self.grid = self._draw_boxes()
        self.current_player = 0
        self.ice_boxes = set()

        # Construct the Player objects
        self.players = [
            Player(self, (0, 2), "red"),
            Player(self, (5, 2), "blue")
        ]

        # Additional UI text
        self.player_info_text = Text(
            Point(100, self.getHeight() - 100),
            "PLAYER 0 : [0, 2]\nMOVE"
        )
        self.player_info_text.setSize(14)
        self.player_info_text.draw(self)

        self.bottom_left_text = Text(
            Point(100, self.getHeight() - 40),
            "Mouse"
        )
        self.bottom_left_text.setSize(14)
        self.bottom_left_text.draw(self)

        # Quit logic
        self.quit_button_click_count = 0

    # ---------- Window Lifecycle Utility ----------
    def wait_until_close(self):
        """
        Loops, waiting for user to close the game window,
        ignoring all input until an actual close event.
        """
        try:
            while True:
                self.checkMouse()
        except GraphicsError:
            pass

    # ---------- Grid / Box Rendering ----------
    def _draw_boxes(self):
        """
        Draws the game grid as an NxM set of rectangles.

        Returns:
            List[List[Rectangle]]: 2D array with references to each tile rectangle.
        """
        total_width = self.NUM_COLS * self.BOX_SIZE + (self.NUM_COLS - 1) * self.GAP
        start_x = (self.getWidth() - total_width) // 2
        start_y = 10

        grid = []
        for row in range(self.NUM_ROWS):
            row_boxes = []
            for col in range(self.NUM_COLS):
                x1 = start_x + col * (self.BOX_SIZE + self.GAP)
                y1 = start_y + row * (self.BOX_SIZE + self.GAP)
                x2 = x1 + self.BOX_SIZE
                y2 = y1 + self.BOX_SIZE

                box = Rectangle(Point(x1, y1), Point(x2, y2))
                box.setOutline("black")
                box.setFill(color_rgb(200, 255, 255))
                box.draw(self)
                row_boxes.append(box)
            grid.append(row_boxes)
        return grid

    def get_clicked_box(self, mouse_x, mouse_y):
        """
        Determines which (col, row) was clicked, if any.

        Returns:
            (col, row) or None
        """
        for row_index, row in enumerate(self.grid):
            for col_index, box in enumerate(row):
                # bounding corners
                if (box.getP1().getX() <= mouse_x <= box.getP2().getX() and
                        box.getP1().getY() <= mouse_y <= box.getP2().getY()):
                    return (col_index, row_index)
        return None

    # ---------- Movement / Action Logic ----------
    def is_player_trapped(self, player_index):
        """
        Check if the indicated player is trapped such that they cannot move to any valid neighbor.

        We define 'neighbor' as any adjacent or diagonal tile within 1 step in x and y directions.
        """
        player = self.players[player_index]
        x, y = player.position

        # Evaluate each neighbor cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):
                    continue  # skip checking own cell
                nx = x + dx
                ny = y + dy
                # Ensure neighbor is within grid
                if 0 <= nx < self.NUM_COLS and 0 <= ny < self.NUM_ROWS:
                    # If it's not an ice box and the move is valid, not trapped
                    if (nx, ny) not in self.ice_boxes and player.can_move_to((nx, ny)):
                        return False
        return True

    def handle_click(self, click_point):
        """
        Main click handler for the game: checks if a grid tile was clicked and processes
        game logic for movement or ice-breaking.

        The game logic is:
          - If no prior move selected, attempt to move the current player to the clicked tile.
          - Else, if the tile is different from player's new position, place ice on that tile,
            switch player, check for trap condition, etc.
        """
        if click_point:
            # clear old status text
            self.bottom_left_text.undraw()
            self.bottom_left_text.setText("")

            box_coordinates = self.get_clicked_box(click_point.getX(), click_point.getY())

            if box_coordinates:
                col, row = box_coordinates

                # First click => move
                if self.last_coordinates is None:
                    # Attempt to move current player
                    if not self.players[self.current_player].can_move_to((col, row)):
                        self.message_display("INVALID")
                        return

                    # Actually move
                    self.players[self.current_player].move_to((col, row))
                    self.player_info_message("BREAK ICE", col, row)
                    # Mark last coords
                    self.last_coordinates = (col, row)

                else:
                    # Attempt to place ice
                    if ((col, row) in self.ice_boxes or
                            (col, row) == self.last_coordinates or
                            self.is_player_overlap((col, row))):
                        self.message_display('INVALID')
                    else:
                        # Break ice at tile
                        self.ice_boxes.add((col, row))
                        self.grid[row][col].setFill(color_rgb(0, 255, 255))

                        # Switch active player
                        self.current_player = 1 - self.current_player

                        # If new player is trapped => end
                        if self.is_player_trapped(self.current_player):
                            self.message_display(f"PLAYER {self.current_player} TRAPPED!!")
                            time.sleep(2)
                            self.close()
                            return
                        else:
                            # normal
                            self.message_display(f"ice broken at ({col}, {row})")

                        # reset to None so next user click is for new move
                        self.last_coordinates = None
                        plr = self.players[self.current_player]
                        c, r = plr.position
                        self.player_info_message("MOVE", c, r)

            # Possibly handle button clicks if they are not part of the grid
            # ...
            #  Example: self.some_button.handle_click(click_point)?

    def message_display(self, message):
        """
        A quick way to show a short text message at bottom-left corner.
        """
        self.bottom_left_text.setText(message)
        self.bottom_left_text.setSize(14)
        self.bottom_left_text.draw(self)

    def player_info_message(self, message, col, row):
        """
        Displays the player's coordinates and a 'MOVE' or other status message in the player info text area.
        """
        self.player_info_text.undraw()
        if message == 'MOVE':
            display_text = f"PLAYER {self.current_player}: [{col},{row}]\n{message}"
        else:
            display_text = f"PLAYER {self.current_player}\n{message}"

        self.player_info_text.setText(display_text)
        self.player_info_text.setSize(14)
        self.player_info_text.draw(self)

    def handle_quit_button(self):
        """
        Called when a 'Quit' button is clicked: double-confirmation logic.
        """
        self.quit_button_click_count += 1

        if self.quit_button_click_count == 1:
            self.message_display("Are you sure?")
        elif self.quit_button_click_count == 2:
            self.message_display("Bye")
            time.sleep(1)
            self.close()

    def is_player_overlap(self, position):
        """
        Checks if any player's position matches 'position'.
        """
        return any(player.position == position for player in self.players)

    def reset_game(self):
        """
        Resets the board to default, including players and ice boxes.
        """
        self.message_display("RESET")
        self.players[0].move_to((0, 2))
        self.players[1].move_to((5, 2))
        self.current_player = 0
        self.player_info_message("MOVE", 0, 2)

        # Clear grid to default color
        for row in self.grid:
            for box in row:
                box.setFill(color_rgb(200, 255, 255))

        self.ice_boxes.clear()
        self.quit_button_click_count = 0
        self.last_coordinates = None


class Player:
    """
    Represents a single player in the Icebreaker game.

    Enhanced suggestions:
      - The concept of 'move range' or adjacency can be scaled if you want different rules
        for movement (like only orthonormal or including diagonals).
      - Possibly implement HP or scoring logic if needed.
    """

    def __init__(self, game_win: GameWindow, position, color):
        self.game_win = game_win
        self.position = position
        self.radius = 25
        self.color = color
        self.circle = Circle(self.get_center(), self.radius)
        self.circle.setFill(self.color)
        self.circle.draw(self.game_win)

    def get_center(self):
        """
        Calculate the screen-based center for drawing this player's circle based on self.position in grid coords.
        """
        x, y = self.position
        boxsize = self.game_win.BOX_SIZE
        gap = self.game_win.GAP

        total_width = self.game_win.NUM_COLS * boxsize + (self.game_win.NUM_COLS - 1) * gap
        start_x = (self.game_win.getWidth() - total_width) // 2
        start_y = 10

        center_x = start_x + (x + 0.45) * (boxsize + gap)
        center_y = start_y + (y + 0.45) * (boxsize + gap)
        return Point(center_x, center_y)

    def can_move_to(self, position):
        """
        Checks if the player can legally step to 'position'.
        By default, the movement allows up to 1 tile away (including diagonals).
        """
        x, y = position
        curx, cury = self.position

        # Must be within 1 step in both x and y
        dx = abs(x - curx)
        dy = abs(y - cury)

        if dx <= 1 and dy <= 1 and not (x, y) in self.game_win.ice_boxes:
            # Also ensure not the same tile as themselves and not overlapping another player
            if self.game_win.is_player_overlap(position):
                return False
            return True
        return False

    def move_to(self, position):
        """
        Actually relocates this player's circle to 'position'
        """
        self.circle.undraw()
        self.position = position
        self.circle = Circle(self.get_center(), self.radius)
        self.circle.setFill(self.color)
        self.circle.draw(self.game_win)


class Button:
    """
    A simple clickable button in the game. 
    Enhanced approach:
      - We could unify all button drawing into a single container, or keep them separate if there's a difference in logic.
    """

    def __init__(self, game_win: GraphWin, label: str, width: int, height: int, center: Point, callback):
        self.game_win = game_win
        self.label = label
        self.center = center
        self.width = width
        self.height = height
        self.rectangle = Rectangle(
            Point(center.x - width/2, center.y - height/2),
            Point(center.x + width/2, center.y + height/2)
        )
        self.rectangle.setFill("lightgray")
        self.labelText = Text(center, label)
        self.labelText.setSize(12)

        self.rectangle.draw(game_win)
        self.labelText.draw(game_win)
        self.callback = callback

    def is_clicked(self, click_point):
        """
        Return True if user clicked within button bounds.
        """
        return (self.center.x - self.width/2 <= click_point.getX() <= self.center.x + self.width/2 and
                self.center.y - self.height/2 <= click_point.getY() <= self.center.y + self.height/2)

    def perform_action_if_clicked(self, click_point):
        """
        If the button is clicked, invoke callback.
        """
        if self.is_clicked(click_point):
            self.callback()  # no argument passing, you may want to pass the click info though


# ----------------------
# Windows for Start / End
# ----------------------

class StartWindow(GraphWin):
    """
    Starting menu-like window for the game. 
    """

    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        self.setBackground(color_rgb(200, 255, 255))
        self.draw_decorations()

    def draw_decorations(self):
        """
        A placeholder method for your additional decorative shapes.
        """
        rectangle = Rectangle(Point(50, 200), Point(self.getWidth() - 50, self.getHeight() - 200))
        rectangle.setOutline("black")
        rectangle.setWidth(2)
        rectangle.draw(self)

    def start_game(self):
        """Close the start window and signal we should proceed to the main game."""
        self.close()

    def exit_game(self):
        """Close the start window entirely, signifying user wants to exit."""
        self.close()


class EndWindow(StartWindow):
    """
    Window displayed at the end of the game showing scoreboard, etc.

    Inherits from StartWindow to reuse some drawing logic.
    """

    def __init__(self, title, width, height, scoreboard):
        super().__init__(title, width, height)
        self.setBackground(color_rgb(0, 255, 255))
        self.scoreboard = scoreboard
        self.scoreboard_text = Text(Point(self.getWidth() / 2, 100), "")
        self.scoreboard_text.setSize(16)
        self.scoreboard_text.draw(self)
        self.draw_scoreboard()

    def draw_scoreboard(self):
        """
        Renders scoreboard using text. Extend with more UI elements if needed.
        """
        self.scoreboard_text.setText(self.get_scoreboard_text())

    def get_scoreboard_text(self):
        """
        Builds scoreboard string for display.

        You can expand or customize this format further.
        """
        return f"Player 0: {self.scoreboard[0]}\nPlayer 1: {self.scoreboard[1]}"


# ----------------------
# Main Script
# ----------------------

if __name__ == "__main__":
    """
    Main script controlling flow: Start -> Game -> End -> Possibly replay.
    """

    scoreboard = [0, 0]  # track results across multiple plays

    # Start Window
    start_win = StartWindow("Start Game Window", 500, 600)
    start_win.setBackground(color_rgb(200, 255, 255))

    # Display some text
    welcome_text = Text(Point(250, 150), "Welcome to Icebreaker Game!")
    welcome_text.setSize(20)
    welcome_text.setStyle("bold")
    welcome_text.setTextColor("black")
    welcome_text.draw(start_win)

    about_text = Text(Point(250, 500), 'CMPT103 Milestone 3\nMade by Mohit Saroya\nID: 3132683')
    about_text.setSize(15)
    about_text.setTextColor("black")
    about_text.draw(start_win)

    # Buttons
    start_button = Button(start_win, "Start Game", 100, 40, Point(250, 270), start_win.start_game)
    exit_button = Button(start_win, "Exit Game", 100, 40, Point(250, 350), start_win.exit_game)

    # Wait for user interactions
    while not start_win.isClosed():
        cp = start_win.getMouse()
        start_button.perform_action_if_clicked(cp)
        exit_button.perform_action_if_clicked(cp)

    # If user pressed "Start Game"
    if start_button.is_clicked(cp):
        start_win.close()

        # We can wrap in a loop for repeated plays
        while True:
            game_win = GameWindow("GameWin", 500, 600)

            # Create Reset/Quit Buttons
            reset_button = Button(game_win, "Reset", 80, 30, Point(450, 450), game_win.reset_game)
            quit_button = Button(game_win, "Quit", 80, 30, Point(450, 500), game_win.close)

            while not game_win.isClosed():
                p = game_win.getMouse()
                game_win.handle_click(p)
                reset_button.perform_action_if_clicked(p)
                quit_button.perform_action_if_clicked(p)

            # The game_win closes, possibly if a player got trapped => no direct 'winner' code is here
            # If you want to detect a 'winner', you may store that info in the game window or in scoreboard
            # For now, let's just show EndWindow each time.

            end_win = EndWindow("End Window", 500, 600, scoreboard)
            # If you have logic to find a winner, e.g. winner = 0 or 1
            # scoreboard[winner] += 1
            # end_win.draw_scoreboard()
            # winner_text = Text(Point(250, 500), f"Player {winner} wins!")
            # winner_text.setSize(20)
            # winner_text.draw(end_win)

            play_again_button = Button(end_win, 'Play Again', 100, 40, Point(250, 270), end_win.start_game)
            exit_button2 = Button(end_win, 'Exit Game', 100, 40, Point(250, 350), end_win.exit_game)

            while not end_win.isClosed():
                cpt = end_win.getMouse()
                play_again_button.perform_action_if_clicked(cpt)
                exit_button2.perform_action_if_clicked(cpt)

            if exit_button2.is_clicked(cpt):
                break

    # If user pressed "Exit" on start window
    elif exit_button.is_clicked(cp):
        start_win.close()

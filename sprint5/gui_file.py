import tkinter as tk
import json
from logic_file import SimpleMode, GeneralMode
from player_file import HumanPlayer, ComputerPlayer
from tkinter import messagebox
from tkinter import filedialog

class SOSGame():
    def __init__(self): # Major refactoring
        """Initilize instances/vairables for SOS game"""
        # Make the root window
        self._setup_start_menu()

        # Initiate Tkinter variables 
        self._initialize_game_state()

        # Process the game GUI    
        self.create_start_menu()
        self.start_menu.mainloop() 

   # -------- Private methods for create_start_menu -------- 
    def _initialize_game_state(self):
        """Initialize all the control variables for the start menu and the game state"""
        self.board_size = tk.IntVar(value=3) # starting default, lowest size available
        self.mode = tk.StringVar(value="Simple Game")

        # Player types selection
        self.blue_player_type = tk.StringVar(value="Human")
        self.red_player_type = tk.StringVar(value="Computer")

        self.game = None
        self.game_window = None
        self.board_buttons = []
        self.red_selection_labels = None
        self.blue_selection_labels = None

    def _setup_start_menu(self):
        """Sets up the tkinter root for the start menu"""
        self.start_menu = tk.Tk()
        self.start_menu.title("SOS Start Menu 👾")
        self.start_menu.config(bg="#dedbd2")
    
    def _create_board_frame(self):
        """Creates the Board size and the Game Mode selection"""

        # Board Size
        board_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Label(board_frame, text="Board Size:", bg="#dedbd2", fg="#4a5759").grid(row=0, column=0, padx=5, pady=5)
        tk.Spinbox(board_frame, from_=3, to=12, textvariable=self.board_size, width=5).grid(row=0, column=1, padx=5, pady=5)
        board_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # Game Mode 
        mode_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Label(mode_frame, text="Game Mode:", bg="#dedbd2", fg="#4a5759").grid(row=0, column=0, padx=5, pady=5)
        tk.OptionMenu(mode_frame, self.mode, "Simple Game", "General Game").grid(row=0, column=1, padx=5, pady=5)
        mode_frame.grid(row=2, column=0, columnspan=2, pady=5)

    def _create_player_type_frame(self):
        """Creates the Red and Blue Player type selection controls"""
        player_type_frame = tk.Frame(self.start_menu, bg="#dedbd2")
        player_type_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Red players type controls 
        red_type_frame = tk.Frame(player_type_frame, bd=5, relief=tk.RAISED, bg="#E9967A")
        tk.Label(red_type_frame, text="Red Player:", font=("Helvetica", 10, "bold"), bg="#E9967A").pack()
        tk.Radiobutton(red_type_frame, text="Human", variable=self.red_player_type, value="Human", bg="#E9967A").pack(anchor=tk.W)
        tk.Radiobutton(red_type_frame, text="Computer", variable=self.red_player_type, value="Computer", bg="#E9967A").pack(anchor=tk.W)
        red_type_frame.grid(row=0, column=0, padx=10)

        # Blue players type control 
        blue_type_frame = tk.Frame(player_type_frame, bd=5, relief=tk.RAISED, bg="#1E90FF")
        tk.Label(blue_type_frame, text="Blue Player:", font=("Helvetica", 10, "bold"), bg="#1E90FF").pack()
        tk.Radiobutton(blue_type_frame, text="Human", variable=self.blue_player_type, value="Human", bg="#1E90FF").pack(anchor=tk.W)
        tk.Radiobutton(blue_type_frame, text="Computer", variable=self.blue_player_type, value="Computer", bg="#1E90FF").pack(anchor=tk.W)
        blue_type_frame.grid(row=0, column=1, padx=10)
    
    def _create_start_button_frame(self):
        """Creates the start game button frame"""
        start_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Button(start_frame, text="Start Game", height=2, bg="#dedbd2", fg="#4a5759", command=self.start_game).grid(row=0, column=0, padx=5, pady=5)
        start_frame.grid(row=5, column=0, columnspan=2, pady=5)

    def create_start_menu(self):
        """Sets up the start menu button and main components"""
        for widget in self.start_menu.winfo_children():
            widget.destroy()

        title = tk.Label(self.start_menu, text="SOS Game Setup", font=("Helvetica", 10, "bold"), bg="#f7e1d7", fg="#4a5759")
        title.grid(row=0, column=0, columnspan=3, pady=5)

        # Attached the needed methods for the start menu 
        self._create_board_frame()
        self._create_player_type_frame()
        self._create_start_button_frame()

    # -------- Private methods for start_game method -------- 
    
    def _initialize_game_instance(self):
        """Create the player and game logic instance based on player selections"""
        board_size = self.board_size.get()
        red_type = self.red_player_type.get()
        blue_type = self.blue_player_type.get()
        game_mode = self.mode.get()

        red_player = HumanPlayer("Red") if red_type == "Human" else ComputerPlayer("Red")
        blue_player = HumanPlayer("Blue") if blue_type == "Human" else ComputerPlayer("Blue")

        if game_mode == "Simple Game":
            self.game = SimpleMode(board_size, blue_player, red_player)
        else:
            self.game = GeneralMode(board_size, blue_player, red_player)
        
        return red_type, blue_type

    def _setup_game_window (self):
        """Destroys the start menu window and starts the main game window"""
        self.start_menu.destroy()
        self.game_window = tk.Tk()
        self.game_window.title("SOS Game Window 🕹️")
        self.game_window.config(bg="#dedbd2")
    
    def _setup_game_board_and_visuals(self, red_type, blue_type):
        """Sets up the game board, initializes the visuals and starts computer's turn"""
        self.create_game_widgets()
        self.create_board(self.game.board.board_size)

        self.red_label.config(text=f"Red Player: ({red_type})")
        self.blue_label.config(text=f"Blue Player: ({blue_type})")

        # Initialize the visual controls by querying Human default choice to S 
        self.set_letter_selection("Red", self.game.player_red.get_letter_choice() if isinstance(self.game.player_red, HumanPlayer) else "S")
        self.set_letter_selection("Blue", self.game.player_blue.get_letter_choice() if isinstance(self.game.player_blue, HumanPlayer) else "S")
    
        self.update_turn_display()
        self.update_player_controls()

        # Start the computer's swuence if the current player is the computer 
        self.game_window.after(300, self.computer_move_sequence)
    
    def start_game(self): # Major refactor
        """Starting the game window after players enter settings for SOS Game"""
        self._setup_game_window()

        red_type, blue_type = self._initialize_game_instance()

        self._setup_game_board_and_visuals(red_type, blue_type)

        self.game_window.mainloop()
        
    def set_letter_selection (self, player_color, letter):
        """Sets the letters by players selection on Human player and update visuals"""

        if player_color == "Red":
            player = self.game.player_red
            s_button = self.red_s_button
            o_button = self.red_o_button
            display_labels = self.red_selection_label
        else:
            player = self.game.player_blue
            s_button = self.blue_s_button
            o_button = self.blue_o_button
            display_labels = self.blue_selection_label

        if isinstance(player, HumanPlayer):
            player.set_letter_choice(letter)
        else:
            return # Prevent the visual update for computer control 
        
        # Visually updates based on the state of the current player 
        current_choice = player.get_letter_choice()

        if current_choice == "S":
            s_button.config(bg="#b0c4b1", relief=tk.RAISED)
            o_button.config(bg="#dedbd2", relief=tk.SUNKEN)
        else:
            s_button.config(bg="#dedbd2", relief=tk.SUNKEN)
            o_button.config(bg="#b0c4b1", relief=tk.RAISED)

        if display_labels:
            display_labels.config(text=f"Selected Letter: {current_choice}")

    # -------- Private methods for create_game_widgets -------- 

    def _create_turn_mode_display(self):
        """Creates and packs the Turn Label and game mode label displays"""
        turn_frame = tk.Frame(self.game_window, bd=5, relief=tk.RAISED, bg="#f7e1d7")
        self.turn_label = tk.Label(turn_frame, text="...", font=("Helvetica", 16, "bold"), bg="#dedbd2", fg="#4a5759")
        self.turn_label.pack(padx=5, pady=5)
        turn_frame.pack(pady=10)

        mode_frame = tk.Frame(self.game_window, bd=3, relief=tk.RAISED, bg="#f7e1d7")
        self.mode_label = tk.Label(mode_frame, text=f"Game Mode: {self.mode.get()}", font=("Helvetica", 14, "bold"), bg="#dedbd2", fg="#4a5759")
        self.mode_label.pack(padx=5, pady=3)
        mode_frame.pack(pady=5)

    def _create_player_controls(self, color, frame_row, frame_col):
        """Create the controls such as the lables and letter buttons for a single player (either red or blue)"""

        if color == "Red":
            bg_color, accent_color = "#E9967A", "#E9967A"
            player_label_ref = "red_label"
            selection_label_ref = "red_selection_label"
            s_command = lambda: self.set_letter_selection("Red", "S")
            o_command = lambda: self.set_letter_selection("Red", "O")
        else: # For Blue
            bg_color, accent_color = "#1E90FF", "#1E90FF"
            player_label_ref = "blue_label"
            selection_label_ref = "blue_selection_label"
            s_command = lambda: self.set_letter_selection("Blue", "S")
            o_command = lambda: self.set_letter_selection("Blue", "O")
        
        controls_frame = tk.Frame(self.main_game_area_frame, bg="#dedbd2")
        controls_frame.grid(row=frame_row, column=frame_col, padx=20, pady=10, sticky=tk.N)

        player_frame = tk.Frame(controls_frame, bd=5, relief=tk.RIDGE, bg=bg_color)
        setattr(self, player_label_ref, tk.Label(player_frame, text="", bg=accent_color, fg="white", font=("Helvetica", 14, "bold")))
        getattr(self, player_label_ref).pack(padx=10, pady=5)
        player_frame.pack(pady=10)

        letter_frame = tk.Frame(controls_frame, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Label(letter_frame, text="Selected Move:", bg="#dedbd2", fg="#4a5759", font=("Helvetica", 14, "bold")).pack(side=tk.TOP, padx=5, pady=5)

        s_button = tk.Button(letter_frame, text="S", width=4, command=s_command)
        o_button = tk.Button(letter_frame, text="O", width=4, command=o_command)
        s_button.pack(side=tk.LEFT, padx=5)
        o_button.pack(side=tk.LEFT, padx=5)
        letter_frame.pack(pady=10)

        setattr(self, f"{color.lower()}_s_button", s_button)
        setattr(self, f"{color.lower()}_o_button", o_button)

        setattr(self, selection_label_ref, tk.Label(controls_frame, text=f"Selected Letter: S", bg="#dedbd2", fg="#4a5759"))
        getattr(self, selection_label_ref).pack(pady=5)
    
    def _create_board_canvas(self):
        """Creates the central canvas for the game board"""
        self.board_container = tk.Frame(self.main_game_area_frame, bg="#f7e1d7", bd=5, relief=tk.RIDGE)
        self.board_container.grid(row=0, column=1, padx=20, pady=10)

        size = (self.board_size.get()) * 75

        self.canvas = tk.Canvas(self.board_container, width=size, height=size)
        self.canvas.pack(fill="both", expand=True)
    
    def _create_bottom_buttons(self):
        """Creates the Replay, new, and exit game buttons at the bottom of window"""
        button_bottom_frame = tk.Frame(self.game_window, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Button(button_bottom_frame, text="REPLAY GAME", height=2, bg="#dedbd2", command=self.reset_game, fg="#4a5759").grid(row=0, column=0, padx=4, pady=4)
        tk.Button(button_bottom_frame, text="NEW GAME", height=2, bg="#dedbd2", command=self.start_game_from_setup, fg="#4a5759").grid(row=0, column=1, padx=4, pady=4)
        tk.Button(button_bottom_frame, text="EXIT GAME", height=2, bg="#dedbd2", command=self.game_window.destroy, fg="#4a5759").grid(row=0, column=2, padx=4, pady=4)
        button_bottom_frame.pack(pady=10)
    
    # -------- Private method for record widget --------

    def _create_record_button(self):
        """Create the record check button"""
        record_frame = tk.Frame(self.game_window, bd=5, relief=tk.RIDGE, bg="#f7e1d7")
        tk.Checkbutton(record_frame, text="RECORD", height=2, bg="#dedbd2", command=self.record_game, fg="#4a5759").grid(padx=4, pady=4)
        record_frame.pack(padx=10, pady=10)
    
    def record_game(self):
        """Saves the current game state to a file"""

        if not self.game:
            return 
        
        game_data = {
            "board_size": self.game.board.board_size,
            "game_mode": self.game.game_mode,
            "move_history": self.game.move_history
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All fies", "*.*")],
            title="Save Game Record"
        )

        if file_path:
            with open(file_path, 'w') as f: 
                json.dump(game_data, f, indent=3)
            messagebox.showinfo("Save Game", f"Game saved was successfully to {file_path}")

    def _create_replay_game_buttons(self):
        """Create the replay and next move buttons"""
        replay_frame = tk.Frame()
        pass



    def create_game_widgets(self):
        """Creates all the game widgets in the game window """
        self._create_turn_mode_display()

        # Make the frame for the game area
        self.main_game_area_frame = tk.Frame(self.game_window, bg="#dedbd2")
        self.main_game_area_frame.pack(pady=10)

        # Red player info 
        self._create_player_controls("Red", 0, 0)

        # Make the game board
        self._create_board_canvas()

        # Blue player info 
        self._create_player_controls("Blue", 0, 2)

        # Bottom game widget buttons
        self._create_bottom_buttons()

        # Record game widget button
        self._create_record_button()

    def create_board(self, size):
        """Making the button grid for the actual game board"""

        # Set up the board game variables
        self.board_buttons = []
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        cell_width = self.canvas.winfo_width() / size
        cell_height = self.canvas.winfo_height() / size

        for widget in self.canvas.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Create the board, and make the cells clickable 
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button = tk.Button(
                    master=self.canvas,
                    text="",
                    width=6, 
                    height=3,
                    bg="#f7e1d7",
                    font=("Helvetica", 20, "bold"),
                    command=lambda r=i,  c=j: self.handle_clicks(r,c))
                
                x_center = j * cell_width + cell_width / 2
                y_center = i * cell_height + cell_height / 2
                self.canvas.create_window(x_center, y_center, window=button, anchor=tk.CENTER, width=cell_width, height=cell_height)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)
    
    def _get_current_player_letter(self, current_player_color):
        """Returns the letter selected by the human player"""
        if current_player_color == "Red":
            player = self.game.player_red
        else:
            player = self.game.player_blue

        if isinstance(player, HumanPlayer):
            return player.get_letter_choice()
        
        # a fall back
        return "S"
    
    def _handle_human_turns(self, row, col, letter):
        """Processes the moves, updates visuals and starts the computer turn if need to"""
        success, _ = self.game.making_move(row, col, letter)

        if success:
            self.process_visual_updates(row, col, letter)

            if not self.game.is_game_over:
                self.update_turn_display()
                self.update_player_controls()

                # Starts the computer's turn sequence if the turn switched to the computer player 
                if isinstance(self.game.current_turn, ComputerPlayer):
                    self.game_window.after(100, self. computer_move_sequence)

    def handle_clicks(self, row, col):
        """Handles the clicks or events for Human Player on the game board"""
        
        current_player_before_move = self.game.current_turn

        # Current players clicks go through ONLY if current player is the human player 
        if not isinstance(current_player_before_move, HumanPlayer):
            return None 
        
        letter = self._get_current_player_letter(current_player_before_move.color)

        self._handle_human_turns(row, col, letter)

    def update_turn_display(self):
        """Updates turn labels and scores"""

        # Get the scores for each player 
        red_score = self.game.score_count.get("Red", 0)
        blue_score = self.game.score_count.get("Blue", 0)

        if self.game.is_game_over: # only display when game IS over
            final_text = f"Blue Score: {blue_score} || Red Score: {red_score}"

            # Prevents overwriting 
            if "GAME OVER" not in self.turn_label.cget("text"):
                self.turn_label.config(text=f"GAME OVER\n{final_text}")
            return
        
        current_player_color = self.game.current_turn.color

        turn_text = f"Current Turn: {current_player_color}\n"
        turn_text += f"Blue Score: {blue_score} || Red Score: {red_score}"

        self.turn_label.config(text=turn_text)

    def update_player_controls(self):
        """Keeps each players controls in check while opposing player makes a move"""

        current_player = self.game.current_turn

        # function to disable player controls 
        def set_the_control_state(s_btn, o_btn, enable):
            state = tk.NORMAL if enable and not self.game.is_game_over else tk.DISABLED # deliberately controls the players interactions during each turns 
            s_btn.config(state=state)
            o_btn.config(state=state)
        
        # Default setting, disable the controls for both player controls 
        set_the_control_state(self.red_s_button, self.red_o_button, False)
        set_the_control_state(self.blue_s_button, self.blue_o_button, False)

        # Enable the controls ONLY for the Human player 
        if isinstance(current_player, HumanPlayer) and not self.game.is_game_over:
            if current_player.color == "Red":
                set_the_control_state(self.red_s_button, self.red_o_button, True)
            else:
                set_the_control_state(self.blue_s_button, self.blue_o_button, True)

    def process_visual_updates(self, row, col, letter):
        """Updates the GUI game board"""

        if not (self.board_buttons and 0 <= row < len(self.board_buttons) and 0 <= col < len(self.board_buttons[0])):
            return None

        self.board_buttons[row][col].config(text=letter, state=tk.DISABLED)

        if self.game.is_game_over:
            self.end_game()

    def computer_move_sequence(self):
        """Schedules the conputer to takes its turns with a delay"""

        if self.game.is_game_over:
            self.end_game()
            return None
        
        current_player = self.game.current_turn

        # only human player controls are enabled if its both the computers turn 
        if not isinstance(current_player, ComputerPlayer):
            self.update_player_controls() 
            return None
        
        self.update_player_controls() # disable human controls

        # Schedule move with a delay 
        self.game_window.after(700, self.execute_computer_moves)

    def execute_computer_moves(self):
        """Execute the computers turn with a delay"""

        # check if game has ended while waiting for the delay 
        if self.game.is_game_over or not isinstance(self.game.current_turn, ComputerPlayer):
            self.update_player_controls()
            return None
        
        current_player = self.game.current_turn

        computer_move = current_player.get_move(self.game.board)

        if computer_move:
            row, col, letter = computer_move 
            
            success, _ = self.game.making_move(row, col, letter)

            if success:
                self.process_visual_updates(row, col, letter)
                self.update_turn_display()
                self.update_player_controls()

                # Checks the game state after computer move was done & if still computers move (aka General Mode or Computer vs Computer)
                if not self.game.is_game_over and isinstance(self.game.current_turn, ComputerPlayer):
                    self.computer_move_sequence()

                # otherwise if the turn went to the human playe , exit methods and gui will wait for the human player to make a move
            else:
                self.end_game()
        else:
            self.end_game()

    def reset_game(self):
        """Reset the game"""
 
        if self.game:
            self.game.reset()

        if self.game_window and self.game: 
            self.create_board(self.game.board.board_size)

        # update the user interface buttons/elements
        self.set_letter_selection("Red", self.game.player_red.get_letter_choice() if isinstance(self.game.player_red, HumanPlayer) else "S")
        self.set_letter_selection("Blue", self.game.player_blue.get_letter_choice() if isinstance(self.game.player_blue, HumanPlayer) else "S")

        self.update_turn_display()
        self.update_player_controls()

        # this starts the computer move seuwnce if the game setting starts with the computer turn to go first 
        self.game_window.after(700, self.computer_move_sequence)

    def end_game(self):
        """Determine the winner of the game"""

        self.update_turn_display()
        self.update_player_controls()

        winner_color = self.game.determine_winner()
        mode = self.game.game_mode

        red_score = self.game.score_count.get("Red", 0)
        blue_score = self.game.score_count.get("Blue", 0)
        final_score = f"FINAL SCORE: BLUE {blue_score} || RED SCORE: {red_score}"

        if winner_color == "Draw":
            self.turn_label.config(text=f"GAME OVER: IT'S A DRAW! ({mode})")
            messagebox.showinfo("Game Over", f"The {mode} has ended in a DRAW!\n{final_score}")
        else:
            self.turn_label.config(text=f"GAME OVER: {winner_color.upper()} WINS! ({mode})")
            messagebox.showinfo("Game Over", f"The {self.mode.get()} WINNER is: {winner_color.upper()}!\n{final_score}")
            
    def start_game_from_setup(self):
        """Exits the current game window and reopens the setup menu"""
        
        if self.game_window:
            self.game_window.destroy()
            
        SOSGame()

if __name__ == "__main__":
    SOSGame()
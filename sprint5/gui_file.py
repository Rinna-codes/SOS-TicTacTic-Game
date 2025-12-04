import tkinter as tk
from sos_logic import SimpleMode, GeneralMode
from player_class import HumanPlayer, ComputerPlayer
from tkinter import messagebox

class SOSGame():
    def __init__(self):
        """Initilize instances/vairables for SOS game"""

        # Create start_menu instances 
        self.start_menu = tk.Tk()
        self.start_menu.title("SOS Start Menu")
        self.start_menu.config(bg="#008B8B")

        # Varaibles for start_menu buttons (board size and mode)
        self.board_size = tk.IntVar(value=3) 
        self.mode = tk.StringVar(value="Simple Game")

        # For the player type (Human or Computer) selection variables 
        self.blue_player_type = tk.StringVar(value="Human")
        self.red_player_type = tk.StringVar(value="Computer")

        # To start with for letter choices
        self.red_letter_choice = tk.StringVar(value="S")
        self.blue_letter_choice = tk.StringVar(value="S")
        self.red_selection_label = None
        self.blue_selection_label = None

        self.game = None
        self.game_window = None 
        
        self.create_start_menu()
        self.start_menu.mainloop() 

    def create_start_menu(self):
        """Setting up the start menu buttons """

        for widget in self.start_menu.winfo_children():
            widget.destroy()

        # Creating the title of the start menu 
        title = tk.Label(self.start_menu, text="SOS Game Setup", font=("Helvetica", 16, "bold"), bg="#008B8B", fg="#FFFAFA")
        title.grid(row=0, column=0, columnspan=3, pady=10)

        # Making the Board Size Spinbox Selection
        board_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#20B2AA",)
        tk.Label(board_frame, text="Board Size:", bg="#FFFAFA", fg="black").grid(row=0, column=0, padx=5, pady=5)
        tk.Spinbox(board_frame, from_=3, to=10, textvariable=self.board_size, width=5).grid(row=0, column=1, padx=5, pady=5)
        board_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # Making the Game Mode Options Button
        mode_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#20B2AA")
        tk.Label(mode_frame, text="Game Mode:", bg="#FFFAFA", fg="black").grid(row=0,column=0, padx=5,pady=5)
        tk.OptionMenu(mode_frame, self.mode, "Simple Game", "General Game").grid(row=0, column=1, padx=5, pady=5)
        mode_frame.grid(row=2, column=0, columnspan=2, pady=5)

        # Plyaer Type Selections 
        player_type_frame = tk.Frame(self.start_menu, bg="#008B8B")
        player_type_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Red player type controls
        red_type_frame = tk.Frame(player_type_frame, bd=5, relief=tk.RAISED, bg="#E9967A")
        tk.Label(red_type_frame, text="Red Player:", font=("Helvetica", 10, "bold"), bg="#E9967A").pack()
        tk.Radiobutton(red_type_frame, text="Human", variable=self.red_player_type, value="Human", bg="#E9967A").pack(anchor=tk.W)
        tk.Radiobutton(red_type_frame, text="Computer", variable=self.red_player_type, value="Computer", bg="#E9967A").pack(anchor=tk.W)
        red_type_frame.grid(row=0, column=0, padx=10)

        # Blue player type controls
        blue_type_frame = tk.Frame(player_type_frame, bd=5, relief=tk.RAISED, bg="#1E90FF")
        tk.Label(blue_type_frame, text="Blue Player:", font=("Helvetica", 10, "bold"), bg="#1E90FF").pack()
        tk.Radiobutton(blue_type_frame, text="Human", variable=self.blue_player_type, value="Human", bg="#1E90FF").pack(anchor=tk.W)
        tk.Radiobutton(blue_type_frame, text="Computer", variable=self.blue_player_type, value="Computer", bg="#1E90FF").pack(anchor=tk.W)
        blue_type_frame.grid(row=0, column=1, padx=10)

        # Making the Start Game Button
        start_frame = tk.Frame(self.start_menu, bd=5, relief=tk.RIDGE, bg="#008B8B")
        tk.Button(start_frame, text="Start SOS Game", height=2, bg="#FFFAFA", fg="black", command=self.start_game).grid(row=0, column=0, padx=5, pady=5)
        start_frame.grid(row=5, column=0, columnspan=2, pady=10)
    
    def start_game(self):
        """Starting the game window after players enter settings for SOS Game"""
        self.start_menu.destroy()

        # Create the game window after set up menu 
        self.game_window = tk.Tk()
        self.game_window.title("SOS Game Window")
        self.game_window.config(bg="#008B8B")

        board_size = self.board_size.get() 

        red_type = self.red_player_type.get()
        blue_type = self.blue_player_type.get()

        red_player = HumanPlayer("Red") if red_type == "Human" else ComputerPlayer("Red")
        blue_player = HumanPlayer("Blue") if blue_type == "Human" else ComputerPlayer("Blue")
 
        game_mode = self.mode.get()

        if game_mode == "Simple Game":
            self.game = SimpleMode(board_size, blue_player, red_player)
        else:
            self.game = GeneralMode(board_size, blue_player, red_player)

        # set the the game board and widgets 
        self.board_buttons = []
        self.create_game_widgets()
        self.create_board(board_size)

        # updates the pkayer labels to show type (Human or computer)
        self.red_label.config(text=f"Red Player ({red_type})")
        self.blue_label.config(text=f"Blue Player ({blue_type})")

        # update the letter selection display
        self.set_letter_selection("Red", self.red_letter_choice.get())
        self.set_letter_selection("Blue", self.blue_letter_choice.get())
        self.update_turn_display()
        self.update_player_controls()

        # starts the computer seuqnce if the current player is now the computer + add a short delaye for rendering 
        self.game_window.after(100, self.computer_move_sequence)

        self.game_window.mainloop()
        
    def set_letter_selection (self, player_color, letter):
        """Sets the letters to players with toggle"""

        # ONLY set if the current player is human 
        if self.game and player_color == "Red" and not isinstance(self.game.player_red, HumanPlayer):
            return None
        if self.game and player_color == "Blue" and not isinstance(self.game.player_blue, HumanPlayer):
            return None

        if player_color == "Red":
            self.red_letter_choice.set(letter)
            s_btn = self.red_s_button
            o_btn = self.red_o_button
            display_labels = self.red_selection_label
        else:
            self.blue_letter_choice.set(letter)
            s_btn = self.blue_s_button
            o_btn = self.blue_o_button
            display_labels = self.blue_selection_label

        # Highlight the selected letters to show which one is picked 
        if letter == "S":
            s_btn.config(bg="#0C530C", relief=tk.RAISED)
            o_btn.config(bg="SystemButtonFace", relief=tk.SUNKEN)
        else:
            s_btn.config(bg="SystemButtonFace", relief=tk.SUNKEN)
            o_btn.config(bg="#0C530C", relief=tk.RAISED)

        if display_labels:
            display_labels.config(text=f"Selected Letter: {letter}")

    def create_game_widgets(self):
        """Creates the game widgets in game window"""

        # Turn Label
        turn_frame = tk.Frame(self.game_window, bd=5, relief=tk.RAISED, bg="#20B2AA")
        self.turn_label = tk.Label(turn_frame, text="....", font=("Helvetica", 16, "bold"), bg="#FFFAFA")
        self.turn_label.pack(padx=5, pady=5)
        turn_frame.pack(pady=10)

        # Game Mode Label 
        mode_frame  = tk.Frame(self.game_window, bd=3, relief=tk.RIDGE, bg="#008B8B")
        self.mode_label = tk.Label(mode_frame, text=f"Game Mode: {self.mode.get()}", font=("Helvetica", 14, "bold"), bg="#E0FFFF", fg="black")
        self.mode_label.pack(padx=5, pady=3)
        mode_frame.pack(pady=5)

        # Creating the frame for the game area
        main_game_area_frame = tk.Frame(self.game_window, bg="#008B8B")
        main_game_area_frame.pack(pady=10)

        # Red player Info
        red_controls_frame = tk.Frame(main_game_area_frame, bg="#008B8B")
        red_controls_frame.grid(row=0, column=0, padx=20, pady=10, sticky=tk.N)

        red_frame = tk.Frame(red_controls_frame, bd=5, relief=tk.RIDGE, bg="red")
        self.red_label = tk.Label(red_frame, text="", bg="#E9967A", fg="black", font=("Helvetica", 14, "bold"))
        self.red_label.pack(padx=10, pady=5)
        red_frame.pack(pady=10)

        red_letter_frame = tk.Frame(red_controls_frame, bd=5, relief=tk.RIDGE, bg="#20B2AA")
        tk.Label(red_letter_frame, text="Selected Move:", bg="#FFFAFA", fg="black").pack(side=tk.TOP, padx=5, pady=5)

        # Red Player toggle buttons for S or O 
        self.red_s_button = tk.Button(red_letter_frame, text="S", width=4, command=lambda: self.set_letter_selection("Red", "S"))
        self.red_o_button = tk.Button(red_letter_frame, text="O", width=4, command=lambda: self.set_letter_selection("Red", "O"))

        self.red_s_button.pack(side=tk.LEFT, padx=5)
        self.red_o_button.pack(side=tk.LEFT, padx=5)
        red_letter_frame.pack(pady=10)

        # red players selection label 
        self.red_selection_label = tk.Label(red_controls_frame, text=f"Selected Letter: {self.red_letter_choice.get()}", bg="#008B8B", fg="#FFFAFA")
        self.red_selection_label.pack(pady=5)

        # Creating the game board 
        self.board_container = tk.Frame(main_game_area_frame, bg="lightblue", bd=5, relief=tk.RIDGE)
        self.board_container.grid(row=0, column=1, padx=20, pady=10)

        # Configure the size of game board  
        size = (self.board_size.get()) * 75
        
        self.canvas = tk.Canvas(self.board_container, width=size, height=size)
        self.canvas.pack(fill="both", expand=True)

        # Blue player Info
        blue_controls_frame = tk.Frame(main_game_area_frame, bg="#008B8B")
        blue_controls_frame.grid(row=0, column=2, padx=20, pady=10, sticky=tk.N)

        blue_frame = tk.Frame(blue_controls_frame, bd=5, relief=tk.RIDGE, bg="#0000CD")
        self.blue_label = tk.Label(blue_frame, text="", bg="#1E90FF", fg="black", font=("Helvetica", 14, "bold"))
        self.blue_label.pack(padx=10, pady=5)
        blue_frame.pack(pady=10)

        blue_letter_frame = tk.Frame(blue_controls_frame, bd=5, relief=tk.RIDGE, bg="#20B2AA")
        tk.Label(blue_letter_frame, text="Selected Move:", bg="#FFFAFA", fg="black").pack(side=tk.TOP, padx=5, pady=5)

        # Blue player toggle button for S or O
        self.blue_s_button = tk.Button(blue_letter_frame, text="S", width=4, command=lambda: self.set_letter_selection("Blue", "S"))
        self.blue_o_button = tk.Button(blue_letter_frame, text="O", width=4, command=lambda: self.set_letter_selection("Blue", "O"))
        
        self.blue_s_button.pack(side=tk.LEFT, padx=5)
        self.blue_o_button.pack(side=tk.LEFT, padx=5)
        blue_letter_frame.pack(pady=10)

        # blue players selection label
        self.blue_selection_label = tk.Label(blue_controls_frame, text=f"Selected Letter: {self.blue_letter_choice.get()}", bg="#008B8B", fg="#FFFAFA")
        self.blue_selection_label.pack(pady=5)

        # Bottom Game widget buttons 
        button_bottom_frame = tk.Frame(self.game_window, bd=5, relief=tk.RIDGE, bg="#008B8B")

        tk.Button(button_bottom_frame, text="REPLAY GAME", height=2, bg="#FFFAFA", command=self.reset_game).grid(row=0, column=0, padx=4, pady=4)
        tk.Button(button_bottom_frame, text="NEW GAME", height=2, bg="#FFFAFA", command=self.start_game_from_setup).grid(row=0, column=1, padx=4, pady=4)
        tk.Button(button_bottom_frame, text="EXIT GAME", height=2, bg="#FFFAFA", command=self.game_window.destroy).grid(row=0, column=2, padx=4, pady=4)
        button_bottom_frame.pack(pady=10)

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
                    bg="white",
                    font=("Helvetica", 20, "bold"),
                    command=lambda r=i,  c=j: self.handle_clicks(r,c))
                
                x_center = j * cell_width + cell_width / 2
                y_center = i * cell_height + cell_height / 2
                self.canvas.create_window(x_center, y_center, window=button, anchor=tk.CENTER, width=cell_width, height=cell_height)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

    def handle_clicks(self, row, col):
        """Handles the clicks or events for Human Player on the game board"""
        
        current_player_before_move = self.game.current_turn

        # Current players clicks go through ONLY if current player is the human player 
        if not isinstance(current_player_before_move, HumanPlayer):
            return None 

        if current_player_before_move.color == "Red":
            letter = self.red_letter_choice.get()
        else: 
            letter = self.blue_letter_choice.get()

        success = self.game.making_move(row, col, letter)

        if success: 
            self.process_visual_updates(row, col, letter)

            if not self.game.is_game_over:
                self.update_turn_display()
                self.update_player_controls()

                current_player_before_move = self.game.current_turn

                # start the computers move sequence with a slight delay 
                if isinstance(current_player_before_move, ComputerPlayer):
                    self.game_window.after(60, self.computer_move_sequence)

    def update_turn_display(self):
        """Updates turn labels and scores"""

        # Get the scores for each player 
        red_score = self.game.score_count.get("Red", 0)
        blue_score = self.game.score_count.get("Blue", 0)

        if self.game.is_game_over:
            return None
        
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

        if self.board_buttons and 0 <= row < len(self.board_buttons) and 0 <= col < len(self.board_buttons[0]):
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
            
            success = self.game.making_move(row, col, letter)

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
        self.set_letter_selection("Red", "S")
        self.set_letter_selection("Blue", "S")
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

        if winner_color == "Draw":
            self.turn_label.config(text=f"GAME OVER: IT'S A DRAW! ({mode})")
            messagebox.showinfo("Game Over", f"The {mode} has ended in a DRAW!\nFINAL SCORE: BLUE {blue_score} || RED {red_score}")
        else:
            self.turn_label.config(text=f"GAME OVER: {winner_color.upper()} WINS! ({mode})")
            messagebox.showinfo("Game Over", f"The {self.mode.get()} WINNER is: {winner_color.upper()}!\nFINAL SCORE: BLUE {blue_score} || RED {red_score}")
            
    def start_game_from_setup(self):
        """Exits the current game window and reopens the setup menu"""
        
        if self.game_window:
            self.game_window.destroy()
            
        SOSGame()

if __name__ == "__main__":
    SOSGame()
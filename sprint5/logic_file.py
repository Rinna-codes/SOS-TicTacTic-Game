from board_file import Board
from abc import ABC, abstractmethod  

class SOSLogic(ABC):
    def __init__(self, game_board_size, player_blue, player_red):
        """Initialize instance for logic of game"""
        self.board = Board(game_board_size)
        self.player_blue = player_blue 
        self.player_red = player_red
        self.current_turn = player_blue 
        self.score_count = {self.player_blue.color : 0, self.player_red.color : 0} # sets the initial score to zero 
    
        self.is_game_over = False
        self.game_mode = ""

        self.blue_lines = []
        self.red_lines = []
    
    @abstractmethod
    def check_game_over(self):
        pass
    
    @abstractmethod
    def determine_winner(self):
        pass

    def _process_found_SOS(self, found_SOS, current_player_color):
        """Handles the score increments and the line coordinates for the current player"""

        score_made = len(found_SOS) 
        if score_made: 
            self.score_count[current_player_color] += len(found_SOS) # for that current player that made SOS pattern, increment their score
        
            if current_player_color == "Blue": # "extend" onto the end of the container
                self.blue_lines.extend(found_SOS)
            else: 
                self.red_lines.extend(found_SOS)
        
        return score_made 
    
    def _process_turn_management(self, score_made):
        """Handles the turn switching and game over is based on the game mode"""

        if self.game_mode == "Simple Game":
            if score_made: # Abides rule for Simple Game in ending when a player completes an SOS pattern
                self.is_game_over = True 
            else:
                self.switch_turn()
        elif self.game_mode == "General Game":
            if not score_made: # Abide General Game in game continues and player turn switch
                self.switch_turn()     
     
    def making_move(self, row, col, letter): # For human player, slight refactoring
        """Human Player make a move on board"""  

        # set the right variables for the current player + color 
        current_player = self.current_turn      
        current_player_color = current_player.color 

        if not self.board.is_cell_empty(row, col):
            return False, []
        
        valid_move = self.board.place(row, col, letter, current_player_color) 

        if valid_move:
            found_sos = self.board.check_for_SOS(row, col)

            # Handles the scores and line/pattern coordinates 
            score_made = self._process_found_SOS(found_sos, current_player_color)

            # Handle the turn management 
            self._process_turn_management(score_made)

            # Chekcs is the board is full
            self.check_game_over() 

            return True, found_sos
        
        return False, [] # Reached if self.board.place returns False
                
    def switch_turn(self):
        """Switch turns between players after each move"""
        self.current_turn = self.player_red if self.current_turn == self.player_blue else self.player_blue

    def reset(self):
        """Resets the game board"""
        self.board.reset() 
        self.current_turn = self.player_blue  
        self.score_count = {self.player_blue.color : 0, self.player_red.color: 0} 
        self.is_game_over = False
        self.blue_lines = []
        self.red_lines = []

class SimpleMode(SOSLogic):
    def __init__(self, game_board_size, player_blue, player_red):
        super().__init__(game_board_size, player_blue, player_red)
        self.game_mode = "Simple Game"

    def check_game_over(self):
        """Game is over the board is full"""
        if self.board.is_full():
            self.is_game_over = True 

    def determine_winner(self):
        """Simple Mode rule: First player to create an SOS pattern is the winner, otherwise draw"""
        red_score = self.score_count["Red"]
        blue_score = self.score_count["Blue"]

        if red_score > 0 and blue_score == 0: 
            return "Red" # red is the winner
        elif blue_score > 0 and red_score == 0: 
            return "Blue" # blue is the winner 
        
        return "Draw"

class GeneralMode(SOSLogic):
    def __init__(self, game_board_size, player_blue, player_red):
        super().__init__(game_board_size, player_blue, player_red)
        self.game_mode = "General Game"
    
    def check_game_over(self):
        """Game is over the board is full or players have the same score"""
        if self.board.is_full():
            self.is_game_over = True 
    
    def determine_winner(self):
        """General Mode rule: The player with the highest score (most sos patterns) wins, otherwise draw"""
        red_score = self.score_count["Red"]
        blue_score = self.score_count["Blue"]

        if red_score > blue_score: 
            return "Red" 
        elif blue_score > red_score: 
            return "Blue" 
        
        return "Draw" 
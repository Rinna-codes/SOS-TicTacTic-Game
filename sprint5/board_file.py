class Board():
    def __init__(self, board_size):
        """Initiate the 2d nested list for board"""
        self.board_size = board_size
        self.game_board = self._create_empty_board()

    def _create_empty_board(self):
        """Creates and returns a new, empty 2D nested list (board)"""
        game_board = []
        for _ in range(self.board_size):
            row = [None] * self.board_size # changed for clealiness and shorter lines
            game_board.append(row)
        return game_board

    def _is_value_coordinates(self, row, col):
        """Checks if the coordinates of the SOS patter is within the board boundaries"""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def is_cell_empty(self, row, col):
        """Checks if board cell is empty and double checks the board boundaries"""
        if not self._is_value_coordinates(row, col):
            return False
        return self.game_board[row][col] is None 

    def place(self, row, col, letter, color):
        """Place a ltter on the game board"""
        if not self.is_cell_empty(row, col):
            return False
        
        self.game_board[row][col] = (letter, color)
        return True 

    def unplace(self, row, col):
        """Remove the content of a cell, make it empty again"""
        if not self._is_value_coordinates(row, col):
            return 
        
        self.game_board[row][col] = None 

    def get_letter(self, row, col):
        """Returns the letter (S or O) from an occupied cell or None for empty cell"""
        if not self._is_value_coordinates(row, col):
            return None
        
        content = self.game_board[row][col]

        if content is not None: 
            return content[0] 
        return None
 
    def _checks_o_center_sos(self, row, col, rd, cd, found_SOS):
        """Will check for an SOS pattern when current letter "O" is in the middle"""
        s1_r, s1_c = (row - rd), (col - cd)
        s2_r, s2_c = (row + rd), (col + cd)

        s1 = self.get_letter(s1_r, s1_c) # First S in S-O-S
        s2 = self.get_letter(s2_r, s2_c) # Second S in S-O-S

        if s1 == "S" and s2 == "S":
            line_tuple = ((s1_r,s1_c), (row, col), (s2_r, s2_c))
            found_SOS.append(line_tuple)

   
   
   def check_for_SOS(self, row, col):
        """Detects an SOS and return line coordinates"""
        directions = [
            (-1, 0), (1, 0),  # Vertical (N, S)
            (0, -1), (0, 1),  # Horizontal (W,E)
            (-1, -1), (1, 1), # Diagonal 1 (NW, SE)
            (-1, 1), (1, -1) # Diagonal 2 (NE, SW) 
        ]
  
        found_SOS= [] 
        current_letter = self.get_letter(row, col)

        if current_letter is None: 
            return found_SOS

        for rd, cd in directions: # row direction = rd, cd = column direction, refactors to recognize pattern not current letter

            # Current cell is the center O 
            s1_r, s1_c = (row + rd), (col + cd) 
            s2_r, s2_c = (row - rd), (col -cd) 

            s1 = self.get_letter(s1_r, s1_c)
            s2 = self.get_letter(s2_r, s2_c)

            if current_letter == "O" and s1 == "S" and s2 == "S":
                line_tuple1 = ((s1_r, s1_c), (row, col), (s2_r, s2_c)) 
                found_SOS.append(line_tuple1)

            # Current cell is the first S 
            o1_r, o1_c = (row + rd), (col + cd) 
            s1_r, s1_c = row + (2 * rd), col + (2 * cd)

            o1 = self.get_letter(o1_r, o1_c)
            s1 = self.get_letter(s1_r, s1_c)

            if current_letter == "S" and o1 == "O" and s1 == "S":
                line_tuple2 = ((row, col), (o1_r, o1_c), (s1_r, s1_c))
                found_SOS.append(line_tuple2)

            # Current cell is the last S 
            s2_r, s2_c = row - (2 * rd), col - (2 * cd)
            o2_r, o2_c = (row - rd), (col- cd)

            s2 = self.get_letter(s2_r, s2_c)
            o2 = self.get_letter(o2_r, o2_c)

            if current_letter == "S" and s2 == "S" and o2 == "O":
                line_tuple3 = ((s2_r, s2_c), (o2_r, o2_c), (row, col))
                found_SOS.append(line_tuple3)

        return found_SOS
    
    def reset(self):
        """Resets the game board, all cells empty"""
        self.game_board = []
        for i in range(self.board_size): 
            row = []
            for j in range(self.board_size):
                row.append(None)
            self.game_board.append(row)
    
    def is_full(self):
        """Checks if the game board is filled"""
        for row in self.game_board:
            if None in row:
                return False
        return True 
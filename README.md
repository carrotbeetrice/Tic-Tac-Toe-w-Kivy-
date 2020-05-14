# Tic Tac Toe Game
A 1v1, GUI-based tic-tac-toe game between two players sharing the same screen.

## How to play
[Link to video](https://youtu.be/9wtHw00vLKU)
Each player is randomly assigned a mark, either X or O. Players take turns putting their marks in empty squares on a 3x3 grid of squares.
The first player to get 3 of their marks in a row (horizontally, vertically or diagonally) wins the round. The losing player starts the next round.
The round is over when all 9 squares are full. If neither player wins, the round ends in a draw.

## Description of code

### Draw tic-tac-toe grid
```

Builder.load_string("""
<TicTacToeBoard>:
    canvas:  
        Rectangle:
            pos: self.width / 3, 0
            size: 5, self.height
            
        Rectangle:
            pos: 2 * self.width / 3, 0
            size: 5, self.height
        
        Rectangle:
            pos: 0, self.height / 3
            size: self.width, 5
            
        Rectangle:
            pos: 0, 2 * self.height / 3
            size: self.width, 5
""")
```

Draw the tic-tac-toe grid in TicTacToeBoard by loading the kivy language with kivy Builder.

### class CellLabel
> Child class of Label

```
class CellLabel(Label):
    
    def __init__(self, game_state = 0, **kwargs):
        super(CellLabel, self).__init__(**kwargs)
        self.height = 200
        self.game_state = game_state # 1
        self.font_size = 72
        self.text = ''
        self.bind(on_touch_down=self.make_move) # 2
                
    def make_move(self, instance, touch):
        """Change empty cell's text when tapped/ clicked on"""
        if self.text == '' and self.collide_point(*touch.pos): # 3
            if self.game_state == 1:
                self.text = 'X'
            elif self.game_state == 0:
                self.text = 'O'  
```
Create a custom label to represent each square or cell in the grid.
1) The current game state corresponds to which player is currently playing on the board. (O is state 0, X is state 1)
2) Callback make_move() checks if cell is 'empty' and if position of touch is within the bounds of the cell before reflecting the player's mark on the cell. Move not reflected otherwise.

### class TicTacToeBoard
> Child class of GridLayout
```
class TicTacToeBoard(GridLayout):
    
    def __init__(self, game_state = 0, **kwargs):
        super(TicTacToeBoard, self).__init__(**kwargs)
        self.cols = 3
        self.game_state = game_state
        self.current_move = "{}'s turn".format(self.get_starting_move())
        self.last_winner = None
        
        """Creating cells"""
        self.cell_1 = CellLabel(self.game_state)
        self.cell_2 = CellLabel(self.game_state)
        self.cell_3 = CellLabel(self.game_state)
        self.cell_4 = CellLabel(self.game_state)
        self.cell_5 = CellLabel(self.game_state)
        self.cell_6 = CellLabel(self.game_state)
        self.cell_7 = CellLabel(self.game_state)
        self.cell_8 = CellLabel(self.game_state)
        self.cell_9 = CellLabel(self.game_state)
        
        """Playing grid as a nested list of the cells"""
        self.playing_grid = [[self.cell_1, self.cell_2, self.cell_3], 
                             [self.cell_4, self.cell_5, self.cell_6], 
                             [self.cell_7, self.cell_8, self.cell_9]]
        
        for row in self.playing_grid:
            for cell in row:
                cell.bind(on_touch_up=self.on_cell_touch_up)
                self.add_widget(cell)

```
Create a GridLayout containing 9 instances of CellLabel to represent the tic-tac-toe grid. 

```
    def get_starting_move(self):
        """Get initial starting move"""
        if self.game_state == 0:
            starting_move = 'X'
        else:
            starting_move = 'O'
        return starting_move
```
Determine initial move (starting player mark) based on randomised initial game state.

```
    def on_cell_touch_up(self, instance, touch):
        """Update the game state after a player has finised a move"""
        if self.collide_point(*touch.pos):
            # change the board's game state
            if self.game_state == 1:
                self.game_state = 0
                self.current_move = "X's turn"
            else:
                self.game_state = 1
                self.current_move = "O's turn"
                
            # change the game state for all cells after player has finished 
            # a move
            for row in self.playing_grid:
                for cell in row:
                    if cell.text == '': # only modifies state of empty cells
                        cell.game_state = self.game_state 
                        cell.current_move = self.current_move
            self.last_winner = self.check_for_winner()
```
The callback on_cell_touch_up() changes the game state to the next player after a player has finished their move. Also checks if any player has won or if a draw has occured.

```
    def check_for_winner(self):
        """Check if any player has won after finishing a move"""
        
        # check for row winners
        for row in self.playing_grid:
            cell_A, cell_B, cell_C = row
            if cell_A.text == cell_B.text == cell_C.text != '':
                return cell_B.text
        
        # check for column winners
        row_1, row_2, row_3 = self.playing_grid
        for col in range(0, 3):
            if row_1[col].text == row_2[col].text == row_3[col].text != '':
                return row_1[col].text
        
        # check for diagonal winners
        diagonal_wins = [row_1[0].text == row_2[1].text == row_3[2].text != '',
                         row_1[2].text == row_2[1].text == row_3[0].text != '']
        if any(diagonal_wins):
            return row_2[1].text
        
        # if no winners, check for a draw
        return self.check_for_draw()
```
Method that checks for horizontal, vertical, and diagonal winning combinations; if no winners, checks for a draw. Called at the end of callback on_cell_touch_up()
```
    def check_for_draw(self):
        for row in self.playing_grid:
            for cell in row:
                if cell.text == '':
                    return None
        return 'Draw!'
```
Checks for a draw by checking if all cells are 'marked', given that there are no winning combinations.

```
    def reset_board(self, new_game_state): 
        """Reset the board after a player has won OR a draw has occured"""
        self.game_state = new_game_state
        self.current_move = "{}'s turn".format(self.get_starting_move())
        for row in self.playing_grid:
            for cell in row:
                cell.text = ''
                cell.game_state = new_game_state
```
Method to reset the board after a player has won or a draw has occured; to be called outside the class.

### class QuitButton
> Child class of Button

Creates a quit button class with a red background. Button is not yet bound to a callback.
```
class QuitButton(Button):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 48
        self.background_color = (255, 0, 0, 1) # red button
        self.text = 'Quit Game'
```

### class GameBanner
> Child class of Label

Creates a game banner to display the current player playing on the board and the outcome of each round (a player wins, or there is a draw)
```
class GameBanner(Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "10.009 is fun!!"
        self.font_size = 48
        self.halign = 'center'
        self.valign = 'center'
```

### class PlayerScoreLabel
> Child class of Label

Creates a score label for a player, with each player having an initial score of zero.
```
class PlayerScoreLabel(Label):
    
    def __init__(self, player_move, **kwargs):
        super().__init__(**kwargs)
        self.player_move = player_move
        self.player_score = 0
        self.text = "{0}: {1}".format(self.player_move, self.player_score)
        self.font_size = 48
```

### class ScreenControls
> Child class of BoxLayout

Creates a BoxLayout containing the quit button, the scoreboard and the game banner.
```
class ScreenControls(BoxLayout):
    
    def __init__(self, **kwargs):
        super(ScreenControls, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        """Quit Button-------------------"""
        self.quit_button = QuitButton(on_press=self.quit_game)
        
        self.add_widget(self.quit_button)
        
        """Game Banner----------"""
        self.current_game_banner = GameBanner()
        self.add_widget(self.current_game_banner)
        
        """Score Board----------"""
        self.scoreboard = BoxLayout(orientation='horizontal')
        
        self.X_score_label = PlayerScoreLabel('X')
        self.O_score_label = PlayerScoreLabel('O')
        
        self.score_labels = [self.X_score_label, self.O_score_label]
        
        for score_label in self.score_labels:
            self.scoreboard.add_widget(score_label)
        
        self.add_widget(self.scoreboard)
```

Callback which allows the players to exit the game.
```
    def quit_game(self, value):
        App.get_running_app().stop()
        Window.close()
```

### class TicTacToeScreen
> Child class of BoxLayout

Creates the screen as seen by the players.

```
class TicTacToeScreen(BoxLayout):
    
    def __init__(self, game_state, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.check_for_winner, 0.5)
        
        self.game_state = game_state
        
        self.orientation = 'vertical'
        
        self.screen_controls = ScreenControls()
        
        self.TTT_board = TicTacToeBoard(self.game_state)
        self.playing_grid = self.TTT_board.playing_grid
        
        self.TTT_board.bind(on_touch_up=self.update_game_banner)
        
        self.add_widget(self.screen_controls)
        self.add_widget(self.TTT_board)
```

Checks if any player has won the round or a draw has occured at 0.5s intervals. If round has ended (via a player winning or a draw occuring), the players' scores are updated accordingly and the board is reset.
```
    def check_for_winner(self, dt):
        """Check for any winners at scheduled intervals"""
        current_winner = self.TTT_board.last_winner
        if current_winner != None:
            self.game_state = self.next_game_state(current_winner)
            players = ['O', 'X']
            if current_winner in players:
                players.remove(current_winner)
                current_loser = players[0]
                winner_display = "{0} wins!\n{1}'s turn".format(current_winner,
                                                                current_loser)
            else:
                next_player = players[self.game_state]
                winner_display = "{0}\n{1}'s turn".format(current_winner,
                                                          next_player)
            self.screen_controls.current_game_banner.text = winner_display
            
            self.update_player_score_label(current_winner)
            self.TTT_board.last_winner = None
            
            self.TTT_board.reset_board(self.game_state)
```
Updates the score and score label of the winning player.
```
    def update_player_score_label(self, current_winner):
        """Update the player score label when a winner is found"""
        for score_label in self.screen_controls.score_labels:
            if current_winner == score_label.player_move:
                score_label.player_score += 1
                score_label.text = "{0}: {1}".format(score_label.player_move, 
                                                     score_label.player_score)
```

Updates the game banner to reflect the next player's turn after current player has finished playing.
```
    def update_game_banner(self, instance, touch):
        """Update game banner when touch is released"""
        if self.collide_point(*touch.pos):
            new_text = self.TTT_board.current_move
            self.screen_controls.current_game_banner.text = new_text
```

Determines the next game state, and thus the first player of the new round, after a player has won. If round ended in a draw, the first player is randomly chosen.
```
    def next_game_state(self, current_winner):
        """Get next game state after a player has won OR a draw has occured"""
        if current_winner == 'X':
            new_game_state = 0
        elif current_winner == 'O':
            new_game_state = 1
        else:
            new_game_state = choice((0, 1))
        return new_game_state
```

### class TicTacToeGame
> Child class of App

Root widget of game. Game randomly chooses first player by randomly selecting the starting state.
```
class TicTacToeGame(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_game_state = choice((0, 1)) # randomise a starting state
    
    def build(self):  
        self.playing_screen = TicTacToeScreen(self.initial_game_state)
        return self.playing_screen
```


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.clock import Clock
from random import choice

"""
Player A: X, 1
Player B: O, 0
"""

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

class CellLabel(Label):
    
    def __init__(self, game_state = 0, **kwargs):
        super(CellLabel, self).__init__(**kwargs)
        # self.height = 200
        self.game_state = game_state
        self.font_size = 72
        self.text = ''
        self.bind(on_touch_down=self.make_move)
                
    def make_move(self, instance, touch):
        """Change empty cell's text when tapped/ clicked on"""
        if self.text == '' and self.collide_point(*touch.pos):
            if self.game_state == 1:
                self.text = 'X'
            elif self.game_state == 0:
                self.text = 'O'    
       
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
                
    def get_starting_move(self):
        """Get initial starting move"""
        if self.game_state == 0:
            starting_move = 'X'
        else:
            starting_move = 'O'
        return starting_move
    
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
    
    def check_for_draw(self):
        for row in self.playing_grid:
            for cell in row:
                if cell.text == '':
                    return None
        return 'Draw!'
    
    def reset_board(self, new_game_state):
        """Reset the board after a player has won OR a draw has occured"""
        self.game_state = new_game_state
        self.current_move = "{}'s turn".format(self.get_starting_move())
        for row in self.playing_grid:
            for cell in row:
                cell.text = ''
                cell.game_state = new_game_state
        
class QuitButton(Button):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 48
        self.background_color = (255, 0, 0, 1)
        self.text = 'Quit'
      
        
class GameBanner(Label):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "10.009 is fun!!"
        self.font_size = 48
        self.halign = 'center'
        self.valign = 'center'


class PlayerScoreLabel(Label):
    
    def __init__(self, player_move, **kwargs):
        super().__init__(**kwargs)
        self.player_move = player_move
        self.player_score = 0
        self.text = "{0}: {1}".format(self.player_move, self.player_score)
        self.font_size = 48

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
    
    def quit_game(self, value):
        App.get_running_app().stop()
        Window.close()
        

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
            
    def update_player_score_label(self, current_winner):
        """Update the player score label when a winner is found"""
        for score_label in self.screen_controls.score_labels:
            if current_winner == score_label.player_move:
                score_label.player_score += 1
                score_label.text = "{0}: {1}".format(score_label.player_move, 
                                                     score_label.player_score)
    
    def update_game_banner(self, instance, touch):
        """Update game banner when touch is released"""
        if self.TTT_board.collide_point(*touch.pos):
            new_text = self.TTT_board.current_move
            self.screen_controls.current_game_banner.text = new_text
            
    def next_game_state(self, current_winner):
        """Get next game state after a player has won OR a draw has occured"""
        if current_winner == 'X':
            new_game_state = 0
        elif current_winner == 'O':
            new_game_state = 1
        else:
            new_game_state = choice((0, 1))
        return new_game_state
            

class TicTacToeGame(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_game_state = choice((0, 1)) # randomise a starting state
    
    def build(self):  
        self.playing_screen = TicTacToeScreen(self.initial_game_state)
        return self.playing_screen

        
TicTacToeGame().run()

import pygame,random,sys,os,pdb
import time
from colors import *

# ADD UP and DOWN ARROWS

pygame.init()
pygame.mixer.init()

SCREEN_HEIGHT=640
SCREEN_WIDTH = 900
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


pygame.display.set_caption("Mastermind")


BG_COLOR = (225,153,106)

class Button(pygame.sprite.Sprite):
    
    button_font = pygame.font.SysFont("calibri",50)
    def __init__(self,x,gap,button_text,button_color,text_color,button_width=None,button_height=None,bottom=True,centered=False,font=None):
        super().__init__()
        
        



        if not font:
            text = self.button_font.render(button_text,True,text_color)
        else:
            text = font.render(button_text,True,text_color)
        
        
        w,h = text.get_size()
        w = button_width if button_width is not None else w
        h = button_height if button_height is not None else h

        self.original_image = pygame.Surface((w + 20,h + 20))
        
        self.big_image = pygame.Surface((w + 40,h + 40))
        
        
        images = (self.original_image,self.big_image)

        for image in images:
            image.fill(button_color)
            image.blit(text,(image.get_width()//2- text.get_width()//2,image.get_height()//2 - text.get_height()//2))

        if centered:
            x = SCREEN_WIDTH//2 - w//2
            y = SCREEN_HEIGHT//2 - h//2
        elif bottom:
            y = SCREEN_HEIGHT - gap - self.original_image.get_height()
        else:
            y = gap
        self.original_rect = self.original_image.get_rect(topleft=(x,y))
        self.big_rect = self.big_image.get_rect(center=self.original_rect.center)


        self.image,self.rect = self.original_image,self.original_rect

        self.hovered_on = False
    




    def update(self,point):

        collided = self.is_hovered_on(point)

        if collided and not self.hovered_on:
            self.hovered_on = True
            self.image = self.big_image
            self.rect = self.big_rect
            return False
        elif not collided and self.hovered_on:
            self.hovered_on = False
            self.image = self.original_image
            self.rect = self.original_rect
            return True


        
    def is_hovered_on(self,point):
        return self.rect.collidepoint(point)




















class Menu:

    menu_font = pygame.font.SysFont("calibri",50,bold=True)
    main_menu_song = os.path.join('sounds','mainmenu.ogg') 
    MIN_CODE_LENGTH = 4
    MAX_CODE_LENGTH = 10
    MIN_GUESSES = 8
    MAX_GUESSES = 20

    def __init__(self):


        self.title_text = self.menu_font.render("MASTERMIND",True,BLACK)
        top_gap = 50
        self.title_text_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2,top_gap + self.title_text.get_height()//2))

        
        self._create_buttons()
        
        

        self._load_and_play()

        self._display()
    
    def _load_and_play(self):
        #pygame.mixer.Sound(self.main_menu_song).play()
        pygame.mixer.music.load(self.main_menu_song)
        pygame.mixer.music.play(-1)

    def _create_buttons(self):
        start_game_button = Button(None,None,"START",RED,BLACK,centered=True,font=self.menu_font) 
        start_game_button = Button(None,None,"START",RED,BLACK,centered=True,font=self.menu_font) 

        

        difficulty_buttons  = pygame.sprite.Group()
        sample_text = self.menu_font.render("NORMAL",True,BLACK)

        button_width = sample_text.get_width() + 20
        button_height  = sample_text.get_height() + 20


        gap = (SCREEN_HEIGHT - button_height * 3)//4
        texts = ('NORMAL',"HARD","EXPERT")

        for i in range(3):
            button = Button(SCREEN_WIDTH//2 - button_width//2, gap + i * (gap + button_height),texts[i],RED,BLACK,bottom=False,button_width= button_width,button_height=button_height,font=self.menu_font)
            difficulty_buttons.add(button)

        
    


    
        enter_button  = Button(SCREEN_WIDTH//2 - button_width//2,20,"ENTER",RED,BLACK,button_width=button_width,button_height=button_height,font=self.menu_font)






        self.buttons = {'start_screen': pygame.sprite.GroupSingle(start_game_button),
                        'difficulty_screen': difficulty_buttons,
                        'enter_button': pygame.sprite.GroupSingle(enter_button)
                                    

                }
    


    def _get_user_input(self,label,min_value,max_value,default_value):

        self.menu_font.set_underline(True)
        label_text = self.menu_font.render(f"{label}({min_value}-{max_value})",True,BLACK)
        self.menu_font.set_underline(False)
        gap_from_center = 20
        label_text_rect= label_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 - gap_from_center - label_text.get_height()))
        buttons = self.buttons['enter_button'] 
        

        invalid_text = self.menu_font.render(f"Number has to be between {min_value} and {max_value}",True,BLACK)

        
        invalid_text_rect = invalid_text.get_rect(center=(SCREEN_WIDTH//2,buttons.sprite.rect.top - 20 - invalid_text.get_height()//2))

        


        def check_value():

            if value:
                last = value[-1]
                if last == '|':
                    true_value = value[:-1]
                else:
                    true_value = value
                true_value = int(true_value)
                if min_value <= true_value <= max_value:
                    return true_value
            return False


        def update_value(character_to_add=None,remove=False):
            nonlocal value,value_text,value_text_rect
            
            if remove:
                if value and value[-1] == '|':
                    value = value[:-2] + '|'
                else:
                    value = value[:-1]
            elif character_to_add:
                if value and value[-1] == '|':
                    value = value[:-1] + character_to_add + '|'
                else:
                    value += character_to_add

            elif value:
                last = value[-1]

                if last == '|':
                    value = value[:-1]
                else:
                    value += '|'
            else:
                value += '|'

            value_text = self.menu_font.render(value,True,BLACK)
            temp_value = value_text
            if value and value[-1] == '|':
                temp_value = self.menu_font.render(value[:-1],True,BLACK)

            value_text_rect = temp_value.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)) 

            
        true_length = lambda val: len(val[:-1]) if val and val[-1] == '|' else len(val)

        value = str(default_value)
        
        value_text = self.menu_font.render(value,True,BLACK)
        value_text_rect = value_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        FLICKER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(FLICKER_EVENT,250)
        
        
        def start_timer():
            nonlocal invalid_start
            invalid_start = time.time()

        
        backspace_start_time = None
        invalid = False
        invalid_start = None
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == FLICKER_EVENT:
                    update_value()
                elif event.type == pygame.KEYDOWN:
                    if true_length(value) <= 1 and pygame.K_0 <= event.key <= pygame.K_9:
                        update_value(character_to_add=chr(event.key))
                    elif event.key == pygame.K_BACKSPACE:
                        update_value(remove=True)
                        backspace_start_time = time.time()
                    elif event.key == pygame.K_RETURN:
                        value = check_value()
                        if value:
                            return value
                        start_timer()
                elif backspace_start_time and event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                    backspace_start_time = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()

                    if buttons.sprite.is_hovered_on(point):
                        value = check_value()
                        if value:
                            return value
                        start_timer()



        
            point = pygame.mouse.get_pos()

            buttons.update(point)

            if backspace_start_time or invalid_start: 
                current_time =  time.time()
                if backspace_start_time:
                    if current_time - backspace_start_time >= 0.25:
                        update_value(remove=True)
                        backspace_start_time = current_time
                else:
                    if current_time - invalid_start >= 1:
                        invalid_start = None


            
              

            screen.fill(BG_COLOR)
            screen.blit(label_text,label_text_rect)
            screen.blit(value_text,value_text_rect)
            if invalid_start:
                screen.blit(invalid_text,invalid_text_rect)
            buttons.draw(screen)
            pygame.display.update()


    def _get_code_length(self):


        
        return self._get_user_input("Code Length",self.MIN_CODE_LENGTH,self.MAX_CODE_LENGTH,4)


    def _get_guesses(self):
        return self._get_user_input("Number of Guesses",self.MIN_GUESSES,self.MAX_GUESSES,8)



    def _difficulty_screen(self):


        buttons = self.buttons['difficulty_screen']
        
        

        texts = ('UNIQUE COLORS ONLY',"DUPLICATE COLORS ALLOWED","DUPLICATES AND BLANKS ALLOWED")
        

        button_texts = []
        for text in texts:
            button_texts.append(self.menu_font.render(text,True,BLACK))

        
        difficulty_map = {0:'normal',1: 'hard',2: 'expert'}

        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    for i,button in enumerate(buttons):
                        if button.is_hovered_on(point):
                            if i == 2:
                                return True,True
                            elif i == 1:
                                return True,False
                            return False,False


            
        

            point = pygame.mouse.get_pos()
            current_text = None
            for i,button in enumerate(buttons):
                button.update(point)
                if button.is_hovered_on(point):
                    current_text = button_texts[i]
                    break

        
            screen.fill(BG_COLOR)

            buttons.draw(screen)
            if current_text:
                screen.blit(current_text,(SCREEN_WIDTH//2 - current_text.get_width()//2,5))
            pygame.display.update()








    def _display(self):

        

        buttons = self.buttons['start_screen']

        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    if buttons.sprite.is_hovered_on(point):
                        duplicates,blanks = self._difficulty_screen()
                        code_length = self._get_code_length()
                        guesses = self._get_guesses()
                        Game(code_length=code_length,duplicates=duplicates,blanks=blanks)
                        self._load_and_play()



            
        

            point = pygame.mouse.get_pos()
            buttons.update(point)

            screen.fill(BG_COLOR)
            screen.blit(self.title_text,self.title_text_rect)
            buttons.draw(screen)
            pygame.display.update()








class Game:

    

    colors = [BLUE,RED,YELLOW,GREEN,BLACK,WHITE]
    board_color = (162,98,80)
    line_color = (173,115,99)
    bg_color = (225,153,106)
    circle_color = (71,43,36)
    question_mark = pygame.image.load(os.path.join('images','question_mark.png')).convert_alpha()
    
    font = pygame.font.SysFont("calibri",40)


    game_song = os.path.join('sounds','music.ogg')




    class PegSurface(pygame.sprite.Sprite):

        def __init__(self,x,y,guesses,square_size=15,peg_rows=2,peg_cols=2):
            super().__init__()
            

            
            self.image = pygame.Surface((square_size * peg_cols,square_size * 2))
            self.image.fill(Game.board_color)
            self.square_size = square_size

            self.radius = int(self.square_size * 0.75/2)
            self.rect = self.image.get_rect(topleft=(x,y))
            for row in range(peg_rows):
                for col in range(peg_cols):
                    if peg_cols * row + col + 1> guesses:
                        break
                    pygame.draw.circle(self.image,Game.circle_color,(col * self.square_size + self.square_size//2,row * self.square_size + self.square_size//2),self.radius)
                else:
                    continue
                break
        def draw_color(self,row,col,color): 

            pygame.draw.circle(self.image,color,(col * self.square_size + self.square_size//2,row * self.square_size + self.square_size//2),self.radius)
    class ColorGrid(pygame.sprite.Sprite):

        def __init__(self,x,width,bottom_gap):
            super().__init__()

            self.square_size = width//3 # will always have at most 3 colors per row even if have more than 6 colors


            self.image = pygame.Surface((width,self.square_size * 2)) 
            self.cols = 3
            self.rows = len(Game.colors)//self.cols
            self.rect = self.image.get_rect(topleft=(x,SCREEN_HEIGHT - bottom_gap - self.square_size * self.rows))
            self.hovered_on = False
            self._create_surface()

        
        def get_top_of_grid(self):


            return self.rect.top
        
        def update(self,point):

            collided = self.rect.collidepoint(point)
            if collided:
                self._create_surface()

                x_rel = point[0] - self.rect.x
                y_rel = point[1] - self.rect.y


                row = (y_rel - 2) //self.square_size
                col = (x_rel - 2)//self.square_size
                
                index = row * self.cols + col
                pygame.draw.circle(self.image,Game.colors[index],(col * self.square_size + self.square_size//2,row * self.square_size + self.square_size//2),self.square_size//2)
                self.hovered_on = True
            elif not collided and self.hovered_on:
                self._create_surface()
                self.hovered_on = False


        def _get_color(self,point):
            x,y = point
            x_rel = point[0] - self.rect.x
            y_rel = point[1] - self.rect.y


            row = y_rel//self.square_size
            col = x_rel//self.square_size

            index = row * self.cols + col


            return Game.colors[index]
        
        def clicked_on(self,point):


            collided = self.rect.collidepoint(point)


            if collided:

                return self._get_color(point)








    
        def _create_surface(self):

            self.image.fill(Game.board_color)

            for row in range(self.rows - 1):
                pygame.draw.line(self.image,BLACK,(0,self.square_size + row * self.square_size),(self.image.get_width(),self.square_size + row * self.square_size))

            for col in range(self.cols -1):
                pygame.draw.line(self.image,BLACK,(self.square_size +col * self.square_size,0),(self.square_size + col * self.square_size,self.image.get_height()))


            for row in range(self.rows):
                for col in range(self.cols):
                    index = row * self.cols + col
                    pygame.draw.circle(self.image,Game.colors[index],(col * self.square_size + self.square_size//2,row * self.square_size + self.square_size//2),int(self.square_size * .75/2))









    MAX_GUESS_DISPLAY = 10

            

    def __init__(self,code_length=4,guesses=15,duplicates=False,blanks=False,mode=1):
        
        self.guesses = guesses 
        self.code_length = code_length 
        self.board_width = 300
        self.square_width = self.board_width//self.code_length
        

        self.rows = min(guesses + 1,self.MAX_GUESS_DISPLAY + 1)
        self.square_height = SCREEN_HEIGHT// (self.rows)
        self.radius = int(self.square_height * .75/2)
        self.question_mark = pygame.transform.scale(self.question_mark,(self.radius,self.radius))
        self.cols = code_length
        self.game_over = False

        self.num_guesses = 0
        self.duplicates =duplicates
        self.blanks = blanks
        description = "NO DUPLICATES" if not duplicates else "DUPLICATES"
        description += " NO BLANKS" if not blanks else " BLANKS"
        pygame.display.set_caption(f"MASTERMIND {description}")
        self._generate_code()
        self.font.set_bold(True)
        self.win_text = self.font.render("YOU WIN",True,GREEN)
        self.lose_text = self.font.render("YOU LOSE",True,RED)
        self.font.set_bold(False)

        self.pick_piece_text = self.font.render("Pick Color Here",True,BLACK)
        
        self.all_guesses = []
        self.start_guess_display = 0

        self.peg_rows =2 
        self.peg_cols = self.code_length//2 if code_length %2 == 0 else  code_length//2 + 1
        self.current_square = [self.rows - 1,0]
        self.current_row = [None] * self.code_length
        self._create_board_surface()
        self._create_peg_surfaces()
        self._create_guesses_text()

        self.mapping = {}
        

        
        w = 200
        gap = ((SCREEN_WIDTH - self.board_width)//2 - w)/2






        self.color_grid =pygame.sprite.GroupSingle(Game.ColorGrid(gap,w,gap))
        self.top_of_grid = self.color_grid.sprite.get_top_of_grid()

        self.check_button = Button(self.board_rect.right + gap *2,gap,"CHECK",RED,BLACK)

        self.reset_button = Button(self.board_rect.right + gap * 2,gap,"RESET",RED,BLACK,bottom=False)


        self.buttons = pygame.sprite.Group(self.check_button,self.reset_button)


        self._load_and_play()
        self.play()
    

    def _create_guesses_text(self):

        self.texts = []
        for i in range(1,self.guesses + 1):
            text = self.font.render(str(i),True,RED)
            self.texts.append(text)
    def _load_and_play(self):

        pygame.mixer.music.load(self.game_song)
        pygame.mixer.music.play(-1)
    

    def _redraw_board(self):


        
        row = self.rows - 1
        for i in range(self.start_guess_display,self.start_guess_display + self.MAX_GUESS_DISPLAY - 1):
            
            guess_code = self.mapping[i][0]
            peg = self.pegs_ordered[row - 1]
            peg_colors = self.mapping[i][1]


            


            for col in range(self.cols):
                pygame.draw.circle(self.board_surface,guess_code[col] if guess_code[col] is not None else self.circle_color,(col * self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)

            for i,color in enumerate(peg_colors):
                _row = i // self.peg_cols
                col = i % self.peg_cols
                
                peg.draw_color(_row,col,self.circle_color if color is None else color)


            row -= 1        

        





    def _create_board_surface(self):
        self.board_surface = pygame.Surface((self.board_width,SCREEN_HEIGHT))
        self.board_surface.fill(self.board_color)
        self.board_rect = self.board_surface.get_rect(midtop=(SCREEN_WIDTH//2,0))
        
        




        for row in range(self.rows):
            pygame.draw.line(self.board_surface,self.line_color,(0,row * self.square_height),(self.board_width,row * self.square_height),4 if row != 1 else 8)
            for col in range(self.cols):
                if row != -1:
                    pygame.draw.circle(self.board_surface,self.circle_color,(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)
                else:
                    pygame.draw.circle(self.board_surface,self.code[col],(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)
        
        for i in range(self.code_length):
            self.board_surface.blit(self.question_mark,(i * self.square_width + self.square_width//2 - self.question_mark.get_width()//2,self.square_height//2 - self.question_mark.get_height()//2))
    
    def _create_peg_surfaces(self):
        self.pegs = pygame.sprite.Group()
        

        self.pegs_ordered = []

        for row in range(self.rows):
            if row == 0:
                continue
            peg_surface= Game.PegSurface(self.board_rect.right,row * self.square_height + self.square_height//2 - 15,self.code_length,peg_rows=self.peg_rows,peg_cols=self.peg_cols)
            self.pegs.add(peg_surface)
            self.pegs_ordered.append(peg_surface)

        
    
    


    def _draw_board(self):


        screen.blit(self.board_surface,self.board_rect)

        if not self.game_over:
            row,col = self.current_square
            pygame.draw.rect(screen,RED,(self.board_rect.left + col * self.square_width,row * self.square_height,self.square_width,self.square_height),5)

        for i in range(self.MAX_GUESS_DISPLAY- 1):
            guess_text = self.texts[self.start_guess_display + i]
            row = self.rows - 1 - i
            screen.blit(guess_text,(self.board_rect.left - 5 - guess_text.get_width(),row * self.square_height + self.square_height//2 - guess_text.get_height()//2))

        
        guess_text = self.texts[self.MAX_GUESS_DISPLAY -1] if self.num_guesses < self.MAX_GUESS_DISPLAY else  self.texts[self.num_guesses]
        screen.blit(guess_text,(self.board_rect.left - 5 - guess_text.get_width(),1 * self.square_height + self.square_height//2 - guess_text.get_height()//2))





    

    def _place_piece(self,color):

        board_row,board_col = self.current_square



        self.current_row[board_col] = color


        self.current_square[1] = min(self.current_square[1] + 1,self.code_length - 1)


        pygame.draw.circle(self.board_surface,color,(board_col * self.square_width + self.square_width//2,board_row * self.square_height + self.square_height//2),self.radius)



    def _generate_code(self):
        
        
        if self.blanks:
            self.colors.append(None)
        
        if not self.duplicates:
            self.code = random.sample(self.colors,k=self.code_length)
        else:
            self.code = random.choices(self.colors,k=4)


        random.shuffle(self.code)




    def play(self):



        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:



                    point = pygame.mouse.get_pos()
                    

                    if not self.game_over:
                        color = self.color_grid.sprite.clicked_on(point)
                        if color:
                            self._place_piece(color)
                        elif self.check_button.is_hovered_on(point):
                            self.game_over = self._check()
                            if self.game_over:
                                self._reveal_code()
                                if self.current_square[0] == 0:
                                    game_over_text = self.lose_text
                                else:
                                    game_over_text = self.win_text

                    elif self.reset_button.is_hovered_on(point):
                        self._reset()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_square[1] = (self.current_square[1] - 1) % self.code_length
                    elif event.key == pygame.K_RIGHT:
                        self.current_square[1] = (self.current_square[1] + 1) % self.code_length
                    elif self.num_guesses >= self.MAX_GUESS_DISPLAY and event.key in (pygame.K_DOWN,pygame.K_UP):
                        if self.start_guess_display != 0 and event.key == pygame.K_UP:
                            self.start_guess_display -= 1
                        elif event.key == pygame.K_DOWN and self.start_guess_display != self.num_guesses - self.MAX_GUESS_DISPLAY + 1:
                            self.start_guess_display += 1
                        self._redraw_board()






            

            point = pygame.mouse.get_pos()
                
            self.buttons.update(point)

            self.color_grid.update(point)
            

            screen.fill(self.bg_color)

            if self.game_over:
                screen.blit(game_over_text,(self.board_rect.left//2 - game_over_text.get_width()//2,SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            self._draw_board()
            self.pegs.draw(screen)
            self.color_grid.draw(screen)
            #self.check_button.draw(screen)
            self.buttons.draw(screen)
            screen.blit(self.pick_piece_text,(self.board_rect.left//2 - self.pick_piece_text.get_width()//2,self.top_of_grid - self.pick_piece_text.get_height()))
            pygame.display.update()
    
    

    def _reveal_code(self):
        row = 0
        for col in range(self.code_length):
            pygame.draw.circle(self.board_surface,self.code[col],(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)
    
    def _hide_code(self):
        row = 0
        for col in range(self.code_length):
            pygame.draw.circle(self.board_surface,Game.circle_color,(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)

        for i in range(self.code_length):
            self.board_surface.blit(self.question_mark,(i * self.square_width + self.square_width//2 - self.question_mark.get_width()//2,self.square_height//2 - self.question_mark.get_height()//2))
    def _reset_board_and_pegs_surface(self):

        
        for row in range(self.current_square[0],self.rows):
            for col in range(self.code_length):
                pygame.draw.circle(self.board_surface,Game.circle_color,(col * self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)


        for peg in self.pegs_ordered:
            for row in range(self.peg_rows):
                for col in range(self.peg_cols):
                    peg.draw_color(row,col,Game.circle_color)

        
        self._hide_code()


    def _reset(self):

        self._generate_code()
        
        self._reset_board_and_pegs_surface()

        self.current_square = [self.rows - 1,0]
        self.current_row = [None] * self.code_length
        self.game_over = False






    def _update_peg(self,peg,key_pegs):



        for i,color in enumerate(key_pegs):
            
            if color is None:
                break
            row = i // self.peg_cols
            col = i % self.peg_cols
            peg.draw_color(row,col,key_pegs[i])
    
    def _reveal_code(self):

    

        row = 0
        for col in range(self.code_length):
            pygame.draw.circle(self.board_surface,self.code[col],(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)


    
    def _check(self):
        key_pegs = []
        
        if self.code == self.current_row:
            return True
        
        
        code_copy = self.code.copy()
        for i,(color_1,color_2) in enumerate(zip(self.code,self.current_row)):
            if color_1 == color_2:
                code_copy[i] = -1
                key_pegs.append(RED)
        

        code_copy_2 = code_copy.copy()
        print("CODE",code_copy)
        for i,color in enumerate(self.current_row):
            if code_copy[i] != -1:
                if color in code_copy_2:
                    index = code_copy_2.index(color) 
                    code_copy_2[index] = -1
                    key_pegs.append(WHITE)
        
        random.shuffle(key_pegs)
        


        while len(key_pegs) != self.code_length:
            key_pegs.append(None)

        self.mapping[self.num_guesses] = (self.current_row.copy(),key_pegs)

        self.num_guesses += 1


        self._update_peg(self.pegs_ordered[self.current_square[0] - 1],key_pegs)
        
        self.current_square[0] -= 1
                
        if self.num_guesses == self.guesses:
            self.num_guesses -= 1
            return True

        
        
        if self.current_square[0] == 0:
            self.current_square[0] =  1
            self.current_row = [None] * 4
            peg = self.pegs_ordered[0]
            for col in range(self.code_length): 
                pygame.draw.circle(self.board_surface,self.circle_color,(col * self.square_width + self.square_width//2,self.square_height * 1.5),self.radius)
            for row in range(self.pegs_rows):
                for col in range(self.peg_cols):
                    peg.draw_color(row,col,Game.circle_color)
            self.start_guess_display += 1
            self._redraw_board()

        

        self.current_square[1] = 0

        self.current_row = [None] * self.code_length

        #return True if self.current_square[0] == 0 else False
        return False



if __name__ == "__main__":
    Menu()
#    Game()






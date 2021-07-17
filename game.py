import pygame,random,sys,os
from colors import *

pygame.init()

SCREEN_HEIGHT=640
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


pygame.display.set_caption("Mastermind")




class Game:


    colors = [BLUE,RED,YELLOW,GREEN,BLACK,WHITE]
    board_color = (162,98,80)
    line_color = (173,115,99)
    bg_color = (225,153,106)
    circle_color = (71,43,36)
    question_mark = pygame.image.load(os.path.join('images','question_mark.png')).convert_alpha()
    
    font = pygame.font.SysFont("calibri",40)
    class PegSurface(pygame.sprite.Sprite):

        def __init__(self,x,y,size=30):
            super().__init__()

            self.image = pygame.Surface((size,size))
            self.image.fill(Game.board_color)
            self.rect = self.image.get_rect(topleft=(x,y))
            self.square_size = self.image.get_width()//2
            radius = int(self.square_size * 0.75/2)
            
            for row in range(2):
                for col in range(2):
                    pygame.draw.circle(self.image,Game.circle_color,(col * self.square_size + self.square_size//2,row * self.square_size + self.square_size//2),radius)
    
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


        
        def update(self,point):

            collided = self.rect.collidepoint(point)
            if collided:
                self._create_surface()

                x_rel = point[0] - self.rect.x
                y_rel = point[1] - self.rect.y


                row = (y_rel -1) //self.square_size
                col = (x_rel - 1)//self.square_size
                
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











            

    def __init__(self,code_length=4,guesses=10,duplicates=False):
        
        self.guesses = guesses 
        self.code_length = code_length 
        self.square_height = SCREEN_HEIGHT// (guesses + 1)
        self.board_width = 300
        self.square_width = self.board_width//self.code_length
        
        self.radius = int(self.square_height * .75/2)

        self.question_mark = pygame.transform.scale(self.question_mark,(self.radius,self.radius))
        self.rows = guesses + 1
        self.cols = code_length


        self.pick_piece_text = self.font.render("Pick Color Here",True,BLACK)
        
        self.current_square = [self.guesses,0]
        self._create_board_surface()
        self._create_peg_surfaces()
        

        
        w = 200
        gap = ((SCREEN_WIDTH - self.board_width)//2 - w)/2






        self.color_grid =pygame.sprite.GroupSingle(Game.ColorGrid(gap,w,gap))



        self._generate_code()
        self.play()
    

    def _create_board_surface(self):
        self.board_surface = pygame.Surface((self.board_width,SCREEN_HEIGHT))
        self.board_surface.fill(self.board_color)
        self.board_rect = self.board_surface.get_rect(midtop=(SCREEN_WIDTH//2,0))
        
        


        for row in range(self.rows):
            pygame.draw.line(self.board_surface,self.line_color,(0,row * self.square_height),(self.board_width,row * self.square_height),4 if row != 1 else 8)
            for col in range(self.cols):
                pygame.draw.circle(self.board_surface,self.circle_color,(col *self.square_width + self.square_width//2,row * self.square_height + self.square_height//2),self.radius)
        

        for i in range(self.code_length):
            self.board_surface.blit(self.question_mark,(i * self.square_width + self.square_width//2 - self.question_mark.get_width()//2,self.square_height//2 - self.question_mark.get_height()//2))
    
    def _create_peg_surfaces(self):
        self.pegs = pygame.sprite.Group()


        for row in range(self.rows):
            if row == 0:
                continue
            for col in range(self.cols):
                peg_surface= Game.PegSurface(self.board_rect.right,row * self.square_height + self.square_height//2 - 15)
                self.pegs.add(peg_surface)

        


    def _draw_board(self):


        screen.blit(self.board_surface,self.board_rect)
        row,col = self.current_square
        pygame.draw.rect(screen,RED,(self.board_rect.left + col * self.square_width,row * self.square_height,self.square_width,self.square_height),5)


    

    def _place_piece(self,color):

        board_row,board_col = self.current_square


        pygame.draw.circle(self.board_surface,color,(board_col * self.square_width + self.square_width//2,board_row * self.square_height + self.square_height//2),self.radius)



    def _generate_code(self):


        self.colors_chosen = random.choices(self.colors,k=4)


        random.shuffle(self.colors_chosen)




    def play(self):



        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()

                    color = self.color_grid.sprite.clicked_on(point)
                    if color:
                        self._place_piece(color)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_square[1] = (self.current_square[1] - 1) % self.code_length
                    elif event.key == pygame.K_RIGHT:
                        self.current_square[1] = (self.current_square[1] + 1) % self.code_length



            

            point = pygame.mouse.get_pos()

            self.color_grid.update(point)

            screen.fill(self.bg_color)
            self._draw_board()
            self.pegs.draw(screen)
            self.color_grid.draw(screen)
            pygame.display.update()





if __name__ == "__main__":
    Game()






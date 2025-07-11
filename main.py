import zipfile
import math
import pygame
import io
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
BUTTON_WIDTH = SCREEN_WIDTH/9
BUTTON_HEIGHT = 150//3
BUTTON_PADDING = 15
NUM_ROWS = 3
NUM_COLS = 5
BUTTON_COLOR = (255, 255, 0)
FONT_COLOR = (0,0,0)
FONT_SIZE = 65
SEA_COLOR = (0, 158, 255)
IS_DRAWING=False
IS_DRAWN=False
delay=0
deadboats=[]       

def check_collisions(pirates):
     for i in pirates:
           for pirate in pirates:       
            overlapx=0
            overlapy=0
            if i.rect.colliderect(pirate.rect):
                if (i.rect.right>pirate.rect.left ) and (i.rect.right<pirate.rect.right):
                    overlapx=-(i.rect.right-pirate.rect.left)
                if (i.rect.left<pirate.rect.right ) and (i.rect.left>pirate.rect.right):
                    overlapx=i.rect.left-pirate.rect.right
                if (i.rect.top<pirate.rect.bottom ) and (i.rect.top>pirate.rect.top):
                    overlapy=pirate.rect.bottom-i.rect.top
                if (i.rect.bottom>pirate.rect.top ) and (i.rect.top>pirate.rect.bottom):
                    overlapx=-(i.rect.bottom-pirate.rect.top)
                i.rect.move_ip(overlapx,overlapy)
                i.x+=overlapx
                i.y+=overlapy

     
def checkboatcollisions(i,pirates,screen,lvl):
           dead=[]
           for pirate in pirates:
               x=pirate.rect.centerx-pirate.rect.width//2
               y=pirate.rect.centery-pirate.rect.height//2
               pirate.rect=pygame.Rect(x+38, y+63,pirate.rect.width-75,pirate.rect.height-125)
               if pirate.rect.colliderect(i.rect):
                     dead.append(pirate)
                     if pirate.grade==1: 
                       if 3>=lvl:  
                         i.health-=35
                       else:  
                         i.health-=50
                     if pirate.grade==2: 
                       if 3>=lvl:  
                         i.health-=50
                       else:  
                         i.health-=75                             
                     if i.health<=0:
                         return False
                            
           for pirate in dead:
               pirate.timer=60
               pirates.remove(pirate)
               
           drawdeatheffect(dead,screen)
                 
           return True      
           
def check_islandcollision(i,pirates):
         for pirate in pirates:              
            if i.rect.colliderect(pirate.rect):
                return False
            return True    

def checkwinner(i,b):
      if b.rect.colliderect(i.rect):
                return False
      return True     
                   

def drawdeatheffect(dead,screen):
    deadboats.extend(dead)
    for pirate in deadboats:
        pirate.image=pirate.image.convert_alpha()
        pirate.image.set_colorkey(pirate.colorkey)
        pirate.image.fill((255, 0, 0),special_flags=pygame.BLEND_RGBA_MULT)         
        pirate.rect=pirate.image.get_bounding_rect() 
        pirate.rect.center=(pirate.x,pirate.y)
        screen.blit(pirate.image,pirate.rect)
        pirate.timer-=1
        if pirate.timer<=0:
            deadboats.remove(pirate)

class Pirate:
    def __init__(self, x, y,path,speed=4):
        self.grade=1
        self.path=path
        self.nextpos=0
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('pirate_ship.png') as file:
                pirate_ship = file.read()
        self.image = pygame.image.load(io.BytesIO(pirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(60,100))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self):
        dx = self.path[self.nextpos][0]- self.rect.centerx
        dy = self.path[self.nextpos][1] - self.rect.centery
        if dx==0 and dy==0:
          if self.nextpos<len(self.path)-1:
            self.nextpos+=1
          else:
            self.nextpos=0
          self.update_position
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135           
        if dx<0 and dy==0:
            self.angle=90
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]    
        if dx >0:
            if dx <4:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=4
        if dy >0:
            if dy <4:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=4   
        if dy <0:
            if dy >(-4):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=4 
        if dx <0:
            if dx >(-4):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=4
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect)
        
class ElitePirate:
    def __init__(self, x, y, speed=1):
        self.grade=2
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('elitepirate_ship.png') as file:
                elitepirate_ship= file.read()
        self.image = pygame.image.load(io.BytesIO(elitepirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(60,100))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self, player_pos,pirates):
        # Move towards player
        dx = player_pos.centerx- self.rect.centerx
        dy = player_pos.centery - self.rect.centery
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135         
        if dx<0 and dy==0:
            self.angle=-270
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]            
        if dx >0:
            if dx <3:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=3
        if dy >0:
            if dy <3:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=3   
        if dy <0:
            if dy >(-3):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=3 
        if dx <0:
            if dx >(-3):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=3
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect)         

class SpecialPirate:
    def __init__(self, x, y, speed=1):
        self.grade=2
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('specialpirate_ship.png') as file:
                elitepirate_ship= file.read()
        self.image = pygame.image.load(io.BytesIO(elitepirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(40,100))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self, player_pos,pirates):
        # Move towards player
        dx = player_pos.centerx- self.rect.centerx
        dy = player_pos.centery - self.rect.centery
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135         
        if dx<0 and dy==0:
            self.angle=-270
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]            
        if dx >0:
            if dx <6:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=6
        if dy >0:
            if dy <6:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=6   
        if dy <0:
            if dy >(-6):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=6 
        if dx <0:
            if dx >(-6):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=6
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect) 
   
class Boat:
    def __init__(self, x, y, image_path='player_ship.png'):
        self.angle=0
        self.x = x
        self.y = y
        self.health=100
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('player_ship.png') as file:
                player_ship = file.read()
        self.image = pygame.image.load(io.BytesIO(player_ship)).convert_alpha()
        self.og_image= pygame.transform.scale(self.image,(60,100))
        self.colorkey = self.og_image.get_at((0, 0))
        self.og_image.set_colorkey(self.colorkey)
       

    def render(self,screen):
            self.image = pygame.transform.rotate(self.og_image, self.angle)
            self.rect=self.image.get_bounding_rect()
            self.image.set_colorkey(self.colorkey)    
            self.rect.center=(self.x+45,self.y+75)
            screen.blit(self.image, self.rect)
            health_bar_rect = pygame.Rect(self.x+25, self.y, (self.health*6)//10, 4)
            health_bar_surface = pygame.Surface(((self.health*6//10), 4))
            health_bar_surface.fill((0, 255, 0))
            screen.blit(health_bar_surface, health_bar_rect)
    
    def getpos(self):
        return self.x,self.y
    
    def update_position(self,positions,path):
        dx=positions[0][0]
        dy=positions[0][1]
        if path.index//7 < len(path.direc):
            self.angle = path.direc[path.index//7]
        self.x = dx-45
        self.y = dy-75
        self.rect.centerx=dx
        self.rect.centery=dy
        path.index+=1
        positions=positions[1:len(positions)]
        return positions
    
    
class Path:
    def __init__(self):
        self.direc=[]
        self.points = []
        self.index=1

    def add(self, pos):
        self.points.append(pos)
        
    def update(self, pos):
        self.points=pos
    
    def reset(self):
        self.points=[]
        self.index=0
        self.direc=[]
    
    def getpath(self):
        return self.points

    def draw(self, surface):
        if len(self.points) < 2:
            return
        pygame.draw.lines(surface, (0, 0, 255), False, self.points, 10)
        
    def smooth(self, points):
        for i in range(7,len(points),7):
            dx=points[i][0]
            dy=points[i][1]
            direcx=dx-points[i-7][0]
            direcy=dy-points[i-7][1]
            if direcx==0 and direcy<0:
                self.direc.append(0)
            if direcx>0 and direcy<0:
                self.direc.append(-45)
            if direcx>0 and direcy==0:
                self.direc.append(270)
            if direcx>0 and direcy>0:
                self.direc.append(225)
            if direcx==0 and direcy>0:
                self.direc.append(180)
            if direcx<0 and direcy>0:
                self.direc.append(225-90)          
            if direcx<0 and direcy==0:
                self.direc.append(270+180)
            if direcx<0 and direcy<0:
                self.direc.append(45)         

class Island:
    def __init__(self, position):
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('island.png') as file:
                island = file.read()
        self.image = pygame.image.load(io.BytesIO(island)).convert_alpha()        
        self.image= pygame.transform.scale(self.image,(120,120))
        self.rect=self.image.get_bounding_rect()
        self.position=position
        self.rect=self.image.get_bounding_rect()
        self.rect.center=((self.position[0]+90,self.position[1]+90))
    def render(self, screen):
        screen.blit(self.image, self.rect)

def levels(selected):
    if selected == 1:
        boat = Boat(673, 468)
        island = Island((60, 67))
        pirates = [Pirate(100, 300, ((333, 112), (100, 300)))]
        elitepirates = []
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 2:
        boat = Boat(400, 468)
        island = Island((400, 67))
        pirates = [Pirate(333, 300, ((733, 300), (333, 300))),
                Pirate(533, 450, ((333, 450), (733, 450)))]
        elitepirates = []
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 3:
        boat = Boat(400, 468)
        island = Island((400, 67))
        pirates = [Pirate(333, 300, ((733, 300), (333, 300))),
                Pirate(533, 450, ((333, 450), (733, 450)))]
        elitepirates = [ElitePirate(60, 67)]
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 4:
        boat = Boat(673, 243)
        island = Island((0, 232))
        pirates = [Pirate(200, 56, ((200, 543), (200, 56))),
                Pirate(600, 56, ((600, 543), (600, 56)))]
        elitepirates = [ElitePirate(400, 300)]
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 5:
        boat = Boat(673, 468)
        island = Island((0, 232))
        pirates = [Pirate(200, 468, ((200, 56), (200, 468))),
                Pirate(600, 468, ((600, 56), (600, 468)))]
        elitepirates = [ElitePirate(673, 56)]
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 6:
        boat = Boat(50, 468)
        island = Island((400, 232))
        pirates = [Pirate(400, 165, ((533, 165), (533, 412), (266, 412), (266, 165)), speed=6),
                Pirate(400, 412, ((266, 412), (266, 165), (533, 165), (533, 412)), speed=6)]
        elitepirates = [ElitePirate(673, 56)]
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 7:
        boat = Boat(50, 187)
        island = Island((667, 300))
        pirates = [Pirate(266, 56, ((533, 468), (266, 468), (266, 56)), speed=5),
                Pirate(266, 468, ((266, 56), (533, 468), (266, 468)), speed=5),
                Pirate(400, 232, ((533, 468), (266, 468), (266, 56)), speed=5),
                Pirate(266, 300, ((266, 56), (533, 468), (266, 468)), speed=5),
                Pirate(533, 468, ((266, 468), (266, 56), (533, 468)), speed=5)]
        elitepirates = []
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 8:
        boat = Boat(50, 243)
        island = Island((667, 300))
        pirates = []
        elitepirates = []
        specialpirates = [SpecialPirate(266, 300), SpecialPirate(266, 150), SpecialPirate(266, 450)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 9:
        boat = Boat(366, 450)
        island = Island((667, 75))
        pirates = [Pirate(466, 225, ((266, 225), (266, 450), (600, 450))),
                Pirate(133, 525, ((533, 525), (533, 300), (66, 300)))]
        elitepirates = []
        specialpirates = [SpecialPirate(266, 300)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 10:
        boat = Boat(50, 450)
        island = Island((667, 67))
        pirates = [Pirate(400, 165, ((533, 165), (533, 412), (266, 412), (266, 165)), speed=6),
                Pirate(400, 412, ((266, 412), (266, 165), (533, 165), (533, 412)), speed=6)]
        elitepirates = [ElitePirate(667, 487)]
        specialpirates = [SpecialPirate(266, 300)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 11:
        boat = Boat(50, 56)
        island = Island((667, 450))
        pirates = [Pirate(266, 450, ((667, 150), (266, 450)), speed=6),
                Pirate(50, 300, ((266, 56), (50, 300)), speed=6)]
        elitepirates = [ElitePirate(667, 56)]
        specialpirates = [SpecialPirate(50, 450)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 12:
        boat = Boat(206, 468)
        island = Island((266, 67))
        pirates = [Pirate(333, 300, ((733, 300), (333, 300))),
                Pirate(533, 450, ((333, 450), (733, 450)))]
        elitepirates = [ElitePirate(60, 67), ElitePirate(667, 67)]
        specialpirates = [SpecialPirate(60, 468), SpecialPirate(667, 468)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 13:
        boat = Boat(50, 450)
        island = Island((667, 180))
        pirates = [Pirate(50, 56, ((667, 450), (50, 56)), speed=8)]
        elitepirates = []
        specialpirates = [SpecialPirate(266, 300), SpecialPirate(533, 300)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 14:
        boat = Boat(50, 450)
        island = Island((567, 120))
        pirates = [Pirate(633, 56, ((710, 56), (710, 303), (487, 303), (487, 56)), speed=10),
                Pirate(633, 303, ((487, 303), (487, 56), (710, 56), (710, 303)), speed=10),
                Pirate(400, 56, ((400, 450), (400, 56)))]
        elitepirates = [ElitePirate(50, 56)]
        specialpirates = [SpecialPirate(50, 300), SpecialPirate(400, 450)]
        return boat, island, pirates, elitepirates, specialpirates

    elif selected == 15:
        boat = Boat(366, 450)
        island = Island((66, 525))
        pirates = [Pirate(533, 150, ((266, 150), (266, 450), (600, 450))),
                Pirate(733, 375, ((533, 375), (533, 150), (333, 150)))]
        elitepirates = []
        specialpirates = []
        return boat, island, pirates, elitepirates, specialpirates
      

def game_over(screen):
    
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background2.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()    
    font = pygame.font.SysFont("Calibiri", 60)
    game_over_text = font.render("  Defeat", True, (0, 0, 0))
    text_rect = pygame.Rect(500,200,180, 60)
    text = font.render(' menu ', True, (0, 0, 0))
    rect=text.get_rect()  
    rect.center=((600,400))
    rect.height+=10
    image1= pygame.transform.scale(image,(rect.width, rect.height))
    image2= pygame.transform.scale(image,(text_rect.width, text_rect.height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    game(screen,False,False,0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return True
        screen.blit(background,(0,0))        
        screen.blit(image1,rect)       
        screen.blit(image2,text_rect)
        screen.blit(text,rect)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

def you_won(screen):
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background2.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()    
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()    
    font = pygame.font.SysFont("Calibiri", 60)
    game_over_text = font.render("You won", True, (0, 0, 0))
    text_rect = pygame.Rect(500,200,180, 60)
    text = font.render(' menu ', True, (0, 0, 0))
    rect=text.get_rect()  
    rect.center=((600,400))
    rect.height+=10
    image1= pygame.transform.scale(image,(rect.width, rect.height))
    image2= pygame.transform.scale(image,(text_rect.width, text_rect.height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    game(screen,False,False,0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return True
        screen.blit(background,(0,0))        
        screen.blit(image1,rect)       
        screen.blit(image2,text_rect)
        screen.blit(text,rect)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

def create_menu(surface):
    # Initialize Pygame
    pygame.init()
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()
    image= pygame.transform.scale(image,(BUTTON_WIDTH, BUTTON_HEIGHT))
    
    font = pygame.font.SysFont("Calibiri", 60)
    title = font.render('Levels', True, (0, 0, 0))
    image2= pygame.transform.scale(image,(550//3, 70)) 
    font = pygame.font.Font(None, FONT_SIZE)

    # Create buttons
    buttons = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            # Calculate button position and rect
            x = (col * (BUTTON_WIDTH + BUTTON_PADDING)) + (SCREEN_WIDTH - (BUTTON_WIDTH + BUTTON_PADDING) * NUM_COLS) // 2
            y = (row * (BUTTON_HEIGHT + BUTTON_PADDING)) + (SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_PADDING) * NUM_ROWS) // 2
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            # Create button text
            text = font.render(str(row * NUM_COLS + col + 1), True, FONT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            # Append button and text to buttons list
            buttons.append((rect, text))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a button was clicked
                for i, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        return i + 1

        # Draw buttons and text on surface
        surface.fill(SEA_COLOR)
        surface.blit(background, (0,0))
        surface.blit(image2, (470,90))
        surface.blit(title, (500,100))
        for rect, text in buttons:
            surface.blit(image,rect)
            surface.blit(text, text.get_rect(center=rect.center))

        # Update display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

def game(screen,IS_DRAWN,IS_DRAWING,delay):

    pygame.display.set_caption("Pirate Hunter: The Quest for Treasure")
    
    selected_level = create_menu(screen)
    
    path = Path()
    
    entities=levels(selected_level)
    boat=entities[0]
    island=entities[1]
    pirates=entities[2]
    elitepirates=entities[3]
    specialpirates=entities[4]
    
    pygame.init()
    
    boat.render(screen)
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b=boat.getpos()
                e=event.pos
                if e[0]>=b[0] and e[1]>=b[1] and (e[0]<=b[0]+150) and (e[1]<=b[1]+250):
                    if IS_DRAWN==False:
                        IS_DRAWING = True
            elif event.type == pygame.MOUSEMOTION:
                if IS_DRAWING:
                        path.add(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:       
                if IS_DRAWING==True:
                     IS_DRAWN= True
                     IS_DRAWING=False
                     path.smooth(path.getpath())     
        else:
                                                                
            screen.fill(SEA_COLOR)
            
            if (delay%70==0):            
                for pirate in elitepirates:
                    pirate.update_position(island.rect,pirates)
                    r=check_islandcollision(island,elitepirates)
                    if r==False:
                        game_over(screen)
                    
                for pirate in specialpirates:
                    pirate.update_position(boat.rect,pirates)                
                
                for pirate in pirates:
                    pirate.update_position()
                    check_collisions(pirates+elitepirates+specialpirates)
            
            if (IS_DRAWN==True) and (delay%40==0):
                if delay==299:
                    delay=0            
                p=boat.update_position(path.points,path)
                if p==[]:
                    path.reset()    
                    IS_DRAWN=False
                else:
                    path.update(p)    
            delay+=1
            
            running=checkboatcollisions(boat,pirates,screen,selected_level)
            if running==False:
                dead=[]
                game_over(screen)
            
            running=checkboatcollisions(boat,specialpirates,screen,selected_level)
            if running==False:
                dead=[]
                game_over(screen)
                    
            running=checkboatcollisions(boat,elitepirates,screen,selected_level)
            if running==False:
                dead=[]
                game_over(screen)
            
            running=checkwinner(boat,island)
            if running==False:
                dead=[]
                you_won(screen)  
            
            boat.render(screen)  
            
            island.render(screen) 
            
            path.draw(screen)        
            
            for pirate in pirates:
                pirate.draw(screen)
                
            for pirate in specialpirates:
                pirate.draw(screen)
            
            for pirate in elitepirates:
                pirate.draw(screen)
                
            pygame.display.update()
    
    # Quit Pygame
    pygame.quit()

    
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

game(screen,IS_DRAWN,IS_DRAWING,delay)  

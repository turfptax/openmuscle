import pygame
import math

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Origin
x = int(screen_width/2)
y = int(screen_height/2)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

finger_width = 51
finger_height = 120
finger_spacing = 10
palm_width = finger_spacing + 4*(finger_width+finger_spacing)
palm_height = 200
finger_length = [finger_height, int(finger_height*1.5), int(finger_height*1.8), int(finger_height*1.5)]
radius = 20

def yy(y):
    return screen_height-y

def drawLine(x1,y1, x2,y2, w, color):
    pygame.draw.line(screen, color, (x1, yy(y1)), (x2, yy(y2) ), width=w, )
    #pygame.display.update()

def drawDisc(x,y, dia, color):
    r = int(dia/2)
    pygame.draw.ellipse(screen, color, (x-r, yy(y+r), dia,dia))
    #pygame.display.update()

def drawRect(x,y,width,height, color):
    pygame.draw.rect(screen, color, (x, yy(y)-height, width, height))
    #pygame.display.update()

def drawRoundRect(x,y,width,height, r, color):
    pygame.draw.rect(screen, color, (x, yy(y)-height, width, height), border_radius=r)
    pygame.display.update()

def drawPalm():    
    drawRoundRect(0,0, palm_width,palm_height, radius, WHITE)

def drawFinger(index, ratio):
    x = finger_spacing + finger_width/2 + index*(finger_width+finger_spacing)
    y1 = palm_height-5
    y2 = palm_height + int(finger_length[index] * ratio)
    drawDisc(x,y2, finger_width, WHITE)
    drawLine(x,y1, x,y2, finger_width, WHITE)

def drawThumb():
    w2 = int(finger_width / math.sin(math.radians(45)))
    x1 = palm_width-int(w2/2)
    y1 = int(palm_height/3)
    x2 = x1+finger_height-int(finger_width/2)
    y2 = y1+finger_height-int(finger_width/2)
    
    for i in range(-15,15):
        x3 = x2 + i
        y3 = y2 + i
        drawDisc(x3,y3, finger_width, WHITE)

    drawLine(x1,y1, x2,y2, w2, WHITE)

def drawHand(fingerRatios):
    screen.fill(BLACK)
    drawPalm()
    drawThumb()
    drawFinger(0, fingerRatios[0])
    drawFinger(1, fingerRatios[1])
    drawFinger(2, fingerRatios[2])
    drawFinger(3, fingerRatios[3])
    pygame.display.update()
 
#----------------------------------

ratios=[1/3, 2/3, 3/3]

# Main loop
running = True
while running:
    for f in range(3,-1,-1):
        for ratio in ratios:
            if f==0:
                fingerRatios = [ratio,ratios[0],ratios[0],ratios[0]]
            elif f==1:
                fingerRatios = [ratios[0],ratio,ratios[0],ratios[0]]
            elif f==2:
                fingerRatios = [ratios[0],ratios[0],ratio,ratios[0]]
            else:
                fingerRatios = [ratios[0],ratios[0],ratios[0],ratio]
            drawHand(fingerRatios)
            pygame.time.wait(200)

        for ratio in ratios[::-1]:
            if f==0:
                fingerRatios = [ratio,ratios[0],ratios[0],ratios[0]]
            elif f==1:
                fingerRatios = [ratios[0],ratio,ratios[0],ratios[0]]
            elif f==2:
                fingerRatios = [ratios[0],ratios[0],ratio,ratios[0]]
            else:
                fingerRatios = [ratios[0],ratios[0],ratios[0],ratio]
            drawHand(fingerRatios)
            pygame.time.wait(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Quit Pygame
pygame.quit()

import pygame
import time
import random
pygame.font.init()

#will need to be updated
#Make sure to declare all constant variables in CAPS
WIDTH, HEIGHT = 1000, 800 #in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

#Background image and allows you to change scale of the image
BG = pygame.transform.scale(pygame.image.load("2nd-BG.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    #pass coordinates to blit. 0x0 is top left-hand corner of the screen
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    #Also able to use RGB (0, 0, 0)
    pygame.draw.rect(WIN, (245, 66, 141), player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True
    #pygame.Rect(x, y, width, height)
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    #generate projectiles
    star_add_increment = 2000 #2000 milliseconds
    star_count = 0 #copunting when get to increment

    stars = []
    hit = False

#Keeps program running 
    while run:
        #Delays the while loop to only run a maximum of 60 times/sec 
        #Useful for slowing down player icon when moving it 
        star_count += clock.tick(60) #returns the number of milliseconds since the last clock tick
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3): #use underscore when you don't care about the iteration count
                star_x = random.randint(0, WIDTH - STAR_WIDTH) #want to pick rand int in the range of zero
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT) #will make star slowly enter screen
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        #moves player icon to the left when left arrow key is selected (Can look up pygame key codes)
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0 :
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]: #makes copy of the list to loop through the copy so can adjust orginal list
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): #check if the star has collided with player
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) #places text in middle of screen
            pygame.display.update() #manually updates display with text for 4 seconds
            pygame.time.delay(4000) #milliseconds

        draw(player, elapsed_time, stars)
        
    pygame.quit()        

#Calls the file to run directly
if __name__ == "__main__":
    main()
import arcade
import random

#Size of sprite
SPRITE_SCALING = .5
ENEMY_SPRITE_SCALING = .2
SPRITE_SCALING_LASER = .2

#Screen size and title
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TITLE = "First Game"

#Speed of sprites
MOVEMENT_SPEED = 5
LASER_SPEED = 8
ENEMY_SPEED = 5

#How many enemy's in the game 
ENEMY_COUNT = 5

#For playing background music
MUSIC_VOLUME = .2
PAN = 0.0
LOOP = True

EXPLOSION_TEXTURE_COUNT = 60

class Explosion(arcade.Sprite):
    
    def __init__(self, texture_list):
        super().__init__()

        #start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        
    def update(self):
        #Update to the next frame. If at end of frame delete the sprite
        self.current_texture += 1
        
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)

        else:
            self.remove_from_sprite_lists()

        
class Enemy(arcade.Sprite):
    
    def screen_position(self):
        
        #Setting random position above the screen for enemy to fall from
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(30, SCREEN_WIDTH - 30)

    def update(self):

        #Move the sprite down the screen
        self.center_y -= ENEMY_SPEED

        #check to see if sprite is off the screen
        if self.top < 0:
            self.screen_position()

#using arcade.Sprite class and attributes
class Player(arcade.Sprite):

    def __init__(self, filename, scale):
        super().__init__(filename, scale)

        self.respawning = 0

        self.respawn()
        
    def respawn(self):
        self.respawning = 1
        self.center_x = 300
        self.center_y = 20

    #update function in sprite class
    def update(self):

        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 255
        #Player movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        #Check to see if player sprite is out of bounds
        if self.left < 0:
            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH  - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 500:
            self.top = SCREEN_HEIGHT - 500

        super().update()
    

#using arcade.Window class and attributes
class Game(arcade.View):

    #create the game window and set size and color
    def __init__(self):

        # Call the parent class initializer
        super().__init__()

        #sprite list variables
        self.player_list = None
        self.enemy_list = None
        self.laser_list = None
        self.exsplosion_list = None
        self.player_life_list = None

        #music variables and list
        self.music_list = []
        self.music = None

        #sprite variable
        self.player_sprite = None
        self.laser_sprite = None
        self.enemy_sprite = None
        self.player_lives = None

        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.exsplosion_texture_list = []
        
        colums = 16
        count = 60
        sprite_width = 256
        sprite_height = 256

        file_name = ":resources:images/spritesheets/explosion.png"

        #Load the explosin from sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, colums, count)
        

        #sound varibles
        self.laser_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.enemy_explosion = arcade.load_sound(":resources:sounds/explosion1.wav")

        #Music list and calling play_song function
        self.music_list = [":resources:music/1918.mp3"]
        self.play_song()
        
        #loading a texture to use as a background (r) is for formating string so it can be read
        self.back_ground = arcade.load_texture(r"space.png")

        #setting up lists
        self.player_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.player_lives_list = arcade.SpriteList()

        #varible's
        self.score = 0
        self.lives = 3
        

        #setting up player and location on screen
        self.player_sprite = Player(":resources:images/space_shooter/playerShip1_green.png", SPRITE_SCALING)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 20

        #append player sprite to player list
        self.player_list.append(self.player_sprite)

        #setting up extra lives list
        extra_life_position = 10
        
        for extra_lives in range(self.lives):
            player_lives = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", .2)
            player_lives.center_x += extra_life_position
            player_lives.center_y = 560
            extra_life_position += 15
        
            self.player_lives_list.append(player_lives)

        #setting up laser sprite
        self.laser_sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        #create the enemy
        for x in range(ENEMY_COUNT):
            enemy_sprite = Enemy(":resources:images/enemies/bee.png", ENEMY_SPRITE_SCALING)
            enemy_sprite.center_x = random.randrange(SCREEN_WIDTH)
            enemy_sprite.center_y = random.randrange(SCREEN_HEIGHT)

            self.enemy_list.append(enemy_sprite)
  

    def play_song(self):
        self.music = arcade.Sound(self.music_list[0])
        self.x = self.music.play(MUSIC_VOLUME, PAN, LOOP)
        

    #overriding the on_draw funtion in arcade.window
    def on_draw(self):
        #draw the game to the screen 

        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Draw the background. This must be drawn before sprites are
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.back_ground)

        # Draw all the sprites.
        self.enemy_list.draw()
        self.laser_list.draw()
        self.player_list.draw()
        self.explosion_list.draw()
        self.player_lives_list.draw()

        #draw the score to the screen
        total_score = f"Score: {self.score}"
        arcade.draw_text(total_score, 10, 575, arcade.color.WHITE)
        
    #overiding on_key_press in arcade.window
    def on_key_press(self, key, modifiers):

        # If the player presses a key, update the speed
        #using arcade.key 
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            #rotate laser sprite to face up
            self.laser_sprite.angle = 90

            #speed of how fast laser travels
            self.laser_sprite.change_y = LASER_SPEED
            
            arcade.play_sound(self.laser_sound)
            
            #center laser sprite to player sprite center and top
            self.laser_sprite.center_x = self.player_sprite.center_x
            self.laser_sprite.bottom = self.player_sprite.top
                
            self.laser_list.append(self.laser_sprite)
            
    #overriding on_key_release in arcade.window
    #using arcade.key 
    def on_key_release(self, key, modifiers):
        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    #overiding on_update function in arcade.window and using delta_time. (delta_time = time since last time function was called. 
    def on_update(self, delta_time):
        #Movement and game logic here

        #update and move the player
        self.player_list.update()

        self.enemy_list.update()

        self.player_lives_list.update()
        
        #update and move laser sprite
        self.laser_list.update()

        self.explosion_list.update()

        for laser in self.laser_list:
        
            # If laser touches Enemy sprite add enemy sprite to the hit list
            hit_list = arcade.check_for_collision_with_list(laser, self.enemy_list)

            #If enemy sprite in hit list set up explosion
            if len(hit_list) > 0:
                explosion = Explosion(self.explosion_texture_list)

                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y

                explosion.update()

                self.explosion_list.append(explosion)
                laser.remove_from_sprite_lists()

            #If enemy sprite in hit list remove it from sprite list
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.enemy_explosion)
                
            if laser.bottom > SCREEN_HEIGHT - 50:
                    laser.remove_from_sprite_lists()

        for player in self.player_list:
            #check to see if player is hit by enemy. if player is hit by enemy add to hit list. 
            player_hit_list = arcade.check_for_collision_with_list(player, self.enemy_list)
            
            if len(player_hit_list) > 0:
                if self.lives > 0:
                    #subtract one life if player is hit by enemy
                    self.lives -= 1
                    
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = player_hit_list[0].center_x
                    explosion.center_y = player_hit_list[0].center_y

                    explosion.update()

                    self.explosion_list.append(explosion)
                    self.player_lives_list.pop().remove_from_sprite_lists()
                    arcade.play_sound(self.enemy_explosion)

                    #Call the respawn function after player is hit
                    self.player_sprite.respawn()

                    for enemy in player_hit_list:
                        enemy.remove_from_sprite_lists()

                    
                else:
                    self.you_died()


    def you_died(self):    
        game_over = GameOverView()
        self.window.show_view(game_over)
        self.music.stop(self.x)

                
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game over", 260, 300, arcade.color.WHITE, 15)
        arcade.draw_text("Click Mouse to start new game", 200, 250, arcade.color.RED, 15)

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = Game()
        self.window.show_view(game_view)           
    
def main():
    #Main function for game calling
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game = Game()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()


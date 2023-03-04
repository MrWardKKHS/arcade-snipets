"""
Platformer Game
Starting point https://api.arcade.academy/en/latest/examples/platform_tutorial/step_06.html

Simplified Damage calculation
(((2xlevel+2)*(attack/defence))/50) * random.randint(85, 100)

Total experience at any level:
    EXP = n ** 3

Exp awarded = Base * Level / 7
base = ~ 50 to 150

Calculate any stat for any level by using
floor((base * random * 2 * level) / 100) + 5
"""
import arcade
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class Player(arcade.Sprite):
    def __init__(self):
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        super().__init__(image_source)
        self.center_x = 64
        self.center_y = 96
        self.level = 1
        self.attack = random.randint(10, 35)
        self.defence = random.randint(10, 35)
        self.health = random.randint(15, 55)
        self.experience = 0

    def level_up(self):
        self.level += 1
        self.attack += random.randint(0, 4)
        self.defence += random.randint(0, 4)
        self.health += random.randint(0, 6)

    @property
    def experience_at_next_level(self):
        return (self.level + 1) ** 3


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.camera = arcade.Camera(self.width, self.height)
        self.scene = arcade.Scene()
        
        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player = Player()
        self.scene.add_sprite("Player", self.player)

        # Create the ground
        for x in range(0, 5250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            bullet 

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_player()



def main():
    """Main function"""
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

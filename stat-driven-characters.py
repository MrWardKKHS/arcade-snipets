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
import math

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

class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        image_source = ":resources:images/space_shooter/laserBlue01.png"
        super().__init__(image_source)
        self.center_x = x
        self.center_y = y
        self.change_x = 15

class Enemy(arcade.Sprite):
    def __init__(self, x, y, level):
        image_source = ":resources:images/enemies/wormGreen.png"
        super().__init__(image_source)
        self.center_x = x
        self.center_y = y
        self.level = level
        self.attack = math.floor((random.randint(20, 35) * 2 * level) / 30) + 5
        self.defence = math.floor((random.randint(20, 35) * 2 * level) / 30) + 5
        self.health = math.floor((random.randint(40, 65) * 2 * level) / 30) + level + 10
        self.initial_health = self.health
        self.base_experience = 10



class Player(arcade.Sprite):
    def __init__(self):
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        super().__init__(image_source)
        self.center_x = 64
        self.center_y = 96
        self.level = 1
        self.attack = random.randint(10, 15)
        self.defence = random.randint(10, 35)
        self.health = random.randint(15, 55)
        self.experience = 0
        self.experience_at_next_level = (self.level + 1) ** 3

    def level_up(self):
        self.level += 1
        self.attack += random.randint(0, 4)
        self.defence += random.randint(0, 4)
        self.health += random.randint(0, 6)
        self.experience_at_next_level = (self.level + 1) ** 3

    def gain_experience_from_enemy(self, enemy):
        self.experience += (enemy.base_experience * enemy.level) // 7
        if self.experience >= self.experience_at_next_level:
            self.level_up()
        

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.camera = arcade.Camera(self.width, self.height)
        self.HUD_camera = arcade.Camera(self.width, self.height)
        self.scene = arcade.Scene()
        
        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Bullets")
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

        # Create the enemies 
        for x in range(256, 5250, 128):
            enemy = Enemy(x, 150, x//64 + 1)
            self.scene.add_sprite("Enemies", enemy)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

        self.last_hit_enemy = self.scene['Enemies'][0]
        self.damage_text = ""

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.draw_health()
        self.HUD_camera.use()
        arcade.draw_text(f"Player Level: {self.player.level}", 25, SCREEN_HEIGHT - 25)
        arcade.draw_text(f"Attack: {self.player.attack}", 25, SCREEN_HEIGHT - 40)
        arcade.draw_text(f"Defence: {self.player.defence}", 25, SCREEN_HEIGHT - 55)
        arcade.draw_text(f"Experience: {self.player.experience}", 25, SCREEN_HEIGHT - 70)
        arcade.draw_text(f"Next Level: {self.player.experience_at_next_level}", 25, SCREEN_HEIGHT - 85)
        arcade.draw_text(f"Last Damage: {self.damage_text}", 25, SCREEN_HEIGHT - 100)

        arcade.draw_text(f"Enemy Level: {self.last_hit_enemy.level}", SCREEN_WIDTH-150, SCREEN_HEIGHT - 25)
        arcade.draw_text(f"Attack: {self.last_hit_enemy.attack}", SCREEN_WIDTH-150, SCREEN_HEIGHT - 40)
        arcade.draw_text(f"Defence: {self.last_hit_enemy.defence}", SCREEN_WIDTH-150, SCREEN_HEIGHT - 55)
        arcade.draw_text(f"initial_health: {self.last_hit_enemy.initial_health}", SCREEN_WIDTH-150, SCREEN_HEIGHT - 70)
        arcade.draw_text(f"Health: {int(self.last_hit_enemy.health)}", SCREEN_WIDTH-150, SCREEN_HEIGHT - 85)

    def draw_health(self):
        for enemy in self.scene['Enemies']:
            arcade.draw_lrtb_rectangle_filled(enemy.left+enemy.width/4, enemy.right-enemy.width/4, enemy.top + 25, enemy.top + 15, arcade.color.RED)
            health_left_percent = enemy.health / enemy.initial_health
            health_box_width = enemy.width * health_left_percent * 0.5
            arcade.draw_lrtb_rectangle_filled(enemy.left+enemy.width/4, enemy.left+ enemy.width/4 + health_box_width, enemy.top + 25, enemy.top + 15, arcade.color.GREEN)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            bullet = Bullet(self.player.center_x, self.player.center_y)
            self.scene['Bullets'].append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0


    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
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
        self.scene.update()
        for enemy in self.scene['Enemies']:
            bullets = arcade.check_for_collision_with_list(enemy, self.scene['Bullets'])
            for bullet in bullets: 
                damage = (((2 * self.player.level+2)*(self.player.attack/enemy.defence))/100) * random.randint(75, 100)
                enemy.health -= damage
                self.last_hit_enemy = enemy 
                self.damage_text = str(int(damage))
                bullet.kill()
                if enemy.health <= 0:
                    self.player.gain_experience_from_enemy(enemy)
                    enemy.kill()

def main():
    """Main function"""
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

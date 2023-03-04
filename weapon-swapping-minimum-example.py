"""A minimal example showing a potential implementation for multiple weapons
in a python arcade game.

This demo focuses on animation, but it is assumed that when fleshed out into a 
working game each would have different properties, actions, and potentially
different variants of each weapon by modifing or extending each class.

Main ideas:
    - The player has a weapon list and a weapon_index that allows to pick from that list
    - A Weapon class is made that serves as a protocol scaffold to build out each weapon (very limited in this example)
    - Multiple weapons inherit from the Weapon class
    - In order to run the animations, the Player class has a 'action_frames' attribute. 
    - This serves as a queue to run the animation and serves the extra purpose of stopping any other
        actions while the action is underway (and prevents loading up multiple actions)
    - Once it is empty, normal play can resume
    - The player's odo property is a jank way of slowing down the animation rate.

    - In a previous, more advanced version of this code, an arrow could be fired by 
        adding a few extra pieces of logic to the Weapon class. This was cut for brevity. 

Ways to extend this code:
    - Multiple weapons are found as you progress through your game
    - Your backpack contains limited space.
    - You have different types of bow\gun\spells that fire differently
    - The Weapon class is modified to give each weapon stats that could be
        unique to each weapon type or even unique to each weapon. 
"""


import arcade

class Weapon:
    def __init__(self) -> None:
        self.action_frames = []

class Bow(Weapon):
    def __init__(self) -> None:
        super().__init__()
        for i in range(27, 36):
            texture = arcade.load_texture(f"assets/red-hood/red-hood{i}.png")
            self.action_frames.append(texture)

class Axe(Weapon):
    def __init__(self) -> None:
        super().__init__()
        for i in range(86, 129):
            texture = arcade.load_texture(f"assets/red-hood/red-hood{i}.png")
            self.action_frames.append(texture)

class Sword(Weapon):
    def __init__(self) -> None:
        super().__init__()
        for i in range(60, 85):
            texture = arcade.load_texture(f"assets/red-hood/red-hood{i}.png")
            self.action_frames.append(texture)

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/red-hood/red-hood1.png", 2)
        self.center_x = 400
        self.center_y = 400
        self.weapons = [Bow(), Sword(), Axe()]
        self.weapon_index = 0
        self.action_frames = []
        self.odo = 0
        self.odo_limit = 3
        self.idle_texture= arcade.load_texture("assets/red-hood/red-hood1.png")

    def attack(self):
        self.action_frames.extend(self.weapon.action_frames)

    def cycle_weapon(self):
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0 

    @property
    def is_acting(self):
        return len(self.action_frames) > 0 

    @property
    def weapon(self):
        return self.weapons[self.weapon_index]

    def update_animation(self, delta_time: float = 1 / 60):
        if self.odo < self.odo_limit:
            self.odo += 1
            return 
        self.odo = 0 

        if self.action_frames:
            self.texture = self.action_frames.pop(0)
            return 

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture
            return

    def update(self, delta_time: float = 1 / 60):
        super().update()
        self.update_animation()

class Game(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "weapon swapping")
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.scene = arcade.Scene()
        self.player = Player()
        self.scene.add_sprite('player', self.player)        # Track the current state of what key is pressed

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.scene.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.J and not self.player.is_acting:
            self.player.attack()

        if key == arcade.key.K and not self.player.is_acting:
            self.player.cycle_weapon()

game = Game()
arcade.run()

import arcade

PLAYER_MOVEMENT_SPEED = 10 

class Arrow(arcade.Sprite):
    def __init__(self, x, y, flipped):
        super().__init__(":resources:images/space_shooter/laserBlue01.png")
        self.center_x = x
        self.center_y = y
        self.change_x = 10
        if flipped:
            self.change_x *= -1
            self.angle = 180


class Weapon:
    def __init__(self) -> None:
        self.action_frames = []
        self.shoot_projectile = False
        self.projectile = None

class Bow(Weapon):
    def __init__(self) -> None:
        super().__init__()
        self.shoot_projectile = True
        self.projectile = Arrow
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
        self.weapons = []
        self.weapon_index = 0
        self.weapons.append(Bow())
        self.weapons.append(Sword())
        self.weapons.append(Axe())
        self.action_frames = []
        self.cur_texture = 0
        self.walk_textures = []
        self.odo = 0 
        self.odo_limit = 1

        self.idle_texture= arcade.load_texture("assets/red-hood/red-hood1.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(0, 24, 1):
            texture = arcade.load_texture(f"assets/red-hood/red-hood{i+3}.png")
            self.walk_textures.append(texture)


    def attack(self):
        self.action_frames.extend(self.weapon.action_frames)
        self.change_x = 0
        if self.weapon.shoot_projectile:
            return self.weapon.projectile

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
        if self.odo <= self.odo_limit:
            self.odo += 1
            return

        self.odo = 0

        if self.action_frames:
            self.texture = self.action_frames.pop(0)
            return 

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture
            self.cur_texture = 0
            return

        # Walking animation
        self.cur_texture += 1
        self.texture = self.walk_textures[self.cur_texture % len(self.walk_textures)]

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
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player) 

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time: float):
        self.scene.update()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player.change_y = 0

        # Process left/right
        if self.player.is_acting:
            self.player.change_x = 0
            return
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0

    def handle_attack(self):
        projectile_type = self.player.attack()
        if projectile_type:
            projectile = projectile_type(self.player.center_x, self.player.center_y, True)
            self.scene.add_sprite('projectiles', projectile)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.J and not self.player.is_acting:
            self.handle_attack()

        if key == arcade.key.K and not self.player.is_acting:
            self.player.cycle_weapon()


        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()


game = Game()
arcade.run()

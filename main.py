import arcade
from CharacterSelection import CharacterSelection
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Constants for the platforms
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
TILE_SCALING = 0.5

# Constants for the falling objects
OBJECT_SPAWN_INTERVAL = 1.0
MAX_FALLING_DISTANCE = 300


class AnimatedWalkingSprite(arcade.Sprite):
    def __init__(self, scale=1.0):
        super().__init__(scale=scale)
        self.stand_texture = None
        self.walk_textures = []
        self.texture = None
        self.current_texture_index = 0
        self.animation_time = 0.0
        self.animation_interval = 0.2

    def update_animation(self, delta_time: float = 1/60):
        self.animation_time += delta_time
        if self.animation_time >= self.animation_interval:
            self.current_texture_index += 1
            if self.current_texture_index >= len(self.walk_textures):
                self.current_texture_index = 0
            if self.current_texture_index == 0:
                self.texture = self.stand_texture
            else:
                self.texture = self.walk_textures[self.current_texture_index]
            self.animation_time = 0.0


class FallingObject(arcade.Sprite):
    def __init__(self, texture, scale):
        super().__init__(texture, scale)
        self.change_angle = 2

    def update(self):
        self.center_y -= 5
        self.angle += self.change_angle


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Create a SpriteList to hold the platforms
        self.platforms = None

        # Create a player character
        self.player = None

        # Create an object to fall down
        self.falling_objects = arcade.SpriteList()

        # Create a CharacterSelection view
        self.character_selection_view = CharacterSelection()

        self.character_selected = False
        self.timer = 30.0
        self.score = 0
        self.spawn_timer = 0.0

    def setup(self):
        self.character_selection_view.setup()

    def on_draw(self):
        arcade.start_render()

        if self.character_selected:
            self.platforms.draw()
            self.player.draw()
            self.falling_objects.draw()
            arcade.draw_text(
                f"Score: {self.score}",
                SCREEN_WIDTH - 10,
                SCREEN_HEIGHT - 30,
                arcade.color.BLACK,
                font_size=18,
                anchor_x="right",
            )
            arcade.draw_text(
                f"Time: {int(self.timer)}",
                SCREEN_WIDTH - 10,
                SCREEN_HEIGHT - 60,
                arcade.color.BLACK,
                font_size=18,
                anchor_x="right",
            )
        else:
            self.character_selection_view.on_draw()

    def on_update(self, delta_time):
        if self.character_selected:
            self.update_player(delta_time)
            self.update_falling_objects(delta_time)
            self.check_collision()
            self.update_timer(delta_time)

    def on_key_press(self, key, modifiers):
        if not self.character_selected and key == arcade.key.ENTER:
            self.character_selected = True
            self.setup_game()
        elif self.character_selected:
            if self.timer <= 0:
                self.end_game()
            elif key == arcade.key.UP:
                self.player.change_y = 10
            elif key == arcade.key.LEFT:
                self.player.change_x = -5
                self.player.update_animation()
            elif key == arcade.key.RIGHT:
                self.player.change_x = 5
                self.player.update_animation()

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.character_selection_view.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if (key == arcade.key.LEFT or key == arcade.key.RIGHT) and self.player is not None:
            self.player.change_x = 0
            self.player.texture = self.player.stand_texture

    def setup_game(self):
        self.character_selection_view.selected_character = self.character_selection_view.character_images[
            self.character_selection_view.character_index
        ]
        self.player = AnimatedWalkingSprite(scale=0.5)
        self.player.stand_texture = arcade.load_texture(self.character_selection_view.selected_character)
        self.player.walk_textures = []
        self.name = self.character_selection_view.character_names[
            self.character_selection_view.character_index
        ]
        for i in range(7):
            walk_texture = arcade.load_texture(
                f"Players/{self.name}/{self.name.lower()}_walk{i}.png"
            )
            self.player.walk_textures.append(walk_texture)
        self.player.texture = self.player.stand_texture
        self.player.center_x = 130
        self.player.center_y = 120

        # Platform setup
        self.platforms = arcade.SpriteList()

        # Create the platforms
        level_map = [
            "#########################",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "                        #",
            "#########################",
        ]

        for row in range(len(level_map)):
            for col in range(len(level_map[row])):
                if level_map[row][col] == "#":
                    platform = arcade.Sprite(
                        ":resources:images/tiles/grassMid.png", TILE_SCALING
                    )
                    platform.center_x = col * PLATFORM_WIDTH + PLATFORM_WIDTH / 2
                    platform.center_y = row * PLATFORM_HEIGHT + PLATFORM_HEIGHT / 2
                    self.platforms.append(platform)
                elif level_map[row][col] == "X":
                    platform = arcade.Sprite(
                        ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
                    )
                    platform.center_x = col * PLATFORM_WIDTH + PLATFORM_WIDTH / 2
                    platform.center_y = row * PLATFORM_HEIGHT + PLATFORM_HEIGHT / 2
                    self.platforms.append(platform)

    def update_player(self, delta_time):
        if self.player.left < 0:
            self.player.left = 0
        elif self.player.right > SCREEN_WIDTH - 1:
            self.player.right = SCREEN_WIDTH - 1
        if self.player.bottom < 0:
            self.player.bottom = 0
        elif self.player.top > SCREEN_HEIGHT - 1:
            self.player.top = SCREEN_HEIGHT - 1

        self.player.update_animation(delta_time)
        self.player.update()

    def spawn_falling_object(self):
        object_texture = random.choice(self.character_selection_view.character_objects)
        obj = FallingObject(object_texture, 0.5)
        obj.center_x = random.uniform(0, SCREEN_WIDTH)
        obj.center_y = SCREEN_HEIGHT
        self.falling_objects.append(obj)

    def update_falling_objects(self, delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer >= OBJECT_SPAWN_INTERVAL:
            self.spawn_falling_object()
            self.spawn_timer = 0.0

        self.falling_objects.update()

        for obj in self.falling_objects:
            if obj.top < self.player.bottom - MAX_FALLING_DISTANCE:
                obj.remove_from_sprite_lists()

    def check_collision(self):
        hit_list = arcade.check_for_collision_with_list(self.player, self.falling_objects)
        for obj in hit_list:
            obj.remove_from_sprite_lists()
            self.score += 1

    def update_timer(self, delta_time):
        self.timer -= delta_time
        if self.timer <= 0:
            self.timer = 0

    def end_game(self):
        self.character_selected = False
        self.score = 0
        self.timer = 30.0
        self.character_selection_view.selected_character = None
        self.platforms = None
        self.player = None
        self.falling_objects = arcade.SpriteList()

        self.setup_game()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

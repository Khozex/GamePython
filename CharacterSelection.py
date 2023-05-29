import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Character Selection"


class CharacterSelection(arcade.View):
    def __init__(self):
        super().__init__()
        self.character_index = 0
        self.character_images = [
            "Players/Female/female_stand.png",
            "Players/Male/male_stand.png",
            "Players/Robot/robot_stand.png"
        ]
        self.character_names = [
            "Female",
            "Male",
            "Robot"
        ]

        self.character_objects = [
            "Objects/female.png",
            "Objects/male.png",
            "Objects/robot.png"
        ]
        self.selected_character = None

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Select a Character", SCREEN_WIDTH/2, SCREEN_HEIGHT-50,
                         arcade.color.BLACK, font_size=24, anchor_x="center")
        if self.selected_character:
            text = self.character_names[self.character_index]
            arcade.draw_text("Selected Character: {}".format(text),
                             SCREEN_WIDTH/2, 50, arcade.color.BLACK, font_size=18, anchor_x="center")

        character_image = self.character_images[self.character_index]
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 300,
                                      arcade.load_texture(character_image))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.character_index = (self.character_index - 1) % len(self.character_images)
        elif key == arcade.key.RIGHT:
            self.character_index = (self.character_index + 1) % len(self.character_images)
        elif key == arcade.key.ENTER:
            self.selected_character = self.character_images[self.character_index]

    def on_update(self, delta_time):
        pass

    def setup(self):
        pass



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    character_selection_view = CharacterSelection()
    window.show_view(character_selection_view)
    arcade.run()

if __name__ == "__main__":
    main()
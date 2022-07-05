import arcade
import random

# Sprit info
SPRITE_SCALING = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
MOVEMENT_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Slime Eater"

# Slime info
RECT_WIDTH = 50
RECT_HEIGHT = 50


class Player(arcade.Sprite):
    """ Player Class """

    def update(self):

       # Move the slime
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check if we need to bounce of right edge
        if self.center_x > SCREEN_WIDTH - RECT_WIDTH / 2:
            self.change_x *= -1

        # Check if we need to bounce of top edge
        if self.center_y > SCREEN_HEIGHT - RECT_HEIGHT / 2:
            self.change_y *= -1

        # Check if we need to bounce of left edge
        if self.center_x < RECT_WIDTH / 2:
            self.change_x *= -1

        # Check if we need to bounce of bottom edge
        if self.center_y < RECT_HEIGHT / 2:
            self.change_y *= -1


class Coin(arcade.Sprite):
    """ Coin Class """

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1


class GameOver(arcade.View):
    """ Game Over Class """

    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def on_draw(self):
        self.clear()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 220, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Press the space bar to restart",
                         195, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.BATTLESHIP_GREY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.game_view = GameView()
            self.window.show_view(self.game_view)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        self.time_taken = 0
        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(":resources:images/enemies/"
                                    "slimeBlock.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(random.randrange(20, 75)):

            # Create the coin instance
            coin = Coin(":resources:images/items/coinGold.png",
                        SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_x = random.randrange(-3, 4)
            coin.change_y = random.randrange(-3, 4)

            # Add the coin to the list
            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    def on_draw(self):
        """Render the screen."""

        # This command has to happen before we start drawing
        self.clear()
        self.player_list.draw()
        self.coin_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 40, arcade.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.time_taken += delta_time

        # Call update on all sprites
        self.player_list.update()
        self.coin_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.kill()
            self.score += 1
            self.window.total_score += 1

        # If we've collected all the coins, then move to the gameover
        # screen.
        if len(self.coin_list) == 0:
            self.game_over_view = GameOver()
            self.game_over_view.time_taken = self.time_taken
            self.window.show_view(self.game_over_view)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH,
                           SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    start_view = GameView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

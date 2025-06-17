from ursina import *
from ursina.shaders import lit_with_shadows_shader
from random import uniform


class Key(Entity):
    '''Collectible key that glows and can be picked up by the player.'''

    def __init__(self, position, model_path, **kwargs):
        super().__init__(
            model=model_path,
            color=color.yellow,
            scale=1,
            position=position,
            collider=None,
            shader=lit_with_shadows_shader,
            **kwargs
        )
        self.active = True  # Whether the key is still collectible
        self.__create_indicator()

    def __create_indicator(self):
        '''Create a glowing sphere around the key for visual effect.'''
        self.glow = Entity(
            parent=self,
            model='sphere',
            scale=5,
            color=(255/255, 255/255, 100/255, 100/255),  # Yellowish transparent glow
            shader=lit_with_shadows_shader
        )

    def check_player_interaction(self, player_pos, key_count):
        '''Check if the player is close and pressing 'E' to collect the key.'''
        if not self.active:
            return key_count  # Already collected

        if distance(self.position, player_pos) < 2 and held_keys['e']:
            return self.collect(key_count)

        return key_count

    def collect(self, key_count):
        '''Handle key collection: destroy self and increase key count.'''
        print(f"Key collected! Total keys: {key_count + 1}")
        self.active = False
        destroy(self)
        return key_count + 1


class Generator(Entity):
    '''Generator entity that can be activated using a key.'''

    def __init__(self, **kwargs):
        super().__init__(
            scale=uniform(1.0, 1.0),
            collider='box',
            rotation_y=uniform(0, 360),
            shader=lit_with_shadows_shader,
            **kwargs
        )
        self.active = False  # Whether the generator is already activated
        self.__create_indicator()

    def __create_indicator(self):
        '''Add a red glowing indicator above the generator.'''
        self.indicator = Entity(
            parent=self,
            model='sphere',
            scale=0.5,
            color=color.red,
            y=2,  # Position indicator above generator
            shader=lit_with_shadows_shader,
            double_sided=True,
            emissive_color=color.red  # Glow effect
        )

    def check_interaction(self, player_pos, key_count):
        '''
        Check if the player is close and has a key.
        Activate generator if player presses 'E'.
        '''
        if self.active or key_count < 1:
            return key_count  # Already active or no keys

        if distance(self.position, player_pos) < 2 and held_keys['e']:
            self.interact(key_count - 1)
            return key_count - 1

        return key_count

    def interact(self, key_count):
        '''Activate the generator and change indicator color to green.'''
        print(f"Generator activated! Total keys: {key_count}")
        self.active = True
        self.indicator.color = color.green

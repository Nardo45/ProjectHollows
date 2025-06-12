from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import CullFaceAttrib
import os
print("Current working directory:", os.getcwd())

from Entities.terrain import generate_terrain, generate_trees

app = Ursina()

# Window Configurations
window.fullscreen = False
window.cog_button.enabled_setter(False)
window.fps_counter.enabled_setter(True)
window.collider_counter.enabled_setter(False)
window.entity_counter.enabled_setter(False)
window.exit_button.enabled_setter(False)

# Setup lighting
DirectionalLight(shadows=True)
AmbientLight(color=color.rgba(100, 100, 100, 0.5))

# Create ground plane
ground = generate_terrain(grid=(50, 50), scale=8.0, height_scale=5.0)

camera.clip_plane_far = 75
camera.clip_plane_near = 0.01

# Create a simple player entity
def spaw_player():
    player = FirstPersonController()
    player.position = Vec3(10, 10, 10) # Set position so that the player doesn't fall through the ground
invoke(spaw_player, delay=1) # Delay to ensure the ground is ready

# Basic skybox - built-into Ursina
Sky()
generate_trees(ground, tree_model_dir='../assets/models', max_trees=500, min_spacing=1.0)

def update():
    pass

def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.locked

app.run()
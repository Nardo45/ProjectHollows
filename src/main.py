from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import CullFaceAttrib

from Entities.terrain import generate_terrain

app = Ursina()

# Window Configurations
window.fullscreen = False
window.cog_button.enabled_setter(False)
window.fps_counter.enabled_setter(True)
window.collider_counter.enabled_setter(False)
window.entity_counter.enabled_setter(False)
window.exit_button.enabled_setter(False)

# Create ground plane
ground = generate_terrain(grid=(50, 50), scale=8.0, height_scale=5.0)

camera.clip_plane_far = 75
camera.clip_plane_near = 0.01

# Create a simple player entity
player = FirstPersonController()
player.position = Vec3(10, 10, 10) # Set position so that the player doesn't fall through the ground
mouse.locked = True

# Basic skybox - built-into Ursina
Sky()

tree = Entity(
    model='../assets/models/Tree0.obj',
    texture='../assets/textures/Bottom_T.jpg',
    scale=1,
    position=(20, 0, 20),
)
tree.model.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullFront))

def update():
    print(tree.model, tree.position)

app.run()
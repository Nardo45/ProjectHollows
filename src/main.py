# === main.py ===
# Entry point for the game. Initializes the world, entities, UI logic, and update loop.

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import unlit_shader

# === Game Modules ===
from Entities.terrain import generate_terrain, spawn_objects, get_valid_3D_world_positions, spawn_around_point
from Entities.interactables import Key, Generator
from Entities.enemy import Slasher

# === Initialization ===
app = Ursina()

# === Window Configuration ===
window.fullscreen = False
window.cog_button.enabled_setter(False)
window.fps_counter.enabled_setter(True)
window.collider_counter.enabled_setter(False)
window.entity_counter.enabled_setter(False)
window.exit_button.enabled_setter(False)

# === Lighting ===
DirectionalLight(shadows=True)
AmbientLight(color=color.rgba(100, 100, 100, 0))

# === Globals ===
key_count = 0
player = None
player_pos = Vec3(10, 10, 10)
slasher = None

# === Terrain & Environment Setup ===
ground = generate_terrain(grid=(50, 50), scale=8.0, height_scale=3.0)

# === Escape Zone ===
escape_zone = Entity(
    position=Vec3(5, 0, 5),
    model='sphere',
    scale=10,
    collider='mesh',
    color=color.rgba(50, 205, 50, 144),
    visible=False,
    shader=unlit_shader,
    enabled=False
)

# === Camera Configuration ===
camera.clip_plane_far = 75
camera.clip_plane_near = 0.01
camera.fov = 120

# === Deferred Entity Spawning ===
def spawn_gravity_entities():
    global player, slasher
    player = FirstPersonController()
    player.position = player_pos

    slasher = Slasher(
        model_path='../assets/creature/slasher.glb',
        player=player,
        scale=0.9,
        collider='box',
        position=Vec3(200, 3, 300),
        shader=unlit_shader
    )
invoke(spawn_gravity_entities, delay=1.5)

# === Skybox ===
Sky()

# === World Object Spawning ===
valid_positions = get_valid_3D_world_positions(ground)

valid_positions, tree_entities = spawn_objects(
    model_dir='../assets/trees',
    valid_positions=valid_positions,
    player_pos=player_pos,
    max_objects=500,
    min_spacing=3.0,
    scale_range=(0.5, 5.0),
    collect=True
)

valid_positions, used_positions, gen_models = spawn_objects(
    model_dir='../assets/generators',
    valid_positions=valid_positions,
    player_pos=player_pos,
    max_objects=3,
    min_spacing=5.0,
    gen_points_only=True,
)
generators = [Generator(model=gen_models[i], position=used_positions[i]) for i in range(min(3, len(used_positions)))]

valid_positions, used_positions = spawn_objects(
    model_dir='../assets/abandoned',
    valid_positions=valid_positions,
    player_pos=player_pos,
    max_objects=3,
    min_spacing=5.0,
    hitbox_type='mesh',
    scale_range=(0.8, 0.8),
    color=(0.5, 0.33, 0.24, 1),
    return_points=True
)

used_positions, key_models = spawn_around_point(
    points=used_positions,
    terrain_entity=ground,
    model_dir='../assets/keys',
    spacing=9.0,
    exclusion_radius=8.0,
)

keys = [Key(used_positions[i], key_models[i]) for i in range(min(3, len(used_positions)))]

# === Utility Functions ===
def is_in_view(entity, fov=140):
    dir_to_entity = (entity.world_position - camera.world_position).normalized()
    cam_forward = camera.forward.normalized()
    return cam_forward.angleDeg(dir_to_entity) < fov / 2

def update_tree_shadows():
    for tree in tree_entities:
        tree.visible = is_in_view(tree)

def all_generators_active():
    return all(gen.active for gen in generators)

# === Main Update Loop ===
def update():
    global key_count, player_pos

    update_tree_shadows()

    if slasher:
        slasher.slasher_update()

    if player:
        player_pos = player.position

    if not escape_zone.enabled and all_generators_active():
        print("All generators active! Escape zone enabled! Go back to the beginning!")
        escape_zone.enabled = True
        escape_zone.visible = True

    if escape_zone.enabled and distance(player_pos, escape_zone.position) < 8:
        print("You escaped! \U0001F389")
        application.quit()

    # Fall failsafe
    if player_pos.y < -50:
        player.position = Vec3(10, 3, 10)

    # Game Over
    if slasher and distance(slasher.position, player_pos) < 2:
        print("Game Over! The Slasher got you!")
        application.quit()

    # Key Logic
    keys_to_remove = []
    for key in keys:
        key_count = key.check_player_interaction(player_pos, key_count)
        if not key.active:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        keys.remove(key)

    # Generator Logic
    for gen in generators:
        key_count = gen.check_interaction(player_pos, key_count)

# === Input Bindings ===
def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.locked

    if key == 'shift':
        player.speed = 10 if player.speed == 5 else 5

# === Launch ===
app.run()

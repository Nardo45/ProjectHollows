# terrain.py
# Responsible for generating terrain, computing valid spawn points, and spawning objects dynamically.

import os
from random import sample, uniform, randint
from noise import pnoise2
from ursina import Entity, color, Vec3, Mesh, distance, raycast
from ursina.shaders import lit_with_shadows_shader


# === Terrain Generation ===

def generate_terrain(grid=(100, 100), scale=1.0, height_scale=1.0):
    """
    Procedurally generates a terrain mesh using Perlin noise.
    
    Args:
        grid (tuple): Dimensions of the terrain grid (width, height).
        scale (float): Horizontal scale of terrain.
        height_scale (float): Vertical scale of Perlin height.
    
    Returns:
        Entity: A terrain mesh with green vertex color and grass texture.
    """
    verts = []
    tris = []
    uvs = []
    colors = []

    w, h = grid

    for z in range(h):
        for x in range(w):
            y = pnoise2(x * 0.1, z * 0.1, octaves=3) * height_scale
            verts.append(Vec3(x * scale, y, z * scale))
            uvs.append((x / w, z / h))
            colors.append(color.green)

    for z in range(h - 1):
        for x in range(w - 1):
            i = x + z * w
            tris.append((i, i + 1, i + w))
            tris.append((i + 1, i + w + 1, i + w))

    terrain_entity = Entity(
        model=Mesh(vertices=verts, triangles=tris, uvs=uvs, colors=colors, static=True),
        texture="grass",
        collider="mesh",
        scale=1,
        shadow=False
    )

    return terrain_entity


# === Terrain Utility Functions ===

def get_valid_3D_world_positions(terrain_entity, margin=10.0):
    """
    Returns vertex positions on the terrain excluding those near the edge.
    
    Args:
        terrain_entity (Entity): The terrain mesh.
        margin (float): Distance from edge to exclude positions.
    
    Returns:
        list[Vec3]: Valid spawn positions.
    """
    verts = terrain_entity.model.vertices
    if not verts:
        return []

    min_x = max_x = verts[0].x
    min_z = max_z = verts[0].z
    for v in verts:
        min_x = min(min_x, v.x)
        max_x = max(max_x, v.x)
        min_z = min(min_z, v.z)
        max_z = max(max_z, v.z)

    margin_min_x = min_x + margin
    margin_max_x = max_x - margin
    margin_min_z = min_z + margin
    margin_max_z = max_z - margin

    valid_verts = [v for v in verts if margin_min_x <= v.x <= margin_max_x and margin_min_z <= v.z <= margin_max_z]
    return valid_verts


def get_terrain_height(terrain_entity, x: float, z: float) -> float:
    """
    Casts a ray downward to get terrain height at a given (x, z).
    
    Returns:
        float: Height (y) at specified x, z or 0 if not found.
    """
    ray = raycast(
        origin=Vec3(x, 100, z),
        direction=Vec3(0, -1, 0),
        distance=200,
    )
    if ray.hit and ray.entity == terrain_entity:
        return ray.world_point.y
    return 0


# === Object Spawning ===

def spawn_around_point(points, terrain_entity, model_dir, spacing=3.0, exclusion_radius=1.5):
    """
    Spawns a model at a random valid position around each given point.

    Returns:
        tuple: (used_positions, model_paths)
    """
    models = sorted([
        os.path.join(model_dir, f)
        for f in os.listdir(model_dir)
        if f.endswith('.glb')
    ])

    used_positions = []
    found_paths = []

    for point in points:
        pos = None

        while True:
            candidate_pos = Vec3(
                point.x + uniform(spacing, spacing),
                get_terrain_height(terrain_entity, point.x, point.z),
                point.z + uniform(spacing, spacing)
            )

            if distance(candidate_pos, point) >= exclusion_radius:
                pos = candidate_pos
                break

        if pos:
            model_path = models[randint(0, len(models) - 1)]
            found_paths.append(model_path)
            used_positions.append(pos)

    return used_positions, found_paths


def spawn_objects(
        model_dir,
        valid_positions,
        player_pos,
        max_objects=100,
        min_spacing=3.0,
        hitbox_type='capsule',
        scale_range=(0.5, 5),
        color=(0.1, 0.3, 0.1, 1),
        debug_positions=False,
        return_points=False,
        gen_points_only=False,
        collect=False
        ):
    """
    Randomly places models on valid terrain positions, avoiding overlaps.

    Args:
        model_dir (str): Directory containing .glb models.
        valid_positions (list): List of potential spawn positions.
        player_pos (Vec3): Player starting position (excluded from spawn).
        max_objects (int): Max number of objects to place.
        min_spacing (float): Min spacing between objects.
        hitbox_type (str|None): Collider type or None.
        scale_range (tuple): Min and max scale.
        color (Color|None): Object tint.
        debug_positions (bool): Place objects near player for debug.
        return_points (bool): Whether to return used points.
        gen_points_only (bool): Skip entity creation.
        collect (bool): Whether to return created Entity list.

    Returns:
        Depending on flags:
        - candidate_positions, used_positions, model_paths (if gen_points_only)
        - candidate_positions, used_positions (if return_points)
        - candidate_positions, created_entities (default)
    """
    models = sorted([
        os.path.join(model_dir, f)
        for f in os.listdir(model_dir)
        if f.endswith('.glb')
    ])

    if not models:
        print("No 3D models found in the specified directory.")
        return

    candidate_positions = sample(valid_positions, len(valid_positions))
    used_positions = [player_pos]
    model_paths = []
    collection = []
    objects_placed = 0

    for pos in candidate_positions:
        if objects_placed >= max_objects:
            break

        if debug_positions:
            pos = player_pos + Vec3(uniform(-10, 10), -10, uniform(-10, 10))

        if any(distance(pos, existing_pos) < min_spacing for existing_pos in used_positions):
            continue

        model_path = models[randint(0, len(models) - 1)]

        if not gen_points_only:
            entity_args = {
                "model": model_path,
                "position": pos,
                "scale": uniform(*scale_range),
                "rotation_y": uniform(0, 360),
                "collider": hitbox_type,
                "shader": lit_with_shadows_shader,
            }
            if color:
                entity_args["color"] = color

            object = Entity(**entity_args)
            if collect:
                collection.append(object)

        else:
            model_paths.append(model_path)

        used_positions.append(pos)
        objects_placed += 1

    if gen_points_only:
        return candidate_positions, used_positions[1:], model_paths
    elif return_points:
        return candidate_positions, used_positions[1:]
    else:
        return candidate_positions, collection

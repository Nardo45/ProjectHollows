from noise import pnoise2
from ursina import Entity, color, Vec3, Mesh, distance
from ursina.shaders import lit_with_shadows_shader
from random import sample, uniform, randint
import os

def generate_terrain(grid=(100, 100), scale=1.0, height_scale=1.0):
    '''Procedurally generates a terrain mesh using Perlin noise.'''
    verts = []      # Stores all 3D coordinates for terrain points (Vec3)
    tris = []       # Stores indices of vertices that form triangles (int)
    uvs = []        # Stores UV coordinates for texture mapping (Vec2)
    colors = []     # Stores color values for each vertex (Color)

    w, h = grid     # Unpack grid dimensions
    # Loops through every tile coordinate in the grid
    for z in range(h):
        for x in range(w):
            # Param 1 and 2: Smoothes the noise, Lower values = larger hills
            # Param 3: number of noise layers
            y = pnoise2(x * 0.1, z * 0.1, octaves=3) * height_scale
            verts.append(Vec3(x * scale, y, z * scale))  # Append vertex position
            uvs.append((x / w, z / h))  # Append UV coordinates
            colors.append(color.green)  # Append color (green for grass)

    for z in range(h - 1):
        for x in range(w - 1):
            # Create two triangles for each square in the grid
            i = x + z * w # Index of the top left vertex
            tris.append((i, i + 1, i + w))
            tris.append((i + 1, i + w + 1, i + w))

    terrain_entity = Entity(
        model=Mesh(vertices=verts, triangles=tris, uvs=uvs, colors=colors, static=True),
        texture="grass",
        collider="mesh",
        scale=1,
        shadow=False
    )

    return terrain_entity  # Return the created terrain entity

def generate_trees(terrain_entity, tree_model_dir='assets/models', max_trees=100, min_spacing=3.0):
    '''Randomly scatters tree models across the terrain without overlaps.'''
    
    mesh = terrain_entity.model
    verts = mesh.vertices

    # Load all tree model paths
    # Created using a generator expression
    tree_models = sorted([
        os.path.join(tree_model_dir, f)
        for f in os.listdir(tree_model_dir)
        if f.endswith('.glb')
    ])

    if not tree_models:
        print("No tree models found in the specified directory.")
        return
    
    # Shuffle terrain positions and pick candidates
    candidate_positions = sample(verts, len(verts))
    placed_positions = [Vec3(10, 10, 10),]
    trees_placed = 0

    for pos in candidate_positions:
        # Break if max trees limit is reached
        if trees_placed >= max_trees:
            break

        # Check if the position is too close to an already placed tree
        if any(distance(pos, existing_pos) < min_spacing for existing_pos in placed_positions):
            continue

        # Choose a random tree model
        tree_model_path = tree_models[0] #tree_models[randint(0, len(tree_models) - 1)]

        # Spawn the tree entity
        Entity(
            model=tree_model_path,
            position=pos + Vec3(0, 0.1, 0),  # Slightly above the terrain
            scale=uniform(0.5, 5),  # Random scale for variety
            rotation_y=uniform(0, 360),  # Random rotation for natural look
            collider='capsule',
            color=(0.1, 0.3, 0.1, 1),  # Slightly darker green
            shader=lit_with_shadows_shader
        )
        print(f"Placed tree at {pos} using model {tree_model_path}")

        placed_positions.append(pos)
        trees_placed += 1
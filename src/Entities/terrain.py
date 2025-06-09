from noise import pnoise2
from ursina import Entity, color, Vec3, Mesh

def generate_terrain(grid=(100, 100), scale=1.0, height_scale=1.0):
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
    print(f"Triangles: {len(tris)}")

    return terrain_entity  # Return the created terrain entity
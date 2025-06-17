If you saw the timeline before just forget about it. It didn't work out

requirements:
    You should just need to type 'pip install ursina' in the terminal/console.

    Run main.py while you're inside src, ursina couldn't find the model paths when
    I was outside of src for whatever reason.

    For the +50 marks I've done:
        1. More user-defined Classes, the 2 extra ones are Generator and Slasher
        2. Code is organized into multiple files
        3. The terrain uses pnoise2 to generate the hills, it's generated procedurally
        4. Suggest an idea: Use of generator expressions. I'll include an example that was used in main.py
        This is sometimes called a list comprehension, but it's actually a generator expression, they're similar
            generators = [Generator(model=gen_models[i], position=used_positions[i]) for i in range(min(3, len(used_positions)))]
        5. Suggest an idea: Use of 3D graphics and calculations.
        I did mess with most of the models in blender to be more optimized and render better in the world.
        I used 3D calculations to generate the terrain in the generate_terrain() function in terrain.py


        BONUS:
            In case my suggestions aren't good here are some more
            6. Use of shading
            7. Optimizing 3D rendering by culling 3D objects out of view
            8. Use of defensive programming
                One example being the "Fall failsafe" found in the update() function in main.py
            9. Use of gitignore

controls:
    WASD to move
    space to jump
    shift to toggle running
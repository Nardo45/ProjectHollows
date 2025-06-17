from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import unlit_shader

class Slasher(Entity):
    def __init__(
        self,
        player: FirstPersonController = None,
        model_path: str = None,
        wander_radius=5,
        wander_change_interval=10.0,
        chase_speed=6,
        wander_speed=3,
        aggro_distance=80,
        **kwargs
    ):
        super().__init__(model=None, **kwargs)
        self.player = player

        self.visual = Entity(
            parent=self,
            model=model_path,
            y=2.8,              # half your known height
            scale=1,           # or whatever scale you need
            shader=unlit_shader
        )

        # Printing flag
        self.flag = True

        # AI parameters
        self.wander_radius = wander_radius
        self.wander_change_interval = wander_change_interval
        self.chase_speed = chase_speed
        self.wander_speed = wander_speed
        self.aggro_distance = aggro_distance

        # State
        self.state = 'wander'
        self.wander_timer = 0
        self.wander_dir = Vec3(0,0,1)

        # Physics
        self.gravity = 9.8
        self.velocity_y = 0

    def slasher_update(self):
        self.apply_gravity()
        self.ai()

    def apply_gravity(self):
        # Always start from way up high
        origin = Vec3(self.x, 100, self.z)
        # Cast a ray downward while ignoring self
        hit = raycast(
            origin,
            Vec3(0, -1, 0),
            distance=200,
            traverse_target=scene,
            ignore=(self, self.visual),
            debug=False
        )
    
        if hit.hit:
            # Snap to the ground
            ground_y = hit.world_point.y
            self.y = ground_y
        else:
            # No ground under slasher, apply gravity normally
            self.velocity_y -= self.gravity * time.dt
            self.y += self.velocity_y * time.dt

    def ai(self):
        # Distance to player
        dist = distance(self.world_position, self.player.world_position)

        # State transitions
        if self.state == 'wander' and dist < self.aggro_distance:
            self.state = 'chase'
        elif self.state == 'chase' and dist > self.aggro_distance * 1.2:
            # Small hysteresis so it doesn't flicker
            self.state = 'wander'

        # State behaviours
        if self.state == 'wander':
            self.wander()
        else:
            self.chase()

    def wander(self):
        self.wander_timer -= time.dt
        if self.wander_timer <= 0:
            angle = random.random() * 2 * math.pi
            self.wander_dir = Vec3(math.sin(angle), 0, math.cos(angle))
            self.wander_timer = self.wander_change_interval

        # Predict future position
        next_pos = self.position + self.wander_dir * self.wander_speed * time.dt
        forward_origin = Vec3(next_pos.x, 100, next_pos.z)

        hit = raycast(
            origin=forward_origin,
            direction=Vec3(0, -1, 0),
            distance=200,
            traverse_target=scene,
            ignore=(self, self.visual),
            debug=False
        )

        if hit.hit:
            self.position += self.wander_dir * self.wander_speed * time.dt
            # Rotate to face the direction of movement
            angle = math.degrees(math.atan2(self.wander_dir.x, self.wander_dir.z)) + 180
            self.rotation_y = angle
        else:
            # No ground ahead – stop and pick a new direction next frame
            self.wander_timer = 0
            
        if self.flag != False:
            print("He does not see you.")
            self.flag = False

    def chase(self):
        # Head straight for the player
        if self.flag != True:
            print("He SEes YoU")
            self.flag = True
        dir_to_player = (self.player.position - self.position).normalized()
        self.x += dir_to_player.x * self.chase_speed * time.dt
        self.z += dir_to_player.z * self.chase_speed * time.dt

        # Rotate to face movement direction
        angle = math.degrees(math.atan2(dir_to_player.x, dir_to_player.z)) + 180
        self.rotation_y = angle
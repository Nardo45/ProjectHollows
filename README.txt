Player is trapped in a forest at night
    Must find and sole 3-5 puzzles at different locations (cabins, ruins, etc...)
    Each puzzle activates a generator
    Once all are on, th eplayer can escape through a gate or vehicle
    Meanwhile, a creature (e.g., The Rake or Goatman) stalks the area

PUZZLE + GENERATOR PLAN:
| Puzzle # | Location          | Type                                        | Generator Toggled?  |
| -------- | ----------------- | ------------------------------------------- | ------------------- |
| 1        | Abandoned Cabin   | Simple memory game (flip switches in order) | ✅                  |
| 2        | Forest Altar      | Simon Says with lights                      | ✅                  |
| 3        | Water Tower Shack | Pipe rotation minigame                      | ✅                  |
| 4        | Ranger's Tent     | Find missing gear item                      | ✅                  |
| 5 (opt.) | Burnt-out Church  | Sliding tile puzzle or hidden symbols       | ✅                  |


ENEMY DESIGN:
    Creature Options
        The Rake: Fast, lean, scuttles through brush, screeches
        Goatman: Tall, stalks quietly, shape-shifting lore (could appear as random objects before transforming)
        Original Entity: Mix traits and make your own. Ex: “Hollow Walker” — a glowing-eyed humanoid that flickers in/out of existence with static effects.

    Mechanics:
        The creature patrols randomly until a generator is powered on.
        With each new generator, it gets faster or more aggressive.
        Appears more often if the player lingers.

FEATURES TO IMPLEMENT:
| Feature                        | Difficulty | Notes                                           |
| ------------------------------ | ---------- | ----------------------------------------------- |
| First-person movement & camera | Easy       | Built-in to Ursina                              |
| Foggy forest environment       | Easy       | Trees can be reused props                       |
| Puzzle interaction             | Medium     | Minigame logic per puzzle                       |
| Generator activation           | Easy       | Visual/sound cue + state flag                   |
| Creature patrol & chase AI     | Medium     | Basic pathfinding/random patrol + trigger chase |
| Jumpscare audio/static FX      | Easy       | Sound file + screen flicker effect              |
| Endgame state (escape gate)    | Easy       | Open gate once all puzzles complete             |

FEASIBLE TIMELINE:
| Days  | Tasks                                                     |
| ----- | --------------------------------------------------------- |
| 1–2   | Set up engine, forest map, first-person controls          |
| 3–4   | Create basic puzzle interaction + activate generator      |
| 5–6   | Add 1–2 more puzzles, test generator system               |
| 7–8   | Add enemy AI (patrol + chase + scare mechanic)            |
| 9     | Win condition + gate unlock logic                         |
| 10    | Add polish: fog, sound, jumpscares, UI prompt (“press E”) |
| 11–12 | Test, debug, add optional puzzles                         |
| 13–14 | Package project + polish + record demo if needed          |
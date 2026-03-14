import math
import os

# ── Tile emojis ───────────────────────────────────────────────
FLOOR  = "🟫"
PLAYER = "🧙"

# ── Config ────────────────────────────────────────────────────
GRID_SIZE   = 6
MOVE_BUDGET = 2

# ── Monster roster ────────────────────────────────────────────
# Define all monster types here. Add new ones freely.
MONSTER_TYPES = {
    "goblin":  dict(emoji="👹", hp=12, attack=4, chase_radius=5, atk_min=1, atk_max=1),
    "archer":  dict(emoji="🏹", hp=7,  attack=3, chase_radius=5, atk_min=2, atk_max=3),
    "mage":    dict(emoji="🧿", hp=8,  attack=5, chase_radius=6, atk_min=3, atk_max=4),
    "skeleton":dict(emoji="💀", hp=10, attack=3, chase_radius=3, atk_min=1, atk_max=1),
    "dragon":  dict(emoji="🐉", hp=25, attack=8, chase_radius=6, atk_min=2, atk_max=5),
    "snake":   dict(emoji="🐍", hp=6,  attack=2, chase_radius=4, atk_min=1, atk_max=1),
    "troll":   dict(emoji="🧌", hp=20, attack=6, chase_radius=3, atk_min=1, atk_max=1),
    "witch":   dict(emoji="🧙‍♀️", hp=9, attack=7, chase_radius=6, atk_min=4, atk_max=5),
}


# ── Monster class ─────────────────────────────────────────────
class Monster:
    def __init__(self, x, y, emoji, hp, attack,
                 chase_radius, atk_min, atk_max):
        self.x, self.y    = x, y
        self.emoji        = emoji
        self.hp           = hp
        self.attack       = attack
        self.chase_radius = chase_radius
        self.atk_min      = atk_min
        self.atk_max      = atk_max
        self.alive        = True

    def move_toward(self, px, py, occupied):
        dist = math.dist((self.x, self.y), (px, py))
        if dist > self.chase_radius:
            return
        if dist > self.atk_max:
            self._step(px, py, occupied, approach=True)
        elif dist < self.atk_min:
            self._step(px, py, occupied, approach=False)

    def _step(self, px, py, occupied, approach):
        dx = 0 if px == self.x else int(math.copysign(1, px - self.x))
        dy = 0 if py == self.y else int(math.copysign(1, py - self.y))
        if not approach:
            dx, dy = -dx, -dy
        if abs(px - self.x) >= abs(py - self.y):
            candidates = [(self.x+dx, self.y), (self.x, self.y+dy)]
        else:
            candidates = [(self.x, self.y+dy), (self.x+dx, self.y)]
        for nx, ny in candidates:
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in occupied:
                self.x, self.y = nx, ny
                return

    def can_attack(self, px, py):
        return self.atk_min <= math.dist((self.x,self.y),(px,py)) <= self.atk_max

    def is_adjacent(self, px, py):
        return abs(self.x-px) <= 1 and abs(self.y-py) <= 1


# ── Spawn helper ──────────────────────────────────────────────
def spawn_monsters(counts: dict[str, int]) -> list[Monster]:
    """
    Build a monster list from a name→count dict.
    Monsters are placed at random non-overlapping tiles,
    kept away from the player's starting corner (0,0).

    Example:
        spawn_monsters({"goblin": 2, "archer": 1, "dragon": 1})
    """
    import random

    # All tiles except the player's starting 2x2 corner
    safe_tiles = [
        (x, y)
        for x in range(GRID_SIZE)
        for y in range(GRID_SIZE)
        if not (x <= 1 and y <= 1)
    ]
    random.shuffle(safe_tiles)
    tile_pool = iter(safe_tiles)

    monsters = []
    for name, count in counts.items():
        if name not in MONSTER_TYPES:
            raise ValueError(f"Unknown monster type '{name}'. "
                             f"Choose from: {list(MONSTER_TYPES.keys())}")
        stats = MONSTER_TYPES[name]
        for _ in range(count):
            try:
                x, y = next(tile_pool)
            except StopIteration:
                raise ValueError("Too many monsters for the grid size!")
            monsters.append(Monster(x, y, **stats))

    return monsters


# ── Game class ────────────────────────────────────────────────
class Game:
    def __init__(self, monster_counts: dict[str, int] | None = None):
        """
        monster_counts: dict of monster name → how many to spawn.
        Defaults to a balanced starter encounter if not provided.

        Examples:
            Game()                                         # default encounter
            Game({"goblin": 3})                            # goblin horde
            Game({"archer": 2, "mage": 1})                 # ranged squad
            Game({"goblin": 1, "archer": 1, "dragon": 1})  # mixed
        """
        if monster_counts is None:
            monster_counts = {"goblin": 1, "archer": 1, "mage": 1}

        self.grid      = [[FLOOR] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.player_x  = 0
        self.player_y  = 0
        self.player_hp = 30
        self.player_atk= 5
        self.turn      = 1
        self.monsters  = spawn_monsters(monster_counts)

    # ── Helpers ───────────────────────────────────────────────
    def occupied_tiles(self, exclude=None):
        return {(m.x, m.y) for m in self.monsters if m.alive and m is not exclude}

    # ── Rendering ─────────────────────────────────────────────
    def render(self):
        os.system("cls" if os.name == "nt" else "clear")
        alive = [m for m in self.monsters if m.alive]
        print(f"  Turn {self.turn}  |  ❤️  HP: {self.player_hp}  |  ⚔️  ATK: {self.player_atk}"
              f"  |  👾 Remaining: {len(alive)}\n")
        for row in range(GRID_SIZE):
            line = ""
            for col in range(GRID_SIZE):
                if col == self.player_x and row == self.player_y:
                    line += PLAYER; continue
                mon = next((m for m in self.monsters
                            if m.alive and m.x==col and m.y==row), None)
                line += mon.emoji if mon else self.grid[row][col]
            print(line)
        print()

    # ── Player movement ───────────────────────────────────────
    def player_turn(self):
        dirs = {"w":(0,-1),"s":(0,1),"a":(-1,0),"d":(1,0)}
        moves_left = MOVE_BUDGET
        while moves_left > 0:
            self.render()
            print(f"  Move phase — {moves_left} step(s) left")
            print("  [W/A/S/D] move   [Enter] skip remaining steps\n")
            key = input("  > ").strip().lower()
            if key == "": break
            if key not in dirs: continue
            dx, dy = dirs[key]
            nx, ny = self.player_x+dx, self.player_y+dy
            if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                print("  Can't move there."); input("  [Enter]"); continue
            if any(m.alive and m.x==nx and m.y==ny for m in self.monsters):
                print("  A monster is blocking that tile!"); input("  [Enter]"); continue
            self.player_x, self.player_y = nx, ny
            moves_left -= 1

    # ── Action phase ──────────────────────────────────────────
    def action_phase(self):
        self.render()
        print("  Action phase")
        print("  [1] Attack   [2] Rest (+3 HP)   [3] Wait\n")
        targets = [m for m in self.monsters
                   if m.alive and m.is_adjacent(self.player_x, self.player_y)]
        if targets:
            print("  Adjacent monsters: "
                  + "  ".join(f"{m.emoji}({m.hp}hp)" for m in targets))
        else:
            print("  No monsters adjacent (your attack range is 1 tile).")
        print()
        choice = input("  > ").strip()
        if choice == "1":
            if not targets:
                print("  Nothing in range!")
            else:
                t = targets[0]
                t.hp -= self.player_atk
                print(f"  You hit {t.emoji} for {self.player_atk} dmg! ({max(t.hp,0)} HP left)")
                if t.hp <= 0:
                    t.alive = False
                    print(f"  {t.emoji} defeated! 💥")
            input("  [Enter]")
        elif choice == "2":
            self.player_hp = min(self.player_hp+3, 30)
            print(f"  You rest. HP: {self.player_hp}")
            input("  [Enter]")

    # ── Monster turn ──────────────────────────────────────────
    def monster_turn(self):
        attacked = False
        for m in self.monsters:
            if not m.alive: continue
            blocked = self.occupied_tiles(exclude=m)
            blocked.add((self.player_x, self.player_y))
            m.move_toward(self.player_x, self.player_y, blocked)
            if m.can_attack(self.player_x, self.player_y):
                self.player_hp -= m.attack
                print(f"  {m.emoji} attacks you for {m.attack} damage!")
                attacked = True
        if attacked:
            input("  [Enter]")

    # ── Main loop ─────────────────────────────────────────────
    def run(self):
        while self.player_hp > 0:
            if all(not m.alive for m in self.monsters):
                self.render()
                print("  🎉 All monsters defeated! You win!")
                return
            self.player_turn()
            self.action_phase()
            self.monster_turn()
            self.turn += 1
        self.render()
        print("  💀 You have been defeated...")


# ── Launch ────────────────────────────────────────────────────
if __name__ == "__main__":
    # ↓ Change this to whatever encounter you want ↓
    Game({
        "goblin":  3,
        "archer":  0,
        "mage":    0,
        "skeleton":0,
        "dragon":  0,
        "snake":   0,
        "troll":   0,
        "witch":   0,
    }).run()
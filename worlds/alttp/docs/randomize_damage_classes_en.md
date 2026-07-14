# Randomize Damage Classes

`randomize_damage_classes` changes how enemies respond to Link's weapons and items. It is an advanced option. A seed can still be completed, but the combat rules may stop matching player muscle memory from vanilla A Link to the Past.

## What is a damage class?

The game does not store a separate damage value for every weapon on every enemy. Instead, most attacks are grouped into 16 damage classes. Each enemy has a table saying what happens when it is hit by each class.

An entry in an enemy's damage table can mean:

- `0`: no damage and no useful effect
- a normal damage amount, such as `1`, `2`, `4`, `8`, `16`, `32`, or `100`
- `249`: transform into a fairy
- `250`: transform into a 0-HP yellow slime
- `251`, `252`, or `255`: stun
- `253`: incinerate
- `254`: freeze

The randomizer changes the enemy damage tables. It does not change which button swings the sword or casts Fire Rod. If Fire Rod's class does something different to an enemy, Fire Rod still delivers Fire Rod's damage class.

## Damage Classes by Item

These are the damage classes Link can normally deliver.

| Class | Source |
| --- | --- |
| 0 | Blue Boomerang, Red Boomerang |
| 1 | Fighter Sword slash, Master/Tempered/Golden Sword beams, Cane of Somaria, Cane of Byrna |
| 2 | Fighter Sword spin, Master Sword slash, Tempered Sword drawn poke |
| 3 | Master Sword spin, Tempered Sword slash, Hammer, thrown pots, thrown frozen enemies, Fake Master Sword |
| 4 | Tempered Sword spin, Golden Sword slash |
| 5 | Golden Sword spin |
| 6 | Normal arrows |
| 7 | Hookshot |
| 8 | Bombs |
| 9 | Silver arrows |
| 10 | Magic Powder |
| 11 | Fire Rod |
| 12 | Ice Rod |
| 13 | Bombos |
| 14 | Ether |
| 15 | Quake |

Sword classes are the easiest part to misunderstand:

- Fighter Sword can use class 1 with normal swings and class 2 with spin attacks.
- Master Sword can use class 1 with sword beams, class 2 with normal swings, and class 3 with spin attacks.
- Tempered Sword can use class 1 with sword beams, class 2 with the drawn sword poke, class 3 with normal swings, and class 4 with spin attacks.
- Golden Sword can use class 1 with sword beams, class 3 with the drawn sword poke, class 4 with normal swings, and class 5 with spin attacks.

Sword beams require full health in-game. Logic assumes Link can be at full health when that matters.

Class 2 is special because it can be lost when upgrading to Golden Sword. The randomizer protects logic from that by making sure an important class 2 result is also covered by another sword class, or by removing that unsafe class 2 result.

Normal arrows and silver arrows are separate classes. In this randomizer they are not constrained to behave the same way.

## Option Values

### Vanilla

Enemy damage tables are not randomized.

### Enemy Swap

Enemies swap whole damage profiles with each other. For example, one enemy may inherit another enemy's pattern of which classes damage, stun, freeze, incinerate, or transform it.

Some profiles are not allowed on some bosses because they can break phase changes or reward drops. The randomizer avoids unsafe swaps instead of preserving a perfect one-to-one shuffle.

### Damage Class Swap

Damage class meanings are globally shuffled across enemies. For example, Fire Rod might inherit what Ice Rod would have done, and Ice Rod might inherit what arrows would have done.

This is the mode where it is most useful to think "what class does this item deliver?" rather than "what does this item usually do?"

### Mixed

First performs a global Damage Class Swap, then performs Enemy Swap.

### Chaos

Generates random damage table results for each randomized enemy. Chaos can create unusual combinations that do not resemble vanilla enemy profiles.

### Nightmare

Each enemy has no more than one concurrently available damage class that can defeat it. Stuns and freezes may still exist on other classes, but only one class should be the actual way to remove that enemy.

This is intended to make combat logic very visible and punishing. It is possible for different enemies in the same seed to require very different tools.

## Logic Guarantees

The generator tries to keep required combat possible.

- Required enemy kills must have at least one logical kill method.
- Enemies with no meaningful damage table are not included in damage class randomization.
- The `max_attacks_in_logic` option limits how many hits a regular enemy kill may require. It does not apply to bosses.
- Key drop enemies must be truly defeatable. Transforming an enemy into something else only counts when that actually allows the key drop to be obtained.
- Red Bari key drops require an incinerating kill method.
- Bosses are allowed to take more hits than regular enemies.
- In hard item pools, class 4 is not shuffled. In expert item pools, classes 4 and 5 are not shuffled. This prevents logic from depending on sword damage classes that the item pool cannot provide.

These guarantees are about logic, not comfort. A seed may ask you to use awkward but valid combat methods.

## Mechanics That Matter More With This Option

### Pots, Fake Master Sword, and Frozen Enemies

Thrown pots deal class 3 damage.

A Fake Master Sword can also deal class 3 damage once.

Frozen enemies can be picked up and thrown. A thrown frozen enemy deals class 3 damage to other enemies. Logic may expect this. The frozen enemy does not kill itself, so a room may still require another way to finish the enemy you froze.

Hammer always destroys frozen enemies regardless of Hammer's damage class.

### Medallions

Bombos, Ether, and Quake are room-wide effects. If their class can affect several enemies in a room, one cast can count against all of them.

Quake generally does not affect enemies that are airborne at the time it resolves. This matters for enemies that spend time off the ground.

### Magic and Consumables

Logic counts arrows, bombs, and magic. Green or blue potion access can increase available magic based on bottles. This means a magic-heavy solution may be in logic if the seed gives enough magic capacity or refill access.

Cane of Byrna has an initial magic cost and then a drain cost while it remains active.

## Important Special Cases

Some enemies and bosses have hardcoded behavior outside the ordinary damage table. The randomizer logic accounts for these where they matter.

### Lightning Gate / Hyrule Castle Barrier

Most projectiles and medallions cannot affect the Lightning Gate even if its damage table says that class would do damage.

The logical ways through are:

- Cape
- a sword contact class that removes the barrier
- Magic Powder if class 10 removes the barrier
- swordless Hammer behavior where applicable

Master Sword or better can normally contact the barrier. Fighter Sword contact is rejected by the game.

### Moldorm and Giant Moldorm

Moldorm's tail is a special contact target and is effectively a melee surface.

Magic Powder can affect Moldorm's head. If class 10 can defeat Moldorm, Magic Powder can be a logical alternate route. This is not something players normally care about with vanilla tables, but it can matter when classes are randomized.

### Trinexx Main Body

During Trinexx's final phase, the middle body section is treated as melee-only for logic.

Trinexx's head can be hit by many non-melee sources before the middle section starts blinking, but that window is very short. The randomizer may allow the table to contain those effects, but that head-window damage is not considered logical.

### Trinexx Red and Blue Heads

The red and blue heads have a boss-specific vulnerability state. Before that state, sword and hammer contact bounces off. Non-melee attacks such as arrows, boomerangs, hookshot, bombs, sword beams, canes, Magic Powder, Fire Rod, Ice Rod, Bombos, and Ether can make a side head vulnerable if that damage class has a damage, stun, or freeze effect. Quake is not considered logical for this because the generic Quake damage path rejects airborne sprites.

Once a side head is vulnerable, melee attacks can damage it. Logic assumes up to three melee hits during each vulnerability window before another non-melee vulnerability hit is needed.

### Blind

Blind does not use normal HP depletion. Any damage source that successfully connects and has a nonzero, non-transform effect counts as one hit. Blind needs 3 hits per phase and has 3 phases, so logic treats Blind as needing 9 successful hits.

The amount in Blind's damage table does not change that hit count.

### Arrghus

Hookshot is required to pull Arrghus fuzz, but Hookshot does not count as damaging the fuzz through its normal damage class.

### Terrorpins

Terrorpins must be flipped with Hammer before ordinary damage matters. Even if another class could damage a flipped Terrorpin, Hammer access is still required.

### Buzzblobs

Sword and Hammer contact can trigger Buzzblob's shock behavior. Logic distinguishes safe delivery methods from unsafe contact methods, even if they share a damage class.

### Anti-Fairies

Normal melee contact is not a reliable way to damage Anti-Fairies. Sword beams and projectile-like sources can matter if their classes have damage effects.

### Floating Stalfos Heads

Some positive damage table results only knock the enemy back instead of killing it. Logic uses explicit delivery rules for these.

### Boss Special Effects

Many bosses do not tolerate transformations, incineration, or permanent freeze effects safely. Those effects can prevent phase changes or reward drops. The randomizer sanitizes boss rows so unsafe special effects are avoided on bosses where they are known to cause problems.

## Practical Advice

Read enemy behavior from what happens in-game. If an enemy is not taking damage from your usual weapon, try thinking in damage classes:

- another sword technique may be a different class
- Hammer and thrown objects are class 3
- rods, arrows, powder, and medallions are all separate classes
- freezing an enemy may create a class 3 thrown object

In Nightmare especially, it is normal for one enemy to require a very specific class.

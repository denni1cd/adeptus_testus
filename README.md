# Adeptus Testus Facility

Adeptus Testus Facility is a small deterministic Python simulation of Sarah moving through exactly seven rooms:

- Dormitory
- Kitchen
- Workshop
- Infirmary
- Recreation
- Garden
- Control Room

The default normal-day scenario starts at 08:00 in the Dormitory and advances through 12:00 without randomness. Each scheduled activity records the time, origin room, destination room, activity name, explicit reason, and need changes.

## Needs Model

Sarah has four bounded needs: hunger, energy, morale, and health. Each value is clamped from `0` to `100`, where higher is better. The default day applies small documented deltas:

- Breakfast improves hunger and morale.
- Workshop activity lowers hunger and energy slightly while improving morale.
- Infirmary check improves health.
- Recreation improves morale and reduces energy slightly.
- Garden walk improves morale and health while slightly lowering hunger.
- Control Room review lowers hunger and energy slightly.

Sarah is considered to require sleep only when energy is below `25`. At 09:00 in the default scenario her energy remains well above that threshold.

## Preview

Run a preview through noon:

```powershell
python -m adeptus_testus --until 12:00
```

After installing the package, the console script is also available:

```powershell
adeptus-testus --until 12:00
```

The preview prints a headless room map after each step. All seven rooms are listed and Sarah's current room is marked with `[Sarah]`.

## Tests

Install pytest if needed, then run:

```powershell
python -m pytest -q
```

The tests cover the required room set, predictable invalid-room errors, deterministic 08:00 through 12:00 behavior, 09:00 no-sleep behavior, bounded needs, explicit history reasons, renderer output, JSON save/load, CLI preview behavior, and README command documentation.

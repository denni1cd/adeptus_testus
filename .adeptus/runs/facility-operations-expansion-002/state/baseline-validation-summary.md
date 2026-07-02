# Baseline Validation Summary

## Baseline Commands
- `adeptus_python_compile(paths=["src/adeptus_testus", "tests"])`
- `adeptus_pytest(args=["-q"], timeout_seconds=60)`

## Result
- Syntax validation: pass, 5 files checked.
- Pytest validation: pass, `5 passed in 0.02s`.
- Pytest command: `C:\Users\Zero\miniforge3\python.exe -B -m pytest -p no:cacheprovider -q`
- `stdin`: `DEVNULL`
- `timed_out`: `false`
- Cleanup from `adeptus_pytest`: removed 0 artifacts, 0 errors.

## Baseline Preservation Contract
- Existing pytest suite must remain meaningful and passing.
- Existing `python -m adeptus_testus --until 12:00` and `--until 09:00` behavior must remain compatible.
- Existing required rooms, 08:00 start, 09:00 no-sleep behavior, deterministic noon run, renderer, save/load, and invalid room failures must remain covered.

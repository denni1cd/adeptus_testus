# pathaudit

`pathaudit` classifies paths from a UTF-8 text manifest so Adeptus runtime artifacts can be reported separately from product files.

Run a deterministic sample:

```bash
python -m pathaudit --sample
```

Run against a manifest:

```bash
python -m pathaudit path/to/manifest.txt
```

Blank lines and lines beginning with `#` are ignored. Output is one tab-separated classification and path per manifest entry.

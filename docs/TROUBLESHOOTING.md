# ASS-ADE troubleshooting

## Stale editable installs

The merged CLI wrappers force this checkout's bundled engine first for `ass-ade` and `atomadic` commands. Raw Python imports can still be affected by old editable installs or `.pth` files in site-packages.

Read-only checks:

```text
where ass-ade
where atomadic
python -m pip list | findstr /I "ass atomadic"
python -m pip show ass-ade
python -c "import ass_ade; print(ass_ade.__file__)"
python -c "import ass_ade_v11; print(ass_ade_v11.__file__)"
```

Expected product CLI check:

```text
ass-ade doctor
```

The doctor output should report `ass_ade` from:

```text
C:\!aaaa-nexus\!ass-ade\atomadic-engine\src\ass_ade
```

Do not delete sibling folders or uninstall packages as part of a blind cleanup. First capture the paths, then decide which old editable distributions are safe to remove.

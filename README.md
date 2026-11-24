# dep-vet Scoop bucket

Windows manifests for [dep-vet](https://github.com/nassih-yassine/Dep-Vet), a
dependency risk scanner for npm, PyPI, crates.io, Go, JSR, RubyGems, NuGet,
Maven, and Composer.

```powershell
scoop bucket add nassih-yassine https://github.com/nassih-yassine/scoop-bucket
scoop install nassih-yassine/dep-vet
```

`dep-vet --version` confirms the install. The manifest pins the published
Windows zip and its SHA256, and a daily workflow moves it to the newest release.

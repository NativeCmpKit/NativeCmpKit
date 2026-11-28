# NativeCmpKit maintainer instructions

NativeCmpKit is a Kotlin Multiplatform component library derived from Calf.
Use `development/preview-hardening` for migration and verification. Preserve all
imported Git history, tags, authorship, license, and upstream attribution. The
`upstream` remote is read-only. The historical `gh-pages` branch is archival.

## Project identity

- Public Kotlin packages and the Maven group use `io.github.apdelrahman1911.nativecmpkit`.
  Library Gradle projects, directories, and artifact IDs use `nativecmpkit-*`.
  Keep the Android namespaces, opt-ins, native filenames, and JNI exports aligned
  with that identity. Use `NativeCmpKit` for the Swift framework and
  `io.github.apdelrahman1911.nativecmpkit.framework` for its bundle identifier.
- The generated Cupertino resource package is
  `io.github.apdelrahman1911.nativecmpkit.nativecmpkit_cupertino_icons.generated.resources`.
- The Gradle property names are case-sensitive. Use `nativeCmpkit.version`,
  `nativeCmpkit.allowPublishing`, `nativecmpkitVerification`,
  `nativecmpkitVerificationTargets`, and `nativecmpkitNativeMode`.
- Find build projects and sample projects in [settings.gradle.kts](settings.gradle.kts).
  `nativecmpkit-maps` contains a build file. The media and notifications modules
  are outside the current build. Maven staging covers all 23 roots, including
  Geo and Navigation. See the [identity manifest](docs/migration/current-identity.json).
- Supported Kotlin targets are Android, desktop JVM, JS, WasmJS, iOS arm64, and
  iOS Simulator arm64. Desktop and browser camera and permissions have explicit
  unsupported behavior.

## Toolchain and verification

Use the pinned Gradle wrapper, Kotlin and Compose versions in the repository and
an installed JDK 17. For Android, install `platforms;android-37.0`. Linux desktop
tests may need Xvfb, Chrome or an owned GTK, DBus and portal session. Picker and
Share JNI use the pinned Rust toolchain. Apple tests need macOS and Xcode.
Windows JNI needs MSVC.

Run migration builds and platform tests on GitHub Actions. Reserve no more than
two hosted heavy jobs across the project, including queued and reserved jobs.
Coordinate capacity before dispatch. If an owner authorizes heavy local builds
in separate work, follow `/root/VPS_RESOURCE_POLICY.md` and use `vps-build` with
the required 8 GiB disk and 6 GiB available-memory reserves. Preserve other jobs
and shared caches. `cleanup.sh` removes build evidence and caches.

Fast checks from the repository root:

```sh
python3 scripts/migration/verify_migration.py
python3 scripts/development/verify_namespace.py
python3 scripts/audit/validate_audit.py
python3 scripts/audit/source_inventory.py --check
python3 scripts/development/validate_resolutions.py --check
python3 scripts/development/generate_icon_catalogues.py --check
```

Verification workflows use a selected action allowlist, mandatory SHA pinning
and read-only workflow defaults. Keep verification job permissions at
`contents: read`. Use `actions: read` only for tool evidence reuse. Use the
manual workflows and the smallest profile that runs the intended test. Approval
to verify covers staging in a disposable Maven repository. The build gates
remote publication, release, signing, deployment and Pages separately.

Report exact commands, revision, exit status, and counts. For hosted tests also
record run, attempt, job, and artifact. Distinguish source checks, host tests,
native tests, device tests, and independent packaged consumers. A task that is
skipped, up to date or has no source supplies zero executed tests. A framework
link checks linking. An audit defect probe confirms the specified failure when
its assertion passes. Close issues only with the original acceptance evidence.

An Android host test covers JVM behavior. Use an emulator or device for OS
permission, activity lifecycle and content-provider evidence. For iOS, use a
real owned UIKit host where tests depend on presentation or WebKit. Test each
WebView engine in its own runtime. For Linux picker cancellation use a real
owned desktop session and portal. Use a macOS runner to verify AppKit JNI paths.

For isolated publication checks, run `stageVerificationPublications` with
`-PnativecmpkitVerification=true` and the requested
`-PnativecmpkitVerificationTargets=desktop` or `all`. The isolated output is
`build/verification-repo`. Require full artifact and consumer evidence before
reporting publication readiness.

## Evidence and protected files

Keep original receipts, archived upstream snapshots, CI fixtures, and dated
evidence byte-for-byte. Record new results under `docs/development/`. Use the top
of [the development log](docs/development/README.md) and the
[identity migration record](docs/development/nativecmpkit-identity-migration.md)
for checkpoints. Historical instructions remain available in Git.

`scripts/ci/test_javafx_ordinary_success_trace.py` is owner-protected. Exclude it
from reading, stat, searches, copies, edits and staging. Keep credentials,
signing files, local environment configuration and private traces outside Git.

Delegation requires an owner request. Use the owner-requested model and effort,
separate worktrees and disjoint source ownership. The lead owns integration,
pushes, dispatches, evidence acceptance and issue closure.

<!-- Modified for nativeCmpkit migration (2026-10-24). -->
# Installation and source development

## Publication status

The coordinates below describe this development branch. The repository’s published preview
uses a separate set of coordinates documented on `main`:

```kotlin
// Future coordinates only — do not expect these to resolve from Maven Central yet.
implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-ui:0.1.0-SNAPSHOT")
implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-file-picker:0.1.0-SNAPSHOT")
implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-permissions-camera:0.1.0-SNAPSHOT")
implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-navigation:0.1.0-SNAPSHOT")
implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-geo:0.1.0-SNAPSHOT")
```

A future publication requires owner authorization, namespace verification,
license packaging, signing, native artifact completeness and release-gate tests.
See [the roadmap](roadmap/README.md). Historical Calf Maven coordinates and tags
do **not** designate NativeCmpKit builds; their history is [archived](migration/legacy/installation.upstream.md).

## Work with the checked-in source

Clone this independent repository and use its sample projects / Gradle project
dependencies (`projects.nativecmpkitUi`, `projects.nativecmpkitFilePicker`, etc.). This avoids any
runtime or source-fetch dependency on the original repository.

```sh
git clone https://github.com/NativeCmpKit/NativeCmpKit.git
cd NativeCmpKit
./gradlew :nativecmpkit-io:desktopTest :nativecmpkit-file-picker:desktopTest
# These require an appropriate local graphical / Android / browser environment:
./gradlew :sample:desktop:run
./gradlew :sample:android:assembleDebug
./gradlew :sample:web-wasm:wasmJsBrowserDevelopmentRun
```

Required baseline: JDK 17; Kotlin 2.4.20; Compose 1.12.0; Gradle 9.7.1; Android
SDK 37 and AGP 9.4.0; library minSdk 23, sample minSdk 24. Desktop picker/share
builds need Rust on PATH and native host packages. A Debian/Ubuntu development
host needs `pkg-config`, `libgtk-3-dev` and `libwayland-dev`; headless desktop tests
also need Xvfb. The official SDK package is `platforms;android-37.0`, while the
source remains `compileSdk = 37`. Apple builds require macOS/Xcode and the iOS SDK. Do not assume a
sample compile or an isolated JVM probe verifies a native device flow. Exact
attempts, overrides, results and blocked checks are in [testing](testing/README.md).

## Project names and imports

Use `io.github.apdelrahman1911.nativecmpkit.*` imports and `:nativecmpkit-*`
Gradle paths. The [identity manifest](migration/current-identity.json) lists the
projects with Maven publication configuration.

iOS consumers of native UI must export `projects.nativecmpkitUi` from their
shared framework, as the sample does. The sample generates and imports the
`NativeCmpKit` framework.

The historical Calf API remains documented in the migration archive.

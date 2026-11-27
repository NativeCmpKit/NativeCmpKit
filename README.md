# NativeCmpKit

[![Verification](https://github.com/Apdelrahman1911/NativeCmpKit/actions/workflows/gradle.yml/badge.svg?branch=main)](https://github.com/Apdelrahman1911/NativeCmpKit/actions/workflows/gradle.yml)
[![Maven Central](https://img.shields.io/maven-central/v/io.github.apdelrahman1911.nativecmpkit/kira-core)](https://central.sonatype.com/artifact/io.github.apdelrahman1911.nativecmpkit/kira-core)
[![Apache-2.0](https://img.shields.io/github/license/Apdelrahman1911/NativeCmpKit)](LICENSE)

NativeCmpKit provides optional building blocks for Kotlin and Compose Multiplatform
apps. Use its Kira modules to add adaptive controls, pick and share files, request
mobile permissions, or embed web content. Each of the 23 components has its own
Maven coordinate. A file-picker dependency brings in the shared file APIs it needs.

## Supported targets

| Target | Integration requirements | Feature boundaries |
| --- | --- | --- |
| Android | API 23 or later. Android hosts supply a valid context and declare the permissions their features need. | The preview WebView is exercised on API 23 and 35 emulators. Camera and permission flows can depend on device hardware and OS version. |
| iOS | Arm64 devices and Apple Silicon simulators. Build with macOS and Xcode. | UIKit and WKWebView run in the native host. Check availability for system features such as newer privacy permissions. |
| Desktop JVM | Java 17 for the Kotlin desktop artifacts. Native picker/share payloads cover Linux x64 and ARM64, macOS Intel and Apple Silicon, and Windows x64. | WebView also requires JavaFX 21 for the target OS and architecture. Share uses desktop fallback behavior on Windows and Linux. |
| Browser | Compose Multiplatform browser targets for Kotlin/JS and Kotlin/Wasm. | WebView uses an iframe and follows browser origin and framing rules. Folder selection, camera capture and mobile permission requests are unavailable. |

The first preview uses desktop, browser, emulator and simulator verification.
Device-only behavior awaits physical-device checks. Consult the
[feature-by-platform matrix](docs/platforms/README.md) and
[verification guide](docs/testing/README.md) before choosing a component.

## Install

Add `google()` and `mavenCentral()` to the repositories used for dependency
resolution. The first preview, `0.1.0-preview.1`, is on
[Maven Central](https://central.sonatype.com/artifact/io.github.apdelrahman1911.nativecmpkit/kira-core/0.1.0-preview.1).
Use compatible Compose Multiplatform and Kotlin versions. The preview is built
with Compose Multiplatform 1.12.0 and Kotlin 2.4.20.

In an existing Kotlin Multiplatform build:

```kotlin
kotlin {
    sourceSets.commonMain.dependencies {
        implementation("io.github.apdelrahman1911.nativecmpkit:kira-ui:0.1.0-preview.1")
        implementation("io.github.apdelrahman1911.nativecmpkit:kira-file-picker:0.1.0-preview.1")
        implementation("org.jetbrains.compose.material3:material3:1.12.0-alpha03")
    }
}
```

Add only the modules you use. The [installation guide](docs/installation.md)
lists all 23 root artifacts, their direct dependencies and the Kira import
migration. Gradle selects each matching platform artifact automatically.

## Pick a file

This composable launches a document picker from a user action. The result
contains platform-backed `KmpFile` handles. An empty result leaves the selection
unchanged.

```kotlin
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.kira.io.KmpFile
import io.github.apdelrahman1911.kira.picker.FilePickerFileType
import io.github.apdelrahman1911.kira.picker.rememberFilePickerLauncher
import io.github.apdelrahman1911.kira.ui.button.AdaptiveButton

@Composable
fun OpenDocument(onFile: (KmpFile) -> Unit) {
    val picker = rememberFilePickerLauncher(type = FilePickerFileType.Document) { files ->
        files.firstOrNull()?.let(onFile)
    }
    AdaptiveButton(onClick = { picker.launch() }) {
        Text("Open document")
    }
}
```

Use the Kira I/O helpers to read the handle. Close any raw source you open,
handle access or read errors, and import a file into app-owned storage if you
need access after the picker grant expires. See [file and picker integration](docs/modules/io-and-file-picker.md).

## Choose modules

| What you need | Maven artifact ID |
| --- | --- |
| Adaptive controls, platform context, or Cupertino icons | `kira-ui`, `kira-core`, `kira-cupertino-icons` |
| File reads, document picking/export, or Coil file integration | `kira-io`, `kira-file-picker`, `kira-file-picker-coil` |
| Mobile camera capture or system sharing | `kira-camera-picker`, `kira-share` |
| One permission such as camera or microphone | `kira-permissions-camera`, `kira-permissions-microphone`, or another permission leaf |
| Several permissions through the optional permission bundle | `kira-permissions` |
| Experimental adaptive navigation or location | `kira-navigation`, `kira-geo` |
| Embedded web content and navigation | `kira-webview` |

### Embed web content

Add `kira-webview` and use the remembered state as part of your Compose
screen. Keep a separate state for each view and observe loading or page errors
from that state. Web session and cookie semantics depend on the host. Desktop
consumers need the [JavaFX runtime configuration](docs/platforms/desktop.md#javafx-specific-prerequisites).

```kotlin
import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.kira.ui.web.WebView
import io.github.apdelrahman1911.kira.ui.web.rememberWebViewState

@Composable
fun HelpPage(url: String) {
    WebView(state = rememberWebViewState(url))
}
```

## Development and project links

Use the checked-in Gradle wrapper and JDK 17. Android source builds also require
`platforms;android-37.0`. Desktop picker/share source builds use the pinned Rust
toolchain and host libraries. See [development setup](docs/installation.md#build-from-source).

```sh
./gradlew :kira-io:desktopTest :kira-file-picker:desktopTest
```

### Showcase and device coverage

The checked-in sample doubles as the reusable showcase: a searchable component
index, stable routes, semantic tags, a Known Limitations screen and hosted
Android/iOS UI capture. See [showcase/README.md](showcase/README.md) for the
build/session commands, the [coverage manifest](showcase/coverage.json) and
[screenshot index](screenshots/INDEX.md).

- [Releases and release notes](https://github.com/Apdelrahman1911/NativeCmpKit/releases)
- [Maven Central namespace](https://central.sonatype.com/namespace/io.github.apdelrahman1911.nativecmpkit)
- [CI runs](https://github.com/Apdelrahman1911/NativeCmpKit/actions)
- [Repository guidelines](AGENTS.md) and [issue tracker](https://github.com/Apdelrahman1911/NativeCmpKit/issues). Include the module version, OS/architecture and a minimal reproduction with reports.

## License and credits

**Maintainer:** Abdelrahman Fahmy. NativeCmpKit is licensed under
[Apache-2.0](LICENSE). See [NOTICE](NOTICE) and [third-party notices](THIRD_PARTY_NOTICES.md).
Thanks to Mohamed Rejeb and the [original Calf contributors](https://github.com/MohamedRejeb/Calf)
for their foundational code and iOS sample. The project also incorporates
contributions from compose-cupertino, AndroidLiquidGlass, Jodd and the Cupertino
icon font authors. Original copyright notices and Git attribution are preserved.

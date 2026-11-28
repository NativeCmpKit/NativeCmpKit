# NativeCmpKit namespace migration

The owner approved a package and module rename across active code, including the
JVM and native interfaces. This supersedes the package-retention provisions of
ADR 0001 and ADR 0008. The public Kotlin root and Maven group are
`io.github.apdelrahman1911.nativecmpkit`. Gradle project paths and artifact IDs use
`nativecmpkit-*`. The sample Swift framework is `NativeCmpKit`. The native crate
and JNI loader identities use the same branding. See the
[current identity manifest](../migration/current-identity.json).

The original license, attribution, imported history and historical receipts keep
their original identities. The old JVM binary linkage fixture belongs to the
pre-rename baseline. The Android host-test shim in `android.webkit` must remain
in the platform package to invoke its package-private test constructor.

## Upstream PR review

The GitHub API returned five open pull requests at the review snapshot. The
comparison uses the starting development revision `d968257f`.

| PR and reviewed head | Decision |
| --- | --- |
| [#556](https://github.com/MohamedRejeb/Calf/pull/556) `482f517d` | The reported detached-coordinate crash uses three iOS `onPlaced` callbacks. Our dropdown uses a UIKit button, and the two bars use a UIKit host that measures and lays out its own view. The corresponding iOS implementations do not query detached Compose coordinates. No guard or upstream reproduction fixture was copied. |
| [#555](https://github.com/MohamedRejeb/Calf/pull/555) `cd14bf2e` | The equality fix targets the split-view tab controller introduced by #553. Our navigation module has no `IosTabController` or native list-detail tab host. The existing standalone tab-item delegate uses Objective-C pointer identity and checks current membership. |
| [#554](https://github.com/MohamedRejeb/Calf/pull/554) `68dbdfe5` | The default creation extras fix applies to the `NavEntryScope` introduced by #553. Our navigation module has no such entry owner. |
| [#553](https://github.com/MohamedRejeb/Calf/pull/553) `53f502a7` | The PR introduces a different Navigation 3 implementation, foldables, a bar host, a toolchain update, and a redesigned sample. Importing those changes would expand the task. The Material dropdown and minute validation, cross-origin requested-URL tracking, desktop inline HTML, and Android icon resource enablement already have independent implementations here. Our iOS bar layout, sheet/picker behavior, calendar semantics, and popover ownership differ. The upstream diff does not establish the corresponding device behavior on this branch. |
| [#552](https://github.com/MohamedRejeb/Calf/pull/552) `d7f022d8` | The bitmap color/alpha failure has an independent fix and native pixel tests. NativeCmpKit also invalidates images after density and layout-direction changes. Painter images and richer appearance are new APIs. Its positional reuse of equal-count tab items would invalidate our stale-selection test on reorder, so that implementation was not imported. |

The hosted `identity-*` profiles report results for separate desktop, Android
host, browser, package staging, iOS simulator and UIKit application scopes. Historical source-projection and full verification
profiles require separate results. The identity profiles do not issue an
offline-tooling reuse certificate.

The [physical-device checklist](../testing/nativecmpkit-physical-device-verification.md)
covers manual Android, iPhone and iPad release verification.

The API 35 remote IO cancellation fixture opens the granted tree URI through
`ContentProviderClient.openFile`. Android 15 routes a read-only
`ContentResolver.openFileDescriptor` call through a wildcard typed-open path
that discards the cancellation signal in `DocumentsProvider`. The client passes
the signal directly to the provider's open operation. The fixture still requires
the actual resulting `OperationCanceledException`, no transferred descriptor,
and independent provider, socket and worker cleanup. The separate positive
case exercises the public `KmpFile` stream through `ContentResolver`. See the
[Android 15 resolver](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/android/content/ContentResolver.java#1741),
[DocumentsProvider](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/android/provider/DocumentsProvider.java#1366)
and [ContentProviderClient](https://android.googlesource.com/platform/frameworks/base/+/refs/tags/android-15.0.0_r1/core/java/android/content/ContentProviderClient.java#407).

// Test-only NativeCmpKit picker application host (2026-10-29).
// Reuses nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt; unchanged ownership/Worker/cleanup contract.
@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)

package io.github.apdelrahman1911.nativecmpkit.picker.internal

import kotlinx.cinterop.objcPtr
import platform.darwin.NSObject

/**
 * Exact identity of retained native objects, not Kotlin wrapper identity or
 * NSObject value equality. Two nil objects never establish an ownership lease.
 * Keep both references alive and compare only during the owning native call;
 * native addresses are neither cached nor exported as persistent identities.
 */
internal fun sameNativeObject(first: NSObject?, second: NSObject?): Boolean =
    first != null && second != null && first.objcPtr() == second.objcPtr()

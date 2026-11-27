// NativeCmpKit (2026-11-04): test admission uses the real device OS, never a forced renderer.
@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)

package io.github.apdelrahman1911.nativecmpkit.ui.controls

import androidx.compose.ui.test.ComposeUiTest
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.v2.runComposeUiTest
import io.github.apdelrahman1911.nativecmpkit.ui.internal.onApplicationMain
import io.github.apdelrahman1911.nativecmpkit.ui.internal.requireOwnedApplicationWindow
import platform.UIKit.UIDevice
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

internal enum class AdaptiveControlBranch(val label: String) {
    Pre26("pre26"), IOS26Plus("ios26plus"),
}

/** The wrong runtime is an assertion failure, not ignored/assumed old-OS coverage. */
internal fun requireAdaptiveControlHost(branch: AdaptiveControlBranch) {
    val version = onApplicationMain {
        requireOwnedApplicationWindow()
        UIDevice.currentDevice.systemVersion
    }
    val major = assertNotNull(version.split('.').firstOrNull()?.toIntOrNull(),
        "An actual, valid iOS systemVersion is required")
    assertTrue(major > 0, "An actual positive iOS major version is required")
    assertTrue(if (branch == AdaptiveControlBranch.Pre26) major < 26 else major >= 26,
        "${branch.label} must execute on its actual iOS runtime; observed major=$major")
    println("NATIVECMPKIT_ADAPTIVE_CONTROL_HOST branch=${branch.label} major=$major")
}

/** Let the scene close before reporting a caller assertion to the native test runner. */
@OptIn(ExperimentalTestApi::class)
internal fun runAdaptiveControlUiTest(block: suspend ComposeUiTest.() -> Unit) {
    var assertion: AssertionError? = null
    runComposeUiTest {
        try {
            block()
        } catch (failure: AssertionError) {
            assertion = failure
        }
    }
    assertion?.let { throw it }
}

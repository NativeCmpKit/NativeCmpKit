package io.github.apdelrahman1911.nativecmpkit.ui.utils

import platform.UIKit.UIDevice

/** True when the device runs iOS [major].[minor] or newer. */
internal fun isIOSVersionAtLeast(major: Int, minor: Int = 0): Boolean =
    isVersionAtLeast(UIDevice.currentDevice.systemVersion, major, minor)

/** Compares the major and minor components of a dotted version string. */
internal fun isVersionAtLeast(version: String, major: Int, minor: Int = 0): Boolean {
    val components = version.split('.')
    val currentMajor = components.firstOrNull()?.toIntOrNull() ?: 0
    val currentMinor = components.getOrNull(1)?.toIntOrNull() ?: 0
    return currentMajor > major || (currentMajor == major && currentMinor >= minor)
}

internal fun isIOS26OrAbove(): Boolean = isIOSVersionAtLeast(26)

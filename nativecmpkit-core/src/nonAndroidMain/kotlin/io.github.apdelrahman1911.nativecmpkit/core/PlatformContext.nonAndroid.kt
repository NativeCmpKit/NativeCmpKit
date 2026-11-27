package io.github.apdelrahman1911.nativecmpkit.core

import kotlin.jvm.JvmField

actual abstract class PlatformContext private constructor() {
    companion object {
        @JvmField
        val INSTANCE = object : PlatformContext() {}
    }
}

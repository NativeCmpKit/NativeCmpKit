package io.github.apdelrahman1911.nativecmpkit.core

import androidx.compose.runtime.staticCompositionLocalOf

actual val LocalPlatformContext =
    staticCompositionLocalOf {
        PlatformContext.INSTANCE
    }

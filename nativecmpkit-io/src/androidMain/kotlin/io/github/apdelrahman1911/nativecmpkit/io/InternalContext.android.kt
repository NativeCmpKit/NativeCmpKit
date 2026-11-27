package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext

internal actual fun resolveContext(): PlatformContext = AndroidContextHolder.context

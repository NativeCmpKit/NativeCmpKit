package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext

/**
 * Resolves the platform context internally.
 * On Android, returns the context from [AndroidContextHolder].
 * On all other platforms, returns [PlatformContext.INSTANCE].
 */
internal expect fun resolveContext(): PlatformContext

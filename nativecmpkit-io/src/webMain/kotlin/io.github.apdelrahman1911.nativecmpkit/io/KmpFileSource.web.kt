package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext
import kotlinx.io.Buffer
import kotlinx.io.RawSource

actual suspend fun KmpFile.source(context: PlatformContext): RawSource =
    Buffer().apply { write(readFileAsBytes(file)) }

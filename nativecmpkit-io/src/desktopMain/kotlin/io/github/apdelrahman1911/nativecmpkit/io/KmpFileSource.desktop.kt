package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext
import kotlinx.io.RawSource
import kotlinx.io.files.Path
import kotlinx.io.files.SystemFileSystem

actual suspend fun KmpFile.source(context: PlatformContext): RawSource =
    SystemFileSystem.source(Path(file.absolutePath))

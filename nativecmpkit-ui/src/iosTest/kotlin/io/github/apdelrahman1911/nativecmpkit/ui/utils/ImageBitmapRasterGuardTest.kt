@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)

package io.github.apdelrahman1911.nativecmpkit.ui.utils

import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.ImageBitmapConfig
import androidx.compose.ui.graphics.colorspace.ColorSpaces
import platform.CoreGraphics.CGColorSpaceRef
import kotlin.test.Test
import kotlin.test.assertNull

class ImageBitmapRasterGuardTest {
    @Test
    fun emptyOrOverflowedDimensionsStopBeforeReadingPixelsOrAllocating() {
        val bridge = object : BitmapImageBridge() {
            override fun createColorSpace(): CGColorSpaceRef? = error("Invalid bitmap must not allocate native pixels")
        }
        val invalidSizes = listOf(0 to 1, 1 to 0, -1 to 1, Int.MAX_VALUE to 2, 65536 to 8192)
        for ((width, height) in invalidSizes) {
            assertNull(DimensionOnlyBitmap(width, height).toUIImage(1.0, bridge), "size=${width}x$height")
        }
    }

    private class DimensionOnlyBitmap(override val width: Int, override val height: Int) : ImageBitmap {
        override val colorSpace = ColorSpaces.Srgb
        override val hasAlpha = true
        override val config = ImageBitmapConfig.Argb8888

        override fun readPixels(
            buffer: IntArray,
            startX: Int,
            startY: Int,
            width: Int,
            height: Int,
            bufferOffset: Int,
            stride: Int,
        ): Unit = error("Invalid bitmap must not read pixels")

        override fun prepareToDraw() = Unit
    }
}

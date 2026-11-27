package io.github.apdelrahman1911.nativecmpkit.picker

import io.github.apdelrahman1911.nativecmpkit.io.KmpFile
import platform.Foundation.NSURL
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

/**
 * On iOS a folder given as a [KmpFile] is carried as its URL, and a plain path, as Desktop code
 * would pass, still resolves to the same folder.
 */
class InitialDirectoryTest {
    @Test
    fun aFolderRoundTripsToTheSameDirectoryUrl() {
        val folder = NSURL.fileURLWithPath("/private/var/mobile/NativeCmpKit Exports", isDirectory = true)

        val settings = FilePickerSettings(initialDirectory = KmpFile(folder))

        assertEquals("/private/var/mobile/NativeCmpKit Exports", initialDirectoryUrl(settings.initialDirectory)?.path)
    }

    @Test
    fun aPlainPathResolvesToAFileUrl() {
        val url = initialDirectoryUrl("/private/var/mobile/NativeCmpKit Exports")

        assertEquals(true, url?.isFileURL())
        assertEquals("/private/var/mobile/NativeCmpKit Exports", url?.path)
    }

    @Test
    fun noInitialDirectoryGivesNoUrl() {
        assertNull(initialDirectoryUrl(null))
        assertNull(initialDirectoryUrl(""))
    }
}

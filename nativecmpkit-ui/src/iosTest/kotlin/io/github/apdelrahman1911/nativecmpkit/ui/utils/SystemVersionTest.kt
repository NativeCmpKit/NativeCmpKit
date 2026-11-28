package io.github.apdelrahman1911.nativecmpkit.ui.utils

import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class SystemVersionTest {
    @Test
    fun laterMajorReleasesSatisfyAMinorRequirement() {
        // performPrimaryAction() needs 17.4; 18.0 and 26.0 must qualify even though their minor is 0.
        assertTrue(isVersionAtLeast("18.0", 17, 4))
        assertTrue(isVersionAtLeast("26.0.1", 17, 4))
        assertTrue(isVersionAtLeast("17.4", 17, 4))
        assertTrue(isVersionAtLeast("17.10", 17, 4))
    }

    @Test
    fun earlierReleasesDoNot() {
        assertFalse(isVersionAtLeast("17.3.1", 17, 4))
        assertFalse(isVersionAtLeast("16.7", 17, 4))
        assertFalse(isVersionAtLeast("", 17, 4))
    }

    @Test
    fun majorOnlyChecksIgnoreTheMinor() {
        assertTrue(isVersionAtLeast("26.0", 26))
        assertFalse(isVersionAtLeast("25.9", 26))
    }
}

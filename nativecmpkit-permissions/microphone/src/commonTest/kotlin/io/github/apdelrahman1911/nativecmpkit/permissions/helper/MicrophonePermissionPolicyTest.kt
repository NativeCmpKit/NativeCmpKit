@file:OptIn(io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi::class)

package io.github.apdelrahman1911.nativecmpkit.permissions.helper

import io.github.apdelrahman1911.nativecmpkit.permissions.*

import kotlin.test.*

class MicrophonePermissionPolicyTest {
    @Test fun onlyAuthorizedGrantsAccess() {
        MicrophoneAuthorization.entries.forEach {
            assertEquals(it == MicrophoneAuthorization.Authorized, microphoneSnapshot(it).status.isGranted)
        }
    }
    @Test fun restrictedAndNotDeterminedAreNotConflated() {
        val unknown = microphoneSnapshot(MicrophoneAuthorization.NotDetermined)
        assertFalse(unknown.status.shouldShowRationale)
        assertEquals(PermissionRequestability.Requestable, unknown.details.requestability)
        assertEquals(PermissionRequestability.Restricted, microphoneSnapshot(MicrophoneAuthorization.Restricted).details.requestability)
    }
}

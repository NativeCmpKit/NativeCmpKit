@file:OptIn(io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi::class)

package io.github.apdelrahman1911.nativecmpkit.permissions.helper

import io.github.apdelrahman1911.nativecmpkit.permissions.*

import kotlin.test.*

class CameraPermissionPolicyTest {
    @Test fun onlyAuthorizedGrantsAccess() {
        CameraAuthorization.entries.forEach {
            assertEquals(it == CameraAuthorization.Authorized, cameraSnapshot(it).status.isGranted)
        }
    }
    @Test fun restrictedAndNotDeterminedAreNotConflated() {
        val unknown = cameraSnapshot(CameraAuthorization.NotDetermined)
        assertFalse(unknown.status.shouldShowRationale)
        assertEquals(PermissionRequestability.Requestable, unknown.details.requestability)
        assertEquals(PermissionRequestability.Restricted, cameraSnapshot(CameraAuthorization.Restricted).details.requestability)
    }
}

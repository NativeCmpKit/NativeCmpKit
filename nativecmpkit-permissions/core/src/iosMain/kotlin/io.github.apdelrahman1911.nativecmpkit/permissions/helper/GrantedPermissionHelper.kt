// Modified for nativeCmpkit (2026-10-24): permission safety, capability and request-lifecycle fixes.
@file:OptIn(io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi::class)

package io.github.apdelrahman1911.nativecmpkit.permissions.helper

import io.github.apdelrahman1911.nativecmpkit.permissions.*

class GrantedPermissionHelper : PermissionSnapshotHelper {
    override fun getPermissionStatus(onPermissionResult: (PermissionStatus) -> Unit) =
        getPermissionSnapshot { onPermissionResult(it.status) }
    override fun launchPermissionRequest(onPermissionResult: (Boolean) -> Unit) = onPermissionResult(true)
    override fun getPermissionSnapshot(onResult: (PermissionSnapshot) -> Unit) = onResult(PermissionSnapshot(
        PermissionStatus.Granted,
        PermissionDetails(availability = PermissionAvailability.NotRequired,
            access = PermissionAccess.Unknown, requestability = PermissionRequestability.NotRequired),
    ))
}

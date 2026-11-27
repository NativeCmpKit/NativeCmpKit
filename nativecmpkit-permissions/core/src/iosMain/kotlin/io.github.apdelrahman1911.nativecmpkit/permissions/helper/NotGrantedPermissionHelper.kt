// Modified for nativeCmpkit (2026-10-24): permission safety, capability and request-lifecycle fixes.
@file:OptIn(io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi::class)

package io.github.apdelrahman1911.nativecmpkit.permissions.helper

import io.github.apdelrahman1911.nativecmpkit.permissions.*

class NotGrantedPermissionHelper : PermissionSnapshotHelper {
    override fun getPermissionStatus(onPermissionResult: (PermissionStatus) -> Unit) =
        getPermissionSnapshot { onPermissionResult(it.status) }
    override fun launchPermissionRequest(onPermissionResult: (Boolean) -> Unit) = onPermissionResult(false)
    override fun getPermissionSnapshot(onResult: (PermissionSnapshot) -> Unit) = onResult(PermissionSnapshot(
        PermissionStatus.Denied(false),
        PermissionDetails(availability = PermissionAvailability.Unsupported,
            access = PermissionAccess.None, requestability = PermissionRequestability.Unsupported),
    ))
}

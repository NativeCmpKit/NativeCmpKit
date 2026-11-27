// Modified for nativeCmpkit (2026-10-24): permission safety, capability and request-lifecycle fixes.
package io.github.apdelrahman1911.nativecmpkit.permissions

import androidx.compose.runtime.Composable

@ExperimentalPermissionsApi
@Composable
internal actual fun rememberMutablePermissionState(
    permission: Permission,
    onPermissionResult: (Boolean) -> Unit,
): MutablePermissionState = rememberUnsupportedPermissionState(permission, onPermissionResult)

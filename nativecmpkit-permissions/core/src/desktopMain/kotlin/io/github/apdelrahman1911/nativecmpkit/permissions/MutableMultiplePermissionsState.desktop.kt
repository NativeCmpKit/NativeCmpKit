// Modified for nativeCmpkit (2026-10-24): permission safety, capability and request-lifecycle fixes.
package io.github.apdelrahman1911.nativecmpkit.permissions

import androidx.compose.runtime.Composable

@ExperimentalPermissionsApi
@Composable
internal actual fun rememberMutableMultiplePermissionsState(
    permissions: List<Permission>,
    onPermissionsResult: (Map<Permission, Boolean>) -> Unit,
): MultiplePermissionsState = rememberUnsupportedMultiplePermissionsState(permissions, onPermissionsResult)

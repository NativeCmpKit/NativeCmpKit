package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.BackgroundLocationPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerBackgroundLocationPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        BackgroundLocationPermissionHelper()
    }
}

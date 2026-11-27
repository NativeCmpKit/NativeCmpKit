package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.LocalNotificationPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.RemoteNotificationPermissionHelper

internal actual fun registerNotificationPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        LocalNotificationPermissionHelper()
    }
}

internal actual fun registerRemoteNotificationPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        RemoteNotificationPermissionHelper()
    }
}

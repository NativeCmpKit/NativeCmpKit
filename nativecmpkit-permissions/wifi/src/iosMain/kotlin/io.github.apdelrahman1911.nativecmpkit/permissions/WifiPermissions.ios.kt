package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.WifiPermissionHelper

internal actual fun registerWifiAccessStatePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        WifiPermissionHelper()
    }
}

internal actual fun registerWifiChangeStatePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        WifiPermissionHelper()
    }
}

internal actual fun registerWifiNearbyDevicesPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        WifiPermissionHelper()
    }
}

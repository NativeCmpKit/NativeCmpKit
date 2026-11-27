package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.BluetoothPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerBluetoothLePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        BluetoothPermissionHelper()
    }
}

internal actual fun registerBluetoothScanPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        BluetoothPermissionHelper()
    }
}

internal actual fun registerBluetoothConnectPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        BluetoothPermissionHelper()
    }
}

internal actual fun registerBluetoothAdvertisePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        BluetoothPermissionHelper()
    }
}

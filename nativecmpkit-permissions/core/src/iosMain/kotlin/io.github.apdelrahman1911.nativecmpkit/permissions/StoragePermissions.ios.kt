package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.GrantedPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerReadStoragePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GrantedPermissionHelper()
    }
}

internal actual fun registerWriteStoragePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GrantedPermissionHelper()
    }
}

internal actual fun registerReadAudioPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GrantedPermissionHelper()
    }
}

internal actual fun registerCallPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GrantedPermissionHelper()
    }
}

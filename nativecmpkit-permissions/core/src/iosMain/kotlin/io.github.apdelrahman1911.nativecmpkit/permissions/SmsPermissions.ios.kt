package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.GrantedPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.NotGrantedPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerReadSmsPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        NotGrantedPermissionHelper()
    }
}

internal actual fun registerReceiveSmsPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        NotGrantedPermissionHelper()
    }
}

internal actual fun registerSendSmsPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GrantedPermissionHelper()
    }
}

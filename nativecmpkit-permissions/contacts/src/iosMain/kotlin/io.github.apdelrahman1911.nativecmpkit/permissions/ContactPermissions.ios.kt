package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.ContactPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerReadContactsPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        ContactPermissionHelper()
    }
}

internal actual fun registerWriteContactsPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        ContactPermissionHelper()
    }
}

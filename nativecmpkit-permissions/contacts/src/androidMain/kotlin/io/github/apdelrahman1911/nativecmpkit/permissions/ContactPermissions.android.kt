package io.github.apdelrahman1911.nativecmpkit.permissions

import android.Manifest

internal actual fun registerReadContactsPermission(permission: Permission) {
    AndroidPermissionRegistry.register(
        permission,
        AndroidPermissionMapping(
            permissionString = Manifest.permission.READ_CONTACTS,
        ),
    )
}

internal actual fun registerWriteContactsPermission(permission: Permission) {
    AndroidPermissionRegistry.register(
        permission,
        AndroidPermissionMapping(
            permissionString = Manifest.permission.WRITE_CONTACTS,
        ),
    )
}

package io.github.apdelrahman1911.nativecmpkit.permissions

import android.Manifest

internal actual fun registerReadCalendarPermission(permission: Permission) {
    AndroidPermissionRegistry.register(
        permission,
        AndroidPermissionMapping(
            permissionString = Manifest.permission.READ_CALENDAR,
        ),
    )
}

internal actual fun registerWriteCalendarPermission(permission: Permission) {
    AndroidPermissionRegistry.register(
        permission,
        AndroidPermissionMapping(
            permissionString = Manifest.permission.WRITE_CALENDAR,
        ),
    )
}

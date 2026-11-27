package io.github.apdelrahman1911.nativecmpkit.permissions

import android.Manifest

internal actual fun registerRecordAudioPermission(permission: Permission) {
    AndroidPermissionRegistry.register(
        permission,
        AndroidPermissionMapping(
            permissionString = Manifest.permission.RECORD_AUDIO,
        ),
    )
}

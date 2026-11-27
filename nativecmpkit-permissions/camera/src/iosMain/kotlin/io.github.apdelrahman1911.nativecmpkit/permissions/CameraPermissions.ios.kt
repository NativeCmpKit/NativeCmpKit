package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.AVCameraPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry
import platform.AVFoundation.AVMediaTypeVideo

internal actual fun registerCameraPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        AVCameraPermissionHelper(AVMediaTypeVideo)
    }
}

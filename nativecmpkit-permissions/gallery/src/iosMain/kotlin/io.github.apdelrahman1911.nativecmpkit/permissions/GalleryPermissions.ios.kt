package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.GalleryPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerGalleryPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GalleryPermissionHelper()
    }
}

internal actual fun registerReadImagePermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GalleryPermissionHelper()
    }
}

internal actual fun registerReadVideoPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        GalleryPermissionHelper()
    }
}

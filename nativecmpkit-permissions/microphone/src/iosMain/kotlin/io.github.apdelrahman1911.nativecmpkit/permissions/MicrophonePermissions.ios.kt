package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.AVMicrophonePermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry
import platform.AVFoundation.AVMediaTypeAudio

internal actual fun registerRecordAudioPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        AVMicrophonePermissionHelper(AVMediaTypeAudio)
    }
}

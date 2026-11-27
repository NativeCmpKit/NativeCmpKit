package io.github.apdelrahman1911.nativecmpkit.permissions

val Permission.Companion.BackgroundLocation: Permission
    get() = PermissionBackgroundLocation

internal expect fun registerBackgroundLocationPermission(permission: Permission)

internal object PermissionBackgroundLocation : Permission("BackgroundLocation") {
    init {
        registerBackgroundLocationPermission(this)
    }
}

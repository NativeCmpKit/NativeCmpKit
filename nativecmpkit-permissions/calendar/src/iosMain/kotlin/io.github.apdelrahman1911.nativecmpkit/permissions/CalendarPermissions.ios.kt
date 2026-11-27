// Modified for nativeCmpkit (2026-10-24): permission safety, capability and request-lifecycle fixes.
package io.github.apdelrahman1911.nativecmpkit.permissions

import io.github.apdelrahman1911.nativecmpkit.permissions.helper.CalendarPermissionHelper
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.CalendarAccessMode
import io.github.apdelrahman1911.nativecmpkit.permissions.helper.PermissionDelegateRegistry

internal actual fun registerReadCalendarPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        CalendarPermissionHelper(CalendarAccessMode.Read)
    }
}

internal actual fun registerWriteCalendarPermission(permission: Permission) {
    PermissionDelegateRegistry.register(permission) {
        CalendarPermissionHelper(CalendarAccessMode.Write)
    }
}

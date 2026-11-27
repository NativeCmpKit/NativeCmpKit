@file:OptIn(io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi::class)

package io.github.apdelrahman1911.nativecmpkit.permissions.helper

import io.github.apdelrahman1911.nativecmpkit.permissions.*

internal fun localNetworkSnapshot(outcome: PermissionRequestOutcome? = null): PermissionSnapshot {
    val published = outcome == PermissionRequestOutcome.Granted
    return PermissionSnapshot(if (published) PermissionStatus.Granted else PermissionStatus.Denied(false),
        PermissionDetails(PermissionAvailability.Available,
            if (published) PermissionAccess.Full else PermissionAccess.Unknown,
            PermissionRequestability.Requestable, lastRequest = outcome, capability = "local-network-probe"))
}

internal fun localNetworkConfigurationValid(usageDescription: Any?, bonjourServices: Any?): Boolean =
    usageDescription is String && usageDescription.isNotBlank() &&
        bonjourServices is List<*> && "_lnp._tcp." in bonjourServices

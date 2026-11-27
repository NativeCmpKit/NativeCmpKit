// Modified for nativeCmpkit (2026-10-24): correctness, lifecycle, testing and build hardening.
package io.github.apdelrahman1911.nativecmpkit.sample.screens

import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import io.github.apdelrahman1911.nativecmpkit.ui.button.AdaptiveButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.nativecmpkit.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.nativecmpkit.permissions.BackgroundLocation
import io.github.apdelrahman1911.nativecmpkit.permissions.BluetoothAdvertise
import io.github.apdelrahman1911.nativecmpkit.permissions.BluetoothConnect
import io.github.apdelrahman1911.nativecmpkit.permissions.BluetoothLe
import io.github.apdelrahman1911.nativecmpkit.permissions.BluetoothScan
import io.github.apdelrahman1911.nativecmpkit.permissions.Camera
import io.github.apdelrahman1911.nativecmpkit.permissions.CoarseLocation
import io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi
import io.github.apdelrahman1911.nativecmpkit.permissions.FineLocation
import io.github.apdelrahman1911.nativecmpkit.permissions.Gallery
import io.github.apdelrahman1911.nativecmpkit.permissions.Notification
import io.github.apdelrahman1911.nativecmpkit.permissions.Permission
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadAudio
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadCalendar
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadContacts
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadImage
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadStorage
import io.github.apdelrahman1911.nativecmpkit.permissions.ReadVideo
import io.github.apdelrahman1911.nativecmpkit.permissions.RecordAudio
import io.github.apdelrahman1911.nativecmpkit.permissions.RemoteNotification
import io.github.apdelrahman1911.nativecmpkit.permissions.WifiAccessState
import io.github.apdelrahman1911.nativecmpkit.permissions.WifiChangeState
import io.github.apdelrahman1911.nativecmpkit.permissions.WifiNearbyDevices
import io.github.apdelrahman1911.nativecmpkit.permissions.WriteCalendar
import io.github.apdelrahman1911.nativecmpkit.permissions.WriteContacts
import io.github.apdelrahman1911.nativecmpkit.permissions.WriteStorage
import io.github.apdelrahman1911.nativecmpkit.permissions.isGranted
import io.github.apdelrahman1911.nativecmpkit.permissions.rememberMultiplePermissionsState
import io.github.apdelrahman1911.nativecmpkit.permissions.rememberPermissionState
import io.github.apdelrahman1911.nativecmpkit.permissions.shouldShowRationale

@Composable
fun PermissionScreen(navigateBack: () -> Unit) {
    val permissions = remember {
        listOf(
            Permission.Camera,
            Permission.Gallery,
            Permission.ReadStorage,
            Permission.WriteStorage,
            Permission.ReadImage,
            Permission.ReadVideo,
            Permission.ReadAudio,
            Permission.FineLocation,
            Permission.CoarseLocation,
            Permission.BackgroundLocation,
            Permission.Notification,
            Permission.RemoteNotification,
            Permission.RecordAudio,
            Permission.BluetoothLe,
            Permission.BluetoothScan,
            Permission.BluetoothConnect,
            Permission.BluetoothAdvertise,
            Permission.ReadContacts,
            Permission.WriteContacts,
            Permission.ReadCalendar,
            Permission.WriteCalendar,
            Permission.WifiAccessState,
            Permission.WifiChangeState,
            Permission.WifiNearbyDevices,
        )
    }

    SampleScreenScaffold(
        title = "Permissions",
        navigateBack = navigateBack,
    ) { padding ->
        LazyColumn(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
        ) {
            item {
                Text(
                    text = "Permission API demonstrations. Availability and prerequisites vary by platform; a successful no-op is not native permission support.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(vertical = 8.dp),
                )
            }

            item {
                MultiplePermissionsItem(
                    permissions = listOf(Permission.Camera, Permission.RecordAudio),
                )
            }

            items(permissions) { permission ->
                PermissionItem(permission = permission)
            }
        }
    }
}

@OptIn(ExperimentalPermissionsApi::class)
@Composable
private fun MultiplePermissionsItem(permissions: List<Permission>) {
    val multiplePermissionsState = rememberMultiplePermissionsState(permissions = permissions)

    Spacer(modifier = Modifier.height(16.dp))

    Text(
        text = "Multiple: ${permissions.joinToString { it.name }}",
    )

    Text(
        text = "All permissions granted: ${multiplePermissionsState.allPermissionsGranted}",
    )

    Text(
        text = "Should show rationale: ${multiplePermissionsState.shouldShowRationale}",
    )

    Text(
        text = "Revoked permissions: ${multiplePermissionsState.revokedPermissions.joinToString { it.permission.name }}",
    )

    AdaptiveButton(
        onClick = {
            multiplePermissionsState.launchMultiplePermissionRequest()
        },
    ) {
        Text(
            text = "Request permissions",
        )
    }

    Spacer(modifier = Modifier.height(16.dp))

    HorizontalDivider()
}

@OptIn(ExperimentalPermissionsApi::class)
@Composable
private fun PermissionItem(permission: Permission) {
    val permissionState = rememberPermissionState(permission = permission)

    Spacer(modifier = Modifier.height(16.dp))

    Text(
        text = permission.name,
    )

    Text(
        text = "Is permission granted: ${permissionState.status.isGranted}",
    )

    LaunchedEffect(permissionState.status) {
        println("${permission.name}: ${permissionState.status}")
        if (!permissionState.status.isGranted && permissionState.status.shouldShowRationale) {
            println("${permission.name}: Show Rationale")
        }
    }

    AdaptiveButton(
        onClick = {
            permissionState.launchPermissionRequest()
        },
    ) {
        Text(
            text = "Request permission",
        )
    }



    Spacer(modifier = Modifier.height(16.dp))

    if (permission.name == Permission.Notification.name) {
        AdaptiveButton(
            onClick = {
                permissionState.openAppSettings()
            },
        ) {
            Text(
                text = "Open Notification Settings",
            )
        }

        Spacer(modifier = Modifier.height(16.dp))
    }


    HorizontalDivider()
}

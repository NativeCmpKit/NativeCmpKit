package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import io.github.apdelrahman1911.kira.ui.button.AdaptiveButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.kira.permissions.BackgroundLocation
import io.github.apdelrahman1911.kira.permissions.BluetoothAdvertise
import io.github.apdelrahman1911.kira.permissions.BluetoothConnect
import io.github.apdelrahman1911.kira.permissions.BluetoothLe
import io.github.apdelrahman1911.kira.permissions.BluetoothScan
import io.github.apdelrahman1911.kira.permissions.Call
import io.github.apdelrahman1911.kira.permissions.Camera
import io.github.apdelrahman1911.kira.permissions.CoarseLocation
import io.github.apdelrahman1911.kira.permissions.ExperimentalPermissionsApi
import io.github.apdelrahman1911.kira.permissions.FineLocation
import io.github.apdelrahman1911.kira.permissions.Gallery
import io.github.apdelrahman1911.kira.permissions.Notification
import io.github.apdelrahman1911.kira.permissions.Permission
import io.github.apdelrahman1911.kira.permissions.ReadAudio
import io.github.apdelrahman1911.kira.permissions.ReadCalendar
import io.github.apdelrahman1911.kira.permissions.ReadContacts
import io.github.apdelrahman1911.kira.permissions.ReadImage
import io.github.apdelrahman1911.kira.permissions.ReadStorage
import io.github.apdelrahman1911.kira.permissions.ReadVideo
import io.github.apdelrahman1911.kira.permissions.RecordAudio
import io.github.apdelrahman1911.kira.permissions.RemoteNotification
import io.github.apdelrahman1911.kira.permissions.WifiAccessState
import io.github.apdelrahman1911.kira.permissions.WifiChangeState
import io.github.apdelrahman1911.kira.permissions.WifiNearbyDevices
import io.github.apdelrahman1911.kira.permissions.WriteCalendar
import io.github.apdelrahman1911.kira.permissions.WriteContacts
import io.github.apdelrahman1911.kira.permissions.WriteStorage
import io.github.apdelrahman1911.kira.permissions.isGranted
import io.github.apdelrahman1911.kira.permissions.rememberMultiplePermissionsState
import io.github.apdelrahman1911.kira.permissions.rememberPermissionState
import io.github.apdelrahman1911.kira.permissions.shouldShowRationale

@Composable
fun PermissionScreen(navigateBack: () -> Unit) {
    val permissions = remember {
        listOf(
            Permission.Call,
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
                    text = "Runtime permission handling across platforms.",
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

    Text(
        text = "Status: ${permissionState.status}",
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

    AdaptiveButton(
        onClick = {
            permissionState.openAppSettings()
        },
    ) {
        Text(
            text = "Open app settings",
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

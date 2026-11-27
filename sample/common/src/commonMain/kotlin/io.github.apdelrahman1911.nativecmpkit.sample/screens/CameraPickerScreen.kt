package io.github.apdelrahman1911.nativecmpkit.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import io.github.apdelrahman1911.nativecmpkit.ui.button.AdaptiveButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.nativecmpkit.camerapicker.rememberCameraPickerLauncher
import io.github.apdelrahman1911.nativecmpkit.core.LocalPlatformContext
import io.github.apdelrahman1911.nativecmpkit.io.getName
import io.github.apdelrahman1911.nativecmpkit.io.getPath
import io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi
import io.github.apdelrahman1911.nativecmpkit.permissions.Camera
import io.github.apdelrahman1911.nativecmpkit.permissions.Permission
import io.github.apdelrahman1911.nativecmpkit.permissions.isGranted
import io.github.apdelrahman1911.nativecmpkit.permissions.rememberPermissionState
import io.github.apdelrahman1911.nativecmpkit.sample.components.SampleScreenScaffold

@OptIn(ExperimentalPermissionsApi::class)
@Composable
fun CameraPickerScreen(
    navigateBack: () -> Unit,
) {
    val context = LocalPlatformContext.current

    var fileName by remember { mutableStateOf("") }
    var path by remember { mutableStateOf("") }

    val cameraPickerLauncher = rememberCameraPickerLauncher(
        onResult = { file ->
            fileName = file.getName(context).orEmpty()
            path = file.getPath(context).orEmpty()
        },
    )

    val cameraPermissionState = rememberPermissionState(
        permission = Permission.Camera,
        onPermissionResult = { isGranted ->
            if (isGranted)
                cameraPickerLauncher.launch()
        }
    )

    SampleScreenScaffold(
        title = "Camera Picker",
        navigateBack = navigateBack,
    ) { padding ->
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            Text(
                text = "Camera capture using native platform camera APIs. Requires camera permission.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(24.dp))

            AdaptiveButton(
                onClick = {
                    if (cameraPermissionState.status.isGranted) {
                        cameraPickerLauncher.launch()
                    } else {
                        cameraPermissionState.launchPermissionRequest()
                    }
                }
            ) {
                Text("Open Camera")
            }

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "Captured file:",
                style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSurface,
            )

            Spacer(modifier = Modifier.height(8.dp))

            if (fileName.isEmpty()) {
                Text(
                    text = "No photo captured",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            } else {
                Text(
                    text = "Name: $fileName",
                    style = MaterialTheme.typography.bodyMedium,
                    modifier = Modifier.fillMaxWidth(),
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Path: $path",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}

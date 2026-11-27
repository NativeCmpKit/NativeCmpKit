package io.github.apdelrahman1911.nativecmpkit.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import io.github.apdelrahman1911.nativecmpkit.ui.button.AdaptiveButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.nativecmpkit.permissions.ExperimentalPermissionsApi
import io.github.apdelrahman1911.nativecmpkit.permissions.Camera
import io.github.apdelrahman1911.nativecmpkit.permissions.Permission
import io.github.apdelrahman1911.nativecmpkit.permissions.isGranted
import io.github.apdelrahman1911.nativecmpkit.permissions.rememberPermissionState
import io.github.apdelrahman1911.nativecmpkit.sample.components.SampleScreenScaffold

@OptIn(ExperimentalPermissionsApi::class)
@Composable
fun MapScreen(
    navigateBack: () -> Unit
) {
    val cameraPermissionState = rememberPermissionState(
        permission = Permission.Camera,
    ) { isGranted ->
        // Handle permission state change
    }

    SampleScreenScaffold(
        title = "Adaptive Map",
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
                text = "Map views using Apple Maps on iOS and Google Maps on Android.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "Is permission granted: ${cameraPermissionState.status.isGranted}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary,
            )

            Spacer(modifier = Modifier.height(16.dp))

            AdaptiveButton(
                onClick = { cameraPermissionState.launchPermissionRequest() },
            ) {
                Text("Request permission")
            }
        }
    }
}
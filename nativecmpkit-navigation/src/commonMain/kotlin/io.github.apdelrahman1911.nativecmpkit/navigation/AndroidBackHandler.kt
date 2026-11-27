package io.github.apdelrahman1911.nativecmpkit.navigation

import androidx.compose.runtime.Composable

@Composable
expect fun AndroidBackHandler(
    enabled: Boolean = true,
    onBack: () -> Unit
)
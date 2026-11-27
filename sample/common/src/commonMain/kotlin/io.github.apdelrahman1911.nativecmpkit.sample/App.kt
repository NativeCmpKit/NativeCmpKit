package io.github.apdelrahman1911.nativecmpkit.sample

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.nativecmpkit.navigation.rememberNavController
import io.github.apdelrahman1911.nativecmpkit.sample.navigation.AppNavGraph
import io.github.apdelrahman1911.nativecmpkit.sample.ui.theme.NativeCmpKitTheme

@Composable
fun App() =
    NativeCmpKitTheme {
        val navController = rememberNavController()

        Surface(
            color = MaterialTheme.colorScheme.surface,
            contentColor = MaterialTheme.colorScheme.onSurface,
        ) {
            AppNavGraph(navController = navController)
        }
    }

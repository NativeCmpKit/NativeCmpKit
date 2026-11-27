package io.github.apdelrahman1911.kira.sample

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import io.github.apdelrahman1911.kira.navigation.rememberNavController
import io.github.apdelrahman1911.kira.sample.navigation.AppNavGraph
import io.github.apdelrahman1911.kira.sample.ui.theme.KiraTheme

@Composable
fun App() =
    KiraTheme {
        var resetKey by remember { mutableIntStateOf(0) }

        key(resetKey) {
            val navController = rememberNavController()

            Surface(
                color = MaterialTheme.colorScheme.surface,
                contentColor = MaterialTheme.colorScheme.onSurface,
            ) {
                AppNavGraph(
                    navController = navController,
                    onReset = { resetKey++ },
                )
            }
        }
    }

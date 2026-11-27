package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.setValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.kira.ui.gesture.adaptiveClickable

@Composable
fun AdaptiveClickableScreen(
    navigateBack: () -> Unit
) {
    var clicks by remember { mutableIntStateOf(0) }
    var longClicks by remember { mutableIntStateOf(0) }
    var doubleClicks by remember { mutableIntStateOf(0) }
    SampleScreenScaffold(
        title = "Adaptive Clickable",
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
                text = "Platform-aware click feedback. On iOS, uses highlight effect. On Android, uses ripple effect.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(32.dp))

            Box(
                modifier = Modifier
                    .adaptiveClickable(
                        shape = MaterialTheme.shapes.medium,
                        onLongClick = {
                            longClicks++
                        },
                        onDoubleClick = {
                            doubleClicks++
                        }
                    ) {
                        clicks++
                    }
                    .background(MaterialTheme.colorScheme.primary)
                    .padding(
                        horizontal = 20.dp,
                        vertical = 10.dp
                    )
            ) {
                Text(
                    text = "Tap me",
                    color = MaterialTheme.colorScheme.onPrimary,
                )
            }

            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = "Clicks: $clicks · Long: $longClicks · Double: $doubleClicks",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary,
            )
        }
    }
}
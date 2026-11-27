package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.kira.ui.slider.AdaptiveSlider

@Composable
fun SliderScreen(
    navigateBack: () -> Unit
) {
    SampleScreenScaffold(
        title = "Adaptive Slider",
        navigateBack = navigateBack,
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            Text(
                text = "Sliders using Liquid Glass on iOS 26+ and Material3 Slider on other platforms.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(24.dp))

            var brightness by remember { mutableFloatStateOf(0.5f) }
            var volume by remember { mutableFloatStateOf(0.75f) }
            var wide by remember { mutableFloatStateOf(40f) }
            var stepped by remember { mutableFloatStateOf(2f) }
            var locked by remember { mutableFloatStateOf(0.4f) }

            SliderSettingItem(
                title = "Brightness",
                value = brightness,
                onValueChange = { brightness = it },
            )
            SliderSettingItem(
                title = "Volume",
                value = volume,
                onValueChange = { volume = it },
            )
            SliderSettingItem(
                title = "Custom range 0..100",
                value = wide,
                onValueChange = { wide = it },
                valueRange = 0f..100f,
                readout = { "${it.toInt()} / 100" },
            )
            SliderSettingItem(
                title = "Discrete 0..5 (4 steps)",
                value = stepped,
                onValueChange = { stepped = it },
                valueRange = 0f..5f,
                steps = 4,
                readout = { "${it.toInt()} / 5" },
            )
            SliderSettingItem(
                title = "Disabled",
                value = locked,
                onValueChange = {},
                enabled = false,
                readout = { "${(it * 100).toInt()}%" },
            )
        }
    }
}

@Composable
private fun SliderSettingItem(
    title: String,
    value: Float,
    onValueChange: (Float) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    valueRange: ClosedFloatingPointRange<Float> = 0f..1f,
    steps: Int = 0,
    readout: (Float) -> String = { "${(it * 100).toInt()}%" },
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainer,
        ),
        shape = MaterialTheme.shapes.medium,
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)
        ) {
            Text(
                text = "$title — ${readout(value)}",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurface,
            )
            Spacer(modifier = Modifier.height(8.dp))
            AdaptiveSlider(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier.fillMaxWidth(),
                enabled = enabled,
                valueRange = valueRange,
                steps = steps,
            )
        }
    }
}

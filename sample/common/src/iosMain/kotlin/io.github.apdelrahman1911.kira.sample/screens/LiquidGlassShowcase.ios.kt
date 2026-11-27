package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
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
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.isLiquidGlassAvailable
import io.github.apdelrahman1911.kira.ui.ExperimentalKiraUiApi
import io.github.apdelrahman1911.kira.ui.button.LiquidGlassButton
import io.github.apdelrahman1911.kira.ui.button.LiquidGlassButtonDefaults
import io.github.apdelrahman1911.kira.ui.slider.LiquidGlassSlider
import io.github.apdelrahman1911.kira.ui.toggle.LiquidGlassSwitch

@OptIn(ExperimentalKiraUiApi::class)
@Composable
actual fun LiquidGlassShowcaseContent() {
    if (!isLiquidGlassAvailable) {
        Card(
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
            shape = MaterialTheme.shapes.medium,
            modifier = Modifier.fillMaxWidth().testTag("liquidglass.fallback"),
        ) {
            Column(Modifier.padding(16.dp)) {
                Text("Liquid Glass requires iOS 26 or newer", style = MaterialTheme.typography.titleSmall)
                Text(
                    "AdaptiveButton, AdaptiveSwitch and AdaptiveSlider provide the Cupertino fallback on this runtime.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        return
    }

    var clicks by remember { mutableIntStateOf(0) }
    var checked by remember { mutableStateOf(true) }
    var slider by remember { mutableFloatStateOf(0.45f) }

    Column(Modifier.fillMaxWidth().testTag("liquidglass.content")) {
        Text("LiquidGlassButton", style = MaterialTheme.typography.titleSmall)
        Spacer(Modifier.height(8.dp))
        LiquidGlassButton(onClick = { clicks++ }) { Text("Glass click $clicks") }
        Spacer(Modifier.height(8.dp))
        LiquidGlassButton(
            onClick = {},
            colors = LiquidGlassButtonDefaults.borderedButtonColors(),
        ) { Text("Glass bordered") }
        Spacer(Modifier.height(8.dp))
        LiquidGlassButton(
            onClick = {},
            colors = LiquidGlassButtonDefaults.plainButtonColors(),
        ) { Text("Glass plain") }
        Spacer(Modifier.height(8.dp))
        LiquidGlassButton(onClick = {}, enabled = false) { Text("Glass disabled") }

        Spacer(Modifier.height(20.dp))
        Text("LiquidGlassSwitch", style = MaterialTheme.typography.titleSmall)
        Spacer(Modifier.height(8.dp))
        LiquidGlassSwitch(checked = checked, onCheckedChange = { checked = it })
        Text("Glass switch: $checked", style = MaterialTheme.typography.bodySmall)

        Spacer(Modifier.height(20.dp))
        Text("LiquidGlassSlider", style = MaterialTheme.typography.titleSmall)
        Spacer(Modifier.height(8.dp))
        LiquidGlassSlider(value = slider, onValueChange = { slider = it }, modifier = Modifier.fillMaxWidth())
        Text("Glass slider: ${(slider * 100).toInt()}%", style = MaterialTheme.typography.bodySmall)
        Spacer(Modifier.height(8.dp))
        LiquidGlassSlider(value = 0.3f, onValueChange = {}, enabled = false, modifier = Modifier.fillMaxWidth())
    }
}

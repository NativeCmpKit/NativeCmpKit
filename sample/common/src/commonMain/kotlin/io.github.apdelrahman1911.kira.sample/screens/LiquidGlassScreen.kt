package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold

@Composable
fun LiquidGlassScreen(navigateBack: () -> Unit) {
    SampleScreenScaffold(title = "Liquid Glass", navigateBack = navigateBack) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            LiquidGlassShowcaseContent()
        }
    }
}

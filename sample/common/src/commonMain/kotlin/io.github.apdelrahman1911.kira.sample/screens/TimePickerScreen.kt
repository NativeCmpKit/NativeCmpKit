package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TimePickerDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.kira.ui.timepicker.AdaptiveTimePicker
import io.github.apdelrahman1911.kira.ui.timepicker.rememberAdaptiveTimePickerState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TimePickerScreen(
    navigateBack: () -> Unit
) {
    val state = rememberAdaptiveTimePickerState(
        initialHour = 19,
        initialMinute = 20,
    )
    val state24 = rememberAdaptiveTimePickerState(
        initialHour = 19,
        initialMinute = 20,
        is24Hour = true,
    )

    SampleScreenScaffold(
        title = "Adaptive Time Picker",
        navigateBack = navigateBack,
    ) { padding ->
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            Text(
                text = "Time selection using native iOS UIDatePicker and Material3 TimePicker.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(16.dp))

            val formattedMinute = state.minute.toString().padStart(2, '0')
            Text(
                text = "Selected time: ${state.hour}:$formattedMinute",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary,
            )

            Spacer(modifier = Modifier.height(16.dp))

            AdaptiveTimePicker(
                state = state,
                colors = TimePickerDefaults.colors(
                    containerColor = MaterialTheme.colorScheme.surface
                ),
            )

            Spacer(modifier = Modifier.height(24.dp))

            val formatted24 = "${state24.hour}:${state24.minute.toString().padStart(2, '0')}"
            Text(
                text = "24-hour state: $formatted24",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Spacer(modifier = Modifier.height(8.dp))
            AdaptiveTimePicker(state = state24)
        }
    }
}
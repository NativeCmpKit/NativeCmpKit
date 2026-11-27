package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.geo.LatLng
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold

@Composable
fun GeoMathScreen(navigateBack: () -> Unit) {
    val origin = LatLng(0.0, 0.0)
    val east = LatLng(0.0, 1.0)
    val north = LatLng(1.0, 0.0)

    SampleScreenScaffold(
        title = "Geo Maths",
        navigateBack = navigateBack,
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
                .testTag("geo.math"),
        ) {
            Text(
                text = "LatLng is a pure common-maths API. The production tracker is a no-op on iOS, desktop and web, and does not populate its public states on Android at this revision.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(modifier = Modifier.height(16.dp))
            MetricCard(
                title = "Distance (0,0) to (0,1)",
                value = "${origin.distanceTo(east)} km",
                description = "Haversine distance with a 6371 km Earth radius",
            )
            MetricCard(
                title = "Bearing (0,0) to (0,1)",
                value = "${origin.getAngleTo(east)} degrees",
                description = "Rounded to the nearest 10 degrees",
            )
            MetricCard(
                title = "Bearing (0,0) to (1,0)",
                value = "${origin.getAngleTo(north)} degrees",
                description = "North cardinal bearing",
            )
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.errorContainer,
                ),
                shape = MaterialTheme.shapes.medium,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Live tracking: unavailable",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "LocationTracker states stay at (0,0); Android also requires an Android-only bind(lifecycle, context, fragmentManager) call that the common sample cannot supply.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onErrorContainer,
                    )
                }
            }
        }
    }
}

@Composable
private fun MetricCard(title: String, value: String, description: String) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainer,
        ),
        shape = MaterialTheme.shapes.medium,
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = title, style = MaterialTheme.typography.titleSmall)
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = value,
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(
                text = description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

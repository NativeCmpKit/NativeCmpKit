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
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold

private data class Limit(val title: String, val detail: String)

private val LIMITS = listOf(
    Limit(
        "Expandable FAB is internal",
        "AdaptiveExpandableFAB and UIKitExpandableFABItem are internal in this revision, so the showcase cannot present them as a public component.",
    ),
    Limit(
        "No determinate circular progress",
        "AdaptiveCircularProgressIndicator exposes only the indeterminate Material3/Cupertino spinner. A determinate value cannot be supplied through public API.",
    ),
    Limit(
        "Buttons have no size or selected state",
        "AdaptiveButton, AdaptiveIconButton and CupertinoButton expose color, shape and padding variants only. There is no S/M/L or selected API.",
    ),
    Limit(
        "iOS 26 replaces some switch and slider parameters",
        "AdaptiveSwitch ignores thumbContent and per-call colors on iOS 26. AdaptiveSlider silently drops steps on iOS 26. iOS below 26 keeps the Cupertino controls.",
    ),
    Limit(
        "Time format follows the iOS device locale",
        "AdaptiveTimePickerState.is24Hour is accepted but is not applied by the UIKit time picker; the device locale decides 12/24-hour display.",
    ),
    Limit(
        "iOS menu anchor is the parent view",
        "AdaptiveDropDown anchors to its enclosing Box on iOS. Offset, shape, container color, elevation and border parameters are ignored on both platforms.",
    ),
    Limit(
        "Sheet inset and shape parameters are Material-only",
        "AdaptiveBottomSheet ignores contentWindowInsets, sheetMaxWidth, shape, scrimColor and properties on iOS.",
    ),
    Limit(
        "No public action-sheet anchor API",
        "On iPad the action sheet uses a centred popover anchored to the presenting view. The caller cannot supply a source view or bar-button anchor.",
    ),
    Limit(
        "Navigation arguments are declarations only",
        "AdaptiveNavHostController.navigate(route, arguments) ignores argument values. There are no nested graphs, deep links or non-Android system back handling.",
    ),
    Limit(
        "Geo tracker states are not populated",
        "LatLng maths is usable, but LocationTracker never updates its public states on any platform; Android additionally needs an Android-only bind call.",
    ),
    Limit(
        "Maps, media and notification scheduling are excluded",
        "kira-maps has only a build file. kira-media and the kira-notifications scheduler are not included in settings.gradle.kts. The notification permission remains supported.",
    ),
    Limit(
        "Desktop and web permission requests are stubs",
        "They remain Denied(false) forever and never invoke a result callback. Desktop/web camera launches are no-ops and never call back.",
    ),
    Limit(
        "Web save and folder selection are limited",
        "The browser file saver triggers a download but never invokes onResult. Folder selection returns an empty list.",
    ),
    Limit(
        "WebView settings differ by engine",
        "Desktop and web drop URL headers and HTML base/encoding. Only Android restores native view state. JavaScript is off by default.",
    ),
)

@Composable
fun LimitationsScreen(navigateBack: () -> Unit) {
    SampleScreenScaffold(
        title = "Known Limitations",
        navigateBack = navigateBack,
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
                .testTag("limitations.list")
        ) {
            Text(
                text = "These are source-confirmed limits at the pinned revision. They are shown here instead of being presented as working parity.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(modifier = Modifier.height(16.dp))
            LIMITS.forEach { limit ->
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
                        Text(
                            text = limit.title,
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = limit.detail,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

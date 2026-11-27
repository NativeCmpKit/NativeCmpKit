package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.outlined.Favorite
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import io.github.apdelrahman1911.kira.ui.button.AdaptiveIconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.setValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.ui.ExperimentalKiraUiApi
import io.github.apdelrahman1911.kira.ui.navigation.AdaptiveScaffold
import io.github.apdelrahman1911.kira.ui.navigation.AdaptiveTopBar
import io.github.apdelrahman1911.kira.ui.navigation.UIKitNavigationBarConfiguration
import io.github.apdelrahman1911.kira.ui.navigation.UIKitUIBarButtonItem
import io.github.apdelrahman1911.kira.ui.navigation.UIKitUIBarButtonSystemItem
import io.github.apdelrahman1911.kira.ui.uikit.UIKitImage
import io.github.apdelrahman1911.kira.sf.symbols.SFSymbol

@OptIn(ExperimentalMaterial3Api::class, ExperimentalKiraUiApi::class)
@Composable
fun TopBarDemoScreen(
    navigateBack: () -> Unit,
) {
    var lastAction by remember { mutableStateOf("No top-bar action") }
    AdaptiveScaffold(
        topBar = {
            AdaptiveTopBar(
                title = { Text("Adaptive Top Bar") },
                navigationIcon = {
                    IconButton(onClick = navigateBack) {
                        Icon(
                            Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                        )
                    }
                },
                actions = {
                    AdaptiveIconButton(onClick = { lastAction = "Share tapped" }) {
                        Icon(Icons.Filled.Share, contentDescription = "Share")
                    }
                    AdaptiveIconButton(onClick = { lastAction = "More tapped" }) {
                        Icon(Icons.Filled.MoreVert, contentDescription = "More")
                    }
                },
                iosTitle = "Adaptive Top Bar",
                iosLeadingItems = listOf(
                    UIKitUIBarButtonItem(
                        title = "Back",
                        onClick = navigateBack,
                    ),
                ),
                iosTrailingItems = listOf(
                    UIKitUIBarButtonItem(
                        image = UIKitImage.SystemName(SFSymbol.squareAndArrowUp),
                        accessibilityLabel = "Share",
                        onClick = { lastAction = "Share tapped" },
                    ),
                    UIKitUIBarButtonItem(
                        image = UIKitImage.SystemName(SFSymbol.ellipsisCircle),
                        accessibilityLabel = "More",
                        onClick = { lastAction = "More tapped" },
                    ),
                    UIKitUIBarButtonItem.systemItem(
                        systemItem = UIKitUIBarButtonSystemItem.Add,
                        onClick = { lastAction = "Add tapped" },
                    ),
                    UIKitUIBarButtonItem(
                        image = UIKitImage.Vector(Icons.Outlined.Favorite),
                        onClick = { /* vector image variant */ },
                    ),
                ),
                iosConfiguration = UIKitNavigationBarConfiguration(
                    prefersLargeTitles = true,
                    tintColor = MaterialTheme.colorScheme.primary,
                )
            )
        },
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            Text(
                text = "Top app bar using native iOS UINavigationBar and Material3 TopAppBar on other platforms.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Last action: $lastAction",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.primary,
            )

            Spacer(modifier = Modifier.height(24.dp))

            InfoCard(
                title = "Material3 (Android/Desktop/Web)",
                description = "Uses standard Material3 TopAppBar with navigationIcon, title, and actions slots. Supports scroll behavior and expanded height.",
            )

            Spacer(modifier = Modifier.height(12.dp))

            InfoCard(
                title = "iOS (UINavigationBar)",
                description = "Uses native UIKit UINavigationBar with iosTitle, iosLeadingItems, and iosTrailingItems. Automatically adapts to iOS navigation patterns.",
            )

            Spacer(modifier = Modifier.height(12.dp))

            InfoCard(
                title = "This Screen",
                description = "This screen demonstrates a top bar with a back button (leading) and two action buttons (trailing: Share and More). On iOS, these become native UIBarButtonItems.",
            )
        }
    }
}

@Composable
private fun InfoCard(
    title: String,
    description: String,
    modifier: Modifier = Modifier,
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainer,
        ),
        shape = MaterialTheme.shapes.medium,
        modifier = modifier,
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurface,
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

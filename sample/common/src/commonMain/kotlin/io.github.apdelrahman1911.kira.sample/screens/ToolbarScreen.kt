package io.github.apdelrahman1911.kira.sample.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import io.github.apdelrahman1911.kira.ui.button.AdaptiveIconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.kira.sample.components.SampleScreenScaffold
import io.github.apdelrahman1911.kira.sample.currentPlatform
import io.github.apdelrahman1911.kira.ui.ExperimentalKiraUiApi
import io.github.apdelrahman1911.kira.ui.navigation.UIKitUIBarButtonItem
import io.github.apdelrahman1911.kira.ui.toolbar.AdaptiveToolbar
import io.github.apdelrahman1911.kira.ui.toggle.AdaptiveSwitch
import io.github.apdelrahman1911.kira.ui.uikit.UIKitImage
import io.github.apdelrahman1911.kira.sf.symbols.SFSymbol

private enum class SpacingPattern(val label: String) {
    Default("Default"),
    FlexibleSpace("Flexible Space"),
    FixedSpace("Fixed Space"),
    EvenlySpaced("Evenly Spaced"),
    LeadingGroup("Leading Group"),
    Spread("Spread"),
}

@OptIn(ExperimentalKiraUiApi::class, ExperimentalLayoutApi::class)
@Composable
fun ToolbarScreen(
    navigateBack: () -> Unit
) {
    var lastAction by remember { mutableStateOf("Tap a toolbar button") }
    var selectedPattern by remember { mutableStateOf(SpacingPattern.Default) }
    var expanded by remember { mutableStateOf(true) }

    val backItem = UIKitUIBarButtonItem(
        image = UIKitImage.SystemName(SFSymbol.chevronLeft),
        accessibilityLabel = "Back",
        onClick = { lastAction = "Back tapped" },
    )
    val forwardItem = UIKitUIBarButtonItem(
        image = UIKitImage.SystemName(SFSymbol.chevronRight),
        accessibilityLabel = "Forward",
        onClick = { lastAction = "Forward tapped" },
    )
    val shareItem = UIKitUIBarButtonItem(
        image = UIKitImage.SystemName(SFSymbol.squareAndArrowUp),
        accessibilityLabel = "Share",
        onClick = { lastAction = "Share tapped" },
    )
    val bookmarkItem = UIKitUIBarButtonItem(
        image = UIKitImage.SystemName(SFSymbol.book),
        accessibilityLabel = "Bookmark",
        onClick = { lastAction = "Bookmark tapped" },
    )

    val iosItems = when (selectedPattern) {
        SpacingPattern.Default -> listOf(
            backItem, forwardItem, shareItem, bookmarkItem,
        )
        SpacingPattern.FlexibleSpace -> listOf(
            backItem, forwardItem, shareItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            bookmarkItem,
        )
        SpacingPattern.FixedSpace -> listOf(
            backItem,
            UIKitUIBarButtonItem.fixedSpace(32.0),
            forwardItem,
            UIKitUIBarButtonItem.fixedSpace(32.0),
            shareItem,
            UIKitUIBarButtonItem.fixedSpace(32.0),
            bookmarkItem,
        )
        SpacingPattern.EvenlySpaced -> listOf(
            UIKitUIBarButtonItem.flexibleSpace(),
            backItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            forwardItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            shareItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            bookmarkItem,
            UIKitUIBarButtonItem.flexibleSpace(),
        )
        SpacingPattern.LeadingGroup -> listOf(
            backItem, forwardItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            shareItem, bookmarkItem,
        )
        SpacingPattern.Spread -> listOf(
            backItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            forwardItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            shareItem,
            UIKitUIBarButtonItem.flexibleSpace(),
            bookmarkItem,
        )
    }

    SampleScreenScaffold(
        title = "Adaptive Toolbar",
        navigateBack = navigateBack,
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                if (currentPlatform.isIOS) {
                    Text(
                        text = "Spacing Pattern",
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurface,
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp),
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        SpacingPattern.entries.forEach { pattern ->
                            FilterChip(
                                selected = selectedPattern == pattern,
                                onClick = { selectedPattern = pattern },
                                label = { Text(pattern.label) },
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                }

                Text(
                    text = lastAction,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurface,
                )

                Spacer(modifier = Modifier.height(12.dp))

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text(
                        text = "Material expanded",
                        modifier = Modifier.weight(1f),
                        style = MaterialTheme.typography.bodyMedium,
                    )
                    AdaptiveSwitch(
                        checked = expanded,
                        onCheckedChange = { expanded = it },
                    )
                }
            }

            AdaptiveToolbar(
                expanded = expanded,
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(bottom = 16.dp),
                iosItems = iosItems,
                content = {
                    AdaptiveIconButton(onClick = { lastAction = "Back tapped" }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                    AdaptiveIconButton(onClick = { lastAction = "Forward tapped" }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Forward")
                    }
                    AdaptiveIconButton(onClick = { lastAction = "Share tapped" }) {
                        Icon(Icons.Filled.Share, contentDescription = "Share")
                    }
                    AdaptiveIconButton(onClick = { lastAction = "Bookmark tapped" }) {
                        Icon(Icons.Filled.BookmarkBorder, contentDescription = "Bookmark")
                    }
                },
            )
        }
    }
}

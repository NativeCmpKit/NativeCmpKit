package io.github.apdelrahman1911.nativecmpkit.sample.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.outlined.Favorite
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.rounded.Favorite
import androidx.compose.material.icons.rounded.Home
import androidx.compose.material.icons.rounded.Settings
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import io.github.apdelrahman1911.nativecmpkit.ui.button.AdaptiveIconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import io.github.apdelrahman1911.nativecmpkit.ui.ExperimentalNativeCmpKitUiApi
import io.github.apdelrahman1911.nativecmpkit.ui.navigation.AdaptiveNavigationBar
import io.github.apdelrahman1911.nativecmpkit.ui.navigation.AdaptiveScaffold
import io.github.apdelrahman1911.nativecmpkit.ui.navigation.AdaptiveTopBar
import io.github.apdelrahman1911.nativecmpkit.ui.navigation.UIKitUIBarButtonItem
import io.github.apdelrahman1911.nativecmpkit.ui.navigation.UIKitUITabBarItem
import io.github.apdelrahman1911.nativecmpkit.ui.uikit.UIKitImage
import io.github.apdelrahman1911.nativecmpkit.sf.symbols.SFSymbol

@OptIn(ExperimentalNativeCmpKitUiApi::class, ExperimentalMaterial3Api::class)
@Composable
fun ScaffoldDemoScreen(
    navigateBack: () -> Unit,
) {
    var selectedIndex by remember { mutableStateOf(0) }
    val tabs = listOf("Home", "Favorites", "Settings")
    val icons = listOf(
        Icons.Outlined.Home,
        Icons.Outlined.Favorite,
        Icons.Outlined.Settings,
    )
    val selectedIcons = listOf(
        Icons.Filled.Home,
        Icons.Filled.Favorite,
        Icons.Filled.Settings,
    )

    AdaptiveScaffold(
        topBar = {
            AdaptiveTopBar(
                title = { Text(tabs[selectedIndex]) },
                navigationIcon = {
                    AdaptiveIconButton(onClick = navigateBack) {
                        Icon(
                            Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                        )
                    }
                },
                iosTitle = tabs[selectedIndex],
                iosLeadingItems = listOf(
                    UIKitUIBarButtonItem(
                        title = "Back",
                        onClick = navigateBack,
                    )
                ),
            )
        },
        bottomBar = {
            AdaptiveNavigationBar(
                iosItems = listOf(
                    UIKitUITabBarItem(
                        title = "Home",
                        image = UIKitImage.SystemName(SFSymbol.houseFill),
                    ),
                    UIKitUITabBarItem(
                        title = "Favorites",
                        image = UIKitImage.Vector(Icons.Rounded.Favorite),
                    ),
                    UIKitUITabBarItem(
                        title = "Settings",
                        image = UIKitImage.Vector(Icons.Rounded.Settings),
                    ),
                ),
                iosSelectedIndex = selectedIndex,
                iosOnItemSelected = { selectedIndex = it },
                modifier = Modifier.fillMaxWidth(),
            ) {
                tabs.forEachIndexed { index, tab ->
                    NavigationBarItem(
                        selected = selectedIndex == index,
                        onClick = { selectedIndex = index },
                        icon = {
                            Icon(
                                if (selectedIndex == index) selectedIcons[index] else icons[index],
                                contentDescription = tab,
                            )
                        },
                        label = { Text(tab) },
                    )
                }
            }
        },
    ) { padding ->
        AnimatedContent(
            targetState = selectedIndex,
            transitionSpec = {
                fadeIn(animationSpec = tween(300)) togetherWith
                        fadeOut(animationSpec = tween(300))
            },
            modifier = Modifier.fillMaxSize(),
        ) { tabIndex ->
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text(
                        text = tabs[tabIndex],
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                    )
                    Text(
                        text = "This demonstrates AdaptiveScaffold + AdaptiveTopBar + AdaptiveNavigationBar working together. On iOS, native UINavigationBar and UITabBar are used.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

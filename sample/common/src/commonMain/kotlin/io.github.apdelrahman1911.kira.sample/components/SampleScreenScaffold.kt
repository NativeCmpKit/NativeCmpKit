package io.github.apdelrahman1911.kira.sample.components

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.RowScope
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import io.github.apdelrahman1911.kira.ui.ExperimentalKiraUiApi
import io.github.apdelrahman1911.kira.ui.navigation.AdaptiveScaffold
import io.github.apdelrahman1911.kira.ui.navigation.AdaptiveTopBar
import io.github.apdelrahman1911.kira.ui.navigation.UIKitUIBarButtonItem

@OptIn(ExperimentalMaterial3Api::class, ExperimentalKiraUiApi::class)
@Composable
fun SampleScreenScaffold(
    title: String,
    navigateBack: () -> Unit,
    modifier: Modifier = Modifier,
    actions: @Composable RowScope.() -> Unit = {},
    iosTrailingItems: List<UIKitUIBarButtonItem> = emptyList(),
    content: @Composable (PaddingValues) -> Unit,
) {
    val screenTag = "screen." + title.lowercase().replace(Regex("[^a-z0-9]+"), "-").trim('-')
    AdaptiveScaffold(
        modifier = modifier.testTag(screenTag),
        topBar = {
            AdaptiveTopBar(
                title = { Text(title) },
                navigationIcon = {
                    IconButton(onClick = navigateBack) {
                        Icon(
                            Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                        )
                    }
                },
                actions = actions,
                iosTitle = title,
                iosLeadingItems = listOf(
                    UIKitUIBarButtonItem(
                        title = "Back",
                        onClick = navigateBack,
                    )
                ),
                iosTrailingItems = iosTrailingItems,
            )
        },
        content = content,
    )
}

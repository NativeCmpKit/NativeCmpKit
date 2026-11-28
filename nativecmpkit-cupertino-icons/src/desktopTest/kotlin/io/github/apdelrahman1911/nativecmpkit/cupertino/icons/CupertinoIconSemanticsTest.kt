package io.github.apdelrahman1911.nativecmpkit.cupertino.icons

import androidx.compose.material3.Button
import androidx.compose.material3.IconButton
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.assert
import androidx.compose.ui.test.assertContentDescriptionEquals
import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.hasClickAction
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.onAllNodesWithContentDescription
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.v2.runComposeUiTest
import androidx.compose.ui.unit.Density
import kotlin.test.Test
import kotlin.test.assertEquals

@OptIn(ExperimentalTestApi::class)
class CupertinoIconSemanticsTest {
    @Test
    fun decorativeIconDoesNotExposePrivateUseText() = runComposeUiTest {
        setContent { CupertinoIcon(CupertinoIcons.house, contentDescription = null) }
        onAllNodes(hasText(Char(CupertinoIcons.house).toString())).assertCountEquals(0)
        onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.ContentDescription)).assertCountEquals(0)
        onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.Text)).assertCountEquals(0)
    }

    @Test
    fun labeledIconExposesExactlyOneDescriptionAndNoGlyphText() = runComposeUiTest {
        setContent { CupertinoIcon(CupertinoIcons.heartFill, contentDescription = "Favorite") }
        onAllNodesWithContentDescription("Favorite").assertCountEquals(1)
        onNodeWithContentDescription("Favorite")
            .assert(SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Image))
        onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.Text)).assertCountEquals(0)
    }

    @Test
    fun decorativeIconDoesNotReplaceContainingButtonLabelOrAction() = runComposeUiTest {
        setContent {
            IconButton(onClick = {}, modifier = Modifier.semantics { contentDescription = "Open home" }) {
                CupertinoIcon(CupertinoIcons.house)
            }
        }
        onNodeWithContentDescription("Open home").assert(hasClickAction())
        onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.Text)).assertCountEquals(0)
    }

    @Test
    fun labeledIconOnlyButtonKeepsOneLabelAndItsActionAtDifferentFontScales() = runComposeUiTest {
        val fontScales = listOf(0.85f, 1.0f, 2.0f)
        val scale = mutableStateOf(fontScales.first())
        var clicks = 0
        setContent {
            val density = LocalDensity.current
            CompositionLocalProvider(LocalDensity provides Density(density.density, scale.value)) {
                Button(onClick = { clicks++ }, modifier = Modifier.testTag("favorite-button")) {
                    CupertinoIcon(
                        CupertinoIcons.heartFill,
                        modifier = Modifier.testTag("favorite-icon"),
                        contentDescription = "Favorite",
                    )
                }
            }
        }

        val glyphText = SemanticsMatcher("private-use font glyph text") { node ->
            node.config.contains(SemanticsProperties.Text) &&
                node.config[SemanticsProperties.Text].any { text ->
                    text.text.any { it in '\uE000'..'\uF8FF' || it in '\uF900'..'\uF921' }
                }
        }
        for (fontScale in fontScales) {
            runOnIdle { scale.value = fontScale }
            waitForIdle()
            onNodeWithTag("favorite-button", useUnmergedTree = true).assert(hasClickAction())
            onNodeWithTag("favorite-button")
                .assert(hasClickAction())
                .assertContentDescriptionEquals("Favorite")
                .assert(SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Button))
                .performClick()
            onNodeWithTag("favorite-icon", useUnmergedTree = true)
                .assertContentDescriptionEquals("Favorite")
                .assert(SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Image))
            for (unmerged in listOf(false, true)) {
                onAllNodesWithContentDescription("Favorite", useUnmergedTree = unmerged).assertCountEquals(1)
                onAllNodes(glyphText, useUnmergedTree = unmerged).assertCountEquals(0)
            }
        }
        runOnIdle { assertEquals(fontScales.size, clicks) }
    }
}

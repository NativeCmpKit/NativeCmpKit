package io.github.apdelrahman1911.nativecmpkit.picker

import android.net.Uri
import androidx.activity.compose.LocalActivityResultRegistryOwner
import androidx.activity.result.ActivityResultRegistry
import androidx.activity.result.ActivityResultRegistryOwner
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.test.junit4.StateRestorationTester
import androidx.compose.ui.test.junit4.createComposeRule
import io.github.apdelrahman1911.nativecmpkit.core.ExperimentalNativeCmpKitApi
import io.github.apdelrahman1911.nativecmpkit.io.KmpFile
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import kotlin.test.assertContentEquals
import kotlin.test.assertNotNull
import kotlin.test.assertNull

@OptIn(ExperimentalNativeCmpKitApi::class)
@RunWith(RobolectricTestRunner::class)
@Config(shadows = [HostFileStatShadow::class])
class SaverRestorationTest {
    @get:Rule val compose = createComposeRule()
    @get:Rule val folder = TemporaryFolder()
    private val registry = RecordingActivityResultRegistry()
    private lateinit var launcher: FileSaverLauncher
    private var result: KmpFile? = null
    private var error: FilePickerException? = null

    @Test fun rememberedUriRequestSurvivesSavedStateRestore() {
        val restoration = content()
        val source = folder.newFile("source").apply { writeBytes(byteArrayOf(9, 8, 7)) }
        val destination = folder.newFile("destination")
        compose.runOnIdle { launcher.launch(KmpFile(Uri.fromFile(source)), "copy", "bin") }
        restoration.emulateSavedInstanceStateRestore()
        compose.runOnIdle { registry.dispatchLast(Uri.fromFile(destination)) }
        compose.waitUntil(5_000) { result != null || error != null }
        assertNull(error)
        assertContentEquals(byteArrayOf(9, 8, 7), destination.readBytes())
    }

    @Test fun restoredByteRequestReportsErrorInsteadOfEmptySuccess() {
        val restoration = content()
        val destination = folder.newFile("destination")
        compose.runOnIdle { launcher.launch(byteArrayOf(1, 2), "copy", "bin") }
        restoration.emulateSavedInstanceStateRestore()
        compose.runOnIdle { registry.dispatchLast(Uri.fromFile(destination)) }
        compose.waitUntil(5_000) { result != null || error != null }
        assertNotNull(error)
        assertNull(result)
    }

    private fun content(): StateRestorationTester {
        val owner = object : ActivityResultRegistryOwner { override val activityResultRegistry: ActivityResultRegistry = registry }
        return StateRestorationTester(compose).apply {
            setContent {
                CompositionLocalProvider(LocalActivityResultRegistryOwner provides owner) {
                    launcher = rememberFileSaverLauncher(onError = { error = it }, onResult = { result = it })
                }
            }
        }
    }
}

package io.github.apdelrahman1911.nativecmpkit.consumer

import androidx.compose.runtime.Composable
import coil3.fetch.Fetcher
import io.github.apdelrahman1911.nativecmpkit.camerapicker.rememberCameraPickerLauncher
import io.github.apdelrahman1911.nativecmpkit.core.ExperimentalNativeCmpKitApi
import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext
import io.github.apdelrahman1911.nativecmpkit.cupertino.icons.CupertinoIcon
import io.github.apdelrahman1911.nativecmpkit.cupertino.icons.CupertinoIcons
import io.github.apdelrahman1911.nativecmpkit.geo.LocationTracker
import io.github.apdelrahman1911.nativecmpkit.geo.createLocationTracker
import io.github.apdelrahman1911.nativecmpkit.io.KmpFile
import io.github.apdelrahman1911.nativecmpkit.io.source
import io.github.apdelrahman1911.nativecmpkit.navigation.AdaptiveNavHost
import io.github.apdelrahman1911.nativecmpkit.navigation.rememberAdaptiveNavController
import io.github.apdelrahman1911.nativecmpkit.permissions.*
import io.github.apdelrahman1911.nativecmpkit.picker.*
import io.github.apdelrahman1911.nativecmpkit.picker.coil.KmpFileFetcher
import io.github.apdelrahman1911.nativecmpkit.share.*
import io.github.apdelrahman1911.nativecmpkit.ui.progress.AdaptiveCircularProgressIndicator
import io.github.apdelrahman1911.nativecmpkit.ui.toggle.AdaptiveSwitch
import io.github.apdelrahman1911.nativecmpkit.ui.web.*
import kotlinx.io.RawSource

/**
 * Compiled against Maven/KLIB artifacts, never the producer source tree. This is a SOURCE
 * compatibility probe, not a claim that calling it rendered/presented every native control.
 */
@OptIn(ExperimentalNativeCmpKitApi::class, ExperimentalPermissionsApi::class)
@Composable
fun PublicApiConsumer(onFile: (KmpFile) -> Unit) {
    AdaptiveSwitch(checked = false, onCheckedChange = null)
    AdaptiveCircularProgressIndicator()
    CupertinoIcon(CupertinoIcons.house, contentDescription = "Home")
    rememberFilePickerLauncher(onResult = { it.firstOrNull()?.let(onFile) })
    rememberFileSaverLauncher(onResult = { it?.let(onFile) })
    rememberCameraPickerLauncher(onResult = onFile)
    rememberShareLauncher(onResult = {})
    rememberPermissionState(Permission.Camera)
    WebView(rememberWebViewState("about:blank"))
}

// Public RawSource must be consumable via the IO artifact's API dependency.
suspend fun consumeStream(file: KmpFile, context: PlatformContext): RawSource = file.source(context)
fun consumeCoilFactory(): Fetcher.Factory<KmpFile> = KmpFileFetcher.Factory()

@Composable
fun consumePublishedNavigationHost() {
    AdaptiveNavHost(rememberAdaptiveNavController(), startDestination = "home") {
        composable("home") {}
    }
}

fun consumePublishedLocationTracker(): LocationTracker = createLocationTracker()

fun allModularPermissions(): List<Permission> = listOf(
    Permission.Camera, Permission.Gallery, Permission.ReadImage, Permission.ReadVideo,
    Permission.FineLocation, Permission.CoarseLocation, Permission.BackgroundLocation,
    Permission.BluetoothLe, Permission.BluetoothScan, Permission.BluetoothConnect, Permission.BluetoothAdvertise,
    Permission.ReadContacts, Permission.WriteContacts, Permission.ReadCalendar, Permission.WriteCalendar,
    Permission.Notification, Permission.RemoteNotification, Permission.WifiAccessState,
    Permission.WifiChangeState, Permission.WifiNearbyDevices, Permission.RecordAudio,
)

// Adding cases to these legacy sealed types is a source break for real exhaustive consumers.
@OptIn(ExperimentalPermissionsApi::class)
fun legacyPermissionBranch(status: PermissionStatus): String = when (status) {
    PermissionStatus.Granted -> "granted"
    is PermissionStatus.Denied -> "denied"
}

fun legacyShareBranch(result: ShareResult): String = when (result) {
    ShareResult.Success -> "success"
    ShareResult.Dismissed -> "dismissed"
    ShareResult.Unavailable -> "unavailable"
}

fun legacyWebContentBranch(content: WebContent): String = when (content) {
    is WebContent.Url -> content.url
    is WebContent.Data -> content.data
    WebContent.NavigatorOnly -> "navigator-only"
}

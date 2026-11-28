package io.github.apdelrahman1911.nativecmpkit.consumer

import android.content.Context
import androidx.fragment.app.FragmentManager
import androidx.lifecycle.Lifecycle
import androidx.navigation.NavHostController
import com.google.android.gms.location.LocationResult
import io.github.apdelrahman1911.nativecmpkit.geo.LocationTracker
import io.github.apdelrahman1911.nativecmpkit.navigation.navigate as navigatePlatformBridge

// Compile against the staged AARs without declaring their Android API dependencies here.
@Suppress("DEPRECATION")
fun consumeAndroidGeoBindings(
    tracker: LocationTracker,
    lifecycle: Lifecycle,
    context: Context,
    fragments: FragmentManager,
    result: LocationResult,
) {
    tracker.bind(lifecycle, context, fragments)
    tracker.bind(lifecycle, context)
    tracker.onLocationResult(result)
    tracker.unbind()
}

fun consumeAndroidNavigationBridge(controller: NavHostController) {
    controller.navigatePlatformBridge("details")
}

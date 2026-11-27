package io.github.apdelrahman1911.nativecmpkit.navigation

actual typealias NavHostController = AdaptiveNavHostController

actual fun NavHostController.navigate(route: String) {
    navigate(route)
}

actual fun NavHostController.popBackStack(): Boolean {
    return popBackStack()
}

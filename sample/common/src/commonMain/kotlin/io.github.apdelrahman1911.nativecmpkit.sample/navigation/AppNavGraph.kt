package io.github.apdelrahman1911.nativecmpkit.sample.navigation

import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.nativecmpkit.navigation.AdaptiveNavHost
import io.github.apdelrahman1911.nativecmpkit.navigation.AdaptiveNavHostController
import io.github.apdelrahman1911.nativecmpkit.sample.screens.AdaptiveClickableScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.AlertDialogScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.BottomSheetScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ButtonScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.CameraPickerScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.CupertinoIconsCatalogScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.DropDownScreen
//import io.github.apdelrahman1911.nativecmpkit.sample.screens.ExpandableFABScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.DatePickerScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.FilePickerScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.HomeScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ImagePickerScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.FileSaverScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ShowcaseScreen
//import io.github.apdelrahman1911.nativecmpkit.sample.screens.MapScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.NavigationBarScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.PermissionScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ProgressBarScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ScaffoldDemoScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ShareScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.SliderScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.SwitchScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.TimePickerScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.ToolbarScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.TopBarDemoScreen
import io.github.apdelrahman1911.nativecmpkit.sample.screens.WebViewScreen

@Composable
fun AppNavGraph(
    navController: AdaptiveNavHostController
) {
    AdaptiveNavHost(
        navController = navController,
        startDestination = Screen.Home.name
    ) {
        composable(Screen.Home.name) {
            HomeScreen(
                navigate = {
                    navController.navigate(it)
                }
            )
        }
        composable(Screen.Showcase.name) {
            ShowcaseScreen(
                navigateBack = {
                    navController.popBackStack()
                },
            )
        }
        composable(Screen.Dialog.name) {
            AlertDialogScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.BottomSheet.name) {
            BottomSheetScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.ProgressBar.name) {
            ProgressBarScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.Switch.name) {
            SwitchScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.Slider.name) {
            SliderScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.Button.name) {
            ButtonScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.DropDown.name) {
            DropDownScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.DatePicker.name) {
            DatePickerScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.TimePicker.name) {
            TimePickerScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.AdaptiveClickable.name) {
            AdaptiveClickableScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.FilePicker.name) {
            FilePickerScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.ImagePicker.name) {
            ImagePickerScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.ProfilePicture.name) {
            FileSaverScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.CameraPickerScreen.name) {
            CameraPickerScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.CupertinoIconsCatalog.name) {
            CupertinoIconsCatalogScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.Share.name) {
            ShareScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.WebView.name) {
            WebViewScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.Permission.name) {
            PermissionScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
//        composable(Screen.Map.name) {
//            MapScreen(
//                navigateBack = {
//                    navController.popBackStack()
//                }
//            )
//        }
        composable(Screen.NavigationBar.name) {
            NavigationBarScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.ScaffoldDemo.name) {
            ScaffoldDemoScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
        composable(Screen.TopBarDemo.name) {
            TopBarDemoScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
//        composable(Screen.ExpandableFAB.name) {
//            ExpandableFABScreen(
//                navigateBack = {
//                    navController.popBackStack()
//                }
//            )
//        }
        composable(Screen.Toolbar.name) {
            ToolbarScreen(
                navigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}

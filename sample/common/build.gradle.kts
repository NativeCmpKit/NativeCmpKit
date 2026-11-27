// Modified for nativeCmpkit (2026-10-24): correctness, lifecycle, testing and build hardening.
plugins {
    id("compose.multiplatform")
    id("desktop.javafx")
}

kotlin {
    sourceSets.commonTest.dependencies {
        implementation(libs.kotlinx.coroutines.test)
    }

    // Actual Android Bitmap/encoder checks on a JVM native-graphics host, not a device claim.
    sourceSets.named("androidHostTest").dependencies {
        implementation(libs.junit)
        implementation(libs.robolectric)
    }

    // Actual sample coroutine-owner disposal, not a substitute for library integration suites.
    sourceSets.desktopTest.dependencies {
        implementation(libs.compose.ui.test)
    }

    listOf(
        iosArm64(),
        iosSimulatorArm64(),
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "NativeCmpKit"
            isStatic = true

            // IMPORTANT: Exporting nativecmpkit-ui is required for some functionalities to work
            export(projects.nativecmpkitUi)
        }
    }

    sourceSets.commonMain.dependencies {
        api(libs.compose.foundation)
        api(libs.compose.material3)
        implementation(libs.compose.material.icons.extended)

        implementation(libs.kotlinx.datetime)

        // NativeCmpKit
        api(projects.nativecmpkitUi)
        implementation(projects.nativecmpkitFilePicker)
        implementation(projects.nativecmpkitFilePickerCoil)
        implementation(projects.nativecmpkitPermissions)
        implementation(projects.nativecmpkitWebview)
        implementation(projects.nativecmpkitNavigation)
        implementation(projects.nativecmpkitCameraPicker)
        implementation(projects.nativecmpkitShare)
        implementation(projects.nativecmpkitCupertinoIcons)

        // Coil
        implementation(libs.coil.compose)
        implementation(libs.coil.network.ktor)

        // Ktor
        implementation(libs.ktor.client.core)
    }

    sourceSets.androidMain.dependencies {
        implementation(libs.kotlinx.coroutines.android)
        implementation(libs.ktor.client.okhttp)
    }

    sourceSets.desktopMain.dependencies {
        implementation(compose.desktop.currentOs)

        implementation(libs.kotlinx.coroutines.swing)
        implementation(libs.ktor.client.okhttp)
    }

    sourceSets.iosMain.dependencies {
        implementation(libs.ktor.client.darwin)
    }

    sourceSets.jsMain.dependencies {
        implementation(libs.ktor.client.js)
    }

    sourceSets.wasmJsMain.dependencies {
        implementation(libs.ktor.client.wasm)
    }
}

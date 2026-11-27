plugins {
    id("compose.multiplatform")
}

kotlin {
    listOf(
        iosArm64(),
        iosSimulatorArm64(),
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "Common"
            isStatic = true

            // IMPORTANT: Exporting kira-ui is required for some functionalities to work
            export(projects.kiraUi)
        }
    }

    sourceSets.commonMain.dependencies {
        api(libs.compose.foundation)
        api(libs.compose.material3)
        implementation(libs.compose.material.icons.extended)

        implementation(libs.kotlinx.datetime)

        // Kira
        api(projects.kiraUi)
        implementation(projects.kiraFilePicker)
        implementation(projects.kiraFilePickerCoil)
        implementation(projects.kiraPermissions)
        implementation(projects.kiraWebview)
        implementation(libs.jetbrains.navigation.compose)
        implementation(projects.kiraNavigation)
        implementation(projects.kiraGeo)
        implementation(projects.kiraCameraPicker)
        implementation(projects.kiraShare)
        implementation(projects.kiraCupertinoIcons)

        // Coil
        implementation(libs.coil.compose)
        implementation(libs.coil.network.ktor)

        // Ktor
        implementation(libs.ktor.client.core)
    }

    sourceSets.androidMain.dependencies {
        implementation(libs.kotlinx.coroutines.android)
        implementation(libs.ktor.client.okhttp)
        implementation(libs.appcompat)
        implementation(libs.lifecycle.extensions)
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

// Modified for NativeCmpKit migration (2026-10-24): sample identity only.
import org.gradle.api.tasks.Copy

plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.composeMultiplatform)
}

android {
    namespace = "io.github.apdelrahman1911.nativecmpkit.sample"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        minSdk = libs.versions.android.sample.minSdk.get().toInt()
        targetSdk = libs.versions.android.compileSdk.get().toInt()

        applicationId = "io.github.apdelrahman1911.nativecmpkit.sample"
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
    }
    compileOptions {
        // AGP's built-in Kotlin support derives the Kotlin jvmTarget from targetCompatibility.
        val javaVersion = JavaVersion.toVersion(libs.versions.java.get().toInt())
        sourceCompatibility = javaVersion
        targetCompatibility = javaVersion
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(projects.sample.common)

    implementation(libs.activity.compose)
    implementation(libs.compose.tooling.preview)
    implementation(libs.appcompat)
    debugImplementation(libs.compose.tooling)
}

// Compose 1.12 does not package this library font into the APK through the
// com.android.kotlin.multiplatform.library AAR. Keep the public CupertinoIcon
// API unchanged and stage the reviewed font at the Compose Resources asset path.
val cupertinoFontAssets = layout.buildDirectory.dir(
    "generated/cupertinoAssets/composeResources/" +
        "io.github.apdelrahman1911.kira.kira_cupertino_icons.generated.resources/font",
)
val copyCupertinoFont by tasks.registering(Copy::class) {
    from(rootProject.file("kira-cupertino-icons/src/commonMain/composeResources/font/sf_symbols.ttf"))
    into(cupertinoFontAssets)
}
android.sourceSets.getByName("main").assets.srcDir(
    layout.buildDirectory.dir("generated/cupertinoAssets"),
)
tasks.named("preBuild").configure { dependsOn(copyCupertinoFont) }

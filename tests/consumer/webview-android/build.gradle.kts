import java.nio.file.Files
import org.gradle.api.artifacts.component.ModuleComponentIdentifier

plugins {
    id("com.android.application") version "9.4.0"
    id("org.jetbrains.compose") version "1.12.0"
    id("org.jetbrains.kotlin.plugin.compose") version "2.4.20"
}

val candidateVersion = providers.gradleProperty("nativecmpkitVersion").get()
require(candidateVersion == "0.1.0-preview.1") { "Use the exact staged WebView candidate" }

android {
    namespace = "io.github.apdelrahman1911.nativecmpkit.consumer.androidwebview"
    compileSdk = 37
    defaultConfig {
        applicationId = "io.github.apdelrahman1911.nativecmpkit.consumer.androidwebview"
        minSdk = 23
        targetSdk = 37
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    buildFeatures { compose = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-webview:$candidateVersion")
    implementation(compose.foundation)
    implementation("androidx.activity:activity-compose:1.13.0")
    androidTestImplementation("androidx.test:runner:1.7.0")
    androidTestImplementation("androidx.test:core:1.7.0")
    androidTestImplementation("junit:junit:4.13.2")
}

tasks.register("verifyPublishedWebViewBinding") {
    doLast {
        val group = "io.github.apdelrahman1911.nativecmpkit"
        val module = "nativecmpkit-webview-android"
        val staged = file(providers.gradleProperty("nativecmpkitRepository").get())
            .resolve("${group.replace('.', '/')}/$module/$candidateVersion")
            .listFiles()?.single { it.extension == "aar" } ?: error("Missing staged Android WebView AAR")
        val resolved = configurations.getByName("debugRuntimeClasspath").incoming.artifacts.artifacts.single {
            val id = it.id.componentIdentifier
            id is ModuleComponentIdentifier && id.group == group && id.module == module && id.version == candidateVersion
        }
        check(Files.mismatch(staged.toPath(), resolved.file.toPath()) == -1L) { "Resolved Android WebView differs from the staged AAR" }
        println("Independent Android WebView input: $group:$module:$candidateVersion (${staged.length()} bytes)")
    }
}

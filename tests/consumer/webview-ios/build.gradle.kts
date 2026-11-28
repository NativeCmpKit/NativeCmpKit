import java.nio.file.Files
import org.gradle.api.artifacts.component.ModuleComponentIdentifier

plugins {
    kotlin("multiplatform") version "2.4.20"
    id("org.jetbrains.compose") version "1.12.0"
    id("org.jetbrains.kotlin.plugin.compose") version "2.4.20"
}

val candidateVersion = providers.gradleProperty("nativecmpkitVersion").get()
require(candidateVersion == "0.1.0-preview.1") { "Use the exact staged WebView candidate" }

tasks.register("verifyPublishedWebViewBinding") {
    doLast {
        val group = "io.github.apdelrahman1911.nativecmpkit"
        val module = "nativecmpkit-webview-iossimulatorarm64"
        val staged = file(providers.gradleProperty("nativecmpkitRepository").get())
            .resolve("${group.replace('.', '/')}/$module/$candidateVersion")
            .listFiles()?.single { it.extension == "klib" } ?: error("Missing staged WKWebView KLIB")
        val resolved = configurations.getByName("iosSimulatorArm64CompileKlibraries").incoming.artifacts.artifacts.single {
            val id = it.id.componentIdentifier
            id is ModuleComponentIdentifier && id.group == group && id.module == module && id.version == candidateVersion
        }
        check(Files.mismatch(staged.toPath(), resolved.file.toPath()) == -1L) { "Resolved WKWebView differs from the staged KLIB" }
        println("Independent WKWebView input: $group:$module:$candidateVersion (${staged.length()} bytes)")
    }
}

kotlin {
    jvmToolchain(17)
    iosSimulatorArm64 {
        binaries.framework {
            baseName = "NativeCmpKitWebViewConsumer"
            isStatic = true
        }
    }
    sourceSets.iosSimulatorArm64Main.dependencies {
        implementation("io.github.apdelrahman1911.nativecmpkit:nativecmpkit-webview:$candidateVersion")
        implementation(compose.foundation)
        implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.11.0")
    }
}

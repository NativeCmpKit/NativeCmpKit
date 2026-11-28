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
        val basename = "$module-$candidateVersion"
        val names = setOf("$basename.klib", "$basename-cinterop-nskeyvalueobserving.klib")
        val staged = file(providers.gradleProperty("nativecmpkitRepository").get())
            .resolve("${group.replace('.', '/')}/$module/$candidateVersion")
            .listFiles()?.filter { it.isFile && it.extension == "klib" }?.associateBy { it.name }.orEmpty()
        check(staged.keys == names) { "Expected the staged WKWebView KLIB and its Objective-C interop KLIB, got ${staged.keys}" }
        val resolved = configurations.getByName("iosSimulatorArm64CompileKlibraries").incoming.artifacts.artifacts.filter {
            val id = it.id.componentIdentifier
            id is ModuleComponentIdentifier && id.group == group && id.module == module && id.version == candidateVersion
        }.map { it.file }.toMutableList()
        check(resolved.size == names.size && resolved.all { it.isFile && it.extension == "klib" }) {
            "WKWebView compile resolution must carry both published KLIBs, got ${resolved.map { it.name }}"
        }
        for ((name, stagedKlib) in staged.toSortedMap()) {
            // Gradle can materialize a KLIB under the producer name from module metadata.
            val artifact = resolved.singleOrNull { Files.mismatch(stagedKlib.toPath(), it.toPath()) == -1L }
            checkNotNull(artifact) {
                "Expected a distinct byte-for-byte resolved WKWebView match for $name, got ${resolved.map { it.name }}"
            }
            resolved.remove(artifact)
            println("Independent WKWebView input: $group:$module:$candidateVersion $name (${artifact.length()} bytes, resolved as ${artifact.name})")
        }
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

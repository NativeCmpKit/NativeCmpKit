// Modified for nativeCmpkit migration (2026-10-24): sample identity only.
import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.composeMultiplatform)
    id("desktop.javafx")
}

kotlin {
    jvm {
        compilerOptions {
            jvmTarget.set(JvmTarget.fromTarget(libs.versions.java.get()))
        }
    }

    sourceSets.jvmMain.dependencies {
        implementation(projects.sample.common)
        implementation(projects.nativecmpkitFilePicker)
        implementation(projects.nativecmpkitShare)
        implementation(compose.desktop.currentOs)
    }
}

compose.desktop {
    application {
        mainClass = "io.github.apdelrahman1911.nativecmpkit.sample.desktop.MainKt"
        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
            packageName = "nativeCmpkit"
            packageVersion = "1.0.0"

            macOS {
                jvmArgs(
                    "-Dapple.awt.application.appearance=system",
                )
            }
        }
    }
}

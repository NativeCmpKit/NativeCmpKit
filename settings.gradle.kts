// NativeCmpKit module and sample projects.
rootProject.name = "NativeCmpKit"

pluginManagement {
    includeBuild("convention-plugins")
    repositories {
        google {
            mavenContent {
                releasesOnly()
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    @Suppress("UnstableApiUsage")
    repositories {
        google()
        mavenCentral()
    }
}

// Verification requires an explicitly installed JDK17, not a remote JVM resolver.
// See docs/testing/installed-jdk17-prerequisite.md.

include(
    // Artifact modules
    ":nativecmpkit-core",
    ":nativecmpkit-ui",
    ":nativecmpkit-webview",
    ":nativecmpkit-cupertino-icons",
    ":nativecmpkit-navigation",
    ":nativecmpkit-io",
    ":nativecmpkit-file-picker",
    ":nativecmpkit-file-picker-coil",
    ":nativecmpkit-permissions",
    ":nativecmpkit-permissions:core",
    ":nativecmpkit-permissions:camera",
    ":nativecmpkit-permissions:gallery",
    ":nativecmpkit-permissions:location",
    ":nativecmpkit-permissions:background-location",
    ":nativecmpkit-permissions:bluetooth",
    ":nativecmpkit-permissions:contacts",
    ":nativecmpkit-permissions:calendar",
    ":nativecmpkit-permissions:notifications",
    ":nativecmpkit-permissions:wifi",
    ":nativecmpkit-permissions:microphone",
    ":nativecmpkit-geo",
    ":nativecmpkit-maps",
    ":nativecmpkit-camera-picker",
    ":nativecmpkit-share",
    // Sample modules
    ":sample:android",
    ":sample:desktop",
    ":sample:web-js",
    ":sample:web-wasm",
    ":sample:common",
)

// Rename projects to keep published artifact names unchanged
project(":nativecmpkit-permissions:core").name = "nativecmpkit-permissions-core"
project(":nativecmpkit-permissions:camera").name = "nativecmpkit-permissions-camera"
project(":nativecmpkit-permissions:gallery").name = "nativecmpkit-permissions-gallery"
project(":nativecmpkit-permissions:location").name = "nativecmpkit-permissions-location"
project(":nativecmpkit-permissions:background-location").name = "nativecmpkit-permissions-background-location"
project(":nativecmpkit-permissions:bluetooth").name = "nativecmpkit-permissions-bluetooth"
project(":nativecmpkit-permissions:contacts").name = "nativecmpkit-permissions-contacts"
project(":nativecmpkit-permissions:calendar").name = "nativecmpkit-permissions-calendar"
project(":nativecmpkit-permissions:notifications").name = "nativecmpkit-permissions-notifications"
project(":nativecmpkit-permissions:wifi").name = "nativecmpkit-permissions-wifi"
project(":nativecmpkit-permissions:microphone").name = "nativecmpkit-permissions-microphone"

enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")
enableFeaturePreview("STABLE_CONFIGURATION_CACHE")

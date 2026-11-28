pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}

rootProject.name = "nativecmpkit-webview-android-consumer"

val candidate = File(providers.gradleProperty("nativecmpkitRepository").get())
require(candidate.isAbsolute && candidate.isDirectory)

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        exclusiveContent {
            forRepository { maven { url = candidate.toURI() } }
            filter { includeGroup("io.github.apdelrahman1911.nativecmpkit") }
        }
        google()
        mavenCentral()
    }
}

// Disposable source-only API33/34/35 test host; no repository publication.
pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
    versionCatalogs { create("libs") { from(files("../../../gradle/libs.versions.toml")) } }
}
rootProject.name = "nativecmpkit-owned-android-permission-demo"
includeBuild("../../..") {
    dependencySubstitution {
        substitute(module("verification.nativecmpkit:unpublished-permission-core"))
            .using(project(":nativecmpkit-permissions:nativecmpkit-permissions-core"))
        substitute(module("verification.nativecmpkit:unpublished-permission-gallery"))
            .using(project(":nativecmpkit-permissions:nativecmpkit-permissions-gallery"))
        substitute(module("verification.nativecmpkit:unpublished-permission-microphone"))
            .using(project(":nativecmpkit-permissions:nativecmpkit-permissions-microphone"))
        substitute(module("verification.nativecmpkit:unpublished-picker"))
            .using(project(":nativecmpkit-file-picker"))
    }
}

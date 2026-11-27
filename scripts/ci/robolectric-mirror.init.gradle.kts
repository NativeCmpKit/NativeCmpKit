// SPDX-License-Identifier: Apache-2.0
// Used only by the hosted Android host-test lane after it verifies both downloaded files.
import org.gradle.api.tasks.testing.Test

gradle.settingsEvaluated {
    if (rootProject.name == "NativeCmpKit") {
        val repositories = dependencyResolutionManagement.repositories
        val mirror = settingsDir.resolve("build/ci-identity/robolectric-repo")
        check(mirror.isDirectory) { "Verified local Robolectric inputs are required" }
        repositories.exclusiveContent {
            forRepository {
                repositories.maven {
                    name = "NativeCmpKitVerifiedRobolectric"
                    url = mirror.toURI()
                    metadataSources {
                        mavenPom()
                        ignoreGradleMetadataRedirection()
                    }
                }
            }
            filter {
                includeVersion("org.robolectric", "nativeruntime-dist-compat", "1.0.18")
            }
        }
    }
}

// Robolectric fetches the SDK runtime JARs separately from Gradle resolution.
gradle.beforeProject {
    tasks.withType<Test>().matching { it.name == "testAndroidHostTest" }.configureEach {
        systemProperty("robolectric.dependency.repo.id", "google-maven-central")
        systemProperty("robolectric.dependency.repo.url", "https://maven-central.storage-download.googleapis.com/maven2/")
    }
}

// SPDX-License-Identifier: Apache-2.0
// Used only by the hosted Android host-test lane after it verifies both downloaded files.
gradle.settingsEvaluated {
    val repositories = dependencyResolutionManagement.repositories
    val mirror = settingsDir.resolve("build/ci-identity/robolectric-repo")
    if (settingsDir.canonicalFile == gradle.startParameter.currentDir.canonicalFile) {
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

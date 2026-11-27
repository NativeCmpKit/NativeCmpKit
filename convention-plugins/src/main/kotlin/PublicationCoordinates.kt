import groovy.json.JsonSlurper
import org.gradle.api.Project
import org.gradle.api.publish.tasks.GenerateModuleMetadata
import org.gradle.kotlin.dsl.withType

/** Check KGP's metadata, including redirects for targets unavailable on the current host. */
fun Project.configureIndependentPublicationCoordinates() {
    val coordinates = IndependentPublicationCoordinates(name, group.toString(), version.toString())
    tasks.withType<GenerateModuleMetadata>().configureEach {
        inputs.property("nativecmpkitIndependentCoordinateSchema", 2)
        inputs.property("nativecmpkitIndependentCoordinates", coordinates.targets)
        inputs.property("nativecmpkitIndependentCoordinateGroup", coordinates.group)
        inputs.property("nativecmpkitIndependentCoordinateVersion", coordinates.version)
        doLast {
            val document = JsonSlurper().parse(outputFile.get().asFile, "UTF-8") as Map<*, *>
            coordinates.validate(document)
        }
    }
}

internal class IndependentPublicationCoordinates(
    private val base: String,
    val group: String,
    val version: String,
) {
    val targets = listOf("android", "desktop", "js", "wasm-js", "iosarm64", "iossimulatorarm64")
        .map { "$base-$it" }.toSet()

    fun validate(document: Map<*, *>) {
        check(document["formatVersion"] == "1.1") { "Review the new Gradle metadata format before publishing" }
        val component = document["component"] as Map<*, *>
        check(component["group"] == group && component["version"] == version) {
            "Unexpected NativeCmpKit owning component coordinates"
        }
        check(component["module"] == base || component["module"] in targets) {
            "Unexpected NativeCmpKit owning component identity"
        }
        for (variant in document["variants"] as List<*>) {
            val redirect = (variant as Map<*, *>)["available-at"] as? Map<*, *> ?: continue
            check(redirect["group"] == group && redirect["version"] == version) {
                "Foreign NativeCmpKit target redirect"
            }
            val module = redirect["module"]
            check(module in targets) { "Unknown NativeCmpKit target redirect: $module" }
            check(redirect["url"] == "../../$module/$version/$module-$version.module") {
                "Unexpected NativeCmpKit target metadata URL"
            }
        }
    }
}

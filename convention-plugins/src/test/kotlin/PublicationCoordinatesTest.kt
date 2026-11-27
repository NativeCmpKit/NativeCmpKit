import groovy.json.JsonOutput
import org.junit.Assert.*
import org.junit.Test

/** Actual owning Kotlin validator; synthetic metadata, not consumer/native execution. */
class PublicationCoordinatesTest {
    private val group = "io.github.apdelrahman1911.nativecmpkit"
    private val version = "0.1.0-preview.1"
    private val schema = IndependentPublicationCoordinates("nativecmpkit-webview", group, version)

    private fun redirect(module: String) = mutableMapOf<String, Any>(
        "group" to group, "module" to module, "version" to version,
        "url" to "../../$module/$version/$module-$version.module",
    )

    private fun document(vararg modules: String) = mutableMapOf<String, Any>(
        "formatVersion" to "1.1",
        "component" to mutableMapOf("group" to group, "module" to "nativecmpkit-webview", "version" to version),
        "createdBy" to mapOf("gradle" to mapOf("version" to "9.7.1")),
        "variants" to modules.map { mutableMapOf<String, Any>("name" to "$it-published", "available-at" to redirect(it)) },
    )

    @Test fun unavailableAppleTargetsUseTheSameCoordinatesWithoutRewritingMetadata() {
        val actual = document("nativecmpkit-webview-iosarm64", "nativecmpkit-webview-iossimulatorarm64")
        val original = JsonOutput.toJson(actual)
        schema.validate(actual)
        assertEquals(original, JsonOutput.toJson(actual))
    }

    @Test fun foreignUnknownVersionAndUrlAliasesFailClosed() {
        for ((key, bad) in listOf("group" to "example.foreign", "version" to "0.1.0-preview.2",
                "module" to "nativecmpkit-webview-iosx64", "url" to "../../foreign/metadata.module")) {
            val actual = document("nativecmpkit-webview-iosarm64")
            @Suppress("UNCHECKED_CAST")
            val target = ((actual["variants"] as List<*>).first() as Map<*, *>)["available-at"] as MutableMap<String, Any>
            target[key] = bad
            assertThrows("$key must reject rather than guess", IllegalStateException::class.java) { schema.validate(actual) }
        }
    }

    @Test fun changedFormatOrOwningComponentRequiresExplicitReview() {
        val format = document("nativecmpkit-webview-iosarm64")
        format["formatVersion"] = "99.0"
        assertThrows(IllegalStateException::class.java) { schema.validate(format) }
        val root = document("nativecmpkit-webview-iosarm64")
        @Suppress("UNCHECKED_CAST")
        val component = root["component"] as MutableMap<String, Any>
        component["module"] = "foreign-webview"
        assertThrows(IllegalStateException::class.java) { schema.validate(root) }
    }

    @Test fun allSixDeclaredTargetNamesAreAccepted() {
        val suffixes = listOf("android", "desktop", "js", "wasm-js", "iosarm64", "iossimulatorarm64")
        val names = suffixes.map { "nativecmpkit-webview-$it" }
        assertEquals(names.toSet(), schema.targets)
        schema.validate(document(*names.toTypedArray()))
    }
}

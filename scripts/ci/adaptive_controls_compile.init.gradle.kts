import org.gradle.api.file.ConfigurableFileCollection
import org.gradle.api.file.FileCollection
import org.gradle.api.tasks.testing.Test
import groovy.json.JsonOutput
import java.security.MessageDigest

// Independent opt-in compiler selection only; no ordinary source-set/routing/policy change.
gradle.projectsEvaluated {
    val project = rootProject.findProject(":nativecmpkit-ui") ?: return@projectsEvaluated
    val desktopClass = "io.github.apdelrahman1911.nativecmpkit.ui.toggle.CupertinoSwitchThumbContentColorTest"
    val desktopMethods = listOf(
        "currentCallerIconColorsFollowEveryStateAndDoNotLeakToSiblingContent",
        "disabledCustomThumbInDarkLargeTextActuallyDrawsTheSuppliedIconColor",
    )
    val desktopRequest = listOf(":nativecmpkit-ui:desktopTest") + desktopMethods.flatMap { listOf("--tests", "$desktopClass.$it") }
    val desktop = gradle.startParameter.taskNames == desktopRequest
    val paths: List<String>
    val taskName: String
    if (desktop) {
        paths = listOf("nativecmpkit-ui/src/desktopTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toggle/CupertinoSwitchThumbContentColorTest.kt")
        taskName = "compileTestKotlinDesktop"
        project.tasks.withType<Test>().matching { it.name == "desktopTest" }.configureEach {
            doFirst {
                check(filter.includePatterns.isEmpty() && filter.excludePatterns.isEmpty())
                // Inspected Gradle9.7.1 keeps --tests separately from configured includePatterns.
                @Suppress("UNCHECKED_CAST")
                val commandLine = filter.javaClass.getMethod("getCommandLineIncludePatterns").invoke(filter) as Set<String>
                check(commandLine == desktopMethods.map { "$desktopClass.$it" }.toSet())
                check(filter.isFailOnNoMatchingTests && !ignoreFailures && maxParallelForks == 1)
            }
        }
    } else {
        check(gradle.startParameter.taskNames == listOf(":nativecmpkit-ui:compileTestKotlinIosSimulatorArm64")) {
            "Adaptive controls compiler accepts only its exact Desktop2 or iOS test compiler; no default/full native execution"
        }
        paths = listOf(
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlNativeHost.kt",
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/slider/AdaptiveSliderNativeMatrixTest.kt",
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/controls/AdaptiveControlCustomizationMatrixTest.kt",
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/toolbar/AdaptiveToolbarFallbackNativeTest.kt",
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt",
            "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt",
        )
        taskName = "compileTestKotlinIosSimulatorArm64"
    }
    val files = paths.map { relative ->
        val file = rootProject.file(relative)
        check(file.isFile && file.absoluteFile == file.canonicalFile &&
            file.toPath().startsWith(rootProject.projectDir.canonicalFile.toPath())) {
            "Only exact ordinary authored test inputs may be compiled"
        }
        file.canonicalFile
    }
    val compilation = project.tasks.getByName(taskName)
    compilation.javaClass.getMethod("setSource", Array<Any>::class.java).invoke(compilation, files.toTypedArray() as Any)
    // KGP's native compiler exposes public commonSources; its JVM KotlinCompile does not.
    // The JVM path is admitted by its exact public source collection, not guessed reflection.
    val common = if (desktop) null else
        compilation.javaClass.getMethod("getCommonSources").invoke(compilation) as ConfigurableFileCollection
    common?.setFrom(emptyList<Any>())
    val actual = compilation.javaClass.getMethod("getSources").invoke(compilation) as FileCollection
    check(actual.files.map { it.canonicalFile }.toSet() == files.toSet() && common?.files.orEmpty().isEmpty())
    compilation.doFirst {
        check(actual.files.map { it.canonicalFile }.toSet() == files.toSet() && common?.files.orEmpty().isEmpty())
        val hashes = paths.zip(files).associate { (relative, file) ->
            relative to MessageDigest.getInstance("SHA-256").digest(file.readBytes())
                .joinToString("") { "%02x".format(it.toInt() and 255) }
        }
        val receipt = rootProject.file("build/ci-verification/adaptive-controls-focused-compilation.json")
        receipt.parentFile.mkdirs()
        receipt.writeText(JsonOutput.prettyPrint(JsonOutput.toJson(mapOf(
            "task" to compilation.path, "effective_sources" to paths, "source_sha256" to hashes,
            "excluded_unrelated_test_sources" to true, "production_source_sets_changed" to false,
            "native_tests_executed" to 0,
            "scope" to "Precompiler admission only; process exit and fresh XML decide results",
        ))) + "\n")
        logger.lifecycle("NATIVECMPKIT_ADAPTIVE_FOCUSED_COMPILE sources=${paths.size} nativeTestsExecuted=0")
    }
}

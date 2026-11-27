import org.gradle.api.file.ConfigurableFileCollection
import org.gradle.api.file.FileCollection
import groovy.json.JsonOutput
import java.security.MessageDigest

// Explicit three-case lifecycle invocation only. Keep production, dependency
// graphs and the ordinary/full test source sets unchanged. Native tests still
// execute freshly with the original application host, Worker and JUnit parser.
gradle.projectsEvaluated {
    // Init scripts also visit convention/included builds. They do not own UI's
    // compilation and must not reject their independent plugin-resolution tasks.
    val project = rootProject.findProject(":nativecmpkit-ui") ?: return@projectsEvaluated
    // Gradle retains task-specific --tests options in startParameter.taskNames.
    // Admit the exact authored selection, not arbitrary options or wildcards.
    val applicationRequest = listOf(":nativecmpkit-ui:iosSimulatorArm64ApplicationTest") + listOf(
        "publicCompositionDisposalDuringNativeHideReleasesContentAndCanReopen",
        "hoistedStateReattachesToANewRealPresenterAndStaleOwnersCannotDetachItsReplacement",
        "repeatedDisposalDuringBothNativeAnimationsLeavesNoWaiterOrCapturedContent",
    ).flatMap { method -> listOf("--tests", "io.github.apdelrahman1911.nativecmpkit.ui.internal.NativeModalLifecycleReplacementTest.$method") }
    val memoryRecoveryRequest = listOf(":nativecmpkit-ui:iosSimulatorArm64ApplicationTest") + listOf(
        "publicCompositionDisposalDuringNativeHideReleasesContentAndCanReopen",
        "repeatedDisposalDuringBothNativeAnimationsLeavesNoWaiterOrCapturedContent",
    ).flatMap { method -> listOf("--tests", "io.github.apdelrahman1911.nativecmpkit.ui.internal.NativeModalLifecycleReplacementTest.$method") }
    val permittedTasks = setOf(
        listOf(":nativecmpkit-ui:compileTestKotlinIosSimulatorArm64"),
        listOf(":nativecmpkit-ui:iosSimulatorArm64ApplicationTest"),
        applicationRequest,
        memoryRecoveryRequest,
    )
    check(gradle.startParameter.taskNames in permittedTasks) {
        "Focused modal compilation accepts only its exact test compiler or application task"
    }
    val paths = listOf(
        "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeModalLifecycleReplacementTest.kt",
        "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeUiApplicationHost.kt",
        "nativecmpkit-ui/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/ui/internal/NativeObjectIdentity.kt",
    )
    val files = paths.map { relative ->
        val file = rootProject.file(relative)
        check(file.isFile && file.absoluteFile == file.canonicalFile &&
            file.canonicalFile.toPath().startsWith(rootProject.projectDir.canonicalFile.toPath())) {
            "Only the ordinary exact three focused Kotlin sources may be compiled"
        }
        file.canonicalFile
    }
    val compilation = project.tasks.getByName("compileTestKotlinIosSimulatorArm64")
    // Init scripts do not share the later KGP classpath. These are the public
    // source APIs inspected on KGP2.4.20, not replacement compiler internals.
    compilation.javaClass.getMethod("setSource", Array<Any>::class.java)
        .invoke(compilation, files.toTypedArray() as Any)
    val common = compilation.javaClass.getMethod("getCommonSources").invoke(compilation) as ConfigurableFileCollection
    common.setFrom(emptyList<Any>())
    val actual = compilation.javaClass.getMethod("getSources").invoke(compilation) as FileCollection
    check(actual.files.map { it.canonicalFile }.toSet() == files.toSet() && common.files.isEmpty()) {
        "Effective focused test sources differ from the exact three-file compilation"
    }
    compilation.doFirst {
        check(actual.files.map { it.canonicalFile }.toSet() == files.toSet() && common.files.isEmpty()) {
            "Effective focused test sources changed before the native compiler"
        }
        val hashes = paths.zip(files).associate { (relative, file) ->
            relative to MessageDigest.getInstance("SHA-256").digest(file.readBytes())
                .joinToString("") { "%02x".format(it.toInt() and 255) }
        }
        val receipt = rootProject.file("build/ci-verification/ios-focused-compilation.json")
        receipt.parentFile.mkdirs()
        receipt.writeText(JsonOutput.prettyPrint(JsonOutput.toJson(mapOf(
            "task" to compilation.path,
            "focus" to "ui-native-modal-lifecycle-replacement",
            "source_sha256" to hashes,
            "effective_sources" to paths,
            "excluded_unrelated_test_sources" to true,
            "production_source_sets_changed" to false,
            "native_tests_executed" to 0,
            "scope" to "Actual precompiler source admission only; compiler exit and fresh native XML decide outcomes",
        ))) + "\n")
        logger.lifecycle("NATIVECMPKIT_UI_FOCUSED_COMPILE sources=3 nativeTestsExecuted=0 productionChanged=false")
    }
}

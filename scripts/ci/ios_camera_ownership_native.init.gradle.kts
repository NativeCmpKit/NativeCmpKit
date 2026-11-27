import org.gradle.api.file.ConfigurableFileCollection
import org.gradle.api.file.FileCollection
import groovy.json.JsonOutput
import java.security.MessageDigest

// Exact three-source Camera KLIB/native-task admission, not a native result.
// The compiler or an exact application selection uses these same three sources.
gradle.projectsEvaluated {
    val project = rootProject.findProject(":nativecmpkit-camera-picker") ?: return@projectsEvaluated
    val focus = rootProject.providers.gradleProperty("nativecmpkitCameraIosFocus").orNull
    val fullFocus = "ios-camera-ownership-memory-callback"
    val disposalFocus = "ios-camera-ownership-memory-callback-disposal"
    check(focus == fullFocus || focus == disposalFocus) { "Explicit exact Camera ownership focus is required" }
    val prefix = "io.github.apdelrahman1911.nativecmpkit.camerapicker.IosCameraOwnershipAcceptanceTest."
    val disposalMethod = "compositionDisposalDuringObservedPresentingAndPresentedPhasesFinishesOwnedTeardown"
    val fullMethods = listOf(
        "publicOwnerSurvivesOrdinaryRecompositionAndNativeGcAndDeliversToLatestCallback",
        "doubleLaunchDuplicateTerminalInputAndReentrantReplacementKeepOneNativeOwner",
        disposalMethod,
        "actualSimulatorUnavailableAndCompetingModalOutcomesPreserveForeignPresenter",
        "controlledOriginalNativeImageWritesRealPngAndJpegAndSuccessOutlivesOwner",
    )
    val methods = (if (focus == fullFocus) fullMethods else listOf(disposalMethod)).map { prefix + it }
    val compilerRequest = listOf(":nativecmpkit-camera-picker:compileTestKotlinIosSimulatorArm64")
    val applicationRequest = listOf(":nativecmpkit-camera-picker:iosSimulatorArm64ApplicationTest") +
        methods.flatMap { listOf("--tests", it) }
    check(gradle.startParameter.taskNames in setOf(compilerRequest, applicationRequest)) {
        "Camera requires its exact three-input compiler or selected application test task"
    }
    val nativeTaskRequested = gradle.startParameter.taskNames == applicationRequest
    val simulator = rootProject.providers.gradleProperty("nativecmpkitSimulatorDevice").orNull
    if (nativeTaskRequested) {
        check(System.getProperty("os.name") == "Mac OS X" && System.getProperty("os.arch") in setOf("aarch64", "arm64")) {
            "Actual Camera native execution requires the Arm64 Apple host; Linux KLIB is not native evidence"
        }
        check(simulator != null && Regex("[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}").matches(simulator)) {
            "Camera native task requires the same explicit recorded simulator as the original transport"
        }
    }
    val paths = listOf(
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/IosCameraOwnershipAcceptanceTest.kt",
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraApplicationHost.kt",
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraObjectIdentity.kt",
    )
    val expectedHashes = mapOf(
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/IosCameraOwnershipAcceptanceTest.kt" to "1cc490b60054c619fceb6ec42c65cc9067e8beb2822f1859b1d754e3aefb250d",
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraApplicationHost.kt" to "fc6ddb7e7531ef9500388fceaeda04a4aa346f4a9c7601b13c67593c9c8352c5",
        "nativecmpkit-camera-picker/src/iosTest/kotlin/io/github/apdelrahman1911/nativecmpkit/camerapicker/internal/NativeCameraObjectIdentity.kt" to "77ef5f5037b621f1c6cfe4c92c9d469bdbd3d56ba7318632106c2907c9234379",
    )
    val files = paths.map { relative ->
        val file = rootProject.file(relative)
        check(file.isFile && file.absoluteFile == file.canonicalFile &&
            file.toPath().startsWith(rootProject.projectDir.canonicalFile.toPath())) {
            "Only the exact three ordinary Camera authored test/host/identity inputs may be compiled"
        }
        file.canonicalFile
    }
    fun hashes(): Map<String, String> = paths.zip(files).associate { (relative, file) ->
        relative to MessageDigest.getInstance("SHA-256").digest(file.readBytes())
            .joinToString("") { "%02x".format(it.toInt() and 255) }
    }
    val compilation = project.tasks.getByName("compileTestKotlinIosSimulatorArm64")
    compilation.inputs.property("nativecmpkitCameraIosFocus", focus!!)
    // Public KGP source APIs; no replacement compiler or production-source edits.
    compilation.javaClass.getMethod("setSource", Array<Any>::class.java)
        .invoke(compilation, files.toTypedArray() as Any)
    val common = compilation.javaClass.getMethod("getCommonSources").invoke(compilation) as ConfigurableFileCollection
    common.setFrom(emptyList<Any>())
    val actual = compilation.javaClass.getMethod("getSources").invoke(compilation) as FileCollection
    fun verifySources() {
        check(actual.files.map { it.canonicalFile }.toSet() == files.toSet() && common.files.isEmpty() && hashes() == expectedHashes) {
            "Camera effective compiler sources/hashes differ from exact three; common/accepted/foreign inputs forbidden"
        }
    }
    verifySources()
    fun admit(task: String, nativeTask: Boolean) {
        verifySources()
        check(rootProject.providers.gradleProperty("nativecmpkitCameraIosFocus").orNull == focus)
        if (nativeTask) check(gradle.startParameter.taskNames == applicationRequest &&
            rootProject.providers.gradleProperty("nativecmpkitSimulatorDevice").orNull == simulator)
        val receipt = rootProject.file(if (nativeTask)
            "build/ci-verification/camera-ios-native-source-admission.json"
            else "build/ci-verification/camera-ios-precompiler-source-admission.json")
        receipt.parentFile.mkdirs()
        receipt.writeText(JsonOutput.prettyPrint(JsonOutput.toJson(mapOf(
            "schema_version" to 1, "task" to task, "focus" to focus,
            "phase" to if (nativeTask) "native-task-source-admission" else "precompiler-source-admission",
            "selected_methods" to methods, "effective_sources" to paths, "common_sources" to emptyList<String>(),
            "source_sha256" to hashes(), "excluded_unrelated_test_sources" to true,
            "production_source_sets_changed" to false, "compiler_executions_attested" to 0,
            "apple_links_attested" to 0, "native_tests_executed" to 0,
            "scope" to "Source/selection admission only; compiler result and fresh native XML/runtime/cleanup decide results",
        ))) + "\n")
        logger.lifecycle("NATIVECMPKIT_CAMERA_SOURCE_ADMISSION methods=${methods.size} sources=3 common=0 nativeTestsExecuted=0")
    }
    compilation.doFirst { admit(compilation.path, false) }
    // Always a fresh admission before the native task, even if its exact unchanged
    // compiler/link prerequisites are legitimately UP-TO-DATE; never relabel them.
    project.tasks.getByName("iosSimulatorArm64ApplicationTest").doFirst { admit(path, true) }
}

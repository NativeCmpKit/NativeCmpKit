import org.gradle.api.tasks.Copy

// Explicit negative fixture only; never part of ordinary verification. The
// caller copies the public source MimeTypes.properties to this generated file
// first. Equal bytes from a DIFFERENT originating path must still be rejected.
allprojects {
    if (path == ":nativecmpkit-file-picker") {
        tasks.withType<Copy>().matching { it.name == "desktopProcessResources" }.configureEach {
            from(rootProject.layout.buildDirectory.file("resource-copy-probe/MimeTypes.properties")) {
                into("io/github/apdelrahman1911/nativecmpkit/picker/internal/jodd/net")
            }
        }
    }
}

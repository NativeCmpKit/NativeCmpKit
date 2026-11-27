package io.github.apdelrahman1911.nativecmpkit.core

@RequiresOptIn(
    level = RequiresOptIn.Level.ERROR,
    message = "This is an experimental API for NativeCmpKit and is likely to change before becoming " +
            "stable."
)
@Target(
    AnnotationTarget.CLASS,
    AnnotationTarget.FUNCTION,
    AnnotationTarget.PROPERTY,
    AnnotationTarget.PROPERTY_GETTER
)
@Retention(AnnotationRetention.BINARY)
annotation class ExperimentalNativeCmpKitApi

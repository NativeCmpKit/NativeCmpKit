package io.github.apdelrahman1911.nativecmpkit.core

@RequiresOptIn(
    level = RequiresOptIn.Level.ERROR,
    message = "This is internal API for NativeCmpKit modules that may change frequently " +
            "and without warning."
)
@Target(
    AnnotationTarget.CLASS,
    AnnotationTarget.FUNCTION,
    AnnotationTarget.PROPERTY,
    AnnotationTarget.CONSTRUCTOR
)
@Retention(AnnotationRetention.BINARY)
annotation class InternalNativeCmpKitApi

// SPDX-License-Identifier: Apache-2.0
package io.github.apdelrahman1911.nativecmpkit.ui.web

import org.junit.runner.Description
import org.junit.runner.manipulation.Filter

/** One lossless AndroidJUnitRunner filter; no native method/body or dependency changes. */
class AndroidContentPolicyVerificationFilter : Filter() {
    override fun shouldRun(description: Description): Boolean {
        if (!description.isTest) return description.children.any { shouldRun(it) }
        return when (description.className) {
            "io.github.apdelrahman1911.nativecmpkit.ui.web.AndroidWebViewContentPolicyAcceptanceTest" -> when (description.methodName) {
                "savedRemainingStatesRemountWithoutBlankTitleOrFalseHistory",
                "documentedGetReplayAndNonSaveablePostOneTimeOptOutAreObserved",
                "initialHeadersRedirectsAndSubresourcesMatchStateAndNavigatorPolicy",
                "relativeResourcesPreserveSupportedUnicodeEncoding" -> true
                else -> false
            }
            "io.github.apdelrahman1911.nativecmpkit.ui.web.AndroidWebViewLifetimeDeviceTest" ->
                description.methodName == "retainedStateReleasesRepeatedRealActivitiesAndViewsAndRestoresSerializedNativeState"
            else -> false
        }
    }

    override fun describe(): String = "NativeCmpKit content-policy NEW4 plus affected saver1 only"
}

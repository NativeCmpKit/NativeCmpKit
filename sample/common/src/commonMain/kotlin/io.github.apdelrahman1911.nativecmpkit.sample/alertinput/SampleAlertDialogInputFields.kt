// SPDX-License-Identifier: Apache-2.0
// Original Calf authors (MohamedRejeb/Calf); preserved LICENSE/NOTICE govern this extraction.
// Source extracted from the attributed NativeCmpKit sample; descriptor/callback bytes preserved.
// Modified for NativeCmpKit (2026-11-01): isolated test-only source seam; no sample app substitute.
package io.github.apdelrahman1911.nativecmpkit.sample.alertinput

import io.github.apdelrahman1911.nativecmpkit.ui.dialog.uikit.AlertDialogIosTextField
import io.github.apdelrahman1911.nativecmpkit.ui.uikit.IosKeyboardType

/** The unchanged two native alert input descriptors used by the real sample screen. */
internal fun sampleAlertDialogInputFields(): List<AlertDialogIosTextField> = listOf(
                AlertDialogIosTextField(
                    placeholder = "Enter your name",
                    initialValue = "John Doe",
                    keyboardType = IosKeyboardType.EmailAddress,
                    isSecure = false,
                    onValueChange = {
                        // Demonstration only: do not log or persist personal input.
                    }
                ),
                AlertDialogIosTextField(
                    placeholder = "Enter your password",
                    keyboardType = IosKeyboardType.NumberPad,
                    initialValue = "",
                    isSecure = true,
                    onValueChange = {
                        // Secure input must never be written to logs or retained by this demo.
                    }
                ),
            )

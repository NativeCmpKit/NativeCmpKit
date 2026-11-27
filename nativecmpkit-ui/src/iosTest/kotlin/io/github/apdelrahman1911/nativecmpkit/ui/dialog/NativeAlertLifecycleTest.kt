@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class, io.github.apdelrahman1911.nativecmpkit.core.InternalNativeCmpKitApi::class,
    androidx.compose.ui.test.ExperimentalTestApi::class)

package io.github.apdelrahman1911.nativecmpkit.ui.dialog

import io.github.apdelrahman1911.nativecmpkit.ui.internal.runApplicationUiTest
import androidx.compose.ui.uikit.LocalUIViewController
import androidx.compose.ui.window.DialogProperties
import io.github.apdelrahman1911.nativecmpkit.ui.dialog.uikit.*
import io.github.apdelrahman1911.nativecmpkit.ui.internal.requireOwnedApplicationWindow
import io.github.apdelrahman1911.nativecmpkit.ui.internal.sameNativeObject
import io.github.apdelrahman1911.nativecmpkit.ui.internal.waitForNative
import platform.UIKit.*
import kotlin.test.*

class NativeAlertLifecycleTest {
    @Test fun emptyTextIsOmittedOnPresentationAndOnVisibleUpdates() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        val empty = AlertDialogIosProperties(animated = false)
        lateinit var manager: AlertDialogManager
        runOnIdle {
            manager = AlertDialogManager(parent, {}, empty, DialogProperties())
            manager.showAlertDialog()
        }
        try {
            waitForNative { parent.presentedViewController is UIAlertController }
            runOnIdle {
                val alert = parent.presentedViewController as UIAlertController
                assertNull(alert.title)
                assertNull(alert.message)
                manager.iosProperties = empty.copy(title = "Title", text = "Message")
                manager.updateDialogProperties()
                assertEquals("Title", alert.title)
                assertEquals("Message", alert.message)
                manager.iosProperties = empty
                manager.updateDialogProperties()
                assertNull(alert.title)
                assertNull(alert.message)
            }
        } finally {
            runOnIdle { manager.dispose() }
        }
        waitForNative { parent.presentedViewController == null }
    }

    @Test fun presentedAlertUsesLatestActionAndTextFieldCallbacks() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        var oldAction = 0
        var newAction = 0
        var oldField = 0
        var newField = 0
        var dismissals = 0
        lateinit var manager: AlertDialogManager
        val first = AlertDialogIosProperties(animated = false,
            actions = listOf(AlertDialogIosAction("Save", AlertDialogIosActionStyle.Default, { oldAction++ })),
            textFields = listOf(AlertDialogIosTextField(onValueChange = { oldField++ })))
        runOnIdle {
            manager = AlertDialogManager(parent, { dismissals++ }, first, DialogProperties())
            manager.showAlertDialog()
        }
        try {
            waitForNative { parent.presentedViewController is UIAlertController }
            runOnIdle {
                manager.iosProperties = first.copy(
                    actions = listOf(AlertDialogIosAction("Save", AlertDialogIosActionStyle.Default, { newAction++ })),
                    textFields = listOf(AlertDialogIosTextField(onValueChange = { newField++ })))
                manager.updateDialogProperties()
                val alert = parent.presentedViewController as UIAlertController
                val field = alert.textFields?.first() as UITextField
                field.text = "Changed"
                field.sendActionsForControlEvents(UIControlEventEditingChanged)
                // Exercises the production native action dispatch entrypoint, not synthesized touch.
                manager.activateAction(0)
                manager.activateAction(0)
                assertEquals(0, oldAction)
                assertEquals(1, newAction)
                assertEquals(0, oldField)
                assertEquals(1, newField)
            }
            waitForNative { parent.presentedViewController == null }
            assertEquals(0, dismissals)
        } finally { runOnIdle { manager.dispose() } }
    }

    @Test fun disposalDuringPresentationQueuesCleanupAndReplacement() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        var dismissals = 0
        lateinit var first: AlertDialogManager
        lateinit var second: AlertDialogManager
        runOnIdle {
            first = AlertDialogManager(parent, { dismissals++ }, AlertDialogIosProperties(title = "First"), DialogProperties())
            first.showAlertDialog()
            first.dispose()
            second = AlertDialogManager(parent, { dismissals++ }, AlertDialogIosProperties(title = "Second", animated = false), DialogProperties())
            second.showAlertDialog()
        }
        try {
            waitForNative { (parent.presentedViewController as? UIAlertController)?.title == "Second" }
            runOnIdle { second.dispose() }
            waitForNative { parent.presentedViewController == null }
            assertEquals(0, dismissals)
        } finally { runOnIdle { first.dispose(); second.dispose() } }
    }

    @Test fun outsideDismissRequestsAndDisposalRemainExactlyOnce() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        var dismissals = 0
        var first: AlertDialogManager? = null
        var second: AlertDialogManager? = null
        try {
            runOnIdle {
                first = AlertDialogManager(parent, { dismissals++ },
                    AlertDialogIosProperties(title = "Dismiss once", animated = false), DialogProperties())
                    .also { it.showAlertDialog() }
            }
            waitForNative { (parent.presentedViewController as? UIAlertController)?.title == "Dismiss once" }
            runOnIdle {
                // Actual production Objective-C action entrypoint, not a
                // synthesized outside touch or proof of native gesture delivery.
                first?.dismiss(); first?.dismiss()
            }
            waitForNative { parent.presentedViewController == null }
            runOnIdle {
                assertEquals(1, dismissals)
                first?.dispose()
                first?.dismiss()
                first?.showAlertDialog() // A terminal owner cannot reopen.
                assertNull(parent.presentedViewController)
                assertEquals(1, dismissals)
                second = AlertDialogManager(parent, { dismissals++ },
                    AlertDialogIosProperties(title = "Replacement", animated = false), DialogProperties())
                    .also { it.showAlertDialog() }
            }
            waitForNative { (parent.presentedViewController as? UIAlertController)?.title == "Replacement" }
            runOnIdle { second?.dispose() }
            waitForNative { parent.presentedViewController == null }
            runOnIdle { assertEquals(1, dismissals) }
        } finally { runOnIdle { first?.dispose(); second?.dispose() } }
    }

    @Test fun actionSheetHasAPresentingViewPopoverAnchor() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        lateinit var manager: AlertDialogManager
        runOnIdle {
            manager = AlertDialogManager(parent, {}, AlertDialogIosProperties(animated = false,
                style = AlertDialogIosStyle.ActionSheet), DialogProperties())
            manager.popoverAnchor = AlertDialogIosPopoverAnchor.ViewRect(null)
            manager.showAlertDialog()
        }
        try {
            waitForNative { parent.presentedViewController is UIAlertController }
            runOnIdle {
                val popover = requireNotNull((parent.presentedViewController as UIAlertController).popoverPresentationController)
                assertEquals(parent.view, popover.sourceView)
                assertNotNull(popover.delegate) // Supported ActionSheet ownership, never Alert's delegate.
            }
        } finally { runOnIdle { manager.dispose() } }
        waitForNative { parent.presentedViewController == null }
    }

    @Test fun defaultActionSheetKeepsIPhoneCancelAndAnchorsIPad() = runApplicationUiTest {
        lateinit var parent: UIViewController
        setContent { parent = LocalUIViewController.current }
        val isPhone = runOnIdle { UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiomPhone }
        var manager: AlertDialogManager? = null
        var cancels = 0
        var dismissals = 0
        var confirms = 0
        val cancelTitle = "Cancel selection"
        try {
            runOnIdle {
                manager = AlertDialogManager(parent, { dismissals++ }, AlertDialogIosProperties(
                    title = "Choose a value",
                    animated = false,
                    style = AlertDialogIosStyle.ActionSheet,
                    actions = listOf(
                        AlertDialogIosAction("Confirm selection", AlertDialogIosActionStyle.Default, { confirms++ }),
                        AlertDialogIosAction(cancelTitle, AlertDialogIosActionStyle.Cancel, { cancels++ }),
                    ),
                ), DialogProperties()).also { it.showAlertDialog() }
            }
            waitForNative {
                val alert = parent.presentedViewController as? UIAlertController
                alert != null && alert.title == "Choose a value" &&
                    sameNativeObject(alert.view.window, requireOwnedApplicationWindow())
            }
            val sheet = runOnIdle { parent.presentedViewController as UIAlertController }
            runOnIdle {
                assertEquals(UIAlertControllerStyleActionSheet, sheet.preferredStyle)
                if (isPhone) {
                    val window = requireOwnedApplicationWindow()
                    val cancel = sheet.view.visibleDescendants().single {
                        it.accessibilityLabel == cancelTitle &&
                            (it.accessibilityTraits and UIAccessibilityTraitButton) != 0UL && sameNativeObject(it.window, window)
                    }
                    assertTrue(cancel.accessibilityActivate(), "The visible UIKit Cancel button must accept input")
                } else {
                    val popover = requireNotNull(sheet.popoverPresentationController)
                    assertTrue(sameNativeObject(parent.view, popover.sourceView))
                    assertNull(popover.barButtonItem)
                    manager?.dispose()
                }
            }
            waitForNative { parent.presentedViewController == null && sheet.view.window == null }
            runOnIdle {
                assertEquals(if (isPhone) 1 else 0, cancels)
                assertEquals(0, confirms)
                assertEquals(0, dismissals)
            }
        } finally {
            runOnIdle { manager?.dispose() }
        }
    }

    private fun UIView.visibleDescendants(): List<UIView> {
        if (hidden || alpha <= 0.0) return emptyList()
        return listOf(this) + subviews.filterIsInstance<UIView>().flatMap { it.visibleDescendants() }
    }
}

@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)

package io.github.apdelrahman1911.nativecmpkit.ui.timepicker

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.*
import androidx.compose.ui.test.ExperimentalTestApi
import io.github.apdelrahman1911.nativecmpkit.ui.internal.runApplicationUiTest
import androidx.compose.ui.uikit.LocalUIViewController
import io.github.apdelrahman1911.nativecmpkit.ui.internal.datePickers
import io.github.apdelrahman1911.nativecmpkit.ui.internal.runNativeUiTest
import io.github.apdelrahman1911.nativecmpkit.ui.internal.waitForNative
import io.github.apdelrahman1911.nativecmpkit.ui.internal.sameNativeObject
import platform.Foundation.*
import platform.UIKit.*
import kotlin.test.*

@OptIn(ExperimentalMaterial3Api::class, ExperimentalTestApi::class)
class NativeTimePickerTest {
    @Test fun nativeValueChangedTargetRetainsHourAndMinuteCallbacks() = runNativeUiTest {
        val picker = UIDatePicker()
        var hour = -1
        var minute = -1
        val manager = TimePickerManager(picker, 59, 23, true, { hour = it }, { minute = it })
        manager.setTime(12, 34)
        picker.sendActionsForControlEvents(UIControlEventValueChanged)
        assertEquals(12, hour)
        assertEquals(34, minute)
    }

    @Test fun replacingStateReplacesTheNativeOwnerAndNeverWritesToOldState() = runApplicationUiTest {
        val first = AdaptiveTimePickerState(1, 2, true)
        val second = AdaptiveTimePickerState(14, 35, false)
        var state by mutableStateOf(first)
        lateinit var parent: UIViewController
        setContent {
            parent = LocalUIViewController.current
            AdaptiveTimePicker(state)
        }
        waitForIdle()
        // Composition idle alone does not prove deferred UIKit insertion.
        waitForNative {
            val picker = parent.view.datePickers().singleOrNull()
            picker != null && sameNativeObject(picker.window, parent.view.window)
        }
        var oldPicker: UIDatePicker? = null
        runOnIdle { oldPicker = parent.view.datePickers().single() }
        runOnIdle { state = second }
        waitForIdle()
        waitForNative {
            val picker = parent.view.datePickers().singleOrNull()
            picker != null && !sameNativeObject(oldPicker, picker) && oldPicker?.window == null &&
                sameNativeObject(picker.window, parent.view.window)
        }
        runOnIdle {
            val picker = parent.view.datePickers().single()
            assertNotSame(oldPicker, picker)
            assertFalse(sameNativeObject(oldPicker, picker))
            assertNull(oldPicker?.window)
            val calendar = requireNotNull(picker.calendar)
            val components = calendar.components(NSCalendarUnitHour or NSCalendarUnitMinute, picker.date)
            assertEquals(14L, components.hour)
            assertEquals(35L, components.minute)
            picker.sendActionsForControlEvents(UIControlEventValueChanged)
            assertEquals(1, first.hour)
            assertEquals(2, first.minute)
            assertEquals(14, second.hour)
            assertEquals(35, second.minute)
        }
    }
}

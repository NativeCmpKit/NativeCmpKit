// Modified for nativeCmpkit (2026-10-24): correctness, lifecycle, testing and build hardening.
@file:OptIn(ExperimentalForeignApi::class)

package io.github.apdelrahman1911.nativecmpkit.ui.datepicker

import androidx.compose.ui.graphics.Color
import kotlinx.cinterop.ExperimentalForeignApi
import kotlinx.cinterop.ObjCSignatureOverride
import platform.Foundation.NSDateComponents
import platform.UIKit.UICalendarSelectionMultiDate
import platform.UIKit.UICalendarSelectionMultiDateDelegateProtocol
import platform.UIKit.UIView
import platform.darwin.NSObject
import platform.darwin.dispatch_async
import platform.darwin.dispatch_get_main_queue

/**
 * Range calendar backed by `UICalendarView` (iOS 16+) with multi-date selection. Taps are
 * folded into a [DateRangeSelection]. UIKit receives highlights for the visible month and its
 * neighbours. The state retains the complete range, and unavailable days are greyed out.
 */
internal class CalendarRangePickerBackend(
    initialSelection: DateRangeSelection,
    initialDisplayedMonthMillis: Long,
    onDisplayedMonthChanged: (Long) -> Unit,
    private val onSelectionChanged: (selection: DateRangeSelection) -> Unit,
    private val isDaySelectable: (utcTimeMillis: Long) -> Boolean,
    private val enqueueRefresh: (() -> Unit) -> Unit = { refresh ->
        dispatch_async(dispatch_get_main_queue()) { refresh() }
    },
) {
    private val host = CalendarViewHost()
    private var selection = initialSelection
    private var bounds = DateBounds()
    private var disposed = false
    private var rendering = false
    private var refreshQueued = false
    private var renderedDays: List<Long>? = null

    private val selectionDelegate = object : NSObject(), UICalendarSelectionMultiDateDelegateProtocol {
        @ObjCSignatureOverride
        override fun multiDateSelection(
            selection: UICalendarSelectionMultiDate,
            didSelectDate: NSDateComponents,
        ) {
            onTap(didSelectDate.toUtcDayMillis())
        }

        @ObjCSignatureOverride
        override fun multiDateSelection(
            selection: UICalendarSelectionMultiDate,
            didDeselectDate: NSDateComponents,
        ) {
            onTap(didDeselectDate.toUtcDayMillis())
        }

        @ObjCSignatureOverride
        override fun multiDateSelection(
            selection: UICalendarSelectionMultiDate,
            canSelectDate: NSDateComponents,
        ): Boolean = !disposed && canSelectDay(canSelectDate.toUtcDayMillis())

        @ObjCSignatureOverride
        override fun multiDateSelection(
            selection: UICalendarSelectionMultiDate,
            canDeselectDate: NSDateComponents,
        ): Boolean = !disposed
    }

    private val multiSelection = UICalendarSelectionMultiDate(delegate = selectionDelegate)

    val view: UIView
        get() = host.calendarView

    /** Width divided by height of the calendar, or 0 when it has no intrinsic size yet. */
    val aspectRatio: Float

    init {
        host.calendarView.selectionBehavior = multiSelection
        host.onVisibleMonthChanged = {
            requestRender()
            onDisplayedMonthChanged(it)
        }
        host.showMonth(initialDisplayedMonthMillis, animated = false)
        render()
        host.calendarView.sizeToFit()
        aspectRatio = host.calendarView.aspectRatioOrZero()
    }

    private fun onTap(utcTimeMillis: Long) {
        if (disposed || rendering) return
        selection = selection.afterTap(utcTimeMillis)
        // UIKit may have deselected a day that is still part of the owner's range.
        renderedDays = null
        requestRender()
        onSelectionChanged(selection)
    }

    private fun requestRender() {
        if (disposed || refreshQueued) return
        refreshQueued = true
        // Leave UIKit's selection or layout callback before writing its selection.
        enqueueRefresh {
            refreshQueued = false
            render()
        }
    }

    private fun canSelectDay(day: Long): Boolean = bounds.isSelectableDate(day) && isDaySelectable(day)

    private fun render() {
        if (disposed || rendering) return
        val highlightedDays = host.daysAroundVisibleMonth()
            .map { it.toUtcDayMillis() }
            .filter { selection.contains(it) && canSelectDay(it) }
        if (highlightedDays == renderedDays) return
        rendering = true
        try {
            host.preservingVisibleMonth {
                multiSelection.setSelectedDates(highlightedDays.map(::utcDayToDateComponents), animated = false)
            }
            renderedDays = highlightedDays
        } finally {
            rendering = false
        }
    }

    fun setSelectedRange(newSelection: DateRangeSelection) {
        if (disposed || newSelection == selection) return
        selection = newSelection
        render()
    }

    fun setDisplayedMonth(utcTimeMillis: Long) {
        if (!disposed) host.showMonth(utcTimeMillis, animated = false)
    }

    fun applyDateBounds(minDateMillis: Long?, maxDateMillis: Long?) {
        if (disposed) return
        bounds = DateBounds(minDateMillis, maxDateMillis)
        host.applyDateBounds(minDateMillis, maxDateMillis)
        updateSelectableDates()
    }

    fun updateSelectableDates() {
        if (disposed) return
        multiSelection.updateSelectableDates()
        render()
        host.refresh()
    }

    fun dispose() {
        if (disposed) return
        disposed = true
        host.dispose()
        host.calendarView.selectionBehavior = null
    }

    fun applyColors(containerColor: Color, dayContentColor: Color, selectedDayContainerColor: Color) {
        if (disposed) return
        host.applyColors(containerColor, dayContentColor, selectedDayContainerColor)
    }
}

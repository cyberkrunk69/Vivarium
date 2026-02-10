# useDatePicker

Source: https://react-spectrum.adobe.com/react-aria/useDatePicker.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../DatePicker).

# useDatePicker

Provides the behavior and accessibility implementation for a date picker component.
A date picker combines a DateField and a Calendar popover to allow users to enter or select a date and time value.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useDatePicker} from 'react-aria'` |

[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/datepicker "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/datepicker "View package")

## API[#](#api)

---

`useDatePicker<T extends DateValue>(
props: AriaDatePickerProps<T>,
state: DatePickerState,
ref: RefObject<Element
|Â  |Â null>
): DatePickerAria`

## Features[#](#features)

---

A date picker can be built using `<input type="date">`, but this is very limited in functionality, lacking in internationalization capabilities, inconsistent between browsers, and difficult to style. `useDatePicker` helps achieve accessible and international date and time pickers that can be styled as needed.

- **Dates and times** â Support for dates and times with configurable granularity.
- **International** â Support for 13 calendar systems used around the world, including Gregorian, Buddhist, Islamic, Persian, and more. Locale-specific formatting, number systems, hour cycles, and right-to-left support are available as well.
- **Time zone aware** â Dates and times can optionally include a time zone. All modifications follow time zone rules such as daylight saving time.
- **Accessible** â Each date and time unit is displayed as an individually focusable and editable segment, which allows users an easy way to edit dates using the keyboard, in any date format and locale. Users can also open a calendar popover to select dates in a standard month grid. Localized screen reader messages are included to announce when the selection and visible date range change.
- **Touch friendly** â Date segments are editable using an easy to use numeric keypad, and all interactions are accessible using touch-based screen readers.
- **Customizable** â As with all of React Aria, the DOM structure and styling of all elements can be fully customized.

Read our [blog post](../blog/date-and-time-pickers-for-all) for more details about the internationalization, accessibility, and user experience features implemented by `useDatePicker`.

## Anatomy[#](#anatomy)

---

A date picker consists of a label, and group containing a [date field](../DateField/useDateField.html) and a button. Clicking the button opens a popup containing a [calendar](../Calendar/useCalendar.html). The date field includes segments representing each unit of a date and time (e.g. years, months, days, etc.), each of which is individually focusable and editable using the keyboard. The calendar popup offers a more visual way of choosing a date.

`useDatePicker` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useDatePicker` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the date picker's visible label element, if any. |
| `groupProps` | `GroupDOMAttributes` | Props for the grouping element containing the date field and button. |
| `fieldProps` | `AriaDatePickerProps<DateValue>` | Props for the date field. |
| `buttonProps` | `AriaButtonProps` | Props for the popover trigger button. |
| `descriptionProps` | `DOMAttributes` | Props for the description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
| `dialogProps` | `AriaDialogProps` | Props for the popover dialog. |
| `calendarProps` | `CalendarProps<DateValue>` | Props for the calendar within the popover dialog. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useDatePickerState` hook from `@react-stately/datepicker`. The state object should be passed as an argument to `useDatePicker`.

If the date picker does not have a visible label, an `aria-label` or `aria-labelledby` prop must be passed instead to
identify it to assistive technology.

## Date and time values[#](#date-and-time-values)

---

Dates and times are represented in many different ways by cultures around the world. This includes differences in calendar systems, time zones, daylight saving time rules, date and time formatting, weekday and weekend rules, and much more. When building applications that support users around the world, it is important to handle these aspects correctly for each locale.

`useDatePicker` uses the [@internationalized/date](../internationalized/date/) library to represent dates and times. This package provides a library of objects and functions to perform date and time related manipulation, queries, and conversions that work across locales and calendars. Date and time objects can be converted to and from native JavaScript `Date` objects or [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) strings. See the [documentation](../internationalized/date/), or the [examples below](#value) for more details.

## Example[#](#example)

---

A `DatePicker` composes several other components to produce a composite element that can be used to enter dates with a keyboard, or select them on a calendar. The `DateField`, `Popover`, `Calendar`, and `Button` components used in this example are independent and can be used separately from the `DatePicker`. The code is available below, and documentation is available on the corresponding pages.

```
import {useDatePicker} from 'react-aria';
import {useDatePickerState} from 'react-stately';

// Reuse the DateField, Popover, Dialog, Calendar, and Button from your component library.
import {Button, Calendar, DateField, Dialog, Popover} from 'your-component-library';

function DatePicker(props) {
  let state = useDatePickerState(props);
  let ref = React.useRef(null);
  let {
    groupProps,
    labelProps,
    fieldProps,
    buttonProps,
    dialogProps,
    calendarProps
  } = useDatePicker(props, state, ref);

  return (
    <div style={{ display: 'inline-flex', flexDirection: 'column' }}>
      <div {...labelProps}>{props.label}</div>
      <div {...groupProps} ref={ref} style={{ display: 'flex' }}>
        <DateField {...fieldProps} />
        <Button {...buttonProps}>ð</Button>
      </div>
      {state.isOpen &&
        (
          <Popover state={state} triggerRef={ref} placement="bottom start">
            <Dialog {...dialogProps}>
              <Calendar
                {...calendarProps}
                firstDayOfWeek={props.firstDayOfWeek}
              />
            </Dialog>
          </Popover>
        )}
    </div>
  );
}

<DatePicker label="Event date" />
```

```
import {useDatePicker} from 'react-aria';
import {useDatePickerState} from 'react-stately';

// Reuse the DateField, Popover, Dialog, Calendar, and Button from your component library.
import {
  Button,
  Calendar,
  DateField,
  Dialog,
  Popover
} from 'your-component-library';

function DatePicker(props) {
  let state = useDatePickerState(props);
  let ref = React.useRef(null);
  let {
    groupProps,
    labelProps,
    fieldProps,
    buttonProps,
    dialogProps,
    calendarProps
  } = useDatePicker(props, state, ref);

  return (
    <div
      style={{
        display: 'inline-flex',
        flexDirection: 'column'
      }}
    >
      <div {...labelProps}>{props.label}</div>
      <div
        {...groupProps}
        ref={ref}
        style={{ display: 'flex' }}
      >
        <DateField {...fieldProps} />
        <Button {...buttonProps}>ð</Button>
      </div>
      {state.isOpen &&
        (
          <Popover
            state={state}
            triggerRef={ref}
            placement="bottom start"
          >
            <Dialog {...dialogProps}>
              <Calendar
                {...calendarProps}
                firstDayOfWeek={props.firstDayOfWeek}
              />
            </Dialog>
          </Popover>
        )}
    </div>
  );
}

<DatePicker label="Event date" />
```

```
import {useDatePicker} from 'react-aria';
import {useDatePickerState} from 'react-stately';

// Reuse the DateField, Popover, Dialog, Calendar, and Button from your component library.
import {
  Button,
  Calendar,
  DateField,
  Dialog,
  Popover
} from 'your-component-library';

function DatePicker(
  props
) {
  let state =
    useDatePickerState(
      props
    );
  let ref = React.useRef(
    null
  );
  let {
    groupProps,
    labelProps,
    fieldProps,
    buttonProps,
    dialogProps,
    calendarProps
  } = useDatePicker(
    props,
    state,
    ref
  );

  return (
    <div
      style={{
        display:
          'inline-flex',
        flexDirection:
          'column'
      }}
    >
      <div
        {...labelProps}
      >
        {props.label}
      </div>
      <div
        {...groupProps}
        ref={ref}
        style={{
          display: 'flex'
        }}
      >
        <DateField
          {...fieldProps}
        />
        <Button
          {...buttonProps}
        >
          ð
        </Button>
      </div>
      {state.isOpen &&
        (
          <Popover
            state={state}
            triggerRef={ref}
            placement="bottom start"
          >
            <Dialog
              {...dialogProps}
            >
              <Calendar
                {...calendarProps}
                firstDayOfWeek={props
                  .firstDayOfWeek}
              />
            </Dialog>
          </Popover>
        )}
    </div>
  );
}

<DatePicker label="Event date" />
```

### Button[#](#button)

The `Button` component is used in the above example to trigger the calendar popover. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return <button {...buttonProps} ref={ref}>{props.children}</button>;
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return (
    <button {...buttonProps} ref={ref}>
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(
    null
  );
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  return (
    <button
      {...buttonProps}
      ref={ref}
    >
      {props.children}
    </button>
  );
}
```

### DateField[#](#datefield)

The `DateField` component implements the keyboard editable input used in a `DatePicker`. It can also be used standalone, or within a date range picker. See [useDateField](../DateField/useDateField.html) for more examples and documentation.

 Show code

```
import {useDateFieldState} from 'react-stately';
import {useDateField, useDateSegment, useLocale} from 'react-aria';

function DateField(props) {
  let { locale } = useLocale();
  let state = useDateFieldState({
    ...props,
    locale,
    createCalendar
  });

  let ref = React.useRef(null);
  let { labelProps, fieldProps } = useDateField(props, state, ref);

  return (
    <div className="wrapper">
      <span {...labelProps}>{props.label}</span>
      <div {...fieldProps} ref={ref} className="field">
        {state.segments.map((segment, i) => (
          <DateSegment key={i} segment={segment} state={state} />
        ))}
        {state.isInvalid &&
          <span aria-hidden="true">ð«</span>}
      </div>
    </div>
  );
}

function DateSegment({ segment, state }) {
  let ref = React.useRef(null);
  let { segmentProps } = useDateSegment(segment, state, ref);

  return (
    <div
      {...segmentProps}
      ref={ref}
      className={`segment ${segment.isPlaceholder ? 'placeholder' : ''}`}
    >
      {segment.text}
    </div>
  );
}
```

```
import {useDateFieldState} from 'react-stately';
import {
  useDateField,
  useDateSegment,
  useLocale
} from 'react-aria';

function DateField(props) {
  let { locale } = useLocale();
  let state = useDateFieldState({
    ...props,
    locale,
    createCalendar
  });

  let ref = React.useRef(null);
  let { labelProps, fieldProps } = useDateField(
    props,
    state,
    ref
  );

  return (
    <div className="wrapper">
      <span {...labelProps}>{props.label}</span>
      <div {...fieldProps} ref={ref} className="field">
        {state.segments.map((segment, i) => (
          <DateSegment
            key={i}
            segment={segment}
            state={state}
          />
        ))}
        {state.isInvalid &&
          <span aria-hidden="true">ð«</span>}
      </div>
    </div>
  );
}

function DateSegment({ segment, state }) {
  let ref = React.useRef(null);
  let { segmentProps } = useDateSegment(
    segment,
    state,
    ref
  );

  return (
    <div
      {...segmentProps}
      ref={ref}
      className={`segment ${
        segment.isPlaceholder ? 'placeholder' : ''
      }`}
    >
      {segment.text}
    </div>
  );
}
```

```
import {useDateFieldState} from 'react-stately';
import {
  useDateField,
  useDateSegment,
  useLocale
} from 'react-aria';

function DateField(
  props
) {
  let { locale } =
    useLocale();
  let state =
    useDateFieldState({
      ...props,
      locale,
      createCalendar
    });

  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    fieldProps
  } = useDateField(
    props,
    state,
    ref
  );

  return (
    <div className="wrapper">
      <span
        {...labelProps}
      >
        {props.label}
      </span>
      <div
        {...fieldProps}
        ref={ref}
        className="field"
      >
        {state.segments
          .map((
            segment,
            i
          ) => (
            <DateSegment
              key={i}
              segment={segment}
              state={state}
            />
          ))}
        {state
          .isInvalid &&
          (
            <span aria-hidden="true">
              ð«
            </span>
          )}
      </div>
    </div>
  );
}

function DateSegment(
  { segment, state }
) {
  let ref = React.useRef(
    null
  );
  let { segmentProps } =
    useDateSegment(
      segment,
      state,
      ref
    );

  return (
    <div
      {...segmentProps}
      ref={ref}
      className={`segment ${
        segment
            .isPlaceholder
          ? 'placeholder'
          : ''
      }`}
    >
      {segment.text}
    </div>
  );
}
```

 Show CSS

```
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.field {
  display: inline-flex;
  padding: 2px 4px;
  border-radius: 2px;
  border: 1px solid var(--gray);
  background: var(--spectrum-global-color-gray-50);
}

.field:focus-within {
  border-color: var(--blue);
}

.segment {
  padding: 0 2px;
  font-variant-numeric: tabular-nums;
  text-align: end;
}

.segment.placeholder {
  color: var(--spectrum-gray-600);
}

.segment:focus {
  color: white;
  background: var(--blue);
  outline: none;
  border-radius: 2px;
}
```

```
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.field {
  display: inline-flex;
  padding: 2px 4px;
  border-radius: 2px;
  border: 1px solid var(--gray);
  background: var(--spectrum-global-color-gray-50);
}

.field:focus-within {
  border-color: var(--blue);
}

.segment {
  padding: 0 2px;
  font-variant-numeric: tabular-nums;
  text-align: end;
}

.segment.placeholder {
  color: var(--spectrum-gray-600);
}

.segment:focus {
  color: white;
  background: var(--blue);
  outline: none;
  border-radius: 2px;
}
```

```
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.field {
  display: inline-flex;
  padding: 2px 4px;
  border-radius: 2px;
  border: 1px solid var(--gray);
  background: var(--spectrum-global-color-gray-50);
}

.field:focus-within {
  border-color: var(--blue);
}

.segment {
  padding: 0 2px;
  font-variant-numeric: tabular-nums;
  text-align: end;
}

.segment.placeholder {
  color: var(--spectrum-gray-600);
}

.segment:focus {
  color: white;
  background: var(--blue);
  outline: none;
  border-radius: 2px;
}
```

### Popover[#](#popover)

The `Popover` component is used to contain the popup calendar for the `DatePicker`.
It can be shared between many other components, including [Select](../Select/useSelect.html),
[Menu](../Menu/useMenu.html), and others.
See [usePopover](../Popover/usePopover.html) for more examples of popovers.

 Show code

```
import {DismissButton, Overlay, usePopover} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps extends Omit<AriaPopoverProps, 'popoverRef'> {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover({ children, state, ...props }: PopoverProps) {
  let popoverRef = React.useRef(null);
  let { popoverProps, underlayProps } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div {...underlayProps} style={{ position: 'fixed', inset: 0 }} />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps.style,
          background: 'var(--page-background)',
          border: '1px solid gray'
        }}
      >
        <DismissButton onDismiss={state.close} />
        {children}
        <DismissButton onDismiss={state.close} />
      </div>
    </Overlay>
  );
}
```

```
import {
  DismissButton,
  Overlay,
  usePopover
} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps
  extends Omit<AriaPopoverProps, 'popoverRef'> {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover(
  { children, state, ...props }: PopoverProps
) {
  let popoverRef = React.useRef(null);
  let { popoverProps, underlayProps } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div
        {...underlayProps}
        style={{ position: 'fixed', inset: 0 }}
      />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps.style,
          background: 'var(--page-background)',
          border: '1px solid gray'
        }}
      >
        <DismissButton onDismiss={state.close} />
        {children}
        <DismissButton onDismiss={state.close} />
      </div>
    </Overlay>
  );
}
```

```
import {
  DismissButton,
  Overlay,
  usePopover
} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps
  extends
    Omit<
      AriaPopoverProps,
      'popoverRef'
    > {
  children:
    React.ReactNode;
  state:
    OverlayTriggerState;
}

function Popover(
  {
    children,
    state,
    ...props
  }: PopoverProps
) {
  let popoverRef = React
    .useRef(null);
  let {
    popoverProps,
    underlayProps
  } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div
        {...underlayProps}
        style={{
          position:
            'fixed',
          inset: 0
        }}
      />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps
            .style,
          background:
            'var(--page-background)',
          border:
            '1px solid gray'
        }}
      >
        <DismissButton
          onDismiss={state
            .close}
        />
        {children}
        <DismissButton
          onDismiss={state
            .close}
        />
      </div>
    </Overlay>
  );
}
```

### Dialog[#](#dialog)

The `Dialog` component is rendered within the `Popover` component. It is built using the [useDialog](../Modal/useDialog.html) hook, and can be shared with many other components.

 Show code

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps extends AriaDialogProps {
  title?: React.ReactNode;
  children: React.ReactNode;
}

function Dialog({ title, children, ...props }: DialogProps) {
  let ref = React.useRef(null);
  let { dialogProps, titleProps } = useDialog(props, ref);

  return (
    <div {...dialogProps} ref={ref} style={{ padding: 30 }}>
      {title &&
        (
          <h3 {...titleProps} style={{ marginTop: 0 }}>
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps extends AriaDialogProps {
  title?: React.ReactNode;
  children: React.ReactNode;
}

function Dialog(
  { title, children, ...props }: DialogProps
) {
  let ref = React.useRef(null);
  let { dialogProps, titleProps } = useDialog(props, ref);

  return (
    <div {...dialogProps} ref={ref} style={{ padding: 30 }}>
      {title &&
        (
          <h3 {...titleProps} style={{ marginTop: 0 }}>
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps
  extends
    AriaDialogProps {
  title?:
    React.ReactNode;
  children:
    React.ReactNode;
}

function Dialog(
  {
    title,
    children,
    ...props
  }: DialogProps
) {
  let ref = React.useRef(
    null
  );
  let {
    dialogProps,
    titleProps
  } = useDialog(
    props,
    ref
  );

  return (
    <div
      {...dialogProps}
      ref={ref}
      style={{
        padding: 30
      }}
    >
      {title &&
        (
          <h3
            {...titleProps}
            style={{
              marginTop:
                0
            }}
          >
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

### Calendar[#](#calendar)

The `Calendar` component implements the month grid shown within the `DatePicker` popover. It can also be used standalone, or within other components. See [useCalendar](../Calendar/useCalendar.html) for more examples and documentation.

 Show code

```
import {useCalendar, useCalendarCell, useCalendarGrid} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {createCalendar, getWeeksInMonth} from '@internationalized/date';

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    ...props,
    locale,
    createCalendar
  });

  let { calendarProps, prevButtonProps, nextButtonProps, title } = useCalendar(
    props,
    state
  );

  return (
    <div {...calendarProps} className="calendar">
      <div className="header">
        <h2>{title}</h2>
        <Button {...prevButtonProps}>&lt;</Button>
        <Button {...nextButtonProps}>&gt;</Button>
      </div>
      <CalendarGrid state={state} firstDayOfWeek={props.firstDayOfWeek} />
    </div>
  );
}

function CalendarGrid({ state, ...props }) {
  let { locale } = useLocale();
  let { gridProps, headerProps, weekDays } = useCalendarGrid(props, state);

  // Get the number of weeks in the month so we can render the proper number of rows.
  let weeksInMonth = getWeeksInMonth(state.visibleRange.start, locale);

  return (
    <table {...gridProps}>
      <thead {...headerProps}>
        <tr>
          {weekDays.map((day, index) => <th key={index}>{day}</th>)}
        </tr>
      </thead>
      <tbody>
        {[...new Array(weeksInMonth).keys()].map((weekIndex) => (
          <tr key={weekIndex}>
            {state.getDatesInWeek(weekIndex).map((date, i) => (
              date
                ? (
                  <CalendarCell
                    key={i}
                    state={state}
                    date={date}
                  />
                )
                : <td key={i} />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function CalendarCell({ state, date }) {
  let ref = React.useRef(null);
  let {
    cellProps,
    buttonProps,
    isSelected,
    isOutsideVisibleRange,
    isDisabled,
    isUnavailable,
    formattedDate
  } = useCalendarCell({ date }, state, ref);

  return (
    <td {...cellProps}>
      <div
        {...buttonProps}
        ref={ref}
        hidden={isOutsideVisibleRange}
        className={`cell ${isSelected ? 'selected' : ''} ${
          isDisabled ? 'disabled' : ''
        } ${isUnavailable ? 'unavailable' : ''}`}
      >
        {formattedDate}
      </div>
    </td>
  );
}
```

```
import {
  useCalendar,
  useCalendarCell,
  useCalendarGrid
} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {
  createCalendar,
  getWeeksInMonth
} from '@internationalized/date';

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    ...props,
    locale,
    createCalendar
  });

  let {
    calendarProps,
    prevButtonProps,
    nextButtonProps,
    title
  } = useCalendar(props, state);

  return (
    <div {...calendarProps} className="calendar">
      <div className="header">
        <h2>{title}</h2>
        <Button {...prevButtonProps}>&lt;</Button>
        <Button {...nextButtonProps}>&gt;</Button>
      </div>
      <CalendarGrid
        state={state}
        firstDayOfWeek={props.firstDayOfWeek}
      />
    </div>
  );
}

function CalendarGrid({ state, ...props }) {
  let { locale } = useLocale();
  let { gridProps, headerProps, weekDays } =
    useCalendarGrid(props, state);

  // Get the number of weeks in the month so we can render the proper number of rows.
  let weeksInMonth = getWeeksInMonth(
    state.visibleRange.start,
    locale
  );

  return (
    <table {...gridProps}>
      <thead {...headerProps}>
        <tr>
          {weekDays.map((day, index) => (
            <th key={index}>{day}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {[...new Array(weeksInMonth).keys()].map(
          (weekIndex) => (
            <tr key={weekIndex}>
              {state.getDatesInWeek(weekIndex).map((
                date,
                i
              ) => (
                date
                  ? (
                    <CalendarCell
                      key={i}
                      state={state}
                      date={date}
                    />
                  )
                  : <td key={i} />
              ))}
            </tr>
          )
        )}
      </tbody>
    </table>
  );
}

function CalendarCell({ state, date }) {
  let ref = React.useRef(null);
  let {
    cellProps,
    buttonProps,
    isSelected,
    isOutsideVisibleRange,
    isDisabled,
    isUnavailable,
    formattedDate
  } = useCalendarCell({ date }, state, ref);

  return (
    <td {...cellProps}>
      <div
        {...buttonProps}
        ref={ref}
        hidden={isOutsideVisibleRange}
        className={`cell ${isSelected ? 'selected' : ''} ${
          isDisabled ? 'disabled' : ''
        } ${isUnavailable ? 'unavailable' : ''}`}
      >
        {formattedDate}
      </div>
    </td>
  );
}
```

```
import {
  useCalendar,
  useCalendarCell,
  useCalendarGrid
} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {
  createCalendar,
  getWeeksInMonth
} from '@internationalized/date';

function Calendar(
  props
) {
  let { locale } =
    useLocale();
  let state =
    useCalendarState({
      ...props,
      locale,
      createCalendar
    });

  let {
    calendarProps,
    prevButtonProps,
    nextButtonProps,
    title
  } = useCalendar(
    props,
    state
  );

  return (
    <div
      {...calendarProps}
      className="calendar"
    >
      <div className="header">
        <h2>{title}</h2>
        <Button
          {...prevButtonProps}
        >
          &lt;
        </Button>
        <Button
          {...nextButtonProps}
        >
          &gt;
        </Button>
      </div>
      <CalendarGrid
        state={state}
        firstDayOfWeek={props
          .firstDayOfWeek}
      />
    </div>
  );
}

function CalendarGrid(
  { state, ...props }
) {
  let { locale } =
    useLocale();
  let {
    gridProps,
    headerProps,
    weekDays
  } = useCalendarGrid(
    props,
    state
  );

  // Get the number of weeks in the month so we can render the proper number of rows.
  let weeksInMonth =
    getWeeksInMonth(
      state.visibleRange
        .start,
      locale
    );

  return (
    <table
      {...gridProps}
    >
      <thead
        {...headerProps}
      >
        <tr>
          {weekDays.map((
            day,
            index
          ) => (
            <th
              key={index}
            >
              {day}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {[...new Array(
          weeksInMonth
        ).keys()].map(
          (weekIndex) => (
            <tr
              key={weekIndex}
            >
              {state
                .getDatesInWeek(
                  weekIndex
                ).map((
                  date,
                  i
                ) => (
                  date
                    ? (
                      <CalendarCell
                        key={i}
                        state={state}
                        date={date}
                      />
                    )
                    : (
                      <td
                        key={i}
                      />
                    )
                ))}
            </tr>
          )
        )}
      </tbody>
    </table>
  );
}

function CalendarCell(
  { state, date }
) {
  let ref = React.useRef(
    null
  );
  let {
    cellProps,
    buttonProps,
    isSelected,
    isOutsideVisibleRange,
    isDisabled,
    isUnavailable,
    formattedDate
  } = useCalendarCell(
    { date },
    state,
    ref
  );

  return (
    <td {...cellProps}>
      <div
        {...buttonProps}
        ref={ref}
        hidden={isOutsideVisibleRange}
        className={`cell ${
          isSelected
            ? 'selected'
            : ''
        } ${
          isDisabled
            ? 'disabled'
            : ''
        } ${
          isUnavailable
            ? 'unavailable'
            : ''
        }`}
      >
        {formattedDate}
      </div>
    </td>
  );
}
```

 Show CSS

```
.calendar {
  width: 220px;
}

.header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 8px;
}

.header h2 {
  flex: 1;
  margin: 0;
}

.calendar table {
  width: 100%;
}

.cell {
  cursor: default;
  text-align: center;
}

.selected {
  background: var(--blue);
  color: white;
}

.unavailable {
  color: var(--spectrum-global-color-red-600);
}

.disabled {
  color: gray;
}
```

```
.calendar {
  width: 220px;
}

.header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 8px;
}

.header h2 {
  flex: 1;
  margin: 0;
}

.calendar table {
  width: 100%;
}

.cell {
  cursor: default;
  text-align: center;
}

.selected {
  background: var(--blue);
  color: white;
}

.unavailable {
  color: var(--spectrum-global-color-red-600);
}

.disabled {
  color: gray;
}
```

```
.calendar {
  width: 220px;
}

.header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 8px;
}

.header h2 {
  flex: 1;
  margin: 0;
}

.calendar table {
  width: 100%;
}

.cell {
  cursor: default;
  text-align: center;
}

.selected {
  background: var(--blue);
  color: white;
}

.unavailable {
  color: var(--spectrum-global-color-red-600);
}

.disabled {
  color: gray;
}
```

## Styled examples[#](#styled-examples)

---

[![](/DatePicker-tailwind.4a901e93.png)

Tailwind CSS

A date picker built with Tailwind and React Aria.](https://codesandbox.io/p/sandbox/great-dawn-s7d8th?file=/src/DatePicker.js)
[![](/DatePicker-chakra.0f414e59.png)

Chakra UI

A date and time picker built with Chakra UI and React Aria.](https://codesandbox.io/p/sandbox/competent-tharp-zs37w9?file=/src/DatePicker.js)

## Usage[#](#usage)

---

The following examples show how to use the `DatePicker` component created in the above example.

### Value[#](#value)

A `DatePicker` displays a placeholder by default. An initial, uncontrolled value can be provided to the `DatePicker` using the `defaultValue` prop. Alternatively, a controlled value can be provided using the `value` prop.

Date values are provided using objects in the [@internationalized/date](../internationalized/date/) package. This library handles correct international date manipulation across calendars, time zones, and other localization concerns. `useDatePicker` supports values of the following types:

- `CalendarDate` â a date without any time components. May be parsed from a string representation using the `parseDate` function. Use this type to represent dates where the time is not important, such as a birthday or an all day calendar event.
- `CalendarDateTime` â a date with a time, but not in any specific time zone. May be parsed from a string representation using the `parseDateTime` function. Use this type to represent times that occur at the same local time regardless of the time zone, such as the time of New Years Eve fireworks which always occur at midnight. Most times are better stored as a `ZonedDateTime`.
- `ZonedDateTime` â a date with a time in a specific time zone. May be parsed from a string representation using the `parseZonedDateTime`, `parseAbsolute`, or `parseAbsoluteToLocal` functions. Use this type to represent an exact moment in time at a particular location on Earth.

```
import {parseDate} from '@internationalized/date';

function Example() {
  let [value, setValue] = React.useState(parseDate('2020-02-03'));

  return (
    <>
      <DatePicker
        label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')} />
      <DatePicker
        label="Date (controlled)"
        value={value}
        onChange={setValue} />
    </>
  );
}
```

```
import {parseDate} from '@internationalized/date';

function Example() {
  let [value, setValue] = React.useState(
    parseDate('2020-02-03')
  );

  return (
    <>
      <DatePicker
        label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')}
      />
      <DatePicker
        label="Date (controlled)"
        value={value}
        onChange={setValue}
      />
    </>
  );
}
```

```
import {parseDate} from '@internationalized/date';

function Example() {
  let [value, setValue] =
    React.useState(
      parseDate(
        '2020-02-03'
      )
    );

  return (
    <>
      <DatePicker
        label="Date (uncontrolled)"
        defaultValue={parseDate(
          '2020-02-03'
        )}
      />
      <DatePicker
        label="Date (controlled)"
        value={value}
        onChange={setValue}
      />
    </>
  );
}
```

### Events[#](#events)

`useDatePicker` accepts an `onChange` prop which is triggered whenever the date is edited by the user. The example below uses `onChange` to update a separate element with a formatted version of the date in the user's locale and local time zone. This is done by converting the date to a native JavaScript `Date` object to pass to the formatter.

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] = React.useState(parseDate('1985-07-03'));
  let formatter = useDateFormatter({ dateStyle: 'full' });

  return (
    <>
      <DatePicker label="Birth date" value={date} onChange={setDate} />
      <p>
        Selected date:{' '}
        {date ? formatter.format(date.toDate(getLocalTimeZone())) : '--'}
      </p>
    </>
  );
}
```

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] = React.useState(
    parseDate('1985-07-03')
  );
  let formatter = useDateFormatter({ dateStyle: 'full' });

  return (
    <>
      <DatePicker
        label="Birth date"
        value={date}
        onChange={setDate}
      />
      <p>
        Selected date: {date
          ? formatter.format(
            date.toDate(getLocalTimeZone())
          )
          : '--'}
      </p>
    </>
  );
}
```

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] =
    React.useState(
      parseDate(
        '1985-07-03'
      )
    );
  let formatter =
    useDateFormatter({
      dateStyle: 'full'
    });

  return (
    <>
      <DatePicker
        label="Birth date"
        value={date}
        onChange={setDate}
      />
      <p>
        Selected date:
        {' '}
        {date
          ? formatter
            .format(
              date
                .toDate(
                  getLocalTimeZone()
                )
            )
          : '--'}
      </p>
    </>
  );
}
```

### Time zones[#](#time-zones)

`useDatePicker` is time zone aware when a `ZonedDateTime` object is provided as the value. In this case, the time zone abbreviation is displayed, and time zone concerns such as daylight saving time are taken into account when the value is manipulated.

In most cases, your data will come from and be sent to a server as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted string. [@internationalized/date](../internationalized/date/) includes functions for parsing strings in multiple formats into `ZonedDateTime` objects. Which format you use will depend on what information you need to store.

- `parseZonedDateTime` â This function parses a date with an explicit time zone and optional UTC offset attached (e.g. `"2021-11-07T00:45[America/Los_Angeles]"` or `"2021-11-07T00:45-07:00[America/Los_Angeles]"`). This format preserves the maximum amount of information. If the exact local time and time zone that a user selected is important, use this format. Storing the time zone and offset that was selected rather than converting to UTC ensures that the local time is correct regardless of daylight saving rule changes (e.g. if a locale abolishes DST). Examples where this applies include calendar events, reminders, and other times that occur in a particular location.
- `parseAbsolute` â This function parses an absolute date and time that occurs at the same instant at all locations on Earth. It can be represented in UTC (e.g. `"2021-11-07T07:45:00Z"`), or stored with a particular offset (e.g. `"2021-11-07T07:45:00-07:00"`). A time zone identifier, e.g. `America/Los_Angeles`, must be passed, and the result will be converted into that time zone. Absolute times are the best way to represent events that occurred in the past, or future events where an exact time is needed, regardless of time zone.
- `parseAbsoluteToLocal` â This function parses an absolute date and time into the current user's local time zone. It is a shortcut for `parseAbsolute`, and accepts the same formats.

```
import {parseZonedDateTime} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseZonedDateTime('2022-11-07T00:45[America/Los_Angeles]')}
/>
```

```
import {parseZonedDateTime} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseZonedDateTime(
    '2022-11-07T00:45[America/Los_Angeles]'
  )}
/>
```

```
import {parseZonedDateTime} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseZonedDateTime(
    '2022-11-07T00:45[America/Los_Angeles]'
  )}
/>
```

`useDatePicker` displays times in the time zone included in the `ZonedDateTime` object. The above example is always displayed in Pacific Standard Time because the `America/Los_Angeles` time zone identifier is provided. [@internationalized/date](../internationalized/date/) includes functions for converting dates between time zones, or parsing a date directly into a specific time zone or the user's local time zone, as shown below.

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseAbsoluteToLocal('2021-11-07T07:45:00Z')}
/>
```

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseAbsoluteToLocal(
    '2021-11-07T07:45:00Z'
  )}
/>
```

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DatePicker
  label="Event date"
  defaultValue={parseAbsoluteToLocal(
    '2021-11-07T07:45:00Z'
  )}
/>
```

### Granularity[#](#granularity)

The `granularity` prop allows you to control the smallest unit that is displayed by `useDatePicker`. By default, `CalendarDate` values are displayed with `"day"` granularity (year, month, and day), and `CalendarDateTime` and `ZonedDateTime` values are displayed with `"minute"` granularity. More granular time values can be displayed by setting the `granularity` prop to `"second"`.

In addition, when a value with a time is provided but you wish to only display the date, you can set the granularity to `"day"`. This has no effect on the actual value (it still has a time component), only on what fields are displayed. In the following example, two DatePickers are synchronized with the same value, but display different granularities.

```
function Example() {
  let [date, setDate] = React.useState(
    parseAbsoluteToLocal('2021-04-07T18:45:22Z')
  );

  return (
    <>
      <DatePicker
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DatePicker
        label="Date"
        granularity="day"
        value={date}
        onChange={setDate}
      />
    </>
  );
}
```

```
function Example() {
  let [date, setDate] = React.useState(
    parseAbsoluteToLocal('2021-04-07T18:45:22Z')
  );

  return (
    <>
      <DatePicker
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DatePicker
        label="Date"
        granularity="day"
        value={date}
        onChange={setDate}
      />
    </>
  );
}
```

```
function Example() {
  let [date, setDate] =
    React.useState(
      parseAbsoluteToLocal(
        '2021-04-07T18:45:22Z'
      )
    );

  return (
    <>
      <DatePicker
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DatePicker
        label="Date"
        granularity="day"
        value={date}
        onChange={setDate}
      />
    </>
  );
}
```

If no `value` or `defaultValue` prop is passed, then the `granularity` prop also affects which type of value is emitted from the `onChange` event. Note that by default, time values will not have a time zone because none was supplied. You can override this by setting the `placeholderValue` prop explicitly. Values emitted from `onChange` will use the time zone of the placeholder value.

```
import {now} from '@internationalized/date';

<DatePicker
  label="Event date"
  granularity="second" />
<DatePicker
  label="Event date"
  placeholderValue={now('America/New_York')}
  granularity="second" />
```

```
import {now} from '@internationalized/date';

<DatePicker
  label="Event date"
  granularity="second" />
<DatePicker
  label="Event date"
  placeholderValue={now('America/New_York')}
  granularity="second" />
```

```
import {now} from '@internationalized/date';

<DatePicker
  label="Event date"
  granularity="second"
/>
<DatePicker
  label="Event date"
  placeholderValue={now(
    'America/New_York'
  )}
  granularity="second"
/>
```

### International calendars[#](#international-calendars)

`useDatePicker` supports selecting dates in many calendar systems used around the world, including Gregorian, Hebrew, Indian, Islamic, Buddhist, and more. Dates are automatically displayed in the appropriate calendar system for the user's locale. The calendar system can be overridden using the [Unicode calendar locale extension](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/calendar#adding_a_calendar_in_the_locale_string), passed to the [I18nProvider](../I18nProvider) component.

Selected dates passed to `onChange` always use the same calendar system as the `value` or `defaultValue` prop. If no `value` or `defaultValue` is provided, then dates passed to `onChange` are always in the Gregorian calendar since this is the most commonly used. This means that even though the user selects dates in their local calendar system, applications are able to deal with dates from all users consistently.

The below example displays a `DatePicker` in the Hindi language, using the Indian calendar. Dates emitted from `onChange` are in the Gregorian calendar.

```
import {I18nProvider} from 'react-aria';

function Example() {
  let [date, setDate] = React.useState(null);
  return (
    <I18nProvider locale="hi-IN-u-ca-indian">
      <DatePicker label="Date" value={date} onChange={setDate} />
      <p>Selected date: {date?.toString()}</p>
    </I18nProvider>
  );
}
```

```
import {I18nProvider} from 'react-aria';

function Example() {
  let [date, setDate] = React.useState(null);
  return (
    <I18nProvider locale="hi-IN-u-ca-indian">
      <DatePicker
        label="Date"
        value={date}
        onChange={setDate}
      />
      <p>Selected date: {date?.toString()}</p>
    </I18nProvider>
  );
}
```

```
import {I18nProvider} from 'react-aria';

function Example() {
  let [date, setDate] =
    React.useState(null);
  return (
    <I18nProvider locale="hi-IN-u-ca-indian">
      <DatePicker
        label="Date"
        value={date}
        onChange={setDate}
      />
      <p>
        Selected date:
        {' '}
        {date
          ?.toString()}
      </p>
    </I18nProvider>
  );
}
```

### Minimum and maximum values[#](#minimum-and-maximum-values)

The `minValue` and `maxValue` props can also be used to perform builtin validation. This prevents the user from selecting dates outside the valid range in the calendar, and marks the date field as invalid using ARIA. You should implement a visual indication that the date picker is invalid as well.

This example only accepts dates after today.

```
import {today} from '@internationalized/date';

<DatePicker
  label="Appointment date"
  minValue={today(getLocalTimeZone())}
  defaultValue={parseDate('2022-02-03')} />
```

```
import {today} from '@internationalized/date';

<DatePicker
  label="Appointment date"
  minValue={today(getLocalTimeZone())}
  defaultValue={parseDate('2022-02-03')} />
```

```
import {today} from '@internationalized/date';

<DatePicker
  label="Appointment date"
  minValue={today(
    getLocalTimeZone()
  )}
  defaultValue={parseDate(
    '2022-02-03'
  )}
/>
```

### Unavailable dates[#](#unavailable-dates)

`useDatePicker` supports marking certain dates as *unavailable*. These dates remain focusable with the keyboard in the calendar so that navigation is consistent, but cannot be selected by the user. When an unavailable date is entered into the date field, it is marked as invalid. The `isDateUnavailable` prop accepts a callback that is called to evaluate whether each visible date is unavailable.

This example includes multiple unavailable date ranges, e.g. dates when no appointments are available. In addition, all weekends are unavailable. The `minValue` prop is also used to prevent selecting dates before today.

```
import {useLocale} from 'react-aria';
import {isWeekend, today} from '@internationalized/date';

function Example() {
  let now = today(getLocalTimeZone());
  let disabledRanges = [
    [now, now.add({ days: 5 })],
    [now.add({ days: 14 }), now.add({ days: 16 })],
    [now.add({ days: 23 }), now.add({ days: 24 })]
  ];

  let { locale } = useLocale();
  let isDateUnavailable = (date) =>
    isWeekend(date, locale) ||
    disabledRanges.some((interval) =>
      date.compare(interval[0]) >= 0 && date.compare(interval[1]) <= 0
    );

  return (
    <DatePicker
      label="Appointment date"
      minValue={today(getLocalTimeZone())}
      isDateUnavailable={isDateUnavailable}
    />
  );
}
```

```
import {useLocale} from 'react-aria';
import {isWeekend, today} from '@internationalized/date';

function Example() {
  let now = today(getLocalTimeZone());
  let disabledRanges = [
    [now, now.add({ days: 5 })],
    [now.add({ days: 14 }), now.add({ days: 16 })],
    [now.add({ days: 23 }), now.add({ days: 24 })]
  ];

  let { locale } = useLocale();
  let isDateUnavailable = (date) =>
    isWeekend(date, locale) ||
    disabledRanges.some((interval) =>
      date.compare(interval[0]) >= 0 &&
      date.compare(interval[1]) <= 0
    );

  return (
    <DatePicker
      label="Appointment date"
      minValue={today(getLocalTimeZone())}
      isDateUnavailable={isDateUnavailable}
    />
  );
}
```

```
import {useLocale} from 'react-aria';
import {
  isWeekend,
  today
} from '@internationalized/date';

function Example() {
  let now = today(
    getLocalTimeZone()
  );
  let disabledRanges = [
    [
      now,
      now.add({
        days: 5
      })
    ],
    [
      now.add({
        days: 14
      }),
      now.add({
        days: 16
      })
    ],
    [
      now.add({
        days: 23
      }),
      now.add({
        days: 24
      })
    ]
  ];

  let { locale } =
    useLocale();
  let isDateUnavailable =
    (date) =>
      isWeekend(
        date,
        locale
      ) ||
      disabledRanges
        .some((
          interval
        ) =>
          date.compare(
              interval[0]
            ) >= 0 &&
          date.compare(
              interval[1]
            ) <= 0
        );

  return (
    <DatePicker
      label="Appointment date"
      minValue={today(
        getLocalTimeZone()
      )}
      isDateUnavailable={isDateUnavailable}
    />
  );
}
```

### Placeholder value[#](#placeholder-value)

When no value is set, a placeholder is shown. The format of the placeholder is influenced by the `granularity` and `placeholderValue` props. `placeholderValue` also controls the default values of each segment when the user first interacts with them, e.g. using the up and down arrow keys, as well as the default month shown in the calendar popover. By default, the `placeholderValue` is the current date at midnight, but you can set it to a more appropriate value if needed.

```
import {CalendarDate} from '@internationalized/date';

<DatePicker
  label="Birth date"
  placeholderValue={new CalendarDate(1980, 1, 1)}
/>
```

```
import {CalendarDate} from '@internationalized/date';

<DatePicker
  label="Birth date"
  placeholderValue={new CalendarDate(1980, 1, 1)}
/>
```

```
import {CalendarDate} from '@internationalized/date';

<DatePicker
  label="Birth date"
  placeholderValue={new CalendarDate(
    1980,
    1,
    1
  )}
/>
```

### Hide time zone[#](#hide-time-zone)

When a `ZonedDateTime` object is provided as the value to `useDatePicker`, the time zone abbreviation is displayed by default. However, if this is displayed elsewhere or implicit based on the usecase, it can be hidden using the `hideTimeZone` option.

```
<DatePicker
  label="Appointment time"
  defaultValue={parseZonedDateTime('2022-11-07T10:45[America/Los_Angeles]')}
  hideTimeZone />
```

```
<DatePicker
  label="Appointment time"
  defaultValue={parseZonedDateTime(
    '2022-11-07T10:45[America/Los_Angeles]'
  )}
  hideTimeZone
/>
```

```
<DatePicker
  label="Appointment time"
  defaultValue={parseZonedDateTime(
    '2022-11-07T10:45[America/Los_Angeles]'
  )}
  hideTimeZone
/>
```

### Hour cycle[#](#hour-cycle)

By default, `useDatePicker` displays times in either 12 or 24 hour hour format depending on the user's locale. However, this can be overridden using the `hourCycle` prop if needed for a specific usecase. This example forces `useDatePicker` to use 24-hour time, regardless of the locale.

```
<DatePicker
  label="Appointment time"
  granularity="minute"
  hourCycle={24} />
```

```
<DatePicker
  label="Appointment time"
  granularity="minute"
  hourCycle={24} />
```

```
<DatePicker
  label="Appointment time"
  granularity="minute"
  hourCycle={24}
/>
```

### Custom first day of week[#](#custom-first-day-of-week)

By default, the first day of the week is automatically set based on the current locale. This can be changed by setting the `firstDayOfWeek` prop to `'sun'`, `'mon'`, `'tue'`, `'wed'`, `'thu'`, `'fri'`, or `'sat'`.

```
<DatePicker label="Appointment time" firstDayOfWeek="mon" />
```

```
<DatePicker label="Appointment time" firstDayOfWeek="mon" />
```

```
<DatePicker
  label="Appointment time"
  firstDayOfWeek="mon"
/>
```

`CalendarDate
|Â CalendarDateTime
|Â ZonedDateTime`

A CalendarDate represents a date without any time components in a specific calendar system.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `calendar` | `Calendar` | The calendar system associated with this date, e.g. Gregorian. |
| `era` | `string` | The calendar era for this date, e.g. "BC" or "AD". |
| `year` | `number` | The year of this date within the era. |
| `month` | `number` | The month number within the year. Note that some calendar systems such as Hebrew may have a variable number of months per year. Therefore, month numbers may not always correspond to the same month names in different years. |
| `day` | `number` | The day number within the month. |

### Methods

| Method | Description |
| --- | --- |
| `constructor( (...args: any[] )): void` |  |
| `copy(): CalendarDate` | Returns a copy of this date. |
| `add( (duration: DateDuration )): CalendarDate` | Returns a new `CalendarDate` with the given duration added to it. |
| `subtract( (duration: DateDuration )): CalendarDate` | Returns a new `CalendarDate` with the given duration subtracted from it. |
| `set( (fields: DateFields )): CalendarDate` | Returns a new `CalendarDate` with the given fields set to the provided values. Other fields will be constrained accordingly. |
| `cycle( field: DateField, amount: number, options?: CycleOptions ): CalendarDate` | Returns a new `CalendarDate` with the given field adjusted by a specified amount. When the resulting value reaches the limits of the field, it wraps around. |
| `toDate( (timeZone: string )): Date` | Converts the date to a native JavaScript Date object, with the time set to midnight in the given time zone. |
| `toString(): string` | Converts the date to an ISO 8601 formatted string. |
| `compare( (b: AnyCalendarDate )): number` | Compares this date with another. A negative result indicates that this date is before the given one, and a positive date indicates that it is after. |

A CalendarDateTime represents a date and time without a time zone, in a specific calendar system.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `calendar` | `Calendar` | The calendar system associated with this date, e.g. Gregorian. |
| `era` | `string` | The calendar era for this date, e.g. "BC" or "AD". |
| `year` | `number` | The year of this date within the era. |
| `month` | `number` | The month number within the year. Note that some calendar systems such as Hebrew may have a variable number of months per year. Therefore, month numbers may not always correspond to the same month names in different years. |
| `day` | `number` | The day number within the month. |
| `hour` | `number` | The hour in the day, numbered from 0 to 23. |
| `minute` | `number` | The minute in the hour. |
| `second` | `number` | The second in the minute. |
| `millisecond` | `number` | The millisecond in the second. |

### Methods

| Method | Description |
| --- | --- |
| `constructor( (...args: any[] )): void` |  |
| `copy(): CalendarDateTime` | Returns a copy of this date. |
| `add( (duration: DateTimeDuration )): CalendarDateTime` | Returns a new `CalendarDateTime` with the given duration added to it. |
| `subtract( (duration: DateTimeDuration )): CalendarDateTime` | Returns a new `CalendarDateTime` with the given duration subtracted from it. |
| `set( (fields: DateFields &Â  &Â TimeFields )): CalendarDateTime` | Returns a new `CalendarDateTime` with the given fields set to the provided values. Other fields will be constrained accordingly. |
| `cycle( field: DateField |Â  |Â TimeField, amount: number, options?: CycleTimeOptions ): CalendarDateTime` | Returns a new `CalendarDateTime` with the given field adjusted by a specified amount. When the resulting value reaches the limits of the field, it wraps around. |
| `toDate( (timeZone: string, , disambiguation?: Disambiguation )): Date` | Converts the date to a native JavaScript Date object in the given time zone. |
| `toString(): string` | Converts the date to an ISO 8601 formatted string. |
| `compare( (b: CalendarDate |Â CalendarDateTime |Â ZonedDateTime )): number` | Compares this date with another. A negative result indicates that this date is before the given one, and a positive date indicates that it is after. |

A ZonedDateTime represents a date and time in a specific time zone and calendar system.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `calendar` | `Calendar` | The calendar system associated with this date, e.g. Gregorian. |
| `era` | `string` | The calendar era for this date, e.g. "BC" or "AD". |
| `year` | `number` | The year of this date within the era. |
| `month` | `number` | The month number within the year. Note that some calendar systems such as Hebrew may have a variable number of months per year. Therefore, month numbers may not always correspond to the same month names in different years. |
| `day` | `number` | The day number within the month. |
| `hour` | `number` | The hour in the day, numbered from 0 to 23. |
| `minute` | `number` | The minute in the hour. |
| `second` | `number` | The second in the minute. |
| `millisecond` | `number` | The millisecond in the second. |
| `timeZone` | `string` | The IANA time zone identifier that this date and time is represented in. |
| `offset` | `number` | The UTC offset for this time, in milliseconds. |

### Methods

| Method | Description |
| --- | --- |
| `constructor( (...args: any[] )): void` |  |
| `copy(): ZonedDateTime` | Returns a copy of this date. |
| `add( (duration: DateTimeDuration )): ZonedDateTime` | Returns a new `ZonedDateTime` with the given duration added to it. |
| `subtract( (duration: DateTimeDuration )): ZonedDateTime` | Returns a new `ZonedDateTime` with the given duration subtracted from it. |
| `set( (fields: DateFields &Â  &Â TimeFields, , disambiguation?: Disambiguation )): ZonedDateTime` | Returns a new `ZonedDateTime` with the given fields set to the provided values. Other fields will be constrained accordingly. |
| `cycle( field: DateField |Â  |Â TimeField, amount: number, options?: CycleTimeOptions ): ZonedDateTime` | Returns a new `ZonedDateTime` with the given field adjusted by a specified amount. When the resulting value reaches the limits of the field, it wraps around. |
| `toDate(): Date` | Converts the date to a native JavaScript Date object. |
| `toString(): string` | Converts the date to an ISO 8601 formatted string, including the UTC offset and time zone identifier. |
| `toAbsoluteString(): string` | Converts the date to an ISO 8601 formatted string in UTC. |
| `compare( (b: CalendarDate |Â CalendarDateTime |Â ZonedDateTime )): number` | Compares this date with another. A negative result indicates that this date is before the given one, and a positive date indicates that it is after. |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `autoComplete` | `string` | â | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `pageBehavior` | `PageBehavior` | `visible` | Controls the behavior of paging. Pagination either works by advancing the visible page by visibleDuration (default) or one unit of visibleDuration. |
| `firstDayOfWeek` | `'sun' |Â 'mon' |Â 'tue' |Â 'wed' |Â 'thu' |Â 'fri' |Â 'sat'` | â | The day that starts the week. |
| `minValue` | `DateValue |Â null` | â | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | â | The maximum allowed date that a user may select. |
| `isDateUnavailable` | `( (date: DateValue )) => boolean` | â | Callback that is called for each date of the calendar. If it returns true, then the date is unavailable. |
| `placeholderValue` | `DateValue |Â null` | â | A placeholder date that influences the format of the placeholder shown when no value is selected. Defaults to today's date at midnight. |
| `hourCycle` | `12 |Â 24` | â | Whether to display the time in 12 or 24 hour format. By default, this is determined by the user's locale. |
| `granularity` | `Granularity` | â | Determines the smallest unit that is displayed in the date picker. By default, this is `"day"` for dates, and `"minute"` for times. |
| `hideTimeZone` | `boolean` | `false` | Whether to hide the time zone abbreviation. |
| `shouldForceLeadingZeros` | `boolean` | â | Whether to always show leading zeros in the month, day, and hour fields. By default, this is determined by the user's locale. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: MappedDateValue<DateValue> )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `isOpen` | `boolean` | â | Whether the overlay is open by default (controlled). |
| `defaultOpen` | `boolean` | â | Whether the overlay is open by default (uncontrolled). |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Handler that is called when the overlay's open state changes. |
| `value` | `DateValue |Â null` | â | The current value (controlled). |
| `defaultValue` | `DateValue |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: MappedDateValue<DateValue> |Â  |Â null )) => void` | â | Handler that is called when the value changes. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |

`'single' |Â 'visible'`

`'day'
|Â 'hour'
|Â 'minute'
|Â 'second'`

`'valid' |Â 'invalid'`

`DateValue extends ZonedDateTime ? ZonedDateTime :
DateValue extends CalendarDateTime ? CalendarDateTime :
DateValue extends CalendarDate ? CalendarDate : never`

`string |Â string[]`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `DateValue |Â null` | The currently selected date. |
| `defaultValue` | `DateValue |Â null` | The default date. |
| `dateValue` | `DateValue |Â null` | The date portion of the value. This may be set prior to `value` if the user has selected a date but has not yet selected a time. |
| `timeValue` | `TimeValue |Â null` | The time portion of the value. This may be set prior to `value` if the user has selected a time but has not yet selected a date. |
| `granularity` | `Granularity` | The granularity for the field, based on the `granularity` prop and current value. |
| `hasTime` | `boolean` | Whether the date picker supports selecting a time, according to the `granularity` prop and current value. |
| `isOpen` | `boolean` | Whether the calendar popover is currently open. |
| `isInvalid` | `boolean` | Whether the date picker is invalid, based on the `isInvalid`, `minValue`, and `maxValue` props. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: DateValue |Â  |Â null )): void` | Sets the selected date. |
| `setDateValue( (value: DateValue )): void` | Sets the date portion of the value. |
| `setTimeValue( (value: TimeValue )): void` | Sets the time portion of the value. |
| `setOpen( (isOpen: boolean )): void` | Sets whether the calendar popover is open. |
| `formatValue( (locale: string, , fieldOptions: FieldOptions )): string` | Formats the selected value using the given options. |
| `getDateFormatter( (locale: string, , formatOptions: FormatterOptions )): DateFormatter` | Gets a formatter based on state's props. |
| `open(): void` | Opens the overlay. |
| `close(): void` | Closes the overlay. |
| `toggle(): void` | Toggles the overlay's visibility. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

`Time
|Â CalendarDateTime
|Â ZonedDateTime`

A Time represents a clock time without any date components.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `hour` | `number` | The hour, numbered from 0 to 23. |
| `minute` | `number` | The minute in the hour. |
| `second` | `number` | The second in the minute. |
| `millisecond` | `number` | The millisecond in the second. |

### Methods

| Method | Description |
| --- | --- |
| `constructor( hour: number, minute: number, second: number, millisecond: number ): void` |  |
| `copy(): Time` | Returns a copy of this time. |
| `add( (duration: TimeDuration )): Time` | Returns a new `Time` with the given duration added to it. |
| `subtract( (duration: TimeDuration )): Time` | Returns a new `Time` with the given duration subtracted from it. |
| `set( (fields: TimeFields )): Time` | Returns a new `Time` with the given fields set to the provided values. Other fields will be constrained accordingly. |
| `cycle( field: TimeField, amount: number, options?: CycleTimeOptions ): Time` | Returns a new `Time` with the given field adjusted by a specified amount. When the resulting value reaches the limits of the field, it wraps around. |
| `toString(): string` | Converts the time to an ISO 8601 formatted string. |
| `compare( (b: AnyTime )): number` | Compares this time with another. A negative result indicates that this time is before the given one, and a positive time indicates that it is after. |

`Intl.DateTimeFormatOptions<Intl.DateTimeFormatOptions, 'year'
|Â 'month'
|Â 'day'
|Â 'hour'
|Â 'minute'
|Â 'second'>`

| Name | Type | Description |
| --- | --- | --- |
| `timeZone` | `string` |  |
| `hideTimeZone` | `boolean` |  |
| `granularity` | `DatePickerProps<any>['granularity']` |  |
| `maxGranularity` | `'year' |Â 'month' |Â DatePickerProps<any>['granularity']` |  |
| `hourCycle` | `12 |Â 24` |  |
| `showEra` | `boolean` |  |
| `shouldForceLeadingZeros` | `boolean` |  |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `pageBehavior` | `PageBehavior` | `visible` | Controls the behavior of paging. Pagination either works by advancing the visible page by visibleDuration (default) or one unit of visibleDuration. |
| `firstDayOfWeek` | `'sun' |Â 'mon' |Â 'tue' |Â 'wed' |Â 'thu' |Â 'fri' |Â 'sat'` | â | The day that starts the week. |
| `minValue` | `DateValue |Â null` | â | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | â | The maximum allowed date that a user may select. |
| `isDateUnavailable` | `( (date: DateValue )) => boolean` | â | Callback that is called for each date of the calendar. If it returns true, then the date is unavailable. |
| `placeholderValue` | `DateValue |Â null` | â | A placeholder date that influences the format of the placeholder shown when no value is selected. Defaults to today's date at midnight. |
| `hourCycle` | `12 |Â 24` | â | Whether to display the time in 12 or 24 hour format. By default, this is determined by the user's locale. |
| `granularity` | `Granularity` | â | Determines the smallest unit that is displayed in the date picker. By default, this is `"day"` for dates, and `"minute"` for times. |
| `hideTimeZone` | `boolean` | `false` | Whether to hide the time zone abbreviation. |
| `shouldForceLeadingZeros` | `boolean` | â | Whether to always show leading zeros in the month, day, and hour fields. By default, this is determined by the user's locale. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: MappedDateValue<DateValue> )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `isOpen` | `boolean` | â | Whether the overlay is open by default (controlled). |
| `defaultOpen` | `boolean` | â | Whether the overlay is open by default (uncontrolled). |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Handler that is called when the overlay's open state changes. |
| `value` | `DateValue |Â null` | â | The current value (controlled). |
| `defaultValue` | `DateValue |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: MappedDateValue<DateValue> |Â  |Â null )) => void` | â | Handler that is called when the value changes. |

A wrapper around Intl.DateTimeFormat that fixes various browser bugs, and polyfills new features.

| Method | Description |
| --- | --- |
| `constructor( (locale: string, , options: Intl.DateTimeFormatOptions )): void` |  |
| `format( (value: Date )): string` | Formats a date as a string according to the locale and format options passed to the constructor. |
| `formatToParts( (value: Date )): Intl.DateTimeFormatPart[]` | Formats a date to an array of parts such as separators, numbers, punctuation, and more. |
| `formatRange( (start: Date, , end: Date )): string` | Formats a date range as a string. |
| `formatRangeToParts( (start: Date, , end: Date )): DateRangeFormatPart[]` | Formats a date range as an array of parts. |
| `resolvedOptions(): Intl.ResolvedDateTimeFormatOptions` | Returns the resolved formatting options based on the values passed to the constructor. |

**Extends**: `Intl.DateTimeFormatPart`

| Name | Type | Description |
| --- | --- | --- |
| `source` | `'startRange' |Â 'endRange' |Â 'shared'` |  |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the date picker's visible label element, if any. |
| `groupProps` | `GroupDOMAttributes` | Props for the grouping element containing the date field and button. |
| `fieldProps` | `AriaDatePickerProps<DateValue>` | Props for the date field. |
| `buttonProps` | `AriaButtonProps` | Props for the popover trigger button. |
| `descriptionProps` | `DOMAttributes` | Props for the description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
| `dialogProps` | `AriaDialogProps` | Props for the popover dialog. |
| `calendarProps` | `CalendarProps<DateValue>` | Props for the calendar within the popover dialog. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

| Name | Type | Description |
| --- | --- | --- |
| `role` | `'group' |Â 'region' |Â 'presentation'` |  |
| `id` | `string |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDisabled` | `boolean` | â | Whether the button is disabled. |
| `children` | `ReactNode` | â | The content to display in the button. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `href` | `string` | â | A URL to link to if elementType="a". |
| `target` | `string` | â | The target window for the link. |
| `rel` | `string` | â | The relationship between the linked resource and the current page. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). |
| `elementType` | `ElementType |Â JSXElementConstructor<any>` | `'button'` | The HTML element or React element used to render the button, e.g. 'div', 'a', or `RouterLink`. |
| `aria-disabled` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element is disabled to users of assistive technology. |
| `aria-expanded` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element, or another grouping element it controls, is currently expanded or collapsed. |
| `aria-haspopup` | `boolean |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog' |Â 'true' |Â 'false'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `aria-pressed` | `boolean |Â 'true' |Â 'false' |Â 'mixed'` | â | Indicates the current "pressed" state of toggle buttons. |
| `aria-current` | `boolean |Â 'true' |Â 'false' |Â 'page' |Â 'step' |Â 'location' |Â 'date' |Â 'time'` | â | Indicates whether this element represents the current item within a container or set of related elements. |
| `type` | `'button' |Â 'submit' |Â 'reset'` | `'button'` | The behavior of the button when used in an HTML form. |
| `preventFocusOnPress` | `boolean` | â | Whether to prevent focus from moving to the button when pressing it.  Caution, this can make the button inaccessible and should only be used when alternative keyboard interaction is provided, such as ComboBox's MenuTrigger or a NumberField's increment/decrement control. |
| `form` | `string` | â | The `<form>` element to associate the button with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button#form). |
| `formAction` | `string` | â | The URL that processes the information submitted by the button. Overrides the action attribute of the button's form owner. |
| `formEncType` | `string` | â | Indicates how to encode the form data that is submitted. |
| `formMethod` | `string` | â | Indicates the HTTP method used to submit the form. |
| `formNoValidate` | `boolean` | â | Indicates that the form is not to be validated when it is submitted. |
| `formTarget` | `string` | â | Overrides the target attribute of the button's form owner. |
| `name` | `string` | â | Submitted as a pair with the button's value as part of the form data. |
| `value` | `string` | â | The value associated with the button's name when it's submitted with the form data. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` | The type of press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Methods

| Method | Description |
| --- | --- |
| `continuePropagation(): void` | By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. |

`'mouse'
|Â 'pen'
|Â 'touch'
|Â 'keyboard'
|Â 'virtual'`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `role` | `'dialog' |Â 'alertdialog'` | `'dialog'` | The accessibility role for the dialog. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `minValue` | `DateValue |Â null` | â | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | â | The maximum allowed date that a user may select. |
| `isDateUnavailable` | `( (date: DateValue )) => boolean` | â | Callback that is called for each date of the calendar. If it returns true, then the date is unavailable. |
| `isDisabled` | `boolean` | `false` | Whether the calendar is disabled. |
| `isReadOnly` | `boolean` | `false` | Whether the calendar value is immutable. |
| `autoFocus` | `boolean` | `false` | Whether to automatically focus the calendar when it mounts. |
| `focusedValue` | `DateValue |Â null` | â | Controls the currently focused date within the calendar. |
| `defaultFocusedValue` | `DateValue |Â null` | â | The date that is focused when the calendar first mounts (uncontrolled). |
| `onFocusChange` | `( (date: CalendarDate )) => void` | â | Handler that is called when the focused date changes. |
| `isInvalid` | `boolean` | â | Whether the current selection is invalid according to application logic. |
| `errorMessage` | `ReactNode` | â | An error message to display when the selected value is invalid. |
| `pageBehavior` | `PageBehavior` | `visible` | Controls the behavior of paging. Pagination either works by advancing the visible page by visibleDuration (default) or one unit of visibleDuration. |
| `firstDayOfWeek` | `'sun' |Â 'mon' |Â 'tue' |Â 'wed' |Â 'thu' |Â 'fri' |Â 'sat'` | â | The day that starts the week. |
| `selectionAlignment` | `'start' |Â 'center' |Â 'end'` | `'center'` | Determines the alignment of the visible months on initial render based on the current selection or current date if there is no selection. |
| `value` | `DateValue |Â null` | â | The current value (controlled). |
| `defaultValue` | `DateValue |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: MappedDateValue<DateValue> )) => void` | â | Handler that is called when the value changes. |

`CalendarDate
|Â CalendarDateTime
|Â ZonedDateTime`

`DateValue extends ZonedDateTime ? ZonedDateTime :
DateValue extends CalendarDateTime ? CalendarDateTime :
DateValue extends CalendarDate ? CalendarDate : never`

Provides state management for a date picker component.
A date picker combines a DateField and a Calendar popover to allow users to enter or select a date and time value.

`useDatePickerState<T extends DateValue = DateValue>(
(props: DatePickerStateOptions<T>
)): DatePickerState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `shouldCloseOnSelect` | `boolean |Â () => boolean` | `true` | Determines whether the date picker popover should close automatically when a date is selected. |
| `pageBehavior` | `PageBehavior` | `visible` | Controls the behavior of paging. Pagination either works by advancing the visible page by visibleDuration (default) or one unit of visibleDuration. |
| `firstDayOfWeek` | `'sun' |Â 'mon' |Â 'tue' |Â 'wed' |Â 'thu' |Â 'fri' |Â 'sat'` | â | The day that starts the week. |
| `minValue` | `DateValue |Â null` | â | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | â | The maximum allowed date that a user may select. |
| `isDateUnavailable` | `( (date: DateValue )) => boolean` | â | Callback that is called for each date of the calendar. If it returns true, then the date is unavailable. |
| `placeholderValue` | `DateValue |Â null` | â | A placeholder date that influences the format of the placeholder shown when no value is selected. Defaults to today's date at midnight. |
| `hourCycle` | `12 |Â 24` | â | Whether to display the time in 12 or 24 hour format. By default, this is determined by the user's locale. |
| `granularity` | `Granularity` | â | Determines the smallest unit that is displayed in the date picker. By default, this is `"day"` for dates, and `"minute"` for times. |
| `hideTimeZone` | `boolean` | `false` | Whether to hide the time zone abbreviation. |
| `shouldForceLeadingZeros` | `boolean` | â | Whether to always show leading zeros in the month, day, and hour fields. By default, this is determined by the user's locale. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: MappedDateValue<DateValue> )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `isOpen` | `boolean` | â | Whether the overlay is open by default (controlled). |
| `defaultOpen` | `boolean` | â | Whether the overlay is open by default (uncontrolled). |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Handler that is called when the overlay's open state changes. |
| `value` | `DateValue |Â null` | â | The current value (controlled). |
| `defaultValue` | `DateValue |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: MappedDateValue<DateValue> |Â  |Â null )) => void` | â | Handler that is called when the value changes. |

Provides the behavior and accessibility implementation for a date picker component.
A date picker combines a DateField and a Calendar popover to allow users to enter or select a date and time value.

`useDatePicker<T extends DateValue>(
props: AriaDatePickerProps<T>,
state: DatePickerState,
ref: RefObject<Element
|Â  |Â null>
): DatePickerAria`

Parses an ISO 8601 date string, with no time components.

`parseDate(
(value: string
)): CalendarDate`

Parses an ISO 8601 date and time string, with no time zone.

`parseDateTime(
(value: string
)): CalendarDateTime`

Parses an ISO 8601 date and time string with a time zone extension and optional UTC offset
(e.g. "2021-11-07T00:45[America/Los*Angeles]" or "2021-11-07T00:45-07:00[America/Los*Angeles]").
Ambiguous times due to daylight saving time transitions are resolved according to the `disambiguation`
parameter.

`parseZonedDateTime(
(value: string,
, disambiguation?: Disambiguation
)): ZonedDateTime`

`'compatible'
|Â 'earlier'
|Â 'later'
|Â 'reject'`

Parses an ISO 8601 date and time string with a UTC offset (e.g. "2021-11-07T07:45:00Z"
or "2021-11-07T07:45:00-07:00"). The result is converted to the provided time zone.

`parseAbsolute(
(value: string,
, timeZone: string
)): ZonedDateTime`

Parses an ISO 8601 date and time string with a UTC offset (e.g. "2021-11-07T07:45:00Z"
or "2021-11-07T07:45:00-07:00"). The result is converted to the user's local time zone.

`parseAbsoluteToLocal(
(value: string
)): ZonedDateTime`
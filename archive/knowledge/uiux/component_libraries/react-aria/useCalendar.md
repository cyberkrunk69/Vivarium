# useCalendar

Source: https://react-spectrum.adobe.com/react-aria/useCalendar.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Calendar).

# useCalendar

Provides the behavior and accessibility implementation for a calendar component.
A calendar displays one or more date grids and allows users to select a single date.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useCalendar} from 'react-aria'` |

[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/calendar "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/calendar "View package")

## API[#](#api)

---

`useCalendar<T extends DateValue>(
(props: AriaCalendarProps<T>,
, state: CalendarState
)): CalendarAria`
`useCalendarGrid(
(props: AriaCalendarGridProps,
, state: CalendarState
|Â  |Â RangeCalendarState
)): CalendarGridAria`
`useCalendarCell(
props: AriaCalendarCellProps,
state: CalendarState
|Â  |Â RangeCalendarState,
ref: RefObject<HTMLElement
|Â  |Â null>
): CalendarCellAria`

## Features[#](#features)

---

There is no standalone calendar element in HTML. `<input type="date">` is close, but this is very limited in functionality, lacking in internationalization capabilities, inconsistent between browsers, and difficult to style. `useCalendar` helps achieve accessible and international calendar components that can be styled as needed.

- **Flexible** â Display one or more months at once, or a custom time range for use cases like a week view. Minimum and maximum values, unavailable dates, and non-contiguous selections are supported as well.
- **International** â Support for 13 calendar systems used around the world, including Gregorian, Buddhist, Islamic, Persian, and more. Locale-specific formatting, number systems, and right-to-left support are available as well.
- **Accessible** â Calendar cells can be navigated and selected using the keyboard, and localized screen reader messages are included to announce when the selection and visible date range change.
- **Customizable** â As with all of React Aria, the DOM structure and styling of all elements can be fully customized.

Read our [blog post](../blog/date-and-time-pickers-for-all) for more details about the internationalization, accessibility, and user experience features implemented by `useCalendar`.

## Anatomy[#](#anatomy)

---

A calendar consists of a grouping element containing one or more date grids (e.g. months), and a previous and next button for navigating between date ranges. Each calendar grid consists of cells containing button elements that can be pressed and navigated to using the arrow keys to select a date.

### useCalendar[#](#usecalendar-1)

`useCalendar` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `calendarProps` | `DOMAttributes` | Props for the calendar grouping element. |
| `nextButtonProps` | `AriaButtonProps` | Props for the next button. |
| `prevButtonProps` | `AriaButtonProps` | Props for the previous button. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
| `title` | `string` | A description of the visible date range, for use in the calendar title. |

### useCalendarGrid[#](#usecalendargrid)

`useCalendarGrid` returns props for an individual grid of dates, such as one month, along with a list of formatted weekday names in the current locale for use during rendering:

| Name | Type | Description |
| --- | --- | --- |
| `gridProps` | `DOMAttributes` | Props for the date grid element (e.g. `<table>`). |
| `headerProps` | `DOMAttributes` | Props for the grid header element (e.g. `<thead>`). |
| `weekDays` | `string[]` | A list of week day abbreviations formatted for the current locale, typically used in column headers. |
| `weeksInMonth` | `number` | The number of weeks in the month. |

### useCalendarCell[#](#usecalendarcell)

`useCalendarCell` returns props for an individual cell, along with states and information useful during rendering:

| Name | Type | Description |
| --- | --- | --- |
| `cellProps` | `DOMAttributes` | Props for the grid cell element (e.g. `<td>`). |
| `buttonProps` | `DOMAttributes` | Props for the button element within the cell. |
| `isPressed` | `boolean` | Whether the cell is currently being pressed. |
| `isSelected` | `boolean` | Whether the cell is selected. |
| `isFocused` | `boolean` | Whether the cell is focused. |
| `isDisabled` | `boolean` | Whether the cell is disabled, according to the calendar's `minValue`, `maxValue`, and `isDisabled` props. Disabled dates are not focusable, and cannot be selected by the user. They are typically displayed with a dimmed appearance. |
| `isUnavailable` | `boolean` | Whether the cell is unavailable, according to the calendar's `isDateUnavailable` prop. Unavailable dates remain focusable, but cannot be selected by the user. They should be displayed with a visual affordance to indicate they are unavailable, such as a different color or a strikethrough.  Note that because they are focusable, unavailable dates must meet a 4.5:1 color contrast ratio, [as defined by WCAG](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html). |
| `isOutsideVisibleRange` | `boolean` | Whether the cell is outside the visible range of the calendar. For example, dates before the first day of a month in the same week. |
| `isInvalid` | `boolean` | Whether the cell is part of an invalid selection. |
| `formattedDate` | `string` | The day number formatted according to the current locale. |

State is managed by the `useCalendarState` hook from `@react-stately/calendar`. The state object should be passed as an option to `useCalendar`, `useCalendarGrid`, and `useCalendarCell`.

Note that much of this anatomy is shared with [range calendars](../RangeCalendar/useRangeCalendar.html). The only difference is that `useCalendarState` is used instead of `useRangeCalendarState`, and `useCalendar` is used instead of `useRangeCalendar`.

## Date and time values[#](#date-and-time-values)

---

Dates are represented in many different ways by cultures around the world. This includes differences in calendar systems, date formatting, numbering systems, weekday and weekend rules, and much more. When building applications that support users around the world, it is important to handle these aspects correctly for each locale.

`useCalendar` uses the [@internationalized/date](../internationalized/date/) library to represent dates and times. This package provides a library of objects and functions to perform date and time related manipulation, queries, and conversions that work across locales and calendars. Date and time objects can be converted to and from native JavaScript `Date` objects or [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) strings. See the [documentation](../internationalized/date/), or the [examples below](#value) for more details.

`useCalendarState` requires a `createCalendar` function to be provided, which is used to implement date manipulation across multiple calendar systems. The default implementation in `@internationalized/date` includes all supported calendar systems. While this library is quite small (8 kB minified + Brotli), you can reduce its bundle size further by providing your own implementation that includes only your supported calendars. See [below](#reducing-bundle-size) for an example.

## Example[#](#example)

---

A `Calendar` consists of three components: the main calendar wrapper element with previous and next buttons for navigating, one or more `CalendarGrid` components to display each month, and `CalendarCell` components for each date cell. We'll go through them one by one.

For simplicity, this example only displays a single month at a time. See the [styled examples](#styled-examples) section for more examples with multiple months, as well as other time ranges like weeks.

```
import {useCalendar, useLocale} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    createCalendar,
    ...props,
    locale
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
```

```
import {useCalendar, useLocale} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    createCalendar,
    ...props,
    locale
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
```

```
import {
  useCalendar,
  useLocale
} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function Calendar(
  props
) {
  let { locale } =
    useLocale();
  let state =
    useCalendarState({
      createCalendar,
      ...props,
      locale
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
```

### CalendarGrid[#](#calendargrid)

The `CalendarGrid` component will be responsible for rendering an individual month. It is a separate component so that you can render more than one month at a time if you like. It's rendered as an HTML `<table>` element, and React Aria takes care of adding the proper ARIA roles and event handlers to make it behave as an ARIA grid. You can use the arrow keys to navigate between cells, and the `Enter` key to select a date.

The `state.getDatesInWeek` function returns the dates in each week of the month. Note that this always includes 7 values, but some of them may be null, which indicates that the date doesn't exist within the calendar system. You should render a placeholder `<td>` element in this case so that the cells line up correctly.

**Note**: this component is the same as the `CalendarGrid` component shown in the [useRangeCalendar](../RangeCalendar/useRangeCalendar.html) docs, and you can reuse it between both `Calendar` and `RangeCalendar`.

```
import {useCalendarGrid} from 'react-aria';

function CalendarGrid({ state, ...props }) {
  let { gridProps, headerProps, weekDays, weeksInMonth } = useCalendarGrid(
    props,
    state
  );

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
```

```
import {useCalendarGrid} from 'react-aria';

function CalendarGrid({ state, ...props }) {
  let { gridProps, headerProps, weekDays, weeksInMonth } =
    useCalendarGrid(props, state);

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
```

```
import {useCalendarGrid} from 'react-aria';

function CalendarGrid(
  { state, ...props }
) {
  let {
    gridProps,
    headerProps,
    weekDays,
    weeksInMonth
  } = useCalendarGrid(
    props,
    state
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
```

### CalendarCell[#](#calendarcell)

Finally, the `CalendarCell` component renders an individual cell in a calendar. It consists of two elements: a `<td>` to represent the grid cell, and a `<div>` to represent a button that can be clicked to select the date. The `useCalendarCell` hook also returns the formatted date string in the current locale, as well as some information about the cell's state that can be useful for styling. See [above](#usecalendarcell) for details.

**Note**: this component is the same as the `CalendarCell` component shown in the [useRangeCalendar](../RangeCalendar/useRangeCalendar.html) docs, and you can reuse it between both `Calendar` and `RangeCalendar`.

```
import {useCalendarCell} from 'react-aria';

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
import {useCalendarCell} from 'react-aria';

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
import {useCalendarCell} from 'react-aria';

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

That's it! Now we can render an example of our `Calendar` component in action.

```
<Calendar aria-label="Event date" />
```

```
<Calendar aria-label="Event date" />
```

```
<Calendar aria-label="Event date" />
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

### Button[#](#button)

The `Button` component is used in the above example to navigate between months. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

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

## Styled Examples[#](#styled-examples)

---

[![](/calendar-tailwind.cfd9a5be.png)

Tailwind CSS

A Calendar built with Tailwind, supporting multiple visible months.](https://codesandbox.io/s/objective-shape-8r4utm?file=/src/Calendar.js)
[![](/styled-components.18511cb1.png)

Styled Components

A week view component, built with Styled Components.](https://codesandbox.io/s/stupefied-almeida-01yvsp?file=/src/WeekView.js)
[![](/css-modules.ecac7505.png)

CSS Modules

A Calendar with custom month and year dropdowns, styled with CSS Modules.](https://codesandbox.io/s/affectionate-rosalind-tdm323?file=/src/Calendar.js)

## Usage[#](#usage)

---

The following examples show how to use the `Calendar` component created in the above example.

### Value[#](#value)

A `Calendar` has no selection by default. An initial, uncontrolled value can be provided to the `Calendar` using the `defaultValue` prop. Alternatively, a controlled value can be provided using the `value` prop.

Date values are provided using objects in the [@internationalized/date](../internationalized/date/) package. This library handles correct international date manipulation across calendars, time zones, and other localization concerns.

`useCalendar` supports values with both date and time components, but only allows users to modify the date. By default, `useCalendar` will emit `CalendarDate` objects in the `onChange` event, but if a `CalendarDateTime` or `ZonedDateTime` object is passed as the `value` or `defaultValue`, values of that type will be emitted, changing only the date and preserving the time components.

```
import {parseDate} from '@internationalized/date';

function Example() {
  let [value, setValue] = React.useState(parseDate('2020-02-03'));

  return (
    <div style={{display: 'flex', gap: 20, flexWrap: 'wrap'}}>
      <Calendar
        aria-label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')} />
      <Calendar
        aria-label="Date (controlled)"
        value={value}
        onChange={setValue} />
    </div>
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
    <div
      style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}
    >
      <Calendar
        aria-label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')}
      />
      <Calendar
        aria-label="Date (controlled)"
        value={value}
        onChange={setValue}
      />
    </div>
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
    <div
      style={{
        display: 'flex',
        gap: 20,
        flexWrap: 'wrap'
      }}
    >
      <Calendar
        aria-label="Date (uncontrolled)"
        defaultValue={parseDate(
          '2020-02-03'
        )}
      />
      <Calendar
        aria-label="Date (controlled)"
        value={value}
        onChange={setValue}
      />
    </div>
  );
}
```

### Events[#](#events)

`useCalendar` accepts an `onChange` prop which is triggered whenever a date is selected by the user. The example below uses `onChange` to update a separate element with a formatted version of the date in the user's locale. This is done by converting the date to a native JavaScript `Date` object to pass to the formatter.

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] = React.useState(parseDate('2022-07-04'));
  let formatter = useDateFormatter({ dateStyle: 'full' });

  return (
    <>
      <Calendar aria-label="Event date" value={date} onChange={setDate} />
      <p>Selected date: {formatter.format(date.toDate(getLocalTimeZone()))}</p>
    </>
  );
}
```

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] = React.useState(
    parseDate('2022-07-04')
  );
  let formatter = useDateFormatter({ dateStyle: 'full' });

  return (
    <>
      <Calendar
        aria-label="Event date"
        value={date}
        onChange={setDate}
      />
      <p>
        Selected date:{' '}
        {formatter.format(date.toDate(getLocalTimeZone()))}
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
        '2022-07-04'
      )
    );
  let formatter =
    useDateFormatter({
      dateStyle: 'full'
    });

  return (
    <>
      <Calendar
        aria-label="Event date"
        value={date}
        onChange={setDate}
      />
      <p>
        Selected date:
        {' '}
        {formatter
          .format(
            date.toDate(
              getLocalTimeZone()
            )
          )}
      </p>
    </>
  );
}
```

### International calendars[#](#international-calendars)

`useCalendar` supports selecting dates in many calendar systems used around the world, including Gregorian, Hebrew, Indian, Islamic, Buddhist, and more. Dates are automatically displayed in the appropriate calendar system for the user's locale. The calendar system can be overridden using the [Unicode calendar locale extension](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/calendar#adding_a_calendar_in_the_locale_string), passed to the [I18nProvider](../I18nProvider) component.

Selected dates passed to `onChange` always use the same calendar system as the `value` or `defaultValue` prop. If no `value` or `defaultValue` is provided, then dates passed to `onChange` are always in the Gregorian calendar since this is the most commonly used. This means that even though the user selects dates in their local calendar system, applications are able to deal with dates from all users consistently.

The below example displays a `Calendar` in the Hindi language, using the Indian calendar. Dates emitted from `onChange` are in the Gregorian calendar.

```
import {I18nProvider} from 'react-aria';

function Example() {
  let [date, setDate] = React.useState(null);
  return (
    <I18nProvider locale="hi-IN-u-ca-indian">
      <Calendar aria-label="Date" value={date} onChange={setDate} />
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
      <Calendar
        aria-label="Date"
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
      <Calendar
        aria-label="Date"
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

### Custom calendar systems[#](#custom-calendar-systems)

`Calendar` also supports custom calendar systems that implement custom business rules. An example would be a fiscal year calendar that follows a [4-5-4 format](https://nrf.com/resources/4-5-4-calendar), where month ranges don't follow the usual Gregorian calendar.

The `createCalendar` prop accepts a function that returns an instance of the `Calendar` interface. See the [@internationalized/date docs](../internationalized/date/Calendar.html#custom-calendars) for an example implementation.

```
import {GregorianCalendar} from '@internationalized/date';

function Example() {
  return (
    <Calendar
      firstDayOfWeek="sun"
      createCalendar={() => new Custom454()}
    />
  );
}

class Custom454 extends GregorianCalendar {
  // See @internationalized/date docs linked above...
}
```

```
import {GregorianCalendar} from '@internationalized/date';

function Example() {
  return (
    <Calendar
      firstDayOfWeek="sun"
      createCalendar={() => new Custom454()}
    />
  );
}

class Custom454 extends GregorianCalendar {
  // See @internationalized/date docs linked above...
}
```

```
import {GregorianCalendar} from '@internationalized/date';

function Example() {
  return (
    <Calendar
      firstDayOfWeek="sun"
      createCalendar={() =>
        new Custom454()}
    />
  );
}

class Custom454
  extends GregorianCalendar {
  // See @internationalized/date docs linked above...
}
```

### Validation[#](#validation)

By default, `useCalendar` allows selecting any date. The `minValue` and `maxValue` props can also be used to prevent the user from selecting dates outside a certain range.

This example only accepts dates after today.

```
import {today} from '@internationalized/date';

<Calendar
  aria-label="Appointment date"
  minValue={today(getLocalTimeZone())}
/>
```

```
import {today} from '@internationalized/date';

<Calendar
  aria-label="Appointment date"
  minValue={today(getLocalTimeZone())}
/>
```

```
import {today} from '@internationalized/date';

<Calendar
  aria-label="Appointment date"
  minValue={today(
    getLocalTimeZone()
  )}
/>
```

### Unavailable dates[#](#unavailable-dates)

`useCalendar` supports marking certain dates as *unavailable*. These dates remain focusable with the keyboard so that navigation is consistent, but cannot be selected by the user. In this example, they are displayed in red. The `isDateUnavailable` prop accepts a callback that is called to evaluate whether each visible date is unavailable.

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
    <Calendar
      aria-label="Appointment date"
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
    <Calendar
      aria-label="Appointment date"
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
    <Calendar
      aria-label="Appointment date"
      minValue={today(
        getLocalTimeZone()
      )}
      isDateUnavailable={isDateUnavailable}
    />
  );
}
```

### Controlling the focused date[#](#controlling-the-focused-date)

By default, the selected date is focused when a `Calendar` first mounts. If no `value` or `defaultValue` prop is provided, then the current date is focused. However, `useCalendar` supports controlling which date is focused using the `focusedValue` and `onFocusChange` props. This also determines which month is visible. The `defaultFocusedValue` prop allows setting the initial focused date when the `Calendar` first mounts, without controlling it.

This example focuses July 1, 2021 by default. The user may change the focused date, and the `onFocusChange` event updates the state. Clicking the button resets the focused date back to the initial value.

```
import {CalendarDate} from '@internationalized/date';

function Example() {
  let defaultDate = new CalendarDate(2021, 7, 1);
  let [focusedDate, setFocusedDate] = React.useState(defaultDate);

  return (
    <div style={{ flexDirection: 'column', alignItems: 'start', gap: 20 }}>
      <button onClick={() => setFocusedDate(defaultDate)}>
        Reset focused date
      </button>
      <Calendar focusedValue={focusedDate} onFocusChange={setFocusedDate} />
    </div>
  );
}
```

```
import {CalendarDate} from '@internationalized/date';

function Example() {
  let defaultDate = new CalendarDate(2021, 7, 1);
  let [focusedDate, setFocusedDate] = React.useState(
    defaultDate
  );

  return (
    <div
      style={{
        flexDirection: 'column',
        alignItems: 'start',
        gap: 20
      }}
    >
      <button onClick={() => setFocusedDate(defaultDate)}>
        Reset focused date
      </button>
      <Calendar
        focusedValue={focusedDate}
        onFocusChange={setFocusedDate}
      />
    </div>
  );
}
```

```
import {CalendarDate} from '@internationalized/date';

function Example() {
  let defaultDate =
    new CalendarDate(
      2021,
      7,
      1
    );
  let [
    focusedDate,
    setFocusedDate
  ] = React.useState(
    defaultDate
  );

  return (
    <div
      style={{
        flexDirection:
          'column',
        alignItems:
          'start',
        gap: 20
      }}
    >
      <button
        onClick={() =>
          setFocusedDate(
            defaultDate
          )}
      >
        Reset focused
        date
      </button>
      <Calendar
        focusedValue={focusedDate}
        onFocusChange={setFocusedDate}
      />
    </div>
  );
}
```

### Disabled[#](#disabled)

The `isDisabled` boolean prop makes the Calendar disabled. Cells cannot be focused or selected.

```
<Calendar aria-label="Event date" isDisabled />
```

```
<Calendar aria-label="Event date" isDisabled />
```

```
<Calendar
  aria-label="Event date"
  isDisabled
/>
```

### Read only[#](#read-only)

The `isReadOnly` boolean prop makes the Calendar's value immutable. Unlike `isDisabled`, the Calendar remains focusable.

```
<Calendar
  aria-label="Event date"
  value={today(getLocalTimeZone())}
  isReadOnly
/>
```

```
<Calendar
  aria-label="Event date"
  value={today(getLocalTimeZone())}
  isReadOnly
/>
```

```
<Calendar
  aria-label="Event date"
  value={today(
    getLocalTimeZone()
  )}
  isReadOnly
/>
```

### Custom first day of week[#](#custom-first-day-of-week)

By default, the first day of the week is automatically set based on the current locale. This can be changed by setting the `firstDayOfWeek` prop to `'sun'`, `'mon'`, `'tue'`, `'wed'`, `'thu'`, `'fri'`, or `'sat'`.

```
<Calendar
  aria-label="Event date"
  value={today(getLocalTimeZone())}
  firstDayOfWeek="mon"
/>
```

```
<Calendar
  aria-label="Event date"
  value={today(getLocalTimeZone())}
  firstDayOfWeek="mon"
/>
```

```
<Calendar
  aria-label="Event date"
  value={today(
    getLocalTimeZone()
  )}
  firstDayOfWeek="mon"
/>
```

### Labeling[#](#labeling)

An aria-label must be provided to the `Calendar` for accessibility. If it is labeled by a separate element, an `aria-labelledby` prop must be provided using the `id` of the labeling element instead.

### Internationalization[#](#internationalization)

In order to internationalize a `Calendar`, a localized string should be passed to the `aria-label` prop. For languages that are read right-to-left (e.g. Hebrew and Arabic), keyboard navigation is automatically flipped. Ensure that your CSS accounts for this as well. Dates are automatically formatted using the current locale.

## Advanced topics[#](#advanced-topics)

---

### Reducing bundle size[#](#reducing-bundle-size)

In the example above, the `createCalendar` function from the [@internationalized/date](../internationalized/date/) package is passed to the `useCalendarState` hook. This function receives a [calendar identifier](../internationalized/date/Calendar.html#calendar-identifiers) string, and provides `Calendar` instances to React Stately, which are used to implement date manipulation.

By default, this includes [all calendar systems](../internationalized/date/Calendar.html#implementations) supported by `@internationalized/date`. However, if your application supports a more limited set of regions, or you know you will only be picking dates in a certain calendar system, you can reduce your bundle size by providing your own implementation of `createCalendar` that includes a subset of these `Calendar` implementations.

For example, if your application only supports Gregorian dates, you could implement a `createCalendar` function like this:

```
import {useLocale} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {GregorianCalendar} from '@internationalized/date';

function createCalendar(identifier) {
  switch (identifier) {
    case 'gregory':
      return new GregorianCalendar();
    default:
      throw new Error(`Unsupported calendar ${identifier}`);
  }
}

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    ...props,
    locale,
    createCalendar
  });

  // ...
}
```

```
import {useLocale} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {GregorianCalendar} from '@internationalized/date';

function createCalendar(identifier) {
  switch (identifier) {
    case 'gregory':
      return new GregorianCalendar();
    default:
      throw new Error(`Unsupported calendar ${identifier}`);
  }
}

function Calendar(props) {
  let { locale } = useLocale();
  let state = useCalendarState({
    ...props,
    locale,
    createCalendar
  });

  // ...
}
```

```
import {useLocale} from 'react-aria';
import {useCalendarState} from 'react-stately';
import {GregorianCalendar} from '@internationalized/date';

function createCalendar(
  identifier
) {
  switch (identifier) {
    case 'gregory':
      return new GregorianCalendar();
    default:
      throw new Error(
        `Unsupported calendar ${identifier}`
      );
  }
}

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

  // ...
}
```

This way, only `GregorianCalendar` is imported, and the other calendar implementations can be tree-shaken.

See the [Calendar](../internationalized/date/Calendar.html) documentation in `@internationalized/date` to learn more about the supported calendar systems, and a list of string identifiers.

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
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

`'valid' |Â 'invalid'`

`'single' |Â 'visible'`

`DateValue extends ZonedDateTime ? ZonedDateTime :
DateValue extends CalendarDateTime ? CalendarDateTime :
DateValue extends CalendarDate ? CalendarDate : never`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `CalendarDate |Â null` | The currently selected date. |
| `isDisabled` | `boolean` | Whether the calendar is disabled. |
| `isReadOnly` | `boolean` | Whether the calendar is in a read only state. |
| `visibleRange` | `RangeValue<CalendarDate>` | The date range that is currently visible in the calendar. |
| `timeZone` | `string` | The time zone of the dates currently being displayed. |
| `isValueInvalid` | `boolean` | Whether the calendar is invalid. |
| `focusedDate` | `CalendarDate` | The currently focused date. |
| `isFocused` | `boolean` | Whether focus is currently within the calendar. |
| `minValue` | `DateValue |Â null` | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | The maximum allowed date that a user may select. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: CalendarDate |Â  |Â null )): void` | Sets the currently selected date. |
| `setFocusedDate( (value: CalendarDate )): void` | Sets the focused date. |
| `focusNextDay(): void` | Moves focus to the next calendar date. |
| `focusPreviousDay(): void` | Moves focus to the previous calendar date. |
| `focusNextRow(): void` | Moves focus to the next row of dates, e.g. the next week. |
| `focusPreviousRow(): void` | Moves focus to the previous row of dates, e.g. the previous work. |
| `focusNextPage(): void` | Moves focus to the next page of dates, e.g. the next month if one month is visible. |
| `focusPreviousPage(): void` | Moves focus to the previous page of dates, e.g. the previous month if one month is visible. |
| `focusSectionStart(): void` | Moves focus to the start of the current section of dates, e.g. the start of the current month. |
| `focusSectionEnd(): void` | Moves focus to the end of the current section of dates, e.g. the end of the current month month. |
| `focusNextSection( (larger?: boolean )): void` | Moves focus to the next section of dates based on what is currently displayed. By default, focus is moved by one of the currently displayed unit. For example, if one or more months are displayed, then focus is moved forward by one month. If the `larger` option is `true`, the focus is moved by the next larger unit than the one displayed. For example, if months are displayed, then focus moves to the next year. |
| `focusPreviousSection( (larger?: boolean )): void` | Moves focus to the previous section of dates based on what is currently displayed. By default, focus is moved by one of the currently displayed unit. For example, if one or more months are displayed, then focus is moved backward by one month. If the `larger` option is `true`, the focus is moved by the next larger unit than the one displayed. For example, if months are displayed, then focus moves to the previous year. |
| `selectFocusedDate(): void` | Selects the currently focused date. |
| `selectDate( (date: CalendarDate )): void` | Selects the given date. |
| `setFocused( (value: boolean )): void` | Sets whether focus is currently within the calendar. |
| `isInvalid( (date: CalendarDate )): boolean` | Returns whether the given date is invalid according to the `minValue` and `maxValue` props. |
| `isSelected( (date: CalendarDate )): boolean` | Returns whether the given date is currently selected. |
| `isCellFocused( (date: CalendarDate )): boolean` | Returns whether the given date is currently focused. |
| `isCellDisabled( (date: CalendarDate )): boolean` | Returns whether the given date is disabled according to the `minValue,`maxValue`, and`isDisabled` props. |
| `isCellUnavailable( (date: CalendarDate )): boolean` | Returns whether the given date is unavailable according to the `isDateUnavailable` prop. |
| `isPreviousVisibleRangeInvalid(): boolean` | Returns whether the previous visible date range is allowed to be selected according to the `minValue` prop. |
| `isNextVisibleRangeInvalid(): boolean` | Returns whether the next visible date range is allowed to be selected according to the `maxValue` prop. |
| `getDatesInWeek( (weekIndex: number, , startDate?: CalendarDate )): Array<CalendarDate |Â null>` | Returns an array of dates in the week index counted from the provided start date, or the first visible date if not given. The returned array always has 7 elements, but may include null if the date does not exist according to the calendar system. |

| Name | Type | Description |
| --- | --- | --- |
| `start` | `T` | The start value of the range. |
| `end` | `T` | The end value of the range. |

| Name | Type | Description |
| --- | --- | --- |
| `calendarProps` | `DOMAttributes` | Props for the calendar grouping element. |
| `nextButtonProps` | `AriaButtonProps` | Props for the next button. |
| `prevButtonProps` | `AriaButtonProps` | Props for the previous button. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
| `title` | `string` | A description of the visible date range, for use in the calendar title. |

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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `startDate` | `CalendarDate` | â | The first date displayed in the calendar grid. Defaults to the first visible date in the calendar. Override this to display multiple date grids in a calendar. |
| `endDate` | `CalendarDate` | â | The last date displayed in the calendar grid. Defaults to the last visible date in the calendar. Override this to display multiple date grids in a calendar. |
| `weekdayStyle` | `'narrow' |Â 'short' |Â 'long'` | `"narrow"` | The style of weekday names to display in the calendar grid header, e.g. single letter, abbreviation, or full day name. |
| `firstDayOfWeek` | `'sun' |Â 'mon' |Â 'tue' |Â 'wed' |Â 'thu' |Â 'fri' |Â 'sat'` | â | The day that starts the week. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `RangeValue<DateValue> |Â null` | The currently selected date range. |
| `anchorDate` | `CalendarDate |Â null` | The current anchor date that the user clicked on to begin range selection. |
| `highlightedRange` | `RangeValue<CalendarDate> |Â null` | The currently highlighted date range. |
| `isDragging` | `boolean` | Whether the user is currently dragging over the calendar. |
| `isDisabled` | `boolean` | Whether the calendar is disabled. |
| `isReadOnly` | `boolean` | Whether the calendar is in a read only state. |
| `visibleRange` | `RangeValue<CalendarDate>` | The date range that is currently visible in the calendar. |
| `timeZone` | `string` | The time zone of the dates currently being displayed. |
| `isValueInvalid` | `boolean` | Whether the calendar is invalid. |
| `focusedDate` | `CalendarDate` | The currently focused date. |
| `isFocused` | `boolean` | Whether focus is currently within the calendar. |
| `minValue` | `DateValue |Â null` | The minimum allowed date that a user may select. |
| `maxValue` | `DateValue |Â null` | The maximum allowed date that a user may select. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: RangeValue<DateValue> |Â  |Â null )): void` | Sets the currently selected date range. |
| `highlightDate( (date: CalendarDate )): void` | Highlights the given date during selection, e.g. by hovering or dragging. |
| `setAnchorDate( (date: CalendarDate |Â  |Â null )): void` | Sets the anchor date that the user clicked on to begin range selection. |
| `setDragging( (isDragging: boolean )): void` | Sets whether the user is dragging over the calendar. |
| `setFocusedDate( (value: CalendarDate )): void` | Sets the focused date. |
| `focusNextDay(): void` | Moves focus to the next calendar date. |
| `focusPreviousDay(): void` | Moves focus to the previous calendar date. |
| `focusNextRow(): void` | Moves focus to the next row of dates, e.g. the next week. |
| `focusPreviousRow(): void` | Moves focus to the previous row of dates, e.g. the previous work. |
| `focusNextPage(): void` | Moves focus to the next page of dates, e.g. the next month if one month is visible. |
| `focusPreviousPage(): void` | Moves focus to the previous page of dates, e.g. the previous month if one month is visible. |
| `focusSectionStart(): void` | Moves focus to the start of the current section of dates, e.g. the start of the current month. |
| `focusSectionEnd(): void` | Moves focus to the end of the current section of dates, e.g. the end of the current month month. |
| `focusNextSection( (larger?: boolean )): void` | Moves focus to the next section of dates based on what is currently displayed. By default, focus is moved by one of the currently displayed unit. For example, if one or more months are displayed, then focus is moved forward by one month. If the `larger` option is `true`, the focus is moved by the next larger unit than the one displayed. For example, if months are displayed, then focus moves to the next year. |
| `focusPreviousSection( (larger?: boolean )): void` | Moves focus to the previous section of dates based on what is currently displayed. By default, focus is moved by one of the currently displayed unit. For example, if one or more months are displayed, then focus is moved backward by one month. If the `larger` option is `true`, the focus is moved by the next larger unit than the one displayed. For example, if months are displayed, then focus moves to the previous year. |
| `selectFocusedDate(): void` | Selects the currently focused date. |
| `selectDate( (date: CalendarDate )): void` | Selects the given date. |
| `setFocused( (value: boolean )): void` | Sets whether focus is currently within the calendar. |
| `isInvalid( (date: CalendarDate )): boolean` | Returns whether the given date is invalid according to the `minValue` and `maxValue` props. |
| `isSelected( (date: CalendarDate )): boolean` | Returns whether the given date is currently selected. |
| `isCellFocused( (date: CalendarDate )): boolean` | Returns whether the given date is currently focused. |
| `isCellDisabled( (date: CalendarDate )): boolean` | Returns whether the given date is disabled according to the `minValue,`maxValue`, and`isDisabled` props. |
| `isCellUnavailable( (date: CalendarDate )): boolean` | Returns whether the given date is unavailable according to the `isDateUnavailable` prop. |
| `isPreviousVisibleRangeInvalid(): boolean` | Returns whether the previous visible date range is allowed to be selected according to the `minValue` prop. |
| `isNextVisibleRangeInvalid(): boolean` | Returns whether the next visible date range is allowed to be selected according to the `maxValue` prop. |
| `getDatesInWeek( (weekIndex: number, , startDate?: CalendarDate )): Array<CalendarDate |Â null>` | Returns an array of dates in the week index counted from the provided start date, or the first visible date if not given. The returned array always has 7 elements, but may include null if the date does not exist according to the calendar system. |

| Name | Type | Description |
| --- | --- | --- |
| `gridProps` | `DOMAttributes` | Props for the date grid element (e.g. `<table>`). |
| `headerProps` | `DOMAttributes` | Props for the grid header element (e.g. `<thead>`). |
| `weekDays` | `string[]` | A list of week day abbreviations formatted for the current locale, typically used in column headers. |
| `weeksInMonth` | `number` | The number of weeks in the month. |

| Name | Type | Description |
| --- | --- | --- |
| `date` | `CalendarDate` | The date that this cell represents. |
| `isDisabled` | `boolean` | Whether the cell is disabled. By default, this is determined by the Calendar's `minValue`, `maxValue`, and `isDisabled` props. |
| `isOutsideMonth` | `boolean` | Whether the cell is outside of the current month. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `cellProps` | `DOMAttributes` | Props for the grid cell element (e.g. `<td>`). |
| `buttonProps` | `DOMAttributes` | Props for the button element within the cell. |
| `isPressed` | `boolean` | Whether the cell is currently being pressed. |
| `isSelected` | `boolean` | Whether the cell is selected. |
| `isFocused` | `boolean` | Whether the cell is focused. |
| `isDisabled` | `boolean` | Whether the cell is disabled, according to the calendar's `minValue`, `maxValue`, and `isDisabled` props. Disabled dates are not focusable, and cannot be selected by the user. They are typically displayed with a dimmed appearance. |
| `isUnavailable` | `boolean` | Whether the cell is unavailable, according to the calendar's `isDateUnavailable` prop. Unavailable dates remain focusable, but cannot be selected by the user. They should be displayed with a visual affordance to indicate they are unavailable, such as a different color or a strikethrough.  Note that because they are focusable, unavailable dates must meet a 4.5:1 color contrast ratio, [as defined by WCAG](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html). |
| `isOutsideVisibleRange` | `boolean` | Whether the cell is outside the visible range of the calendar. For example, dates before the first day of a month in the same week. |
| `isInvalid` | `boolean` | Whether the cell is part of an invalid selection. |
| `formattedDate` | `string` | The day number formatted according to the current locale. |

Provides state management for a calendar component.
A calendar displays one or more date grids and allows users to select a single date.

`useCalendarState<T extends DateValue = DateValue>(
(props: CalendarStateOptions<T>
)): CalendarState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `locale` | `string` | â | The locale to display and edit the value according to. |
| `createCalendar` | `( (name: CalendarIdentifier )) => Calendar` | â | A function that creates a [Calendar](../internationalized/date/Calendar.html) object for a given calendar identifier. Such a function may be imported from the `@internationalized/date` package, or manually implemented to include support for only certain calendars. |
| `visibleDuration` | `DateDuration` | `{months: 1}` | The amount of days that will be displayed at once. This affects how pagination works. |
| `selectionAlignment` | `'start' |Â 'center' |Â 'end'` | `'center'` | Determines the alignment of the visible months on initial render based on the current selection or current date if there is no selection. |
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
| `value` | `DateValue |Â null` | â | The current value (controlled). |
| `defaultValue` | `DateValue |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: MappedDateValue<DateValue> )) => void` | â | Handler that is called when the value changes. |

`'gregory'
|Â 'buddhist'
|Â 'chinese'
|Â 'coptic'
|Â 'dangi'
|Â 'ethioaa'
|Â 'ethiopic'
|Â 'hebrew'
|Â 'indian'
|Â 'islamic'
|Â 'islamic-umalqura'
|Â 'islamic-tbla'
|Â 'islamic-civil'
|Â 'islamic-rgsa'
|Â 'iso8601'
|Â 'japanese'
|Â 'persian'
|Â 'roc'`

The Calendar interface represents a calendar system, including information
about how days, months, years, and eras are organized, and methods to perform
arithmetic on dates.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `identifier` | `CalendarIdentifier` | A string identifier for the calendar, as defined by Unicode CLDR. See [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/supportedValuesOf#supported_calendar_types). |

### Methods

| Method | Description |
| --- | --- |
| `fromJulianDay( (jd: number )): CalendarDate` | Creates a CalendarDate in this calendar from the given Julian day number. |
| `toJulianDay( (date: AnyCalendarDate )): number` | Converts a date in this calendar to a Julian day number. |
| `getDaysInMonth( (date: AnyCalendarDate )): number` | Returns the number of days in the month of the given date. |
| `getMonthsInYear( (date: AnyCalendarDate )): number` | Returns the number of months in the year of the given date. |
| `getYearsInEra( (date: AnyCalendarDate )): number` | Returns the number of years in the era of the given date. |
| `getEras(): string[]` | Returns a list of era identifiers for the calendar. |
| `getMinimumMonthInYear( (date: AnyCalendarDate )): number` | Returns the minimum month number of the given date's year. Normally, this is 1, but in some calendars such as the Japanese, eras may begin in the middle of a year. |
| `getMinimumDayInMonth( (date: AnyCalendarDate )): number` | Returns the minimum day number of the given date's month. Normally, this is 1, but in some calendars such as the Japanese, eras may begin in the middle of a month. |
| `getFormattableMonth( (date: AnyCalendarDate )): CalendarDate` | Returns a date that is the first day of the month for the given date. This is used to determine the month that the given date falls in, if the calendar has months that do not align with the standard calendar months (e.g. fiscal calendars). |
| `isEqual( (calendar: Calendar )): boolean` | Returns whether the given calendar is the same as this calendar. |

An interface that is compatible with any object with date fields.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `calendar` | `Calendar` |  |
| `era` | `string` |  |
| `year` | `number` |  |
| `month` | `number` |  |
| `day` | `number` |  |

### Methods

| Method | Description |
| --- | --- |
| `copy(): this` |  |

Represents an amount of time in calendar-specific units, for use when performing arithmetic.

| Name | Type | Description |
| --- | --- | --- |
| `years` | `number` | The number of years to add or subtract. |
| `months` | `number` | The number of months to add or subtract. |
| `weeks` | `number` | The number of weeks to add or subtract. |
| `days` | `number` | The number of days to add or subtract. |

Provides the behavior and accessibility implementation for a calendar component.
A calendar displays one or more date grids and allows users to select a single date.

`useCalendar<T extends DateValue>(
(props: AriaCalendarProps<T>,
, state: CalendarState
)): CalendarAria`

Creates a `Calendar` instance from a Unicode calendar identifier string.

`createCalendar(
(name: CalendarIdentifier
)): Calendar`
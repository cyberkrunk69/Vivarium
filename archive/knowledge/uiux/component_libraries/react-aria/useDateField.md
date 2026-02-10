# useDateField

Source: https://react-spectrum.adobe.com/react-aria/useDateField.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../DateField).

# useDateField

Provides the behavior and accessibility implementation for a date field component.
A date field allows users to enter and edit date and time values using a keyboard.
Each part of a date value is displayed in an individually editable segment.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useDateField} from 'react-aria'` |

[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/datepicker "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/datepicker "View package")

## API[#](#api)

---

`useDateField<T extends DateValue>(
props: AriaDateFieldOptions<T>,
state: DateFieldState,
ref: RefObject<Element
|Â  |Â null>
): DateFieldAria`
`useDateSegment(
segment: DateSegment,
state: DateFieldState,
ref: RefObject<HTMLElement
|Â  |Â null>
): DateSegmentAria`

## Features[#](#features)

---

A date field can be built using `<input type="date">`, but this is very limited in functionality, lacking in internationalization capabilities, inconsistent between browsers, and difficult to style. `useDateField` helps achieve accessible and international date and time fields that can be styled as needed.

- **Dates and times** â Support for dates and times with configurable granularity.
- **International** â Support for 13 calendar systems used around the world, including Gregorian, Buddhist, Islamic, Persian, and more. Locale-specific formatting, number systems, hour cycles, and right-to-left support are available as well.
- **Time zone aware** â Dates and times can optionally include a time zone. All modifications follow time zone rules such as daylight saving time.
- **Accessible** â Each date and time unit is displayed as an individually focusable and editable segment, which allows users an easy way to edit dates using the keyboard, in any date format and locale.
- **Touch friendly** â Date segments are editable using an easy to use numeric keypad, and all interactions are accessible using touch-based screen readers.
- **Customizable** â As with all of React Aria, the DOM structure and styling of all elements can be fully customized.

Read our [blog post](../blog/date-and-time-pickers-for-all) for more details about the internationalization, accessibility, and user experience features implemented by `useDateField`.

## Anatomy[#](#anatomy)

---

A date field consists of a label, and a group of segments representing each unit of a date and time (e.g. years, months, days, etc.). Each segment is individually focusable and editable by the user, by typing or using the arrow keys to increment and decrement the value. This approach allows values to be formatted and parsed correctly regardless of the locale or date format, and offers an easy and error-free way to edit dates using the keyboard.

`useDateField` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useDateField` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the field's visible label element, if any. |
| `fieldProps` | `GroupDOMAttributes` | Props for the field grouping element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the hidden input element for HTML form submission. |
| `descriptionProps` | `DOMAttributes` | Props for the description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

`useDateSegment` returns props for an individual date segment:

| Name | Type | Description |
| --- | --- | --- |
| `segmentProps` | `React.HTMLAttributes<HTMLDivElement>` | Props for the segment element. |

Note that most of this anatomy is shared with [useTimeField](../TimeField/useTimeField.html), so you can reuse many components between them if you have both.

State is managed by the `useDateFieldState` hook from `@react-stately/datepicker`.
The state object should be passed as an option to `useDateField` and `useDateSegment`.

If the date field does not have a visible label, an `aria-label` or `aria-labelledby` prop must be passed instead to
identify it to assistive technology.

## Date and time values[#](#date-and-time-values)

---

Dates and times are represented in many different ways by cultures around the world. This includes differences in calendar systems, time zones, daylight saving time rules, date and time formatting, weekday and weekend rules, and much more. When building applications that support users around the world, it is important to handle these aspects correctly for each locale.

`useDateField` uses the [@internationalized/date](../internationalized/date/) library to represent dates and times. This package provides a library of objects and functions to perform date and time related manipulation, queries, and conversions that work across locales and calendars. Date and time objects can be converted to and from native JavaScript `Date` objects or [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) strings. See the [documentation](../internationalized/date/), or the [examples below](#value) for more details.

`useDateFieldState` requires a `createCalendar` function to be provided, which is used to implement date manipulation across multiple calendar systems. The default implementation in `@internationalized/date` includes all supported calendar systems. While this library is quite small (8 kB minified + Brotli), you can reduce its bundle size further by providing your own implementation that includes only your supported calendars. See [below](#reducing-bundle-size) for an example.

## Example[#](#example)

---

```
import {useDateField, useDateSegment, useLocale} from 'react-aria';
import {useDateFieldState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

export function DateField(props) {
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
    <span
      {...segmentProps}
      ref={ref}
      className={`segment ${segment.isPlaceholder ? 'placeholder' : ''}`}
    >
      {segment.text}
    </span>
  );
}

<DateField label="Event date" />
```

```
import {
  useDateField,
  useDateSegment,
  useLocale
} from 'react-aria';
import {useDateFieldState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

export function DateField(props) {
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
    <span
      {...segmentProps}
      ref={ref}
      className={`segment ${
        segment.isPlaceholder ? 'placeholder' : ''
      }`}
    >
      {segment.text}
    </span>
  );
}

<DateField label="Event date" />
```

```
import {
  useDateField,
  useDateSegment,
  useLocale
} from 'react-aria';
import {useDateFieldState} from 'react-stately';
import {createCalendar} from '@internationalized/date';

export function DateField(
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
    <span
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
    </span>
  );
}

<DateField label="Event date" />
```

 Show CSS

```
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.field {
  display: block;
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
  display: block;
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
  display: block;
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

## Styled examples[#](#styled-examples)

---

[![](/DateField-tailwind.70fdeb58.png)

Tailwind CSS

A date and time field built with Tailwind and React Aria.](https://codesandbox.io/s/small-water-y5dgj4?file=/src/DateField.js)

## Usage[#](#usage)

---

The following examples show how to use the `DateField` component created in the above example.

### Value[#](#value)

A `DateField` displays a placeholder by default. An initial, uncontrolled value can be provided to the `DateField` using the `defaultValue` prop. Alternatively, a controlled value can be provided using the `value` prop.

Date values are provided using objects in the [@internationalized/date](../internationalized/date/) package. This library handles correct international date manipulation across calendars, time zones, and other localization concerns. `useDateField` supports values of the following types:

- `CalendarDate` â a date without any time components. May be parsed from a string representation using the `parseDate` function. Use this type to represent dates where the time is not important, such as a birthday or an all day calendar event.
- `CalendarDateTime` â a date with a time, but not in any specific time zone. May be parsed from a string representation using the `parseDateTime` function. Use this type to represent times that occur at the same local time regardless of the time zone, such as the time of New Years Eve fireworks which always occur at midnight. Most times are better stored as a `ZonedDateTime`.
- `ZonedDateTime` â a date with a time in a specific time zone. May be parsed from a string representation using the `parseZonedDateTime`, `parseAbsolute`, or `parseAbsoluteToLocal` functions. Use this type to represent an exact moment in time at a particular location on Earth.

```
import {parseDate} from '@internationalized/date';

function Example() {
  let [value, setValue] = React.useState(parseDate('2020-02-03'));

  return (
    <>
      <DateField
        label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')} />
      <DateField
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
      <DateField
        label="Date (uncontrolled)"
        defaultValue={parseDate('2020-02-03')}
      />
      <DateField
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
      <DateField
        label="Date (uncontrolled)"
        defaultValue={parseDate(
          '2020-02-03'
        )}
      />
      <DateField
        label="Date (controlled)"
        value={value}
        onChange={setValue}
      />
    </>
  );
}
```

### Events[#](#events)

`useDateField` accepts an `onChange` prop which is triggered whenever the date is edited by the user. The example below uses `onChange` to update a separate element with a formatted version of the date in the user's locale and local time zone. This is done by converting the date to a native JavaScript `Date` object to pass to the formatter.

```
import {useDateFormatter} from 'react-aria';
import {getLocalTimeZone} from '@internationalized/date';

function Example() {
  let [date, setDate] = React.useState(parseDate('1985-07-03'));
  let formatter = useDateFormatter({ dateStyle: 'full' });

  return (
    <>
      <DateField label="Birth date" value={date} onChange={setDate} />
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
      <DateField
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
      <DateField
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

`useDateField` is time zone aware when a `ZonedDateTime` object is provided as the value. In this case, the time zone abbreviation is displayed, and time zone concerns such as daylight saving time are taken into account when the value is manipulated.

In most cases, your data will come from and be sent to a server as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted string. [@internationalized/date](../internationalized/date/) includes functions for parsing strings in multiple formats into `ZonedDateTime` objects. Which format you use will depend on what information you need to store.

- `parseZonedDateTime` â This function parses a date with an explicit time zone and optional UTC offset attached (e.g. `"2021-11-07T00:45[America/Los_Angeles]"` or `"2021-11-07T00:45-07:00[America/Los_Angeles]"`). This format preserves the maximum amount of information. If the exact local time and time zone that a user selected is important, use this format. Storing the time zone and offset that was selected rather than converting to UTC ensures that the local time is correct regardless of daylight saving rule changes (e.g. if a locale abolishes DST). Examples where this applies include calendar events, reminders, and other times that occur in a particular location.
- `parseAbsolute` â This function parses an absolute date and time that occurs at the same instant at all locations on Earth. It can be represented in UTC (e.g. `"2021-11-07T07:45:00Z"`), or stored with a particular offset (e.g. `"2021-11-07T07:45:00-07:00"`). A time zone identifier, e.g. `America/Los_Angeles`, must be passed, and the result will be converted into that time zone. Absolute times are the best way to represent events that occurred in the past, or future events where an exact time is needed, regardless of time zone.
- `parseAbsoluteToLocal` â This function parses an absolute date and time into the current user's local time zone. It is a shortcut for `parseAbsolute`, and accepts the same formats.

```
import {parseZonedDateTime} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseZonedDateTime('2022-11-07T00:45[America/Los_Angeles]')}
/>
```

```
import {parseZonedDateTime} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseZonedDateTime(
    '2022-11-07T00:45[America/Los_Angeles]'
  )}
/>
```

```
import {parseZonedDateTime} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseZonedDateTime(
    '2022-11-07T00:45[America/Los_Angeles]'
  )}
/>
```

`useDateField` displays times in the time zone included in the `ZonedDateTime` object. The above example is always displayed in Pacific Standard Time because the `America/Los_Angeles` time zone identifier is provided. [@internationalized/date](../internationalized/date/) includes functions for converting dates between time zones, or parsing a date directly into a specific time zone or the user's local time zone, as shown below.

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseAbsoluteToLocal('2021-11-07T07:45:00Z')}
/>
```

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseAbsoluteToLocal(
    '2021-11-07T07:45:00Z'
  )}
/>
```

```
import {parseAbsoluteToLocal} from '@internationalized/date';

<DateField
  label="Event date"
  defaultValue={parseAbsoluteToLocal(
    '2021-11-07T07:45:00Z'
  )}
/>
```

### Granularity[#](#granularity)

The `granularity` prop allows you to control the smallest unit that is displayed by `useDateField`. By default, `CalendarDate` values are displayed with `"day"` granularity (year, month, and day), and `CalendarDateTime` and `ZonedDateTime` values are displayed with `"minute"` granularity. More granular time values can be displayed by setting the `granularity` prop to `"second"`.

In addition, when a value with a time is provided but you wish to only display the date, you can set the granularity to `"day"`. This has no effect on the actual value (it still has a time component), only on what fields are displayed. In the following example, two DateFields are synchronized with the same value, but display different granularities.

```
function Example() {
  let [date, setDate] = React.useState(
    parseAbsoluteToLocal('2021-04-07T18:45:22Z')
  );

  return (
    <>
      <DateField
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DateField
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
      <DateField
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DateField
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
      <DateField
        label="Date and time"
        granularity="second"
        value={date}
        onChange={setDate}
      />
      <DateField
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

<DateField
  label="Event date"
  granularity="second" />
<DateField
  label="Event date"
  placeholderValue={now('America/New_York')}
  granularity="second" />
```

```
import {now} from '@internationalized/date';

<DateField
  label="Event date"
  granularity="second" />
<DateField
  label="Event date"
  placeholderValue={now('America/New_York')}
  granularity="second" />
```

```
import {now} from '@internationalized/date';

<DateField
  label="Event date"
  granularity="second"
/>
<DateField
  label="Event date"
  placeholderValue={now(
    'America/New_York'
  )}
  granularity="second"
/>
```

### International calendars[#](#international-calendars)

`useDateField` supports selecting dates in many calendar systems used around the world, including Gregorian, Hebrew, Indian, Islamic, Buddhist, and more. Dates are automatically displayed in the appropriate calendar system for the user's locale. The calendar system can be overridden using the [Unicode calendar locale extension](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/calendar#adding_a_calendar_in_the_locale_string), passed to the [I18nProvider](../I18nProvider) component.

Selected dates passed to `onChange` always use the same calendar system as the `value` or `defaultValue` prop. If no `value` or `defaultValue` is provided, then dates passed to `onChange` are always in the Gregorian calendar since this is the most commonly used. This means that even though the user selects dates in their local calendar system, applications are able to deal with dates from all users consistently.

The below example displays a `DateField` in the Hindi language, using the Indian calendar. Dates emitted from `onChange` are in the Gregorian calendar.

```
import {I18nProvider} from 'react-aria';

function Example() {
  let [date, setDate] = React.useState(null);
  return (
    <I18nProvider locale="hi-IN-u-ca-indian">
      <DateField label="Date" value={date} onChange={setDate} />
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
      <DateField
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
      <DateField
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

The `minValue` and `maxValue` props can also be used to perform builtin validation. This marks the date field as invalid using ARIA if the user enters an invalid date. You should implement a visual indication that the date field is invalid as well.

This example only accepts dates after today.

```
import {today} from '@internationalized/date';

<DateField
  label="Appointment date"
  minValue={today(getLocalTimeZone())}
  defaultValue={parseDate('2022-02-03')} />
```

```
import {today} from '@internationalized/date';

<DateField
  label="Appointment date"
  minValue={today(getLocalTimeZone())}
  defaultValue={parseDate('2022-02-03')} />
```

```
import {today} from '@internationalized/date';

<DateField
  label="Appointment date"
  minValue={today(
    getLocalTimeZone()
  )}
  defaultValue={parseDate(
    '2022-02-03'
  )}
/>
```

### Placeholder value[#](#placeholder-value)

When no value is set, a placeholder is shown. The format of the placeholder is influenced by the `granularity` and `placeholderValue` props. `placeholderValue` also controls the default values of each segment when the user first interacts with them, e.g. using the up and down arrow keys. By default, the `placeholderValue` is the current date at midnight, but you can set it to a more appropriate value if needed.

```
import {CalendarDate} from '@internationalized/date';

<DateField
  label="Birth date"
  placeholderValue={new CalendarDate(1980, 1, 1)}
/>
```

```
import {CalendarDate} from '@internationalized/date';

<DateField
  label="Birth date"
  placeholderValue={new CalendarDate(1980, 1, 1)}
/>
```

```
import {CalendarDate} from '@internationalized/date';

<DateField
  label="Birth date"
  placeholderValue={new CalendarDate(
    1980,
    1,
    1
  )}
/>
```

### Hide time zone[#](#hide-time-zone)

When a `ZonedDateTime` object is provided as the value to `useDateField`, the time zone abbreviation is displayed by default. However, if this is displayed elsewhere or implicit based on the usecase, it can be hidden using the `hideTimeZone` option.

```
<DateField
  label="Appointment time"
  defaultValue={parseZonedDateTime('2022-11-07T10:45[America/Los_Angeles]')}
  hideTimeZone />
```

```
<DateField
  label="Appointment time"
  defaultValue={parseZonedDateTime(
    '2022-11-07T10:45[America/Los_Angeles]'
  )}
  hideTimeZone
/>
```

```
<DateField
  label="Appointment time"
  defaultValue={parseZonedDateTime(
    '2022-11-07T10:45[America/Los_Angeles]'
  )}
  hideTimeZone
/>
```

### Hour cycle[#](#hour-cycle)

By default, `useDateField` displays times in either 12 or 24 hour hour format depending on the user's locale. However, this can be overridden using the `hourCycle` prop if needed for a specific usecase. This example forces `useDateField` to use 24-hour time, regardless of the locale.

```
<DateField
  label="Appointment time"
  granularity="minute"
  hourCycle={24} />
```

```
<DateField
  label="Appointment time"
  granularity="minute"
  hourCycle={24} />
```

```
<DateField
  label="Appointment time"
  granularity="minute"
  hourCycle={24}
/>
```

## Advanced topics[#](#advanced-topics)

---

### Reducing bundle size[#](#reducing-bundle-size)

In the example above, the `createCalendar` function from the [@internationalized/date](../internationalized/date/) package is passed to the `useDateFieldState` hook. This function receives a [calendar identifier](../internationalized/date/Calendar.html#calendar-identifiers) string, and provides `Calendar` instances to React Stately, which are used to implement date manipulation.

By default, this includes [all calendar systems](../internationalized/date/Calendar.html#implementations) supported by `@internationalized/date`. However, if your application supports a more limited set of regions, or you know you will only be picking dates in a certain calendar system, you can reduce your bundle size by providing your own implementation of `createCalendar` that includes a subset of these `Calendar` implementations.

For example, if your application only supports Gregorian dates, you could implement a `createCalendar` function like this:

```
import {useLocale} from 'react-aria';
import {useDateFieldState} from 'react-stately';
import {GregorianCalendar} from '@internationalized/date';

function createCalendar(identifier) {
  switch (identifier) {
    case 'gregory':
      return new GregorianCalendar();
    default:
      throw new Error(`Unsupported calendar ${identifier}`);
  }
}

export function DateField(props) {
  let { locale } = useLocale();
  let state = useDateFieldState({
    ...props,
    locale,
    createCalendar
  });

  // ...
}
```

```
import {useLocale} from 'react-aria';
import {useDateFieldState} from 'react-stately';
import {GregorianCalendar} from '@internationalized/date';

function createCalendar(identifier) {
  switch (identifier) {
    case 'gregory':
      return new GregorianCalendar();
    default:
      throw new Error(`Unsupported calendar ${identifier}`);
  }
}

export function DateField(props) {
  let { locale } = useLocale();
  let state = useDateFieldState({
    ...props,
    locale,
    createCalendar
  });

  // ...
}
```

```
import {useLocale} from 'react-aria';
import {useDateFieldState} from 'react-stately';
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

export function DateField(
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
| `inputRef` | `RefObject<HTMLInputElement |Â null>` | â | A ref for the hidden input element for HTML form submission. |
| `autoComplete` | `string` | â | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `isDateUnavailable` | `( (date: DateValue )) => boolean` | â | Callback that is called for each date of the calendar. If it returns true, then the date is unavailable. |
| `hourCycle` | `12 |Â 24` | â | Whether to display the time in 12 or 24 hour format. By default, this is determined by the user's locale. |
| `granularity` | `Granularity` | â | Determines the smallest unit that is displayed in the date picker. By default, this is `"day"` for dates, and `"minute"` for times. |
| `hideTimeZone` | `boolean` | `false` | Whether to hide the time zone abbreviation. |
| `shouldForceLeadingZeros` | `boolean` | â | Whether to always show leading zeros in the month, day, and hour fields. By default, this is determined by the user's locale. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

`'day'
|Â 'hour'
|Â 'minute'
|Â 'second'`

`'valid' |Â 'invalid'`

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
| `value` | `DateValue |Â null` | The current field value. |
| `defaultValue` | `DateValue |Â null` | The default field value. |
| `dateValue` | `Date` | The current value, converted to a native JavaScript `Date` object. |
| `calendar` | `Calendar` | The calendar system currently in use. |
| `segments` | `DateSegment[]` | A list of segments for the current value. |
| `dateFormatter` | `DateFormatter` | A date formatter configured for the current locale and format. |
| `isInvalid` | `boolean` | Whether the date field is invalid, based on the `isInvalid`, `minValue`, and `maxValue` props. |
| `granularity` | `Granularity` | The granularity for the field, based on the `granularity` prop and current value. |
| `maxGranularity` | `'year' |Â 'month' |Â Granularity` | The maximum date or time unit that is displayed in the field. |
| `isDisabled` | `boolean` | Whether the field is disabled. |
| `isReadOnly` | `boolean` | Whether the field is read only. |
| `isRequired` | `boolean` | Whether the field is required. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: DateValue |Â  |Â null )): void` | Sets the field's value. |
| `increment( (type: SegmentType )): void` | Increments the given segment. Upon reaching the minimum or maximum value, the value wraps around to the opposite limit. |
| `decrement( (type: SegmentType )): void` | Decrements the given segment. Upon reaching the minimum or maximum value, the value wraps around to the opposite limit. |
| `incrementPage( (type: SegmentType )): void` | Increments the given segment by a larger amount, rounding it to the nearest increment. The amount to increment by depends on the field, for example 15 minutes, 7 days, and 5 years. Upon reaching the minimum or maximum value, the value wraps around to the opposite limit. |
| `decrementPage( (type: SegmentType )): void` | Decrements the given segment by a larger amount, rounding it to the nearest increment. The amount to decrement by depends on the field, for example 15 minutes, 7 days, and 5 years. Upon reaching the minimum or maximum value, the value wraps around to the opposite limit. |
| `setSegment( (type: SegmentType, , value: number )): void` | Sets the value of the given segment. |
| `confirmPlaceholder(): void` | Updates the remaining unfilled segments with the placeholder value. |
| `clearSegment( (type: SegmentType )): void` | Clears the value of the given segment, reverting it to the placeholder. |
| `formatValue( (fieldOptions: FieldOptions )): string` | Formats the current date value using the given options. |
| `getDateFormatter( (locale: string, , formatOptions: FormatterOptions )): DateFormatter` | Gets a formatter based on state's props. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

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

| Name | Type | Description |
| --- | --- | --- |
| `type` | `SegmentType` | The type of segment. |
| `text` | `string` | The formatted text for the segment. |
| `isPlaceholder` | `boolean` | Whether the value is a placeholder. |
| `placeholder` | `string` | A placeholder string for the segment. |
| `isEditable` | `boolean` | Whether the segment is editable. |
| `value` | `number` | The numeric value for the segment, if applicable. |
| `minValue` | `number` | The minimum numeric value for the segment, if applicable. |
| `maxValue` | `number` | The maximum numeric value for the segment, if applicable. |

`'era'
|Â 'year'
|Â 'month'
|Â 'day'
|Â 'hour'
|Â 'minute'
|Â 'second'
|Â 'dayPeriod'
|Â 'literal'
|Â 'timeZoneName'`

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

`'single' |Â 'visible'`

`DateValue extends ZonedDateTime ? ZonedDateTime :
DateValue extends CalendarDateTime ? CalendarDateTime :
DateValue extends CalendarDate ? CalendarDate : never`

`string |Â string[]`

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the field's visible label element, if any. |
| `fieldProps` | `GroupDOMAttributes` | Props for the field grouping element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the hidden input element for HTML form submission. |
| `descriptionProps` | `DOMAttributes` | Props for the description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the error message element, if any. |
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

| Name | Type | Description |
| --- | --- | --- |
| `segmentProps` | `React.HTMLAttributes<HTMLDivElement>` | Props for the segment element. |

Provides state management for a date field component.
A date field allows users to enter and edit date and time values using a keyboard.
Each part of a date value is displayed in an individually editable segment.

`useDateFieldState<T extends DateValue = DateValue>(
(props: DateFieldStateOptions<T>
)): DateFieldState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `locale` | `string` | â | The locale to display and edit the value according to. |
| `createCalendar` | `( (name: CalendarIdentifier )) => Calendar` | â | A function that creates a [Calendar](../internationalized/date/Calendar.html) object for a given calendar identifier. Such a function may be imported from the `@internationalized/date` package, or manually implemented to include support for only certain calendars. |
| `maxGranularity` | `'year' |Â 'month' |Â Granularity` | `'year'` | The maximum unit to display in the date field. |
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

Provides the behavior and accessibility implementation for a date field component.
A date field allows users to enter and edit date and time values using a keyboard.
Each part of a date value is displayed in an individually editable segment.

`useDateField<T extends DateValue>(
props: AriaDateFieldOptions<T>,
state: DateFieldState,
ref: RefObject<Element
|Â  |Â null>
): DateFieldAria`

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

Creates a `Calendar` instance from a Unicode calendar identifier string.

`createCalendar(
(name: CalendarIdentifier
)): Calendar`
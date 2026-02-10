# Date picker

Source: https://carbondesignsystem.com/components/date-picker/usage/

---

# Date picker

Date and time pickers allow users to select a single instance or range of dates
and times.

Date picker
[with AI label](https://react.carbondesignsystem.com/?path=/story/components-datepicker--with-ai-label)
is now stable. This addition changes the visual appearance of the component and
introduces an AI explainability feature when AI is present in the component. See
the [AI presence](/components/date-picker/usage/#ai-presence) section for more
details.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Universal behaviors](#universal-behaviors)
- [Simple date input](#simple-date-input)
- [Calendar pickers](#calendar-pickers)
- [Time pickers](#time-pickers)
- [AI presence](#ai-presence)
- [Related](#related)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Range with calendar

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-datepicker--range-with-calendar&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

Variant

Date picker

---

[##### Default state

Tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Partially tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

[##### Default state

Not tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Not tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Not available](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Not available](//accessibility/#accessibility-testing-status)

## Overview

Date pickers allow users to select past, present, or future dates. The kind of
date you are requesting from the user will determine which date picker (simple
or calendar) is best to use. A time picker helps users select a specific time.
You can customize the time picker’s format depending on location or need.

### When to use

- When asking the user for an exact, approximate, or memorable date or time.
- For scheduling tasks.

### Variants

| Variant | Purpose |
| --- | --- |
| [Simple date input](/components/date-picker/usage#simple-date-input) | Use if the date can be remembered by the user easily, such as a date of birth, and they don’t need a calendar to anticipate the dates. It consists only of input fields. |
| [Calendar picker](/components/date-picker/usage#calendar-pickers) | Use a calendar picker (single or range) when the user needs to know a date’s relationship to other days or when a date could be variable. The user can view and pick dates from a calendar widget or manually type them in the text field. |
| [Time picker](/components/date-picker/usage/#time-pickers) | Use when asking the user to input a specific time. |

## Formatting

### Anatomy of date pickers

- Default
- Fluid

![Default date picker anatomy](/static/d4f663c750fd3c45a5f2c31aa048a003/3cbba/date-picker-anatomy.png)

![Fluid date picker anatomy](/static/49ab39956bdcc045dd25de1babc1316e/3cbba/date-picker-anatomy-fluid.png)

Anatomy of a simple date input and a single date calendar picker.

1. **Label**: Instructs the user what to do with the control.
2. **Date field**: A text input field where the user can manually type in the
   date.
3. **Date format**: Format instructions should appear as helper text below the
   field or inline with the label.
4. **Icon**:

   ```
   calendar
   ```

   Copy to clipboard

   icon indicates the calendar menu is available.
5. **Calendar**: The menu where a date may be selected.
6. **Month and year controls**: Allows the user to navigate through past and
   future time frames.
7. **Previous and next month controls**: Allows the user to move forward or
   backward one month at a time.
8. **Week day**: Days of the week.
9. **Day**: Days in the month, see
   [calendar variants](/components/date-picker/usage#calendar-variants) for
   specific day styles.

### Anatomy of a time picker

- Default
- Fluid

![Default time picker anatomy](/static/b6a0cc99b29bf0270965319390fccf04/3cbba/time-picker-anatomy.png)

![Fluid time picker anatomy](/static/4b2dcfd8fdf50271713ef0722f320892/3cbba/time-picker-anatomy-fluid.png)

1. **Label**: Instructs the user what to do with the control.
2. **Hour and minute field**: A text input field where the user types the hours
   and minutes of the desired time.
3. **AM/PM selector**: A select control that allows the user to choose time
   period.
4. **Timezone selector**: A select control that allows the user to set the
   associated time zone.

### Styling

There are two styles of date picker inputs, default and fluid. They share the
same functionality but look visually different, influencing where to use them.

| Style | Appearance | Use case |
| --- | --- | --- |
| Default | A traditional style where the label is positioned outside and above the input field. | Use when white space is needed between input components or in productive moments where space is at a premium, and smaller components are needed. |
| Fluid | An alternative style where the label is placed inside of the input field and is stacked inline with the user input text. | Use in expressive moments, fluid forms, contained spaces, or attached to complex components, like a toolbar. |

![An example of a default and fluid date picker input](/static/55ce18129af77ec1dfb9d5a68efe0931/3cbba/date-picker-formatting-styling.png)

### Sizes

#### Default input heights

The default input fields for date and time picker come in three height sizes:
small (32px), medium (40px), and large (48px). The calendar menu in the date
picker is a fixed height and width and does not change with the input size.

| Default size | Height (px/rem) | Use case |
| --- | --- | --- |
| Small (sm) | 32 / 2 | Use when space is constricted or when placing a dropdown in a form that is long and complex. |
| Medium (md) | 40 / 2.5 | This is the default size and the most commonly used size. When in doubt, use the medium size. |
| Large (lg) | 48 / 3 | Use when there is a lot of space to work with. This size is typically used in simple forms or when a dropdown is placed by itself on a page, for example as a filter. |

![Default input size example](/static/9ee70bdb834116c0adb66a3855fdb28d/3cbba/date-picker-sizes.png)

#### Fluid input heights

There is only one fluid input height and it is visually larger than the default
heights. The input is a set height of 64px except when a warning or error
message has been added to the bottom.

![Fluid input size example](/static/6ac344e1280532d3f0dac0674f8f67f3/3cbba/date-picker-sizes-fluid.png)

### Alignment

By default, the pickers have set widths. If you are placing the picker inline
with other inputs, such as in a form, then the widths can be adjusted to match
the other inputs. The picker can either increase or decrease in width as needed.
If you adjust the size, be aware that pickers have minimum widths and the date
content should never horizontally scroll or overflow.

![Alignment example](/static/80e573d88a78b46494ad20bd80f9c179/3cbba/date-picker-alignment-01.png)

#### Aligning the calendar menu

The calendar itself will always remain a set width and is not adjustable. It
should always be aligned to the left edge of its assigned text field.

![Alignment example](/static/87425242ecd7f29fa7e805bd05b20bd6/3cbba/date-picker-alignment-02.png)

## Content

### Main elements

#### Label

- Both date and time pickers must be accompanied with labels.
- The labels should be clear and descriptive.
- Range inputs should be being properly labeled with a start and end label.

#### Date format

- When using a simple date input, include the date format in parentheses inline
  with the label or as helper text below the label.
- When using the calendar picker, the date format will be automated if the user
  selects from the calendar menu.
- Only including the date format as placeholder text inside the field is
  problematic because it will disappear from view once the user begins typing.

![Alignment example](/static/a2e0508f4f15603b9f1cc9feb60dcf2c/3cbba/date-format-placement.png)

Example suggesting the proper date format in helper text on the left or in a
label on the right.

- The date format can be displayed differently depending on your location. For
  example, some countries use the format month/day/year, while others may change
  the order to year-month-day and can use dashes instead of slashes. The date
  picker utilizes [flatpickr](https://flatpickr.js.org/), which accepts

  ```
  dateFormat
  ```

  Copy to clipboard

  and

  ```
  locale
  ```

  Copy to clipboard

  props that allow you to change how the date is
  displayed and lets you change the language of the calendar. Localizing static
  dates in the same UI is also recommended if you choose to localize your date
  entries.

![Localized dates example](/static/a8a61edbabb10c1afc6afc24f72bc1a9/3cbba/date-picker-usage-localized.png)

Example of formatting dates with American English format on the left and
International Standard format on the right.

#### Time format

- Both the 12-hour and 24-hour time systems are allowed.
- If using the 12-hour format it must be accompanied by an AM/PM selection.
- Use uppercase letters and no periods for the abbreviations AM and PM.
- Specific times should specify a timezone.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](/guidelines/content/overview/).

## Universal behaviors

The behaviors listed in this section are universal across all of the variants.
For behaviors that are unique to each variant, see each of the component variant
sections below.

### States

#### Date picker and calendar menu

The date picker input is a [text input](/components/text-input/usage) and has
the same interactive state and behaviors. Only date pickers with calendars will
have the calendar icon present in the right side of the input field. See the
[style tab](/components/date-picker/style#date-picker-color) for more details.
For calendar menu states, see the
[calendar variants](/components/date-picker/usage/#calendar-variants) section.

#### Time picker

The time picker is a combination of a [text input](/components/text-input/usage)
and [select inputs](/components/select/usage) and has the same interactive state
and behaviors. See the
[style tab](/components/date-picker/style/#time-picker-color) for more details.

| State | When to use |
| --- | --- |
| *Enabled* | When the date or time picker is live, but a user is not directly interacting with it. This is commonly referred to as the default or normal state of the component. |
| *Hover* | When a user’s mouse cursor is hovering over the field. |
| *Focus* | When a user tabs to or clicks into the input, the field becomes focused, indicating the user has successfully navigated to the component. |
| *Open* | The open state is specifically for the calendar menu. When the calendar menu is open, the user can navigate within the menu to select a single date or a range of dates. |
| *Error* | When the required field for a text input in the date or time picker component has not been filled in or when a select in the time picker component does not have a selection. It can also be triggered due to a system error. This state requires a user response before data can be submitted or saved. |
| *Warning* | When you need to call the user’s attention to an exception condition. The condition might not be an error but can cause problems if not resolved. |
| *Disabled* | When the user cannot interact with a component and all interactive functions have been removed. Unlike read-only states, disabled states are not focusable, are not read by screen readers, and do not need to pass visual contrast, making them inaccessible if they need to be interpreted. |
| *Skeleton* | Use on an initial page load to indicate that the date picker or time picker has not yet fully loaded. |
| *Read-only* | When the user can review but not modify the component. This state removes all interactive functions like the disabled state but can still be focusable, accessible by screen readers, and passes visual contrast for readability. |

#### Validation

Invalid fields should be clearly marked. In pickers with more than one field,
the invalid state should only be set on the individual factor that is triggering
the error so the user can clearly understand which to address.

![Validation example](/static/03b166c16dfff1ee7fdd4037bd169544/3cbba/date-picker-validation.png)

### Internationalization

Internationalization, also referred to as globalization, refers to software
adapting to different languages, regional peculiarities, and technical
requirements of a target locale without additional code changes. This means that
if the location is known, then formatting of a date or time can automatically
change to the acceptable local format. You should always try to design for
internationalization.

## Simple date input

The simple date input provides the user with only a text field in which they can
manually input a date. It allows dates to be entered without adding unnecessary
interactions that come with the calendar menu or a dropdown.

The simple date input can include *month/year* or *month/day/year.* The
formatting may be localized and rearranged in sequence of appearance.

### When to use

#### Use for memorable dates

Simple date inputs are typically used when the date is known by the user, such
as a date of birth or credit card expiration.

#### Use for approximate dates

Simple date inputs are best for when asking the user for an approximate date
instead of an exact date, especially in regards to past dates. For example, when
was asking a user when a purchase was made they will most likely easily recall
the month and year (November 2019) versus the specific date (November 22, 2019).

![Simple date input](/static/eda30a9fc8911e0ca54a2293bd19891f/3cbba/single-date-input.png)

## Calendar pickers

Calendar pickers default to showing today’s date when opened and only one month
is shown at a time. Calendar pickers allow users to navigate through months and
years, however they work best when used for recent or near future dates. If a
user needs to input a far distant or future date consider having the calendar
default open to a more convenient day.

Keep in mind that some users may find calendar pickers difficult to use. There
should always be a simple way to enter dates in a text field when using calendar
pickers.

#### Use for scheduling

Use a calendar picker when the user needs to know a date’s relation to other
days such as the day of the week it falls on or its proximity to today. They are
optimal for scheduling tasks.

### Calendar variants

#### Single date picker

In a single date picker a user has the option to either manually input a date in
the text field or select one specific date from the menu calendar. It requires a
day, month, and year to be selected.

![Single date calendar picker](/static/ab1c2731904f3e37874f7e617d3589c9/3cbba/single-date-picker.png)

1. Today’s date
2. Hover
3. Day in month
4. Selected day
5. Day in next/previous month

#### Date range picker

The date range picker functions much like the single date picker but instead of
choosing just one date the user can choose a

```
start
```

Copy to clipboard

and

```
end
```

Copy to clipboard

date. For each
date in the range, users have the option to manually enter the date in a text
field or select the date in the calendar. Each point requires a day, month, and
year to be selected.

![Date range calendar picker](/static/3755cd6576787b33307d6d515ed79e5f/3cbba/range-date-picker.png)

1. Day in month
2. Today
3. Selected start date
4. Day in range
5. End date hover and focus
6. Day in next/previous month

### Calendar behaviors

#### Opening the calendar

The calendar can be opened in two ways:

- Clicking the

  ```
  calendar
  ```

  Copy to clipboard

  icon on the far right of the field opens the calendar
  menu.
- When the text field receives focus the calendar menu also appears and remains
  open until a date is selected or the focus is removed from the picker.

#### Selecting a date

A date can be selected by:

- Manually entering a date in the text input field.
- Clicking on a date in the calendar menu.
- Navigating to a date by using the

  ```
  Arrow
  ```

  Copy to clipboard

  keys and then pressing

  ```
  Enter
  ```

  Copy to clipboard

  .

#### Next and previous month

A user can navigate between the months in a year by:

- Clicking on

  ```
  chevron
  ```

  Copy to clipboard

  icons at the top left and right of the calendar.
- Using the

  ```
  Arrow
  ```

  Copy to clipboard

  keys to move through the into the next or previous month.

#### Selecting a year

By default the current date and year appears in the calendar. To navigate to
another year the user can do one of the following:

- Manually typing the year in the date text field.
- Clicking the up and down arrows that appear when you focus or hover on the
  year input in the calendar.
- Selecting then typing into the year input.

#### Closing the calendar

The calendar can be closed in one of the following ways:

- Selecting a single date or the end date in a range. This will automatically
  close it.
- Clicking anywhere outside of the calendar menu.
- Removing focus from the picker.
- Pressing

  ```
  Esc
  ```

  Copy to clipboard

  .

#### Selecting a range

There are several ways in which a range can be selected:

- Manually type the start and end dates in the text field.
- Once the calendar is open the first date you click becomes the start date and
  second date you click becomes the end date.
- Navigating to the start date by using the

  ```
  Arrow
  ```

  Copy to clipboard

  keys and pressing

  ```
  Enter
  ```

  Copy to clipboard

  .
  Then continue using the

  ```
  Arrow
  ```

  Copy to clipboard

  keys to navigate to a second date and press

  ```
  Enter
  ```

  Copy to clipboard

  again.

#### Min and max dates

In order to constrain the possible selectable dates in a calendar, a min and max
date may be set. Once set, only the dates that fall within the min/max range
will be selectable with the dates outside of the range being disabled.

Use min and max dates to help prevent user error. If a user cannot select dates
in the past when scheduling, then set a min date to today.

![Min and max date example](/static/378473efb4ba043c64752ddd31aeecd8/3cbba/calendar-picker-min-max.png)

The dates before today are out of range and disabled.

## Time pickers

Time pickers provide the user with a text field in which they can input the hour
and minutes. Additionally, they can be accompanied by an AM/PM and a time zone
control, both styled as selects.

The time field format should include the hour and minutes, for example 11:30. It
may be localized to accommodate the 12-hour or 24-hour format.

#### Use for scheduling

Use the time picker when a specific time needs to be scheduled, such as planning
a meeting time.

![Time picker example](/static/73a4cac2638d03221f341e104b6aa4a3/3cbba/time-picker-example.png)

## AI presence

Date picker has a modification that takes on the AI visual styling when the AI
label is present in the input. The AI variant functions the same as the normal
version except with the addition of the AI label which is both a visual
indicator and the trigger for the explainability popover.

For more information on designing for AI, see the
[Carbon for AI](/guidelines/carbon-for-ai/) guidelines.

- Default
- Fluid

![Default date picker with AI presence](/static/8ee79d72797da5311b86ddef7c343d3d/3cbba/date-picker-AI-presence-default-usage.png)

![Fluid date picker with AI presence](/static/56b745cbd777a137b2430895c1c211be/3cbba/date-picker-AI-presence-fluid-usage.png)

### Revert to AI

A date picker can toggle between the AI variant and the non-AI variant depending
on the user’s interaction. If the user manually overrides the AI-suggested
content then the input will change from the AI variant to the non-AI variant.
Once edited, the user should still be able to switch back to the initially AI
generated content via a revert to AI button.

- Default
- Fluid

![Default date picker with AI revert](/static/7ee587152c90077fefc52a4c62823124/3cbba/date-picker-revert-to-AI-default-usage.png)

![Fluid date picker with AI revert](/static/3dfdbbf7bc96a27f7fae8f603418570b/3cbba/date-picker-revert-to-AI-fluid-usage.png)

## Related

#### Asking for relative times and dates

Another common use case not accounted for in the above pickers is setting a time
or date relative to today or now, such as with a reminder. For example, setting
an install to begin now, in one hour, or tonight. This variant of picker can
made by using the standard [select](/components/select/usage/) component.

#### Using individual inputs

Another acceptable form of a date experience would be using individual inputs
for each factor. Using an individual field for each factor of a date can help
reduce formatting errors. This is especially beneficial when localization cannot
be used to reformat dates.

Instead of having one input for an exact date (month/day/year), you could have
three separate inputs and a clear label for each.

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/date-picker/usage.mdx)

[Previous

Components: Data table](/components/data-table/usage/)

[Next

Date picker: Style](/components/date-picker/style/)
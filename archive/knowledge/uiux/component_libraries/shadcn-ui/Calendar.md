# Calendar

Source: https://ui.shadcn.com/docs/components/calendar

---

Sections

- [Introduction](/docs)
- [Components](/docs/components)
- [Installation](/docs/installation)
- [Directory](/docs/directory)
- [RTL](/docs/rtl)
- [MCP Server](/docs/mcp)
- [Registry](/docs/registry)
- [Forms](/docs/forms)
- [Changelog](/docs/changelog)

Components

- [Accordion](/docs/components/radix/accordion)
- [Alert](/docs/components/radix/alert)
- [Alert Dialog](/docs/components/radix/alert-dialog)
- [Aspect Ratio](/docs/components/radix/aspect-ratio)
- [Avatar](/docs/components/radix/avatar)
- [Badge](/docs/components/radix/badge)
- [Breadcrumb](/docs/components/radix/breadcrumb)
- [Button](/docs/components/radix/button)
- [Button Group](/docs/components/radix/button-group)
- [Calendar](/docs/components/radix/calendar)
- [Card](/docs/components/radix/card)
- [Carousel](/docs/components/radix/carousel)
- [Chart](/docs/components/radix/chart)
- [Checkbox](/docs/components/radix/checkbox)
- [Collapsible](/docs/components/radix/collapsible)
- [Combobox](/docs/components/radix/combobox)
- [Command](/docs/components/radix/command)
- [Context Menu](/docs/components/radix/context-menu)
- [Data Table](/docs/components/radix/data-table)
- [Date Picker](/docs/components/radix/date-picker)
- [Dialog](/docs/components/radix/dialog)
- [Direction](/docs/components/radix/direction)
- [Drawer](/docs/components/radix/drawer)
- [Dropdown Menu](/docs/components/radix/dropdown-menu)
- [Empty](/docs/components/radix/empty)
- [Field](/docs/components/radix/field)
- [Hover Card](/docs/components/radix/hover-card)
- [Input](/docs/components/radix/input)
- [Input Group](/docs/components/radix/input-group)
- [Input OTP](/docs/components/radix/input-otp)
- [Item](/docs/components/radix/item)
- [Kbd](/docs/components/radix/kbd)
- [Label](/docs/components/radix/label)
- [Menubar](/docs/components/radix/menubar)
- [Native Select](/docs/components/radix/native-select)
- [Navigation Menu](/docs/components/radix/navigation-menu)
- [Pagination](/docs/components/radix/pagination)
- [Popover](/docs/components/radix/popover)
- [Progress](/docs/components/radix/progress)
- [Radio Group](/docs/components/radix/radio-group)
- [Resizable](/docs/components/radix/resizable)
- [Scroll Area](/docs/components/radix/scroll-area)
- [Select](/docs/components/radix/select)
- [Separator](/docs/components/radix/separator)
- [Sheet](/docs/components/radix/sheet)
- [Sidebar](/docs/components/radix/sidebar)
- [Skeleton](/docs/components/radix/skeleton)
- [Slider](/docs/components/radix/slider)
- [Sonner](/docs/components/radix/sonner)
- [Spinner](/docs/components/radix/spinner)
- [Switch](/docs/components/radix/switch)
- [Table](/docs/components/radix/table)
- [Tabs](/docs/components/radix/tabs)
- [Textarea](/docs/components/radix/textarea)
- [Toast](/docs/components/radix/toast)
- [Toggle](/docs/components/radix/toggle)
- [Toggle Group](/docs/components/radix/toggle-group)
- [Tooltip](/docs/components/radix/tooltip)
- [Typography](/docs/components/radix/typography)

Get Started

- [Installation](/docs/installation)
- [components.json](/docs/components-json)
- [Theming](/docs/theming)
- [Dark Mode](/docs/dark-mode)
- [CLI](/docs/cli)
- [Monorepo](/docs/monorepo)
- [Open in v0](/docs/v0)
- [JavaScript](/docs/javascript)
- [Blocks](/docs/blocks)
- [Figma](/docs/figma)
- [llms.txt](/llms.txt)
- [Legacy Docs](/docs/legacy)

Forms

- [React Hook Form](/docs/forms/react-hook-form)
- [TanStack Form](/docs/forms/tanstack-form)

Registry

- [Introduction](/docs/registry)
- [Getting Started](/docs/registry/getting-started)
- [Namespaces](/docs/registry/namespace)
- [Authentication](/docs/registry/authentication)
- [Examples](/docs/registry/examples)
- [MCP Server](/docs/registry/mcp)
- [Add a Registry](/docs/registry/registry-index)
- [Open in v0](/docs/registry/open-in-v0)
- [registry.json](/docs/registry/registry-json)
- [registry-item.json](/docs/registry/registry-item-json)

# Calendar

Copy Page

[Previous](/docs/components/radix/button-group)[Next](/docs/components/radix/card)

A calendar component that allows users to select a date or a range of dates.

[Radix UI](/docs/components/radix/calendar)[Base UI](/docs/components/base/calendar)

JanFebMarAprMayJunJulAugSepOctNovDecFeb192619271928192919301931193219331934193519361937193819391940194119421943194419451946194719481949195019511952195319541955195619571958195919601961196219631964196519661967196819691970197119721973197419751976197719781979198019811982198319841985198619871988198919901991199219931994199519961997199819992000200120022003200420052006200720082009201020112012201320142015201620172018201920202021202220232024202520262026February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import * as React from "react"
```

View Code

## Blocks

We have built a collection of 30+ calendar blocks that you can use to build your own calendar components.

See all calendar blocks in the [Blocks Library](/blocks/calendar) page.

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add calendar
```

Copy
```

## Usage

```
Copyimport { Calendar } from "@/components/ui/calendar"
```

```
Copyconst [date, setDate] = React.useState<Date | undefined>(new Date())
 
return (
  <Calendar
    mode="single"
    selected={date}
    onSelect={setDate}
    className="rounded-lg border"
  />
)
```

See the [React DayPicker](https://react-day-picker.js.org) documentation for more information.

## About

The `Calendar` component is built on top of [React DayPicker](https://react-day-picker.js.org).

## Date Picker

You can use the `<Calendar>` component to build a date picker. See the [Date Picker](/docs/components/radix/date-picker) page for more information.

## Persian / Hijri / Jalali Calendar

To use the Persian calendar, edit `components/ui/calendar.tsx` and replace `react-day-picker` with `react-day-picker/persian`.

```
Copy- import { DayPicker } from "react-day-picker"
+ import { DayPicker } from "react-day-picker/persian"
```

خرداد ۱۴۰۴

| ش | ۱ش | ۲ش | ۳ش | ۴ش | ۵ش | ج |
| --- | --- | --- | --- | --- | --- | --- |
| ۲۷ | ۲۸ | ۲۹ | ۳۰ | ۳۱ | ۱ | ۲ |
| ۳ | ۴ | ۵ | ۶ | ۷ | ۸ | ۹ |
| ۱۰ | ۱۱ | ۱۲ | ۱۳ | ۱۴ | ۱۵ | ۱۶ |
| ۱۷ | ۱۸ | ۱۹ | ۲۰ | ۲۱ | ۲۲ | ۲۳ |
| ۲۴ | ۲۵ | ۲۶ | ۲۷ | ۲۸ | ۲۹ | ۳۰ |
| ۳۱ | ۱ | ۲ | ۳ | ۴ | ۵ | ۶ |

Copy

```
"use client"

import * as React from "react"
```

View Code

## Selected Date (With TimeZone)

The Calendar component accepts a `timeZone` prop to ensure dates are displayed and selected in the user's local timezone.

```
Copyexport function CalendarWithTimezone() {
  const [date, setDate] = React.useState<Date | undefined>(undefined)
  const [timeZone, setTimeZone] = React.useState<string | undefined>(undefined)
 
  React.useEffect(() => {
    setTimeZone(Intl.DateTimeFormat().resolvedOptions().timeZone)
  }, [])
 
  return (
    <Calendar
      mode="single"
      selected={date}
      onSelect={setDate}
      timeZone={timeZone}
    />
  )
}
```

**Note:** If you notice a selected date offset (for example, selecting the 20th highlights the 19th), make sure the `timeZone` prop is set to the user's local timezone.

**Why client-side?** The timezone is detected using `Intl.DateTimeFormat().resolvedOptions().timeZone` inside a `useEffect` to ensure compatibility with server-side rendering. Detecting the timezone during render would cause hydration mismatches, as the server and client may be in different timezones.

## Examples

### Basic

A basic calendar component. We used `className="rounded-lg border"` to style the calendar.

February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import { Calendar } from "@/components/ui/calendar"
```

View Code

### Range Calendar

Use the `mode="range"` prop to enable range selection.

January 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 28 | 29 | 30 | 31 | 1 | 2 | 3 |
| 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| 18 | 19 | 20 | 21 | 22 | 23 | 24 |
| 25 | 26 | 27 | 28 | 29 | 30 | 31 |

February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import * as React from "react"
```

View Code

### Month and Year Selector

Use `captionLayout="dropdown"` to show month and year dropdowns.

JanFebMarAprMayJunJulAugSepOctNovDecFeb192619271928192919301931193219331934193519361937193819391940194119421943194419451946194719481949195019511952195319541955195619571958195919601961196219631964196519661967196819691970197119721973197419751976197719781979198019811982198319841985198619871988198919901991199219931994199519961997199819992000200120022003200420052006200720082009201020112012201320142015201620172018201920202021202220232024202520262026February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import { Calendar } from "@/components/ui/calendar"
```

View Code

### Presets

February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |

TodayTomorrowIn 3 daysIn a weekIn 2 weeks

Copy

```
"use client"

import * as React from "react"
```

View Code

### Date and Time Picker

February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Start Time

End Time

Copy

```
"use client"

import * as React from "react"
```

View Code

### Booked dates

February 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import * as React from "react"
```

View Code

### Custom Cell Size

JanuaryFebruaryMarchAprilMayJuneJulyAugustSeptemberOctoberNovemberDecemberDecember192619271928192919301931193219331934193519361937193819391940194119421943194419451946194719481949195019511952195319541955195619571958195919601961196219631964196519661967196819691970197119721973197419751976197719781979198019811982198319841985198619871988198919901991199219931994199519961997199819992000200120022003200420052006200720082009201020112012201320142015201620172018201920202021202220232024202520262026December 2026

| Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | 30 | 1$100 | 2$100 | 3$100 | 4$100 | 5$120 |
| 6$120 | 7$100 | 8$100 | 9$100 | 10$100 | 11$100 | 12$120 |
| 13$120 | 14$100 | 15$100 | 16$100 | 17$100 | 18$100 | 19$120 |
| 20$120 | 21$100 | 22$100 | 23$100 | 24$100 | 25$100 | 26$120 |
| 27$120 | 28$100 | 29$100 | 30$100 | 31$100 |  |  |

Copy

```
"use client"

import * as React from "react"
```

View Code

You can customize the size of calendar cells using the `--cell-size` CSS variable. You can also make it responsive by using breakpoint-specific values:

```
Copy<Calendar
  mode="single"
  selected={date}
  onSelect={setDate}
  className="rounded-lg border [--cell-size:--spacing(11)] md:[--cell-size:--spacing(12)]"
/>
```

Or use fixed values:

```
Copy<Calendar
  mode="single"
  selected={date}
  onSelect={setDate}
  className="rounded-lg border [--cell-size:2.75rem] md:[--cell-size:3rem]"
/>
```

### Week Numbers

Use `showWeekNumber` to show week numbers.

February 2026

|  | Su | Mo | Tu | We | Th | Fr | Sa |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 06 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 07 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 08 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 09 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import * as React from "react"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

See also the [Hijri Guide](#persian--hijri--jalali-calendar) for enabling the Persian / Hijri / Jalali calendar.

Arabic (العربية)Toggle

ينايرفبرايرمارسأبريلمايويونيويوليوأغسطسسبتمبرأكتوبرنوفمبرديسمبرفبراير192619271928192919301931193219331934193519361937193819391940194119421943194419451946194719481949195019511952195319541955195619571958195919601961196219631964196519661967196819691970197119721973197419751976197719781979198019811982198319841985198619871988198919901991199219931994199519961997199819992000200120022003200420052006200720082009201020112012201320142015201620172018201920202021202220232024202520262026فبراير 2026

| أحد | اثنين | ثلاثاء | أربعاء | خميس | جمعة | سبت |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| 22 | 23 | 24 | 25 | 26 | 27 | 28 |

Copy

```
"use client"

import * as React from "react"
```

View Code

When using RTL, import the locale from `react-day-picker/locale` and pass both the `locale` and `dir` props to the Calendar component:

```
Copyimport { arSA } from "react-day-picker/locale"
 
;<Calendar
  mode="single"
  selected={date}
  onSelect={setDate}
  locale={arSA}
  dir="rtl"
/>
```

## API Reference

See the [React DayPicker](https://react-day-picker.js.org) documentation for more information on the `Calendar` component.

## Changelog

### RTL Support

If you're upgrading from a previous version of the `Calendar` component, you'll need to apply the following updates to add locale support:

### Import the `Locale` type.

Add `Locale` to your imports from `react-day-picker`:

```
Copy  import {
    DayPicker,
    getDefaultClassNames,
    type DayButton,
+   type Locale,
  } from "react-day-picker"
```

### Add `locale` prop to the Calendar component.

Add the `locale` prop to the component's props:

```
Copy  function Calendar({
    className,
    classNames,
    showOutsideDays = true,
    captionLayout = "label",
    buttonVariant = "ghost",
+   locale,
    formatters,
    components,
    ...props
  }: React.ComponentProps<typeof DayPicker> & {
    buttonVariant?: React.ComponentProps<typeof Button>["variant"]
  }) {
```

### Pass `locale` to DayPicker.

Pass the `locale` prop to the `DayPicker` component:

```
Copy    <DayPicker
      showOutsideDays={showOutsideDays}
      className={cn(...)}
      captionLayout={captionLayout}
+     locale={locale}
      formatters={{
        formatMonthDropdown: (date) =>
-         date.toLocaleString("default", { month: "short" }),
+         date.toLocaleString(locale?.code, { month: "short" }),
        ...formatters,
      }}
```

### Update CalendarDayButton to accept locale.

Update the `CalendarDayButton` component signature and pass `locale`:

```
Copy  function CalendarDayButton({
    className,
    day,
    modifiers,
+   locale,
    ...props
- }: React.ComponentProps<typeof DayButton>) {
+ }: React.ComponentProps<typeof DayButton> & { locale?: Partial<Locale> }) {
```

### Update date formatting in CalendarDayButton.

Use `locale?.code` in the date formatting:

```
Copy    <Button
      variant="ghost"
      size="icon"
-     data-day={day.date.toLocaleDateString()}
+     data-day={day.date.toLocaleDateString(locale?.code)}
      ...
    />
```

### Pass locale to DayButton component.

Update the `DayButton` component usage to pass the `locale` prop:

```
Copy      components={{
        ...
-       DayButton: CalendarDayButton,
+       DayButton: ({ ...props }) => (
+         <CalendarDayButton locale={locale} {...props} />
+       ),
        ...
      }}
```

### Update RTL-aware CSS classes.

Replace directional classes with logical properties for better RTL support:

```
Copy  // In the day classNames:
- [&:last-child[data-selected=true]_button]:rounded-r-(--cell-radius)
+ [&:last-child[data-selected=true]_button]:rounded-e-(--cell-radius)
- [&:nth-child(2)[data-selected=true]_button]:rounded-l-(--cell-radius)
+ [&:nth-child(2)[data-selected=true]_button]:rounded-s-(--cell-radius)
- [&:first-child[data-selected=true]_button]:rounded-l-(--cell-radius)
+ [&:first-child[data-selected=true]_button]:rounded-s-(--cell-radius)
 
  // In range_start classNames:
- rounded-l-(--cell-radius) ... after:right-0
+ rounded-s-(--cell-radius) ... after:end-0
 
  // In range_end classNames:
- rounded-r-(--cell-radius) ... after:left-0
+ rounded-e-(--cell-radius) ... after:start-0
 
  // In CalendarDayButton className:
- data-[range-end=true]:rounded-r-(--cell-radius)
+ data-[range-end=true]:rounded-e-(--cell-radius)
- data-[range-start=true]:rounded-l-(--cell-radius)
+ data-[range-start=true]:rounded-s-(--cell-radius)
```

After applying these changes, you can use the `locale` prop to provide locale-specific formatting:

```
Copyimport { enUS } from "react-day-picker/locale"
 
;<Calendar mode="single" selected={date} onSelect={setDate} locale={enUS} />
```

[Button Group](/docs/components/radix/button-group)[Card](/docs/components/radix/card)

On This Page

[Blocks](#blocks)[Installation](#installation)[Usage](#usage)[About](#about)[Date Picker](#date-picker)[Persian / Hijri / Jalali Calendar](#persian--hijri--jalali-calendar)[Selected Date (With TimeZone)](#selected-date-with-timezone)[Examples](#examples)[Basic](#basic)[Range Calendar](#range-calendar)[Month and Year Selector](#month-and-year-selector)[Presets](#presets)[Date and Time Picker](#date-and-time-picker)[Booked dates](#booked-dates)[Custom Cell Size](#custom-cell-size)[Week Numbers](#week-numbers)[RTL](#rtl)[API Reference](#api-reference)[Changelog](#changelog)[RTL Support](#rtl-support)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
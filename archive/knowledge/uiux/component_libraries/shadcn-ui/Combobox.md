# Combobox

Source: https://ui.shadcn.com/docs/components/combobox

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

# Combobox

Copy Page

[Previous](/docs/components/radix/collapsible)[Next](/docs/components/radix/command)

Autocomplete input with a list of suggestions.

[Radix UI](/docs/components/radix/combobox)[Base UI](/docs/components/base/combobox)

Copy

```
"use client"

import {
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add combobox
```

Copy
```

## Usage

```
Copyimport {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@/components/ui/combobox"
```

```
Copyconst frameworks = ["Next.js", "SvelteKit", "Nuxt.js", "Remix", "Astro"]
 
export function ExampleCombobox() {
  return (
    <Combobox items={frameworks}>
      <ComboboxInput placeholder="Select a framework" />
      <ComboboxContent>
        <ComboboxEmpty>No items found.</ComboboxEmpty>
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {item}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}
```

## Custom Items

Use `itemToStringValue` when your items are objects.

```
Copyimport * as React from "react"
 
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@/components/ui/combobox"
 
type Framework = {
  label: string
  value: string
}
 
const frameworks: Framework[] = [
  { label: "Next.js", value: "next" },
  { label: "SvelteKit", value: "sveltekit" },
  { label: "Nuxt", value: "nuxt" },
]
 
export function ExampleComboboxCustomItems() {
  return (
    <Combobox
      items={frameworks}
      itemToStringValue={(framework) => framework.label}
    >
      <ComboboxInput placeholder="Select a framework" />
      <ComboboxContent>
        <ComboboxEmpty>No items found.</ComboboxEmpty>
        <ComboboxList>
          {(framework) => (
            <ComboboxItem key={framework.value} value={framework}>
              {framework.label}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}
```

## Multiple Selection

Use `multiple` with chips for multi-select behavior.

```
Copyimport * as React from "react"
 
import {
  Combobox,
  ComboboxChip,
  ComboboxChips,
  ComboboxChipsInput,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
  ComboboxValue,
} from "@/components/ui/combobox"
 
const frameworks = ["Next.js", "SvelteKit", "Nuxt.js", "Remix", "Astro"]
 
export function ExampleComboboxMultiple() {
  const [value, setValue] = React.useState<string[]>([])
 
  return (
    <Combobox
      items={frameworks}
      multiple
      value={value}
      onValueChange={setValue}
    >
      <ComboboxChips>
        <ComboboxValue>
          {value.map((item) => (
            <ComboboxChip key={item}>{item}</ComboboxChip>
          ))}
        </ComboboxValue>
        <ComboboxChipsInput placeholder="Add framework" />
      </ComboboxChips>
      <ComboboxContent>
        <ComboboxEmpty>No items found.</ComboboxEmpty>
        <ComboboxList>
          {(item) => (
            <ComboboxItem key={item} value={item}>
              {item}
            </ComboboxItem>
          )}
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  )
}
```

## Examples

### Basic

A simple combobox with a list of frameworks.

Copy

```
"use client"

import {
```

View Code

### Multiple

A combobox with multiple selection using `multiple` and `ComboboxChips`.

Next.js

Copy

```
"use client"

import * as React from "react"
```

View Code

### Clear Button

Use the `showClear` prop to show a clear button.

Copy

```
"use client"

import {
```

View Code

### Groups

Use `ComboboxGroup` and `ComboboxSeparator` to group items.

Copy

```
"use client"

import {
```

View Code

### Custom Items

You can render custom component inside `ComboboxItem`.

Copy

```
"use client"

import {
```

View Code

### Invalid

Use the `aria-invalid` prop to make the combobox invalid.

Copy

```
"use client"

import {
```

View Code

### Disabled

Use the `disabled` prop to disable the combobox.

Copy

```
"use client"

import {
```

View Code

### Auto Highlight

Use the `autoHighlight` prop automatically highlight the first item on filter.

Copy

```
"use client"

import {
```

View Code

### Popup

You can trigger the combobox from a button or any other component by using the `render` prop. Move the `ComboboxInput` inside the `ComboboxContent`.

Select country

Copy

```
"use client"

import { Button } from "@/components/ui/button"
```

View Code

### Input Group

You can add an addon to the combobox by using the `InputGroupAddon` component inside the `ComboboxInput`.

Copy

```
"use client"

import {
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

الفئات

التكنولوجيا

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Base UI](https://base-ui.com/react/components/combobox#api-reference) documentation for more information.

[Collapsible](/docs/components/radix/collapsible)[Command](/docs/components/radix/command)

On This Page

[Installation](#installation)[Usage](#usage)[Custom Items](#custom-items)[Multiple Selection](#multiple-selection)[Examples](#examples)[Basic](#basic)[Multiple](#multiple)[Clear Button](#clear-button)[Groups](#groups)[Custom Items](#custom-items-1)[Invalid](#invalid)[Disabled](#disabled)[Auto Highlight](#auto-highlight)[Popup](#popup)[Input Group](#input-group)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
# Checkbox

Source: https://ui.shadcn.com/docs/components/checkbox

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

# Checkbox

Copy Page

[Previous](/docs/components/radix/chart)[Next](/docs/components/radix/collapsible)

A control that allows the user to toggle between checked and not checked.

[Radix UI](/docs/components/radix/checkbox)[Base UI](/docs/components/base/checkbox)

Accept terms and conditions

Accept terms and conditions

By clicking this checkbox, you agree to the terms.

Enable notifications

Enable notifications

You can enable or disable notifications at any time.

Copy

```
"use client"

import { Checkbox } from "@/components/ui/checkbox"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add checkbox
```

Copy
```

## Usage

```
Copyimport { Checkbox } from "@/components/ui/checkbox"
```

```
Copy<Checkbox />
```

## Checked State

Use `defaultChecked` for uncontrolled checkboxes, or `checked` and
`onCheckedChange` to control the state.

```
Copyimport * as React from "react"
 
export function Example() {
  const [checked, setChecked] = React.useState(false)
 
  return <Checkbox checked={checked} onCheckedChange={setChecked} />
}
```

## Invalid State

Set `aria-invalid` on the checkbox and `data-invalid` on the field wrapper to
show the invalid styles.

Accept terms and conditions

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
```

View Code

## Examples

### Basic

Pair the checkbox with `Field` and `FieldLabel` for proper layout and labeling.

Accept terms and conditions

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
```

View Code

### Description

Use `FieldContent` and `FieldDescription` for helper text.

Accept terms and conditions

By clicking this checkbox, you agree to the terms and conditions.

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import {
  Field,
```

View Code

### Disabled

Use the `disabled` prop to prevent interaction and add the `data-disabled` attribute to the `<Field>` component for disabled styles.

Enable notifications

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
```

View Code

### Group

Use multiple fields to create a checkbox list.

Show these items on the desktop:

Select the items you want to show on the desktop.

Hard disks

External disks

CDs, DVDs, and iPods

Connected servers

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import {
  Field,
```

View Code

### Table

|  | Name | Email | Role |
| --- | --- | --- | --- |
|  | Sarah Chen | sarah.chen@example.com | Admin |
|  | Marcus Rodriguez | marcus.rodriguez@example.com | User |
|  | Priya Patel | priya.patel@example.com | User |
|  | David Kim | david.kim@example.com | Editor |

Copy

```
"use client"

import * as React from "react"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

قبول الشروط والأحكام

قبول الشروط والأحكام

بالنقر على هذا المربع، فإنك توافق على الشروط.

تفعيل الإشعارات

تفعيل الإشعارات

يمكنك تفعيل أو إلغاء تفعيل الإشعارات في أي وقت.

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix UI](https://www.radix-ui.com/docs/primitives/components/checkbox#api-reference) documentation for more information.

[Chart](/docs/components/radix/chart)[Collapsible](/docs/components/radix/collapsible)

On This Page

[Installation](#installation)[Usage](#usage)[Checked State](#checked-state)[Invalid State](#invalid-state)[Examples](#examples)[Basic](#basic)[Description](#description)[Disabled](#disabled)[Group](#group)[Table](#table)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
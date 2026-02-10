# Textarea

Source: https://ui.shadcn.com/docs/components/textarea

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

# Textarea

Copy Page

[Previous](/docs/components/radix/tabs)[Next](/docs/components/radix/toast)

Displays a form textarea or a component that looks like a textarea.

[Radix UI](/docs/components/radix/textarea)[Base UI](/docs/components/base/textarea)

Copy

```
import { Textarea } from "@/components/ui/textarea"

export function TextareaDemo() {
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add textarea
```

Copy
```

## Usage

```
Copyimport { Textarea } from "@/components/ui/textarea"
```

```
Copy<Textarea />
```

## Examples

### Field

Use `Field`, `FieldLabel`, and `FieldDescription` to create a textarea with a label and description.

Message

Enter your message below.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Textarea } from "@/components/ui/textarea"
```

View Code

### Disabled

Use the `disabled` prop to disable the textarea. To style the disabled state, add the `data-disabled` attribute to the `Field` component.

Message

Copy

```
import { Field, FieldLabel } from "@/components/ui/field"
import { Textarea } from "@/components/ui/textarea"
```

View Code

### Invalid

Use the `aria-invalid` prop to mark the textarea as invalid. To style the invalid state, add the `data-invalid` attribute to the `Field` component.

Message

Please enter a valid message.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Textarea } from "@/components/ui/textarea"
```

View Code

### Button

Pair with `Button` to create a textarea with a submit button.

Send message

Copy

```
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

التعليقات

شاركنا أفكارك حول خدمتنا.

Copy

```
"use client"

import * as React from "react"
```

View Code

[Tabs](/docs/components/radix/tabs)[Toast](/docs/components/radix/toast)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Field](#field)[Disabled](#disabled)[Invalid](#invalid)[Button](#button)[RTL](#rtl)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
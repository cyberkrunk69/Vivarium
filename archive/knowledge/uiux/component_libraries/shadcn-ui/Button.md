# Button

Source: https://ui.shadcn.com/docs/components/button

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

# Button

Copy Page

[Previous](/docs/components/radix/breadcrumb)[Next](/docs/components/radix/button-group)

Displays a button or a component that looks like a button.

[Radix UI](/docs/components/radix/button)[Base UI](/docs/components/base/button)

Button

Copy

```
import { Button } from "@/components/ui/button"
import { ArrowUpIcon } from "lucide-react"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add button
```

Copy
```

## Usage

```
Copyimport { Button } from "@/components/ui/button"
```

```
Copy<Button variant="outline">Button</Button>
```

## Cursor

Tailwind v4 [switched](https://tailwindcss.com/docs/upgrade-guide#buttons-use-the-default-cursor) from `cursor: pointer` to `cursor: default` for the button component.

If you want to keep the `cursor: pointer` behavior, add the following code to your CSS file:

globals.css

```
Copy@layer base {
  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}
```

## Examples

### Size

Use the `size` prop to change the size of the button.

Extra Small

Small

Default

Large

Copy

```
import { Button } from "@/components/ui/button"
import { ArrowUpRightIcon } from "lucide-react"
```

View Code

### Default

Button

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonDefault() {
```

View Code

### Outline

Outline

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonOutline() {
```

View Code

### Secondary

Secondary

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonSecondary() {
```

View Code

### Ghost

Ghost

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonGhost() {
```

View Code

### Destructive

Destructive

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonDestructive() {
```

View Code

### Link

Link

Copy

```
import { Button } from "@/components/ui/button"

export function ButtonLink() {
```

View Code

### Icon

Copy

```
import { Button } from "@/components/ui/button"
import { CircleFadingArrowUpIcon } from "lucide-react"
```

View Code

### With Icon

Remember to add the `data-icon="inline-start"` or `data-icon="inline-end"` attribute to the icon for the correct spacing.

New Branch

Copy

```
import { Button } from "@/components/ui/button"
import { IconGitBranch } from "@tabler/icons-react"
```

View Code

### Rounded

Use the `rounded-full` class to make the button rounded.

Copy

```
import { Button } from "@/components/ui/button"
import { ArrowUpIcon } from "lucide-react"
```

View Code

### Spinner

Render a `<Spinner />` component inside the button to show a loading state. Remember to add the `data-icon="inline-start"` or `data-icon="inline-end"` attribute to the spinner for the correct spacing.

GeneratingDownloading

Copy

```
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"
```

View Code

### Button Group

To create a button group, use the `ButtonGroup` component. See the [Button Group](/docs/components/radix/button-group) documentation for more details.

ArchiveReport

Snooze

Copy

```
"use client"

import * as React from "react"
```

View Code

### Link

You can use the `asChild` prop on `<Button />` to make another component look like a button. Here's an example of a link that looks like a button.

[Login](/login)

Copy

```
import Link from "next/link"
import { Button } from "@/components/ui/button"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

زرحذفإرسال  جاري التحميل

Copy

```
"use client"

import { Button } from "@/examples/radix/ui-rtl/button"
```

View Code

## API Reference

### Button

The `Button` component is a wrapper around the `button` element that adds a variety of styles and functionality.

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" | "outline" | "ghost" | "destructive" | "secondary" | "link"` | `"default"` |
| `size` | `"default" | "xs" | "sm" | "lg" | "icon" | "icon-xs" | "icon-sm" | "icon-lg"` | `"default"` |
| `asChild` | `boolean` | `false` |

[Breadcrumb](/docs/components/radix/breadcrumb)[Button Group](/docs/components/radix/button-group)

On This Page

[Installation](#installation)[Usage](#usage)[Cursor](#cursor)[Examples](#examples)[Size](#size)[Default](#default)[Outline](#outline)[Secondary](#secondary)[Ghost](#ghost)[Destructive](#destructive)[Link](#link)[Icon](#icon)[With Icon](#with-icon)[Rounded](#rounded)[Spinner](#spinner)[Button Group](#button-group)[Link](#link-1)[RTL](#rtl)[API Reference](#api-reference)[Button](#button)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
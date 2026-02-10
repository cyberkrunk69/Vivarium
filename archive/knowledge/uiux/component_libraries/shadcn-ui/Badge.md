# Badge

Source: https://ui.shadcn.com/docs/components/badge

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

# Badge

Copy Page

[Previous](/docs/components/radix/avatar)[Next](/docs/components/radix/breadcrumb)

Displays a badge or a component that looks like a badge.

[Radix UI](/docs/components/radix/badge)[Base UI](/docs/components/base/badge)

BadgeSecondaryDestructiveOutline

Copy

```
import { Badge } from "@/components/ui/badge"

export function BadgeDemo() {
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add badge
```

Copy
```

## Usage

```
Copyimport { Badge } from "@/components/ui/badge"
```

```
Copy<Badge variant="default | outline | secondary | destructive">Badge</Badge>
```

## Examples

### Variants

Use the `variant` prop to change the variant of the badge.

DefaultSecondaryDestructiveOutlineGhost

Copy

```
import { Badge } from "@/components/ui/badge"

export function BadgeVariants() {
```

View Code

### With Icon

You can render an icon inside the badge. Use `data-icon="inline-start"` to render the icon on the left and `data-icon="inline-end"` to render the icon on the right.

VerifiedBookmark

Copy

```
import { Badge } from "@/components/ui/badge"
import { BadgeCheck, BookmarkIcon } from "lucide-react"
```

View Code

### With Spinner

You can render a spinner inside the badge. Remember to add the `data-icon="inline-start"` or `data-icon="inline-end"` prop to the spinner.

DeletingGenerating

Copy

```
import { Badge } from "@/components/ui/badge"
import { Spinner } from "@/components/ui/spinner"
```

View Code

### Link

Use the `asChild` prop to render a link as a badge.

[Open Link](#link)

Copy

```
import { Badge } from "@/components/ui/badge"
import { ArrowUpRightIcon } from "lucide-react"
```

View Code

### Custom Colors

You can customize the colors of a badge by adding custom classes such as `bg-green-50 dark:bg-green-800` to the `Badge` component.

BlueGreenSkyPurpleRed

Copy

```
import { Badge } from "@/components/ui/badge"

export function BadgeCustomColors() {
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

شارةثانويمدمرمخططمتحققإشارة مرجعية

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

### Badge

The `Badge` component displays a badge or a component that looks like a badge.

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" | "secondary" | "destructive" | "outline" | "ghost" | "link"` | `"default"` |
| `className` | `string` | - |

[Avatar](/docs/components/radix/avatar)[Breadcrumb](/docs/components/radix/breadcrumb)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Variants](#variants)[With Icon](#with-icon)[With Spinner](#with-spinner)[Link](#link)[Custom Colors](#custom-colors)[RTL](#rtl)[API Reference](#api-reference)[Badge](#badge)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
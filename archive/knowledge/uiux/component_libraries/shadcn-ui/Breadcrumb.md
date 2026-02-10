# Breadcrumb

Source: https://ui.shadcn.com/docs/components/breadcrumb

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

# Breadcrumb

Copy Page

[Previous](/docs/components/radix/badge)[Next](/docs/components/radix/button)

Displays the path to the current resource using a hierarchy of links.

[Radix UI](/docs/components/radix/breadcrumb)[Base UI](/docs/components/base/breadcrumb)

Copy

```
import Link from "next/link"
import {
  Breadcrumb,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add breadcrumb
```

Copy
```

## Usage

```
Copyimport {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
```

```
Copy<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>Breadcrumb</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>
```

## Examples

### Basic

A basic breadcrumb with a home link and a components link.

Copy

```
import {
  Breadcrumb,
  BreadcrumbItem,
```

View Code

### Custom separator

Use a custom component as `children` for `<BreadcrumbSeparator />` to create a custom separator.

Copy

```
import Link from "next/link"
import {
  Breadcrumb,
```

View Code

### Dropdown

You can compose `<BreadcrumbItem />` with a `<DropdownMenu />` to create a dropdown in the breadcrumb.

Copy

```
import Link from "next/link"
import {
  Breadcrumb,
```

View Code

### Collapsed

We provide a `<BreadcrumbEllipsis />` component to show a collapsed state when the breadcrumb is too long.

Copy

```
import Link from "next/link"
import {
  Breadcrumb,
```

View Code

### Link component

To use a custom link component from your routing library, you can use the `asChild` prop on `<BreadcrumbLink />`.

Copy

```
import Link from "next/link"
import {
  Breadcrumb,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

### Breadcrumb

The `Breadcrumb` component is the root navigation element that wraps all breadcrumb components.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### BreadcrumbList

The `BreadcrumbList` component displays the ordered list of breadcrumb items.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### BreadcrumbItem

The `BreadcrumbItem` component wraps individual breadcrumb items.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### BreadcrumbLink

The `BreadcrumbLink` component displays a clickable link in the breadcrumb.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### BreadcrumbPage

The `BreadcrumbPage` component displays the current page in the breadcrumb (non-clickable).

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### BreadcrumbSeparator

The `BreadcrumbSeparator` component displays a separator between breadcrumb items. You can pass custom children to override the default separator icon.

| Prop | Type | Default |
| --- | --- | --- |
| `children` | `React.ReactNode` | - |
| `className` | `string` | - |

### BreadcrumbEllipsis

The `BreadcrumbEllipsis` component displays an ellipsis indicator for collapsed breadcrumb items.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

[Badge](/docs/components/radix/badge)[Button](/docs/components/radix/button)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Custom separator](#custom-separator)[Dropdown](#dropdown)[Collapsed](#collapsed)[Link component](#link-component)[RTL](#rtl)[API Reference](#api-reference)[Breadcrumb](#breadcrumb)[BreadcrumbList](#breadcrumblist)[BreadcrumbItem](#breadcrumbitem)[BreadcrumbLink](#breadcrumblink)[BreadcrumbPage](#breadcrumbpage)[BreadcrumbSeparator](#breadcrumbseparator)[BreadcrumbEllipsis](#breadcrumbellipsis)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
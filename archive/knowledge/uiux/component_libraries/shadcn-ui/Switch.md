# Switch

Source: https://ui.shadcn.com/docs/components/switch

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

# Switch

Copy Page

[Previous](/docs/components/radix/spinner)[Next](/docs/components/radix/table)

A control that allows the user to toggle between checked and not checked.

[Radix UI](/docs/components/radix/switch)[Base UI](/docs/components/base/switch)

Airplane Mode

Copy

```
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add switch
```

Copy
```

## Usage

```
Copyimport { Switch } from "@/components/ui/switch"
```

```
Copy<Switch />
```

## Examples

### Description

Share across devices

Focus is shared across devices, and turns off when you leave the app.

Copy

```
import {
  Field,
  FieldContent,
```

View Code

### Choice Card

Card-style selection where `FieldLabel` wraps the entire `Field` for a clickable card pattern.

Share across devices

Focus is shared across devices, and turns off when you leave the app.

Enable notifications

Receive notifications when focus mode is enabled or disabled.

Copy

```
import {
  Field,
  FieldContent,
```

View Code

### Disabled

Add the `disabled` prop to the `Switch` component to disable the switch. Add the `data-disabled` prop to the `Field` component for styling.

Disabled

Copy

```
import { Field, FieldLabel } from "@/components/ui/field"
import { Switch } from "@/components/ui/switch"
```

View Code

### Invalid

Add the `aria-invalid` prop to the `Switch` component to indicate an invalid state. Add the `data-invalid` prop to the `Field` component for styling.

Accept terms and conditions

You must accept the terms and conditions to continue.

Copy

```
import {
  Field,
  FieldContent,
```

View Code

### Size

Use the `size` prop to change the size of the switch.

Small

Default

Copy

```
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Switch } from "@/components/ui/switch"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

المشاركة عبر الأجهزة

يتم مشاركة التركيز عبر الأجهزة، ويتم إيقاف تشغيله عند مغادرة التطبيق.

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix Switch](https://www.radix-ui.com/docs/primitives/components/switch#api-reference) documentation.

[Spinner](/docs/components/radix/spinner)[Table](/docs/components/radix/table)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Description](#description)[Choice Card](#choice-card)[Disabled](#disabled)[Invalid](#invalid)[Size](#size)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
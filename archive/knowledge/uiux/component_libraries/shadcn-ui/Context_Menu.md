# Context Menu

Source: https://ui.shadcn.com/docs/components/context-menu

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

# Context Menu

Copy Page

[Previous](/docs/components/radix/command)[Next](/docs/components/radix/data-table)

Displays a menu of actions triggered by a right click.

[Radix UI](/docs/components/radix/context-menu)[Base UI](/docs/components/base/context-menu)

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuCheckboxItem,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add context-menu
```

Copy
```

## Usage

```
Copyimport {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"
```

```
Copy<ContextMenu>
  <ContextMenuTrigger>Right click here</ContextMenuTrigger>
  <ContextMenuContent>
    <ContextMenuItem>Profile</ContextMenuItem>
    <ContextMenuItem>Billing</ContextMenuItem>
    <ContextMenuItem>Team</ContextMenuItem>
    <ContextMenuItem>Subscription</ContextMenuItem>
  </ContextMenuContent>
</ContextMenu>
```

## Examples

### Basic

A simple context menu with a few actions.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

### Submenu

Use `ContextMenuSub` to nest secondary actions.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

### Shortcuts

Add `ContextMenuShortcut` to show keyboard hints.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

### Groups

Group related actions and separate them with dividers.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

### Icons

Combine icons with labels for quick scanning.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

### Checkboxes

Use `ContextMenuCheckboxItem` for toggles.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuCheckboxItem,
```

View Code

### Radio

Use `ContextMenuRadioItem` for exclusive choices.

Right click hereLong press here

Copy

```
"use client"

import * as React from "react"
```

View Code

### Destructive

Use `variant="destructive"` to style the menu item as destructive.

Right click hereLong press here

Copy

```
import {
  ContextMenu,
  ContextMenuContent,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

انقر بزر الماوس الأيمن هنااضغط مطولاً هنا

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix UI](https://www.radix-ui.com/docs/primitives/components/context-menu#api-reference) documentation for more information.

[Command](/docs/components/radix/command)[Data Table](/docs/components/radix/data-table)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Submenu](#submenu)[Shortcuts](#shortcuts)[Groups](#groups)[Icons](#icons)[Checkboxes](#checkboxes)[Radio](#radio)[Destructive](#destructive)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
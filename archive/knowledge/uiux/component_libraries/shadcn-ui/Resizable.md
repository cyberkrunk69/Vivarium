# Resizable

Source: https://ui.shadcn.com/docs/components/resizable

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

# Resizable

Copy Page

[Previous](/docs/components/radix/radio-group)[Next](/docs/components/radix/scroll-area)

Accessible resizable panel groups and layouts with keyboard support.

[Radix UI](/docs/components/radix/resizable)[Base UI](/docs/components/base/resizable)

One

Two

Three

Copy

```
import {
  ResizableHandle,
  ResizablePanel,
```

View Code

## About

The `Resizable` component is built on top of [react-resizable-panels](https://github.com/bvaughn/react-resizable-panels) by [bvaughn](https://github.com/bvaughn).

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add resizable
```

Copy
```

## Usage

```
Copyimport {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"
```

```
Copy<ResizablePanelGroup orientation="horizontal">
  <ResizablePanel>One</ResizablePanel>
  <ResizableHandle />
  <ResizablePanel>Two</ResizablePanel>
</ResizablePanelGroup>
```

## Examples

### Vertical

Use `orientation="vertical"` for vertical resizing.

Header

Content

Copy

```
import {
  ResizableHandle,
  ResizablePanel,
```

View Code

### Handle

Use the `withHandle` prop on `ResizableHandle` to show a visible handle.

Sidebar

Content

Copy

```
import {
  ResizableHandle,
  ResizablePanel,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

واحد

اثنان

ثلاثة

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [react-resizable-panels](https://github.com/bvaughn/react-resizable-panels/tree/main/packages/react-resizable-panels) documentation.

## Changelog

### 2025-02-02 `react-resizable-panels` v4

Updated to `react-resizable-panels` v4. See the [v4.0.0 release notes](https://github.com/bvaughn/react-resizable-panels/releases/tag/4.0.0) for full details.

If you're using `react-resizable-panels` primitives directly, note the following changes:

| v3 | v4 |
| --- | --- |
| `PanelGroup` | `Group` |
| `PanelResizeHandle` | `Separator` |
| `direction` prop | `orientation` prop |
| `defaultSize={50}` | `defaultSize="50%"` |
| `onLayout` | `onLayoutChange` |
| `ImperativePanelHandle` | `PanelImperativeHandle` |
| `ref` prop on Panel | `panelRef` prop |
| `data-panel-group-direction` | `aria-orientation` |

The shadcn/ui wrapper components (`ResizablePanelGroup`, `ResizablePanel`,
`ResizableHandle`) remain unchanged.

[Radio Group](/docs/components/radix/radio-group)[Scroll Area](/docs/components/radix/scroll-area)

On This Page

[About](#about)[Installation](#installation)[Usage](#usage)[Examples](#examples)[Vertical](#vertical)[Handle](#handle)[RTL](#rtl)[API Reference](#api-reference)[Changelog](#changelog)[2025-02-02 `react-resizable-panels` v4](#2025-02-02-react-resizable-panels-v4)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
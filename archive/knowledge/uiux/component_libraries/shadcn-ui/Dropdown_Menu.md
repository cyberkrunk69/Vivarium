# Dropdown Menu

Source: https://ui.shadcn.com/docs/components/dropdown-menu

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

# Dropdown Menu

Copy Page

[Previous](/docs/components/radix/drawer)[Next](/docs/components/radix/empty)

Displays a menu to the user — such as a set of actions or functions — triggered by a button.

[Radix UI](/docs/components/radix/dropdown-menu)[Base UI](/docs/components/base/dropdown-menu)

Open

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add dropdown-menu
```

Copy
```

## Usage

```
Copyimport { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
```

```
Copy<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Open</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuGroup>
      <DropdownMenuLabel>My Account</DropdownMenuLabel>
      <DropdownMenuItem>Profile</DropdownMenuItem>
      <DropdownMenuItem>Billing</DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuGroup>
      <DropdownMenuSeparator />
      <DropdownMenuItem>Team</DropdownMenuItem>
      <DropdownMenuItem>Subscription</DropdownMenuItem>
    </DropdownMenuGroup>
  </DropdownMenuContent>
</DropdownMenu>
```

## Examples

### Basic

A basic dropdown menu with labels and separators.

Open

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

### Submenu

Use `DropdownMenuSub` to nest secondary actions.

Open

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

### Shortcuts

Add `DropdownMenuShortcut` to show keyboard hints.

Open

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

### Icons

Combine icons with labels for quick scanning.

Open

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

### Checkboxes

Use `DropdownMenuCheckboxItem` for toggles.

Open

Copy

```
"use client"

import * as React from "react"
```

View Code

### Checkboxes Icons

Add icons to checkbox items.

Notifications

Copy

```
"use client"

import * as React from "react"
```

View Code

### Radio Group

Use `DropdownMenuRadioGroup` for exclusive choices.

Open

Copy

```
"use client"

import * as React from "react"
```

View Code

### Radio Icons

Show radio options with icons.

Payment Method

Copy

```
"use client"

import * as React from "react"
```

View Code

### Destructive

Use `variant="destructive"` for irreversible actions.

Actions

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

### Avatar

An account switcher dropdown triggered by an avatar.

LR

Copy

```
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
```

View Code

### Complex

A richer example combining groups, icons, and submenus.

Complex Menu

Copy

```
"use client"

import * as React from "react"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

افتح القائمة

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix UI documentation](https://www.radix-ui.com/docs/primitives/components/dropdown-menu) for the full API reference.

[Drawer](/docs/components/radix/drawer)[Empty](/docs/components/radix/empty)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Submenu](#submenu)[Shortcuts](#shortcuts)[Icons](#icons)[Checkboxes](#checkboxes)[Checkboxes Icons](#checkboxes-icons)[Radio Group](#radio-group)[Radio Icons](#radio-icons)[Destructive](#destructive)[Avatar](#avatar)[Complex](#complex)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
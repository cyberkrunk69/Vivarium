# Avatar

Source: https://ui.shadcn.com/docs/components/avatar

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

# Avatar

Copy Page

[Previous](/docs/components/radix/aspect-ratio)[Next](/docs/components/radix/badge)

An image element with a fallback for representing the user.

[Radix UI](/docs/components/radix/avatar)[Base UI](/docs/components/base/avatar)

CNER

CNLRER

+3

Copy

```
import {
  Avatar,
  AvatarBadge,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add avatar
```

Copy
```

## Usage

```
Copyimport { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
```

```
Copy<Avatar>
  <AvatarImage src="https://github.com/shadcn.png" />
  <AvatarFallback>CN</AvatarFallback>
</Avatar>
```

## Examples

### Basic

A basic avatar component with an image and a fallback.

CN

Copy

```
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function AvatarDemo() {
```

View Code

### Badge

Use the `AvatarBadge` component to add a badge to the avatar. The badge is positioned at the bottom right of the avatar.

CN

Copy

```
import {
  Avatar,
  AvatarBadge,
```

View Code

Use the `className` prop to add custom styles to the badge such as custom colors, sizes, etc.

```
Copy<Avatar>
  <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
  <AvatarFallback>CN</AvatarFallback>
  <AvatarBadge className="bg-green-600 dark:bg-green-800" />
</Avatar>
```

### Badge with Icon

You can also use an icon inside `<AvatarBadge>`.

PP

Copy

```
import {
  Avatar,
  AvatarBadge,
```

View Code

### Avatar Group

Use the `AvatarGroup` component to add a group of avatars.

CNLRER

Copy

```
import {
  Avatar,
  AvatarFallback,
```

View Code

### Avatar Group Count

Use `<AvatarGroupCount>` to add a count to the group.

CNLRER

+3

Copy

```
import {
  Avatar,
  AvatarFallback,
```

View Code

### Avatar Group with Icon

You can also use an icon inside `<AvatarGroupCount>`.

CNLRER

Copy

```
import {
  Avatar,
  AvatarFallback,
```

View Code

### Sizes

Use the `size` prop to change the size of the avatar.

CNCNCN

Copy

```
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function AvatarSizeExample() {
```

View Code

### Dropdown

You can use the `Avatar` component as a trigger for a dropdown menu.

CN

Copy

```
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

CNER

CNLRER

+٣

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

### Avatar

The `Avatar` component is the root component that wraps the avatar image and fallback.

| Prop | Type | Default |
| --- | --- | --- |
| `size` | `"default" | "sm" | "lg"` | `"default"` |
| `className` | `string` | - |

### AvatarImage

The `AvatarImage` component displays the avatar image. It accepts all Radix UI Avatar Image props.

| Prop | Type | Default |
| --- | --- | --- |
| `src` | `string` | - |
| `alt` | `string` | - |
| `className` | `string` | - |

### AvatarFallback

The `AvatarFallback` component displays a fallback when the image fails to load. It accepts all Radix UI Avatar Fallback props.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AvatarBadge

The `AvatarBadge` component displays a badge indicator on the avatar, typically positioned at the bottom right.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AvatarGroup

The `AvatarGroup` component displays a group of avatars with overlapping styling.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AvatarGroupCount

The `AvatarGroupCount` component displays a count indicator in an avatar group, typically showing the number of additional avatars.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

For more information about Radix UI Avatar props, see the [Radix UI documentation](https://www.radix-ui.com/primitives/docs/components/avatar#api-reference).

[Aspect Ratio](/docs/components/radix/aspect-ratio)[Badge](/docs/components/radix/badge)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Badge](#badge)[Badge with Icon](#badge-with-icon)[Avatar Group](#avatar-group)[Avatar Group Count](#avatar-group-count)[Avatar Group with Icon](#avatar-group-with-icon)[Sizes](#sizes)[Dropdown](#dropdown)[RTL](#rtl)[API Reference](#api-reference)[Avatar](#avatar)[AvatarImage](#avatarimage)[AvatarFallback](#avatarfallback)[AvatarBadge](#avatarbadge)[AvatarGroup](#avatargroup)[AvatarGroupCount](#avatargroupcount)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
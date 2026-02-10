# Card

Source: https://ui.shadcn.com/docs/components/card

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

# Card

Copy Page

[Previous](/docs/components/radix/calendar)[Next](/docs/components/radix/carousel)

Displays a card with header, content, and footer.

[Radix UI](/docs/components/radix/card)[Base UI](/docs/components/base/card)

Login to your account

Enter your email below to login to your account

Sign Up

Email

Password[Forgot your password?](#)

LoginLogin with Google

Copy

```
import { Button } from "@/components/ui/button"
import {
  Card,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add card
```

Copy
```

## Usage

```
Copyimport {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
```

```
Copy<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card Description</CardDescription>
    <CardAction>Card Action</CardAction>
  </CardHeader>
  <CardContent>
    <p>Card Content</p>
  </CardContent>
  <CardFooter>
    <p>Card Footer</p>
  </CardFooter>
</Card>
```

## Examples

### Size

Use the `size="sm"` prop to set the size of the card to small. The small size variant uses smaller spacing.

Small Card

This card uses the small size variant.

The card component supports a size prop that can be set to "sm" for a more compact appearance.

Action

Copy

```
import { Button } from "@/components/ui/button"
import {
  Card,
```

View Code

### Image

Add an image before the card header to create a card with an image.

![Event cover](https://avatar.vercel.sh/shadcn1)

Featured

Design systems meetup

A practical talk on component APIs, accessibility, and shipping faster.

View Event

Copy

```
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

تسجيل الدخول إلى حسابك

أدخل بريدك الإلكتروني أدناه لتسجيل الدخول إلى حسابك

إنشاء حساب

البريد الإلكتروني

كلمة المرور[نسيت كلمة المرور؟](#)

تسجيل الدخولتسجيل الدخول باستخدام Google

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

### Card

The `Card` component is the root container for card content.

| Prop | Type | Default |
| --- | --- | --- |
| `size` | `"default" | "sm"` | `"default"` |
| `className` | `string` | - |

### CardHeader

The `CardHeader` component is used for a title, description, and optional action.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardTitle

The `CardTitle` component is used for the card title.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardDescription

The `CardDescription` component is used for helper text under the title.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardAction

The `CardAction` component places content in the top-right of the header (for example, a button or a badge).

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardContent

The `CardContent` component is used for the main card body.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### CardFooter

The `CardFooter` component is used for actions and secondary content at the bottom of the card.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

[Calendar](/docs/components/radix/calendar)[Carousel](/docs/components/radix/carousel)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Size](#size)[Image](#image)[RTL](#rtl)[API Reference](#api-reference)[Card](#card)[CardHeader](#cardheader)[CardTitle](#cardtitle)[CardDescription](#carddescription)[CardAction](#cardaction)[CardContent](#cardcontent)[CardFooter](#cardfooter)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
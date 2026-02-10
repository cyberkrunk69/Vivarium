# Alert

Source: https://ui.shadcn.com/docs/components/alert

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

# Alert

Copy Page

[Previous](/docs/components/radix/accordion)[Next](/docs/components/radix/alert-dialog)

Displays a callout for user attention.

[Radix UI](/docs/components/radix/alert)[Base UI](/docs/components/base/alert)

Payment successful

Your payment of $29.99 has been processed. A receipt has been sent to your email address.

New feature available

We've added dark mode support. You can enable it in your account settings.

Copy

```
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { CheckCircle2Icon, InfoIcon } from "lucide-react"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add alert
```

Copy
```

## Usage

```
Copyimport {
  Alert,
  AlertAction,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
```

```
Copy<Alert>
  <InfoIcon />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components and dependencies to your app using the cli.
  </AlertDescription>
  <AlertAction>
    <Button variant="outline">Enable</Button>
  </AlertAction>
</Alert>
```

## Examples

### Basic

A basic alert with an icon, title and description.

Account updated successfully

Your profile information has been saved. Changes will be reflected immediately.

Copy

```
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { CheckCircle2Icon } from "lucide-react"
```

View Code

### Destructive

Use `variant="destructive"` to create a destructive alert.

Payment failed

Your payment could not be processed. Please check your payment method and try again.

Copy

```
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircleIcon } from "lucide-react"
```

View Code

### Action

Use `AlertAction` to add a button or other action element to the alert.

Dark mode is now available

Enable it under your profile settings to get started.

Enable

Copy

```
import {
  Alert,
  AlertAction,
```

View Code

### Custom Colors

You can customize the alert colors by adding custom classes such as `bg-amber-50 dark:bg-amber-950` to the `Alert` component.

Your subscription will expire in 3 days.

Renew now to avoid service interruption or upgrade to a paid plan to continue using the service.

Copy

```
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertTriangleIcon } from "lucide-react"
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

تم الدفع بنجاح

تمت معالجة دفعتك البالغة 29.99 دولارًا. تم إرسال إيصال إلى عنوان بريدك الإلكتروني.

ميزة جديدة متاحة

لقد أضفنا دعم الوضع الداكن. يمكنك تفعيله في إعدادات حسابك.

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

### Alert

The `Alert` component displays a callout for user attention.

| Prop | Type | Default |
| --- | --- | --- |
| `variant` | `"default" | "destructive"` | `"default"` |

### AlertTitle

The `AlertTitle` component displays the title of the alert.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AlertDescription

The `AlertDescription` component displays the description or content of the alert.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

### AlertAction

The `AlertAction` component displays an action element (like a button) positioned absolutely in the top-right corner of the alert.

| Prop | Type | Default |
| --- | --- | --- |
| `className` | `string` | - |

[Accordion](/docs/components/radix/accordion)[Alert Dialog](/docs/components/radix/alert-dialog)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Destructive](#destructive)[Action](#action)[Custom Colors](#custom-colors)[RTL](#rtl)[API Reference](#api-reference)[Alert](#alert)[AlertTitle](#alerttitle)[AlertDescription](#alertdescription)[AlertAction](#alertaction)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
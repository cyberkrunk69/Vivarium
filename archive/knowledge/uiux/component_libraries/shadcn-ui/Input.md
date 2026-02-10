# Input

Source: https://ui.shadcn.com/docs/components/input

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

# Input

Copy Page

[Previous](/docs/components/radix/hover-card)[Next](/docs/components/radix/input-group)

A text input component for forms and user data entry with built-in styling and accessibility features.

[Radix UI](/docs/components/radix/input)[Base UI](/docs/components/base/input)

API Key

Your API key is encrypted and stored securely.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add input
```

Copy
```

## Usage

```
Copyimport { Input } from "@/components/ui/input"
```

```
Copy<Input />
```

## Examples

### Basic

Copy

```
import { Input } from "@/components/ui/input"

export function InputBasic() {
```

View Code

### Field

Use `Field`, `FieldLabel`, and `FieldDescription` to create an input with a
label and description.

Username

Choose a unique username for your account.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Field Group

Use `FieldGroup` to show multiple `Field` blocks and to build forms.

Name

Email

We'll send updates to this address.

ResetSubmit

Copy

```
import { Button } from "@/components/ui/button"
import {
  Field,
```

View Code

### Disabled

Use the `disabled` prop to disable the input. To style the disabled state, add the `data-disabled` attribute to the `Field` component.

Email

This field is currently disabled.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Invalid

Use the `aria-invalid` prop to mark the input as invalid. To style the invalid state, add the `data-invalid` attribute to the `Field` component.

Invalid Input

This field contains validation errors.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### File

Use the `type="file"` prop to create a file input.

Picture

Select a picture to upload.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Inline

Use `Field` with `orientation="horizontal"` to create an inline input.
Pair with `Button` to create a search input with a button.

Search

Copy

```
import { Button } from "@/components/ui/button"
import { Field } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Grid

Use a grid layout to place multiple inputs side by side.

First Name

Last Name

Copy

```
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Required

Use the `required` attribute to indicate required inputs.

Required Field \*

This field must be filled out.

Copy

```
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Badge

Use `Badge` in the label to highlight a recommended field.

Webhook URL Beta

Copy

```
import { Badge } from "@/components/ui/badge"
import { Field, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
```

View Code

### Input Group

To add icons, text, or buttons inside an input, use the `InputGroup` component. See the [Input Group](/docs/components/input-group) component for more examples.

Website URL

https://

Copy

```
import { Field, FieldLabel } from "@/components/ui/field"
import {
  InputGroup,
```

View Code

### Button Group

To add buttons to an input, use the `ButtonGroup` component. See the [Button Group](/docs/components/button-group) component for more examples.

Search

Search

Copy

```
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { Field, FieldLabel } from "@/components/ui/field"
```

View Code

### Form

A full form example with multiple inputs, a select, and a button.

Name

Email

We'll never share your email with anyone.

Phone

Country

Address

CancelSubmit

Copy

```
import { Button } from "@/components/ui/button"
import {
  Field,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

مفتاح API

مفتاح API الخاص بك مشفر ومخزن بأمان.

Copy

```
"use client"

import * as React from "react"
```

View Code

[Hover Card](/docs/components/radix/hover-card)[Input Group](/docs/components/radix/input-group)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Basic](#basic)[Field](#field)[Field Group](#field-group)[Disabled](#disabled)[Invalid](#invalid)[File](#file)[Inline](#inline)[Grid](#grid)[Required](#required)[Badge](#badge)[Input Group](#input-group)[Button Group](#button-group)[Form](#form)[RTL](#rtl)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
# Input OTP

Source: https://ui.shadcn.com/docs/components/input-otp

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

# Input OTP

Copy Page

[Previous](/docs/components/radix/input-group)[Next](/docs/components/radix/item)

Accessible one-time password component with copy paste functionality.

[Radix UI](/docs/components/radix/input-otp)[Base UI](/docs/components/base/input-otp)

1

2

3

4

5

6

Copy

```
import {
  InputOTP,
  InputOTPGroup,
```

View Code

## About

Input OTP is built on top of [input-otp](https://github.com/guilhermerodz/input-otp) by [@guilherme\_rodz](https://twitter.com/guilherme_rodz).

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add input-otp
```

Copy
```

## Usage

```
Copyimport {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp"
```

```
Copy<InputOTP maxLength={6}>
  <InputOTPGroup>
    <InputOTPSlot index={0} />
    <InputOTPSlot index={1} />
    <InputOTPSlot index={2} />
  </InputOTPGroup>
  <InputOTPSeparator />
  <InputOTPGroup>
    <InputOTPSlot index={3} />
    <InputOTPSlot index={4} />
    <InputOTPSlot index={5} />
  </InputOTPGroup>
</InputOTP>
```

## Pattern

Use the `pattern` prop to define a custom pattern for the OTP input.

```
Copyimport { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"
 
;<InputOTP maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS}>
  ...
</InputOTP>
```

Digits Only

Copy

```
"use client"

import { Field, FieldLabel } from "@/components/ui/field"
```

View Code

## Examples

### Separator

Use the `<InputOTPSeparator />` component to add a separator between input groups.

Copy

```
import {
  InputOTP,
  InputOTPGroup,
```

View Code

### Disabled

Use the `disabled` prop to disable the input.

1

2

3

4

5

6

Copy

```
import {
  InputOTP,
  InputOTPGroup,
```

View Code

### Controlled

Use the `value` and `onChange` props to control the input value.

Enter your one-time password.

Copy

```
"use client"

import * as React from "react"
```

View Code

### Invalid

Use `aria-invalid` on the slots to show an error state.

0

0

0

0

0

0

Copy

```
"use client"

import * as React from "react"
```

View Code

### Four Digits

A common pattern for PIN codes. This uses the `pattern={REGEXP_ONLY_DIGITS}` prop.

Copy

```
"use client"

import {
```

View Code

### Alphanumeric

Use `REGEXP_ONLY_DIGITS_AND_CHARS` to accept both letters and numbers.

Copy

```
"use client"

import {
```

View Code

### Form

Verify your login

Enter the verification code we sent to your email address: m@example.com.

Verification codeResend Code

[I no longer have access to this email address.](#)

Verify

Having trouble signing in? [Contact support](#)

Copy

```
import { Button } from "@/components/ui/button"
import {
  Card,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

رمز التحقق

1

2

3

4

5

6

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [input-otp](https://input-otp.rodz.dev) documentation for more information.

[Input Group](/docs/components/radix/input-group)[Item](/docs/components/radix/item)

On This Page

[About](#about)[Installation](#installation)[Usage](#usage)[Pattern](#pattern)[Examples](#examples)[Separator](#separator)[Disabled](#disabled)[Controlled](#controlled)[Invalid](#invalid)[Four Digits](#four-digits)[Alphanumeric](#alphanumeric)[Form](#form)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)
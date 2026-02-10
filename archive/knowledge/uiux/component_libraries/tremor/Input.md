# Input

Source: https://tremor.so/docs/ui/text-input

---

Inputs

# Input

A form input field.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Input)

Preview

Code

```
"use client"
import { Input } from "@/components/Input"
export const InputHero = () => (  <Input className="mx-auto max-w-xs" placeholder="Enter workspace name" />)
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install tailwind-variants @remixicon/react
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Input [v2.0.0]
   import React from "react"import { RiEyeFill, RiEyeOffFill, RiSearchLine } from "@remixicon/react"import { tv, type VariantProps } from "tailwind-variants"
   import { cx, focusInput, focusRing, hasErrorInput } from "@/lib/utils"
   const inputStyles = tv({  base: [    // base    "relative block w-full appearance-none rounded-md border px-2.5 py-2 shadow-xs outline-hidden transition sm:text-sm",    // border color    "border-gray-300 dark:border-gray-800",    // text color    "text-gray-900 dark:text-gray-50",    // placeholder color    "placeholder-gray-400 dark:placeholder-gray-500",    // background color    "bg-white dark:bg-gray-950",    // disabled    "disabled:border-gray-300 disabled:bg-gray-100 disabled:text-gray-400",    "dark:disabled:border-gray-700 dark:disabled:bg-gray-800 dark:disabled:text-gray-500",    // file    [      "file:-my-2 file:-ml-2.5 file:cursor-pointer file:rounded-l-[5px] file:rounded-r-none file:border-0 file:px-3 file:py-2 file:outline-hidden focus:outline-hidden disabled:pointer-events-none file:disabled:pointer-events-none",      "file:border-solid file:border-gray-300 file:bg-gray-50 file:text-gray-500 file:hover:bg-gray-100 dark:file:border-gray-800 dark:file:bg-gray-950 dark:file:hover:bg-gray-900/20 dark:file:disabled:border-gray-700",      "file:[border-inline-end-width:1px] file:[margin-inline-end:0.75rem]",      "file:disabled:bg-gray-100 file:disabled:text-gray-500 dark:file:disabled:bg-gray-800",    ],    // focus    focusInput,    // invalid (optional)    // "dark:aria-invalid:ring-red-400/20 aria-invalid:ring-2 aria-invalid:ring-red-200 aria-invalid:border-red-500 invalid:ring-2 invalid:ring-red-200 invalid:border-red-500"    // remove search cancel button (optional)    "[&::-webkit-search-cancel-button]:hidden [&::-webkit-search-decoration]:hidden",  ],  variants: {    hasError: {      true: hasErrorInput,    },    // number input    enableStepper: {      false:        "[appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none",    },  },})
   interface InputProps  extends React.InputHTMLAttributes<HTMLInputElement>,    VariantProps<typeof inputStyles> {  inputClassName?: string}
   const Input = React.forwardRef<HTMLInputElement, InputProps>(  (    {      className,      inputClassName,      hasError,      enableStepper = true,      type,      ...props    }: InputProps,    forwardedRef,  ) => {    const [typeState, setTypeState] = React.useState(type)
       const isPassword = type === "password"    const isSearch = type === "search"
       return (      <div className={cx("relative w-full", className)} tremor-id="tremor-raw">        <input          ref={forwardedRef}          type={isPassword ? typeState : type}          className={cx(            inputStyles({ hasError, enableStepper }),            {              "pl-8": isSearch,              "pr-10": isPassword,            },            inputClassName,          )}          {...props}        />        {isSearch && (          <div            className={cx(              // base              "pointer-events-none absolute bottom-0 left-2 flex h-full items-center justify-center",              // text color              "text-gray-400 dark:text-gray-600",            )}          >            <RiSearchLine              className="size-[1.125rem] shrink-0"              aria-hidden="true"            />          </div>        )}        {isPassword && (          <div            className={cx(              "absolute bottom-0 right-0 flex h-full items-center justify-center px-3",            )}          >            <button              aria-label="Change password visibility"              className={cx(                // base                "h-fit w-fit rounded-xs outline-hidden transition-all",                // text                "text-gray-400 dark:text-gray-600",                // hover                "hover:text-gray-500 dark:hover:text-gray-500",                focusRing,              )}              type="button"              onClick={() => {                setTypeState(typeState === "password" ? "text" : "password")              }}            >              <span className="sr-only">                {typeState === "password" ? "Show password" : "Hide password"}              </span>              {typeState === "password" ? (                <RiEyeFill aria-hidden="true" className="size-5 shrink-0" />              ) : (                <RiEyeOffFill aria-hidden="true" className="size-5 shrink-0" />              )}            </button>          </div>        )}      </div>    )  },)
   Input.displayName = "Input"
   export { Input, inputStyles, type InputProps }
   ```

## Example: Input with label

Preview

Code

Insert Email

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputLabelExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="email">Insert Email</Label>    <Input placeholder="Enter email" id="email" name="email" type="email" />  </div>)
```

## Example: Input with type "password"

Clicking on the icon switches the input type from password to text.

Preview

Code

Show password

```
"use client"
import { Input } from "@/components/Input"
export const InputPasswordExample = () => (  <Input    className="mx-auto max-w-xs"    placeholder="Enter password"    type="password"  />)
```

## Example: Input with type "search"

Preview

Code

Search

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputSearchExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="search">Search</Label>    <Input      placeholder="Search addresses"      id="search"      name="search"      type="search"      className="mt-2"    />  </div>)
```

## Example: Input with type "number"

Type number activates the prop enableStepper by default.

Preview

Code

Number of orders

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputNumberExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="order">Number of orders</Label>    <Input      placeholder="Enter orders"      id="order"      name="order"      type="number"      className="mt-2"    />  </div>)
```

## Example: Input with type "file"

Preview

Code

Upload a file

You are only allowed to upload .CSV, .XLSX or .XLS files.

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputFileExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="file">Upload a file</Label>    <Input      id="file"      name="file"      type="file"      className="mt-2"      accept=".csv, .xlsx, .xls"    />    <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">      You are only allowed to upload .CSV, .XLSX or .XLS files.    </p>  </div>)
```

## Example: Input with disabled state

Preview

Code

Email

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputDisabledExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="email">Email</Label>    <Input      disabled      placeholder="Enter email"      id="email"      name="email"      type="email"      className="mt-2"    />  </div>)
```

## Example: Input with error

To style the Input for an error state, use the hasError prop.

Preview

Code

Email

```
"use client"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputHasErrorExample = () => (  <div className="mx-auto max-w-xs space-y-2">    <Label htmlFor="email">Email</Label>    <Input      hasError      placeholder="Enter email"      id="email"      name="email"      type="email"      className="mt-2"    />  </div>)
```

## Example: Controlled input

Preview

Code

Search

Search term:

```
"use client"
import React from "react"
import { Input } from "@/components/Input"import { Label } from "@/components/Label"
export const InputControlledExample = () => {  const [search, setSearch] = React.useState("")  return (    <div className="mx-auto flex max-w-xs flex-col gap-2">      <Label htmlFor="File">Search</Label>      <Input        placeholder="Enter search"        id="search"        name="search"        type="search"        value={search}        onChange={(event) => setSearch(event.target.value)}      />      <p className="text-sm text-gray-500">Search term: {search}</p>    </div>  )}
```

## API Reference: Input

This component is based on the Input element and supports all of its props.

className

string

:   Set a className to the wrapping div of the Input.

inputClassName

string

:   Set a className to the nested input.

hasError

boolean

:   Style for erroneous input.

Default: false
# Tracker

Source: https://tremor.so/docs/visualizations/tracker

---

Visualization

# Tracker

Component for visualizing data related to monitoring.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Tracker)

Preview

Code

```
const data = [Show  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-yellow-600", tooltip: "Warn" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },]
export const TrackerHero = () => <Tracker data={data} />
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm i @radix-ui/react-hover-card
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Tracker [v1.0.0]
   import React from "react"import * as HoverCardPrimitives from "@radix-ui/react-hover-card"
   import { cx } from "@/lib/utils"
   interface TrackerBlockProps {  key?: string | number  color?: string  tooltip?: string  hoverEffect?: boolean  defaultBackgroundColor?: string}
   const Block = ({  color,  tooltip,  defaultBackgroundColor,  hoverEffect,}: TrackerBlockProps) => {  const [open, setOpen] = React.useState(false)  return (    <HoverCardPrimitives.Root      open={open}      onOpenChange={setOpen}      openDelay={0}      closeDelay={0}      tremor-id="tremor-raw"    >      <HoverCardPrimitives.Trigger onClick={() => setOpen(true)} asChild>        <div className="size-full overflow-hidden px-[0.5px] transition first:rounded-l-[4px] first:pl-0 last:rounded-r-[4px] last:pr-0 sm:px-px">          <div            className={cx(              "size-full rounded-[1px]",              color || defaultBackgroundColor,              hoverEffect ? "hover:opacity-50" : "",            )}          />        </div>      </HoverCardPrimitives.Trigger>      <HoverCardPrimitives.Portal>        <HoverCardPrimitives.Content          sideOffset={10}          side="top"          align="center"          avoidCollisions          className={cx(            // base            "w-auto rounded-md px-2 py-1 text-sm shadow-md",            // text color            "text-white dark:text-gray-900",            // background color            "bg-gray-900 dark:bg-gray-50",          )}        >          {tooltip}        </HoverCardPrimitives.Content>      </HoverCardPrimitives.Portal>    </HoverCardPrimitives.Root>  )}
   Block.displayName = "Block"
   interface TrackerProps extends React.HTMLAttributes<HTMLDivElement> {  data: TrackerBlockProps[]  defaultBackgroundColor?: string  hoverEffect?: boolean}
   const Tracker = React.forwardRef<HTMLDivElement, TrackerProps>(  (    {      data = [],      defaultBackgroundColor = "bg-gray-400 dark:bg-gray-400",      className,      hoverEffect,      ...props    },    forwardedRef,  ) => {    return (      <div        ref={forwardedRef}        className={cx("group flex h-8 w-full items-center", className)}        {...props}      >        {data.map((props, index) => (          <Block            key={props.key ?? index}            defaultBackgroundColor={defaultBackgroundColor}            hoverEffect={hoverEffect}            {...props}          />        ))}      </div>    )  },)
   Tracker.displayName = "Tracker"
   export { Tracker, type TrackerBlockProps }
   ```

## Example

To render a Tracker you need to pass an array to the data prop. We use CSS to display different lengths, given different breakpoints.

Preview

Code

```
import { Tracker } from '@/components/Tracker'
const data = [Show  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-yellow-600", tooltip: "Warn" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },
  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-yellow-600", tooltip: "Warn" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },]
export const TrackerBreakpointsExample = () => (  <>    <Tracker className="hidden w-full lg:flex" data={data} />    <Tracker      className="hidden w-full sm:flex lg:hidden"      data={data.slice(0, 60)}    />    <Tracker className="flex w-full sm:hidden" data={data.slice(0, 30)} />  </>)
```

## Example with hoverEffect

Preview

Code

```
"use client"
import { Tracker } from "@/components/Tracker"
const data = [  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-red-600", tooltip: "Error" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-yellow-600", tooltip: "Warn" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },  { color: "bg-emerald-600", tooltip: "Tracker Info" },]
export const TrackerHoverExample = () => (  <Tracker data={data} hoverEffect={true} />)
```

## API Reference: Tracker

data

Required

TrackerBlockProps[]

:   Array of objects, with each object containing a key, color and a tooltip.

    - key?: string | number
    - color?: string
    - tooltip?: string

defaultBackgroundColor

string

:   Background color of a bar, when no color is provided in the data array.

Default: "bg-gray-400 dark:bg-gray-400"

hoverEffect

boolean

:   Add a hover effect to the tracker blocks.

Default: false
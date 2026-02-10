# Card

Source: https://tremor.so/docs/ui/card

---

UI

# Card

A fundamental building block for KPI cards, forms, or sections.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Card)

Preview

Code

Card

```
import { Card } from '@/components/Card';
export const CardHero = () => (  <Card className="mx-auto max-w-xs">    <p className="text-center text-gray-400">Card</p>  </Card>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm i @radix-ui/react-slot
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Card [v1.0.0]
   import React from "react"import { Slot } from "@radix-ui/react-slot"
   import { cx } from "@/lib/utils"
   interface CardProps extends React.ComponentPropsWithoutRef<"div"> {  asChild?: boolean}
   const Card = React.forwardRef<HTMLDivElement, CardProps>(  ({ className, asChild, ...props }, forwardedRef) => {    const Component = asChild ? Slot : "div"    return (      <Component        ref={forwardedRef}        className={cx(          // base          "relative w-full rounded-lg border p-6 text-left shadow-xs",          // background color          "bg-white dark:bg-[#090E1A]",          // border color          "border-gray-200 dark:border-gray-900",          className,        )}        tremor-id="tremor-raw"        {...props}      />    )  },)
   Card.displayName = "Card"
   export { Card, type CardProps }
   ```

## Example: Card with content

Place content inside a Card to visually group it.

Preview

Code

### The greatest of all time (in tennis)

Roger Federer's unparalleled combination of skill, longevity, and versatility has led him to hold numerous records, including the most Grand Slam singles titles.

His graceful and effortless style of play, combined with his sportsmanship and impact on the global tennis community, solidify his legacy as the greatest tennis player of all time.

```
import { Card } from '@/components/Card';
export const CardExample = () => (  <Card className="mx-auto max-w-lg">    <h3 className="font-semibold text-gray-900 dark:text-gray-50">      The greatest of all time (in tennis)    </h3>    <p className="mt-2 text-sm leading-6 text-gray-900 dark:text-gray-50">      Roger Federer's unparalleled combination of skill, longevity, and      versatility has led him to hold numerous records, including the most Grand      Slam singles titles.    </p>    <p className="mt-2 hidden text-sm leading-6 text-gray-900 sm:block dark:text-gray-50">      His graceful and effortless style of play, combined with his sportsmanship      and impact on the global tennis community, solidify his legacy as the      greatest tennis player of all time.    </p>  </Card>);
```

## Example: Card with asChild prop

To render semantically correct list items in the style of a card, wrap the <li> elements within a Card component and apply the asChild prop.

Preview

Code

- This card will be turned into a <li> element
- This card will also be turned into a <li> element

```
import { Card } from '@/components/Card';
export const CardAsChildExample = () => (  <ul role="list" className="flex list-none flex-col gap-4">    <Card asChild>      <li className="text-gray-900 dark:text-gray-50">        This card will be turned into a {`<li>`} element      </li>    </Card>    <Card asChild>      <li className="text-gray-900 dark:text-gray-50">        This card will also be turned into a {`<li>`} element      </li>    </Card>  </ul>);
```

## API Reference: Card

This component is based on the div element and supports all of its props.

asChild

boolean

:   When enabled, the wrapper component is rendered as the first child element and its properties combined.

Default: false
# BarList

Source: https://tremor.so/docs/visualizations/bar-list

---

Visualization

# BarList

Horizontal bars with a label inside.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/BarList)

Preview

Code

/home

/documentation

/blocks

/imprint

/cancellation

843

384

108

46

3

```
import { BarList } from "@/components/BarList"import { Toaster } from "@/components/Toaster"import { useToast } from "@/lib/useToast"
const data = [  { name: "/home", value: 843 },  { name: "/imprint", value: 46 },  { name: "/cancellation", value: 3 },  { name: "/blocks", value: 108 },  { name: "/documentation", value: 384 },]
export const BarListHero = () => {  const { toast } = useToast()  return (    <>      <Toaster />      <BarList        data={data}        onValueChange={(item) =>          toast({            description: JSON.stringify(item, null, 2),          })        }      />    </>  )}
```

## Installation

1. 1

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor BarList [v1.0.0]
   import React from "react"
   import { cx, focusRing } from "@/lib/utils"
   type Bar<T> = T & {  key?: string  href?: string  value: number  name: string}
   interface BarListProps<T = unknown>  extends React.HTMLAttributes<HTMLDivElement> {  data: Bar<T>[]  valueFormatter?: (value: number) => string  showAnimation?: boolean  onValueChange?: (payload: Bar<T>) => void  sortOrder?: "ascending" | "descending" | "none"}
   function BarListInner<T>(  {    data = [],    valueFormatter = (value) => value.toString(),    showAnimation = false,    onValueChange,    sortOrder = "descending",    className,    ...props  }: BarListProps<T>,  forwardedRef: React.ForwardedRef<HTMLDivElement>,) {  const Component = onValueChange ? "button" : "div"  const sortedData = React.useMemo(() => {    if (sortOrder === "none") {      return data    }    return [...data].sort((a, b) => {      return sortOrder === "ascending" ? a.value - b.value : b.value - a.value    })  }, [data, sortOrder])
     const widths = React.useMemo(() => {    const maxValue = Math.max(...sortedData.map((item) => item.value), 0)    return sortedData.map((item) =>      item.value === 0 ? 0 : Math.max((item.value / maxValue) * 100, 2),    )  }, [sortedData])
     const rowHeight = "h-8"
     return (    <div      ref={forwardedRef}      className={cx("flex justify-between space-x-6", className)}      aria-sort={sortOrder}      tremor-id="tremor-raw"      {...props}    >      <div className="relative w-full space-y-1.5">        {sortedData.map((item, index) => (          <Component            key={item.key ?? item.name}            onClick={() => {              onValueChange?.(item)            }}            className={cx(              // base              "group w-full rounded-sm",              // focus              focusRing,              onValueChange                ? [                    "-m-0! cursor-pointer",                    // hover                    "hover:bg-gray-50 dark:hover:bg-gray-900",                  ]                : "",            )}          >            <div              className={cx(                // base                "flex items-center rounded-sm transition-all",                rowHeight,                // background color                "bg-blue-200 dark:bg-blue-900",                onValueChange                  ? "group-hover:bg-blue-300 dark:group-hover:bg-blue-800"                  : "",                // margin and duration                {                  "mb-0": index === sortedData.length - 1,                  "duration-800": showAnimation,                },              )}              style={{ width: `${widths[index]}%` }}            >              <div className={cx("absolute left-2 flex max-w-full pr-2")}>                {item.href ? (                  <a                    href={item.href}                    className={cx(                      // base                      "truncate whitespace-nowrap rounded-sm text-sm",                      // text color                      "text-gray-900 dark:text-gray-50",                      // hover                      "hover:underline hover:underline-offset-2",                      // focus                      focusRing,                    )}                    target="_blank"                    rel="noreferrer"                    onClick={(event) => event.stopPropagation()}                  >                    {item.name}                  </a>                ) : (                  <p                    className={cx(                      // base                      "truncate whitespace-nowrap text-sm",                      // text color                      "text-gray-900 dark:text-gray-50",                    )}                  >                    {item.name}                  </p>                )}              </div>            </div>          </Component>        ))}      </div>      <div>        {sortedData.map((item, index) => (          <div            key={item.key ?? item.name}            className={cx(              "flex items-center justify-end",              rowHeight,              index === sortedData.length - 1 ? "mb-0" : "mb-1.5",            )}          >            <p              className={cx(                // base                "truncate whitespace-nowrap text-sm leading-none",                // text color                "text-gray-900 dark:text-gray-50",              )}            >              {valueFormatter(item.value)}            </p>          </div>        ))}      </div>    </div>  )}
   BarListInner.displayName = "BarList"
   const BarList = React.forwardRef(BarListInner) as <T>(  p: BarListProps<T> & { ref?: React.ForwardedRef<HTMLDivElement> },) => ReturnType<typeof BarListInner>
   export { BarList, type BarListProps }
   ```

## Example

To render a BarList you need to pass an array to the data prop.

Preview

Code

/home

/documentation

/blocks

/imprint

/cancellation

843

384

108

46

3

```
import { BarList } from '@/components/BarList'
const data = [  { name: "/home", value: 843 },  { name: "/imprint", value: 46 },  { name: "/cancellation", value: 3 },  { name: "/blocks", value: 108 },  { name: "/documentation", value: 384 },]
export const BarListExample = () => {  return <BarList data={data} />}
```

## Example with sortOrder

To change the sort order, use the sortOrder prop.

Preview

Code

/cancellation

/imprint

/blocks

/documentation

/home

3

46

108

384

843

```
import { BarList } from "@/components/BarList"
const data = [  { name: "/home", value: 843 },  { name: "/imprint", value: 46 },  { name: "/cancellation", value: 3 },  { name: "/blocks", value: 108 },  { name: "/documentation", value: 384 },]
export const BarListSortExample = () => (  <BarList data={data} sortOrder="ascending" />)
```

## Example with href and valueFormatter

When you add a href to the passed array, the labels become anchor tags.

Preview

Code

[/home](https://tremor.so)

[/documentation](https://tremor.so)

[/blocks](https://tremor.so)

[/imprint](https://tremor.so)

[/cancellation](https://tremor.so)

843 Visitors

384 Visitors

108 Visitors

46 Visitors

3 Visitors

```
import { BarList } from '@/components/BarList';
const data = [  { name: "/home", value: 843, href: "https://tremor.so" },  { name: "/imprint", value: 46, href: "https://tremor.so" },  { name: "/cancellation", value: 3, href: "https://tremor.so" },  { name: "/blocks", value: 108, href: "https://tremor.so" },  { name: "/documentation", value: 384, href: "https://tremor.so" },]
export const BarListHrefAndValueFormatterExample = () => (  <BarList data={data} valueFormatter={(value) => `${value} Visitors`} />)
```

## Example with onValueChange

When you add onValueChange to the BarList, the bars become clickable.

Preview

Code

/home

/documentation

/blocks

/imprint

/cancellation

843

384

108

46

3

```
Click on a bar
```

```
import React from "react"import { BarList } from '@/components/BarList'
const data = [  { name: "/home", value: 843 },  { name: "/imprint", value: 46 },  { name: "/cancellation", value: 3 },  { name: "/blocks", value: 108 },  { name: "/documentation", value: 384 },]
export const BarListOnValueChangeExample = () => {  const [selectedItem, setSelectedItem] = React.useState("")  return (    <div className="flex flex-col gap-3">      <BarList        data={data}        onValueChange={(item) => setSelectedItem(JSON.stringify(item, null, 2))}      />      <pre className="w-fit rounded-md bg-gray-100 p-2 font-mono text-sm text-gray-700 dark:bg-gray-800 dark:text-gray-200">        {selectedItem === "" ? "Click on a bar" : selectedItem}      </pre>    </div>  )}
```

## Example with onValueChange and href

It is also possible to combine href and onValueChange.

Preview

Code

[/home](https://tremor.so)

[/documentation](https://tremor.so)

[/blocks](https://tremor.so)

[/imprint](https://tremor.so)

[/cancellation](https://tremor.so)

843

384

108

46

3

```
Click on a bar
```

```
import React from "react"import { BarList } from '@/components/BarList'
const data = [  { name: "/home", value: 843, href: "https://tremor.so" },  { name: "/imprint", value: 46, href: "https://tremor.so" },  { name: "/cancellation", value: 3, href: "https://tremor.so" },  { name: "/blocks", value: 108, href: "https://tremor.so" },  { name: "/documentation", value: 384, href: "https://tremor.so" },]
export const BarListOnValueChangeHrefExample = () => {  const [selectedItem, setSelectedItem] = React.useState("")  return (    <div className="flex flex-col gap-3">      <BarList        data={data}        onValueChange={(item) => setSelectedItem(JSON.stringify(item, null, 2))}      />      <pre className="w-fit rounded-md bg-gray-100 p-2 font-mono text-sm text-gray-700 dark:bg-gray-800 dark:text-gray-200">        {selectedItem === "" ? "Click on a bar" : selectedItem}      </pre>    </div>  )}
```

## API Reference: BarList

data

Required

Bar<T>[]

:   Array of objects, with each object containing a value (number), name (string). Here are the detailed types for Bar<T> = T &

    - value: number
    - name: string
    - key?: string
    - href?: string

onValueChange

(payload: Bar<T>) => void;

:   Handler that is called when the value changes.

showAnimation

boolean

:   Sets an animation to the chart when it is loaded.

Default: false

sortOrder

"ascending" | "descending" | "none"

:   Change the sort order.

Default: desc

valueFormatter

(value: number) => string

:   Controls the text formatting for the y-axis values.
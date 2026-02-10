# Donut Chart

Source: https://tremor.so/docs/visualizations/donut-chart

---

Visualization

# Donut Chart

Displays quantitative information through a circular visualization.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/DonutChart)

Preview

Code

Variant: `donut`

Variant: `pie`

```
"use client"
import { DonutChart } from "@/components/DonutChart"
const data = [  {    name: "SolarCells",    amount: 4890,  },  {    name: "Glass",    amount: 2103,  },  {    name: "JunctionBox",    amount: 2050,  },  {    name: "Adhesive",    amount: 1300,  },  {    name: "BackSheet",    amount: 1100,  },  {    name: "Frame",    amount: 700,  },  {    name: "Encapsulant",    amount: 200,  },]
export const DonutChartHero = () => (  <div className="flex flex-col gap-12">    <div className="flex flex-col items-center justify-center gap-4">      <p className="text-gray-700 dark:text-gray-300">Variant: `donut`</p>      <DonutChart        data={data}        category="name"        value="amount"        valueFormatter={(number: number) =>          `$${Intl.NumberFormat("us").format(number).toString()}`        }      />    </div>    <div className="flex flex-col items-center justify-center gap-4">      <p className="text-gray-700 dark:text-gray-300">Variant: `pie`</p>      <DonutChart        data={data}        variant="pie"        category="name"        value="amount"        valueFormatter={(number: number) =>          `$${Intl.NumberFormat("us").format(number).toString()}`        }      />    </div>  </div>)
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm i recharts
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths. If you have not added the required chartUtils.ts, check out the [add utilities and helpers](/docs/utilities/chartUtils) section in installation.

   Show more

   ```
   // Tremor DonutChart [v1.0.0]/* eslint-disable @typescript-eslint/no-explicit-any */
   "use client"
   import React from "react"import {  Pie,  PieChart as ReChartsDonutChart,  ResponsiveContainer,  Sector,  Tooltip,} from "recharts"
   import {  AvailableChartColors,  constructCategoryColors,  getColorClassName,  type AvailableChartColorsKeys,} from "@/lib/chartUtils"import { cx } from "@/lib/utils"
   const sumNumericArray = (arr: number[]): number =>  arr.reduce((sum, num) => sum + num, 0)
   const parseData = (  data: Record<string, any>[],  categoryColors: Map<string, AvailableChartColorsKeys>,  category: string,) =>  data.map((dataPoint) => ({    ...dataPoint,    color: categoryColors.get(dataPoint[category]) || AvailableChartColors[0],    className: getColorClassName(      categoryColors.get(dataPoint[category]) || AvailableChartColors[0],      "fill",    ),  }))
   const calculateDefaultLabel = (data: any[], valueKey: string): number =>  sumNumericArray(data.map((dataPoint) => dataPoint[valueKey]))
   const parseLabelInput = (  labelInput: string | undefined,  valueFormatter: (value: number) => string,  data: any[],  valueKey: string,): string => labelInput || valueFormatter(calculateDefaultLabel(data, valueKey))
   //#region Tooltip
   type TooltipProps = Pick<ChartTooltipProps, "active" | "payload">
   type PayloadItem = {  category: string  value: number  color: AvailableChartColorsKeys}
   interface ChartTooltipProps {  active: boolean | undefined  payload: PayloadItem[]  valueFormatter: (value: number) => string}
   const ChartTooltip = ({  active,  payload,  valueFormatter,}: ChartTooltipProps) => {  if (active && payload && payload.length) {    return (      <div        className={cx(          // base          "rounded-md border text-sm shadow-md",          // border color          "border-gray-200 dark:border-gray-800",          // background color          "bg-white dark:bg-gray-950",        )}      >        <div className={cx("space-y-1 px-4 py-2")}>          {payload.map(({ value, category, color }, index) => (            <div              key={`id-${index}`}              className="flex items-center justify-between space-x-8"            >              <div className="flex items-center space-x-2">                <span                  aria-hidden="true"                  className={cx(                    "size-2 shrink-0 rounded-full",                    getColorClassName(color, "bg"),                  )}                />                <p                  className={cx(                    // base                    "text-right whitespace-nowrap",                    // text color                    "text-gray-700 dark:text-gray-300",                  )}                >                  {category}                </p>              </div>              <p                className={cx(                  // base                  "text-right font-medium whitespace-nowrap tabular-nums",                  // text color                  "text-gray-900 dark:text-gray-50",                )}              >                {valueFormatter(value)}              </p>            </div>          ))}        </div>      </div>    )  }  return null}
   const renderInactiveShape = (props: any) => {  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, className } =    props
     return (    <Sector      cx={cx}      cy={cy}      innerRadius={innerRadius}      outerRadius={outerRadius}      startAngle={startAngle}      endAngle={endAngle}      className={className}      fill=""      opacity={0.3}      style={{ outline: "none" }}    />  )}
   type DonutChartVariant = "donut" | "pie"
   type BaseEventProps = {  eventType: "sector"  categoryClicked: string  [key: string]: number | string}
   type DonutChartEventProps = BaseEventProps | null | undefined
   interface DonutChartProps extends React.HTMLAttributes<HTMLDivElement> {  data: Record<string, any>[]  category: string  value: string  colors?: AvailableChartColorsKeys[]  variant?: DonutChartVariant  valueFormatter?: (value: number) => string  label?: string  showLabel?: boolean  showTooltip?: boolean  onValueChange?: (value: DonutChartEventProps) => void  tooltipCallback?: (tooltipCallbackContent: TooltipProps) => void  customTooltip?: React.ComponentType<TooltipProps>}
   const DonutChart = React.forwardRef<HTMLDivElement, DonutChartProps>(  (    {      data = [],      value,      category,      colors = AvailableChartColors,      variant = "donut",      valueFormatter = (value: number) => value.toString(),      label,      showLabel = false,      showTooltip = true,      onValueChange,      tooltipCallback,      customTooltip,      className,      ...other    },    forwardedRef,  ) => {    const CustomTooltip = customTooltip    const [activeIndex, setActiveIndex] = React.useState<number | undefined>(      undefined,    )    const isDonut = variant === "donut"    const parsedLabelInput = parseLabelInput(label, valueFormatter, data, value)
       const categories = Array.from(new Set(data.map((item) => item[category])))    const categoryColors = constructCategoryColors(categories, colors)
       const prevActiveRef = React.useRef<boolean | undefined>(undefined)    const prevCategoryRef = React.useRef<string | undefined>(undefined)
       const handleShapeClick = (      data: any,      index: number,      event: React.MouseEvent,    ) => {      event.stopPropagation()      if (!onValueChange) return
         if (activeIndex === index) {        setActiveIndex(undefined)        onValueChange(null)      } else {        setActiveIndex(index)        onValueChange({          eventType: "sector",          categoryClicked: data.payload[category],          ...data.payload,        })      }    }
       return (      <div        ref={forwardedRef}        className={cx("h-40 w-40", className)}        tremor-id="tremor-raw"        {...other}      >        <ResponsiveContainer className="size-full">          <ReChartsDonutChart            onClick={              onValueChange && activeIndex !== undefined                ? () => {                    setActiveIndex(undefined)                    onValueChange(null)                  }                : undefined            }            margin={{ top: 0, left: 0, right: 0, bottom: 0 }}          >            {showLabel && isDonut && (              <text                className="fill-gray-700 dark:fill-gray-300"                x="50%"                y="50%"                textAnchor="middle"                dominantBaseline="middle"              >                {parsedLabelInput}              </text>            )}            <Pie              className={cx(                "stroke-white dark:stroke-gray-950 [&_.recharts-pie-sector]:outline-hidden",                onValueChange ? "cursor-pointer" : "cursor-default",              )}              data={parseData(data, categoryColors, category)}              cx="50%"              cy="50%"              startAngle={90}              endAngle={-270}              innerRadius={isDonut ? "75%" : "0%"}              outerRadius="100%"              stroke=""              strokeLinejoin="round"              dataKey={value}              nameKey={category}              isAnimationActive={false}              onClick={handleShapeClick}              activeIndex={activeIndex}              inactiveShape={renderInactiveShape}              style={{ outline: "none" }}            />            {showTooltip && (              <Tooltip                wrapperStyle={{ outline: "none" }}                isAnimationActive={false}                content={({ active, payload }) => {                  const cleanPayload = payload                    ? payload.map((item: any) => ({                        category: item.payload[category],                        value: item.value,                        color: categoryColors.get(                          item.payload[category],                        ) as AvailableChartColorsKeys,                      }))                    : []
                     const payloadCategory: string = cleanPayload[0]?.category
                     if (                    tooltipCallback &&                    (active !== prevActiveRef.current ||                      payloadCategory !== prevCategoryRef.current)                  ) {                    tooltipCallback({                      active,                      payload: cleanPayload,                    })                    prevActiveRef.current = active                    prevCategoryRef.current = payloadCategory                  }
                     return showTooltip && active ? (                    CustomTooltip ? (                      <CustomTooltip active={active} payload={cleanPayload} />                    ) : (                      <ChartTooltip                        active={active}                        payload={cleanPayload}                        valueFormatter={valueFormatter}                      />                    )                  ) : null                }}              />            )}          </ReChartsDonutChart>        </ResponsiveContainer>      </div>    )  },)
   DonutChart.displayName = "DonutChart"
   export { DonutChart, type DonutChartEventProps, type TooltipProps }
   ```

## Example with label

Preview

Code

```
"use client"
import { DonutChart } from "@/components/DonutChart"
const chartdata = [  {    name: "SolarCells",    amount: 4890,  },  {    name: "Glass",    amount: 2103,  },  {    name: "JunctionBox",    amount: 2050,  },  {    name: "Adhesive",    amount: 1300,  },  {    name: "BackSheet",    amount: 1100,  },  {    name: "Frame",    amount: 700,  },  {    name: "Encapsulant",    amount: 200,  },]
export const DonutChartLabelExample = () => (  <DonutChart    className="mx-auto"    data={chartdata}    category="name"    value="amount"    showLabel={true}    valueFormatter={(number: number) =>      `$${Intl.NumberFormat("us").format(number).toString()}`    }  />)
```

## Example with onValueChange

When you add onValueChange to the DonutChart, it becomes clickable.

Preview

Code

```
null
```

```
"use client"
import React from "react"
import { DonutChart, DonutChartEventProps } from "@/components/DonutChart"
const chartdata = [  {    name: "SolarCells",    amount: 4890,  },  {    name: "Glass",    amount: 2103,  },  {    name: "JunctionBox",    amount: 2050,  },  {    name: "Adhesive",    amount: 1300,  },  {    name: "BackSheet",    amount: 1100,  },  {    name: "Frame",    amount: 700,  },  {    name: "Encapsulant",    amount: 200,  },]
export const DonutChartOnValueChangeExample = () => {  const [value, setValue] = React.useState<DonutChartEventProps>(null)  return (    <>      <DonutChart        className="mx-auto"         data={chartdata}        category="name"        value="amount"        onValueChange={(v) => setValue(v)}      />      <pre className="mt-8 rounded-md bg-gray-950 p-3 text-sm text-white dark:bg-gray-800">        {JSON.stringify(value, null, 2)}      </pre>    </>  )}
```

## Example with tooltipCallback and colors

Preview

Code

Revenue by category

$10,343

```
"use client"
import React from "react"
import { DonutChart, TooltipProps } from "@/components/DonutChart"
interface DataItem {  name: string  amount: number}
const data: DataItem[] = [  {    name: "SolarCells",    amount: 4890,  },  {    name: "Glass",    amount: 2103,  },  {    name: "JunctionBox",    amount: 2050,  },  {    name: "Adhesive",    amount: 1300,  },]
function DonutChartCallbackExample() {  const [datas, setDatas] = React.useState<TooltipProps | null>(null)
  const sumNumericArray = (arr: number[]): number =>    arr.reduce((sum, num) => sum + num, 0)
  const currencyFormatter = (number: number) =>    `$${Intl.NumberFormat("us").format(number)}`
  const payload = datas?.payload?.[0]  const value = payload?.value ?? 0
  const formattedValue = payload    ? currencyFormatter(value)    : currencyFormatter(        sumNumericArray(data.map((dataPoint) => dataPoint.amount)),      )
  return (    <div>      <p className="text-center text-sm text-gray-700 dark:text-gray-300">        Revenue by category      </p>      <p className="mt-2 w-full text-center text-xl font-semibold text-gray-900 dark:text-gray-50">        {formattedValue}      </p>      <DonutChart        data={data}        category="name"        value="amount"        className="mx-auto mt-8"        colors={["blue", "violet", "cyan", "emerald"]}        tooltipCallback={(props) => {          if (props.active) {            setDatas((prev) => {              if (prev?.payload[0].category === props.payload[0].category)                return prev              return props            })          } else {            setDatas(null)          }          return null        }}      />    </div>  )}
```

## API Reference: DonutChart

data

Required

Record<string, any>[]

:   Data used to display the chart.

cateogry

Required

string

:   Key of the data object to map the data to the categories.

value

Required

string

:   Select the value from your data.

colors

AvailableChartColorsKeys[]

:   Change the colors of the categories. To add, update, or remove the colors, edit the 'chartColors' array in your chartUtils.ts file. The AvailableChartColorsKeys will be automatically updated.

Default: AvailableChartColors, which are by default: 'blue' | 'emerald' | 'violet' | 'amber' | 'gray' | 'cyan' | 'pink' | 'lime' | 'fuchsia'

variant

'donut' | 'pie'

:   Select how chart is rendered.

Default: 'donut'

valueFormatter

(value: number) => string

:   Controls the text formatting for the y-axis values. Also used in the Tooltip.

label

string

:   Places a text element in the center of the donut chart. Only available when variant property is set to 'donut'.

showLabel

boolean

:   Controls the visibility of the label displayed in the center. Only available when variant property is set to 'donut'.

Default: false

showTooltip

boolean

:   Controls the visibility of the tooltip.

Default: true

onValueChange

(value: DonutChartEventProps) => void

:   Callback function for when the value of the component changes.

tooltipCallback

(tooltipCallbackContent: TooltipProps) => void

:   Callback function that returns the active, payload, when the tooltip changes.

customTooltip

React.ComponentType<TooltipProps>

:   Render a custom tooltip component.
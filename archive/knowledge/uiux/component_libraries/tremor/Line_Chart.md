# Line Chart

Source: https://tremor.so/docs/visualizations/line-chart

---

Visualization

# Line Chart

Graphical representation connecting one or more series of data points with a line.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/LineChart)

Preview

Code

```
"use client"
import { LineChart } from "@/components/LineChart"
const chartdata = [  {    date: "Jan 23",    SolarPanels: 2890,    Inverters: 2338,  },  {    date: "Feb 23",    SolarPanels: 2756,    Inverters: 2103,  },  {    date: "Mar 23",    SolarPanels: 3322,    Inverters: 2194,  },  {    date: "Apr 23",    SolarPanels: 3470,    Inverters: 2108,  },  {    date: "May 23",    SolarPanels: 3475,    Inverters: 1812,  },  {    date: "Jun 23",    SolarPanels: 3129,    Inverters: 1726,  },  {    date: "Jul 23",    SolarPanels: 3490,    Inverters: 1982,  },  {    date: "Aug 23",    SolarPanels: 2903,    Inverters: 2012,  },  {    date: "Sep 23",    SolarPanels: 2643,    Inverters: 2342,  },  {    date: "Oct 23",    SolarPanels: 2837,    Inverters: 2473,  },  {    date: "Nov 23",    SolarPanels: 2954,    Inverters: 3848,  },  {    date: "Dec 23",    SolarPanels: 3239,    Inverters: 3736,  },]
export const LineChartHero = () => (  <LineChart    className="h-80"    data={chartdata}    index="date"    categories={["SolarPanels", "Inverters"]}    valueFormatter={(number: number) =>      `$${Intl.NumberFormat("us").format(number).toString()}`    }    onValueChange={(v) => console.log(v)}  />)
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm i recharts
   ```
2. 2

   ### Add useOnWindowResize.ts hook:

   Copy and paste the code into your project’s hooks or component directory.

   Show more

   ```
   // Tremor useOnWindowResize [v0.0.2]
   import * as React from "react"
   export const useOnWindowResize = (handler: () => void) => {  React.useEffect(() => {    const handleResize = () => {      handler()    }    handleResize()    window.addEventListener("resize", handleResize)
       return () => window.removeEventListener("resize", handleResize)  }, [handler])}
   ```
3. 3

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths. If you have not added the required chartUtils.ts, check out the [add utilities and helpers](/docs/utilities/chartUtils) section in installation.

   Show more

   ```
   // Tremor LineChart [v1.0.0]/* eslint-disable @typescript-eslint/no-explicit-any */
   "use client"
   import React from "react"import { RiArrowLeftSLine, RiArrowRightSLine } from "@remixicon/react"import {  CartesianGrid,  Dot,  Label,  Line,  Legend as RechartsLegend,  LineChart as RechartsLineChart,  ResponsiveContainer,  Tooltip,  XAxis,  YAxis,} from "recharts"import type { AxisDomain } from "recharts/types/util/types"
   import {  AvailableChartColors,  constructCategoryColors,  getColorClassName,  getYAxisDomain,  hasOnlyOneValueForKey,  type AvailableChartColorsKeys,} from "@/lib/chartUtils"import { useOnWindowResize } from "@/lib/useOnWindowResize"import { cx } from "@/lib/utils"
   //#region Legend
   interface LegendItemProps {  name: string  color: AvailableChartColorsKeys  onClick?: (name: string, color: AvailableChartColorsKeys) => void  activeLegend?: string}
   const LegendItem = ({  name,  color,  onClick,  activeLegend,}: LegendItemProps) => {  const hasOnValueChange = !!onClick  return (    <li      className={cx(        // base        "group inline-flex flex-nowrap items-center gap-1.5 rounded-sm px-2 py-1 whitespace-nowrap transition",        hasOnValueChange          ? "cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"          : "cursor-default",      )}      onClick={(e) => {        e.stopPropagation()        onClick?.(name, color)      }}    >      <span        className={cx(          "h-[3px] w-3.5 shrink-0 rounded-full",          getColorClassName(color, "bg"),          activeLegend && activeLegend !== name ? "opacity-40" : "opacity-100",        )}        aria-hidden={true}      />      <p        className={cx(          // base          "truncate text-xs whitespace-nowrap",          // text color          "text-gray-700 dark:text-gray-300",          hasOnValueChange &&            "group-hover:text-gray-900 dark:group-hover:text-gray-50",          activeLegend && activeLegend !== name ? "opacity-40" : "opacity-100",        )}      >        {name}      </p>    </li>  )}
   interface ScrollButtonProps {  icon: React.ElementType  onClick?: () => void  disabled?: boolean}
   const ScrollButton = ({ icon, onClick, disabled }: ScrollButtonProps) => {  const Icon = icon  const [isPressed, setIsPressed] = React.useState(false)  const intervalRef = React.useRef<NodeJS.Timeout | null>(null)
     React.useEffect(() => {    if (isPressed) {      intervalRef.current = setInterval(() => {        onClick?.()      }, 300)    } else {      clearInterval(intervalRef.current as NodeJS.Timeout)    }    return () => clearInterval(intervalRef.current as NodeJS.Timeout)  }, [isPressed, onClick])
     React.useEffect(() => {    if (disabled) {      clearInterval(intervalRef.current as NodeJS.Timeout)      setIsPressed(false)    }  }, [disabled])
     return (    <button      type="button"      className={cx(        // base        "group inline-flex size-5 items-center truncate rounded-sm transition",        disabled          ? "cursor-not-allowed text-gray-400 dark:text-gray-600"          : "cursor-pointer text-gray-700 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-gray-50",      )}      disabled={disabled}      onClick={(e) => {        e.stopPropagation()        onClick?.()      }}      onMouseDown={(e) => {        e.stopPropagation()        setIsPressed(true)      }}      onMouseUp={(e) => {        e.stopPropagation()        setIsPressed(false)      }}    >      <Icon className="size-full" aria-hidden="true" />    </button>  )}
   interface LegendProps extends React.OlHTMLAttributes<HTMLOListElement> {  categories: string[]  colors?: AvailableChartColorsKeys[]  onClickLegendItem?: (category: string, color: string) => void  activeLegend?: string  enableLegendSlider?: boolean}
   type HasScrollProps = {  left: boolean  right: boolean}
   const Legend = React.forwardRef<HTMLOListElement, LegendProps>((props, ref) => {  const {    categories,    colors = AvailableChartColors,    className,    onClickLegendItem,    activeLegend,    enableLegendSlider = false,    ...other  } = props  const scrollableRef = React.useRef<HTMLInputElement>(null)  const scrollButtonsRef = React.useRef<HTMLDivElement>(null)  const [hasScroll, setHasScroll] = React.useState<HasScrollProps | null>(null)  const [isKeyDowned, setIsKeyDowned] = React.useState<string | null>(null)  const intervalRef = React.useRef<NodeJS.Timeout | null>(null)
     const checkScroll = React.useCallback(() => {    const scrollable = scrollableRef?.current    if (!scrollable) return
       const hasLeftScroll = scrollable.scrollLeft > 0    const hasRightScroll =      scrollable.scrollWidth - scrollable.clientWidth > scrollable.scrollLeft
       setHasScroll({ left: hasLeftScroll, right: hasRightScroll })  }, [setHasScroll])
     const scrollToTest = React.useCallback(    (direction: "left" | "right") => {      const element = scrollableRef?.current      const scrollButtons = scrollButtonsRef?.current      const scrollButtonsWith = scrollButtons?.clientWidth ?? 0      const width = element?.clientWidth ?? 0
         if (element && enableLegendSlider) {        element.scrollTo({          left:            direction === "left"              ? element.scrollLeft - width + scrollButtonsWith              : element.scrollLeft + width - scrollButtonsWith,          behavior: "smooth",        })        setTimeout(() => {          checkScroll()        }, 400)      }    },    [enableLegendSlider, checkScroll],  )
     React.useEffect(() => {    const keyDownHandler = (key: string) => {      if (key === "ArrowLeft") {        scrollToTest("left")      } else if (key === "ArrowRight") {        scrollToTest("right")      }    }    if (isKeyDowned) {      keyDownHandler(isKeyDowned)      intervalRef.current = setInterval(() => {        keyDownHandler(isKeyDowned)      }, 300)    } else {      clearInterval(intervalRef.current as NodeJS.Timeout)    }    return () => clearInterval(intervalRef.current as NodeJS.Timeout)  }, [isKeyDowned, scrollToTest])
     const keyDown = (e: KeyboardEvent) => {    e.stopPropagation()    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {      e.preventDefault()      setIsKeyDowned(e.key)    }  }  const keyUp = (e: KeyboardEvent) => {    e.stopPropagation()    setIsKeyDowned(null)  }
     React.useEffect(() => {    const scrollable = scrollableRef?.current    if (enableLegendSlider) {      checkScroll()      scrollable?.addEventListener("keydown", keyDown)      scrollable?.addEventListener("keyup", keyUp)    }
       return () => {      scrollable?.removeEventListener("keydown", keyDown)      scrollable?.removeEventListener("keyup", keyUp)    }  }, [checkScroll, enableLegendSlider])
     return (    <ol      ref={ref}      className={cx("relative overflow-hidden", className)}      {...other}    >      <div        ref={scrollableRef}        tabIndex={0}        className={cx(          "flex h-full",          enableLegendSlider            ? hasScroll?.right || hasScroll?.left              ? "snap-mandatory items-center overflow-auto pr-12 pl-4 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"              : ""            : "flex-wrap",        )}      >        {categories.map((category, index) => (          <LegendItem            key={`item-${index}`}            name={category}            color={colors[index] as AvailableChartColorsKeys}            onClick={onClickLegendItem}            activeLegend={activeLegend}          />        ))}      </div>      {enableLegendSlider && (hasScroll?.right || hasScroll?.left) ? (        <>          <div            className={cx(              // base              "absolute top-0 right-0 bottom-0 flex h-full items-center justify-center pr-1",              // background color              "bg-white dark:bg-gray-950",            )}          >            <ScrollButton              icon={RiArrowLeftSLine}              onClick={() => {                setIsKeyDowned(null)                scrollToTest("left")              }}              disabled={!hasScroll?.left}            />            <ScrollButton              icon={RiArrowRightSLine}              onClick={() => {                setIsKeyDowned(null)                scrollToTest("right")              }}              disabled={!hasScroll?.right}            />          </div>        </>      ) : null}    </ol>  )})
   Legend.displayName = "Legend"
   const ChartLegend = (  { payload }: any,  categoryColors: Map<string, AvailableChartColorsKeys>,  setLegendHeight: React.Dispatch<React.SetStateAction<number>>,  activeLegend: string | undefined,  onClick?: (category: string, color: string) => void,  enableLegendSlider?: boolean,  legendPosition?: "left" | "center" | "right",  yAxisWidth?: number,) => {  const legendRef = React.useRef<HTMLDivElement>(null)
     useOnWindowResize(() => {    const calculateHeight = (height: number | undefined) =>      height ? Number(height) + 15 : 60    setLegendHeight(calculateHeight(legendRef.current?.clientHeight))  })
     const legendPayload = payload.filter((item: any) => item.type !== "none")
     const paddingLeft =    legendPosition === "left" && yAxisWidth ? yAxisWidth - 8 : 0
     return (    <div      ref={legendRef}      style={{ paddingLeft: paddingLeft }}      className={cx(        "flex items-center",        { "justify-center": legendPosition === "center" },        { "justify-start": legendPosition === "left" },        { "justify-end": legendPosition === "right" },      )}    >      <Legend        categories={legendPayload.map((entry: any) => entry.value)}        colors={legendPayload.map((entry: any) =>          categoryColors.get(entry.value),        )}        onClickLegendItem={onClick}        activeLegend={activeLegend}        enableLegendSlider={enableLegendSlider}      />    </div>  )}
   //#region Tooltip
   type TooltipProps = Pick<ChartTooltipProps, "active" | "payload" | "label">
   type PayloadItem = {  category: string  value: number  index: string  color: AvailableChartColorsKeys  type?: string  payload: any}
   interface ChartTooltipProps {  active: boolean | undefined  payload: PayloadItem[]  label: string  valueFormatter: (value: number) => string}
   const ChartTooltip = ({  active,  payload,  label,  valueFormatter,}: ChartTooltipProps) => {  if (active && payload && payload.length) {    const legendPayload = payload.filter((item: any) => item.type !== "none")    return (      <div        className={cx(          // base          "rounded-md border text-sm shadow-md",          // border color          "border-gray-200 dark:border-gray-800",          // background color          "bg-white dark:bg-gray-950",        )}      >        <div className={cx("border-b border-inherit px-4 py-2")}>          <p            className={cx(              // base              "font-medium",              // text color              "text-gray-900 dark:text-gray-50",            )}          >            {label}          </p>        </div>        <div className={cx("space-y-1 px-4 py-2")}>          {legendPayload.map(({ value, category, color }, index) => (            <div              key={`id-${index}`}              className="flex items-center justify-between space-x-8"            >              <div className="flex items-center space-x-2">                <span                  aria-hidden="true"                  className={cx(                    "h-[3px] w-3.5 shrink-0 rounded-full",                    getColorClassName(color, "bg"),                  )}                />                <p                  className={cx(                    // base                    "text-right whitespace-nowrap",                    // text color                    "text-gray-700 dark:text-gray-300",                  )}                >                  {category}                </p>              </div>              <p                className={cx(                  // base                  "text-right font-medium whitespace-nowrap tabular-nums",                  // text color                  "text-gray-900 dark:text-gray-50",                )}              >                {valueFormatter(value)}              </p>            </div>          ))}        </div>      </div>    )  }  return null}
   //#region LineChart
   interface ActiveDot {  index?: number  dataKey?: string}
   type BaseEventProps = {  eventType: "dot" | "category"  categoryClicked: string  [key: string]: number | string}
   type LineChartEventProps = BaseEventProps | null | undefined
   interface LineChartProps extends React.HTMLAttributes<HTMLDivElement> {  data: Record<string, any>[]  index: string  categories: string[]  colors?: AvailableChartColorsKeys[]  valueFormatter?: (value: number) => string  startEndOnly?: boolean  showXAxis?: boolean  showYAxis?: boolean  showGridLines?: boolean  yAxisWidth?: number  intervalType?: "preserveStartEnd" | "equidistantPreserveStart"  showTooltip?: boolean  showLegend?: boolean  autoMinValue?: boolean  minValue?: number  maxValue?: number  allowDecimals?: boolean  onValueChange?: (value: LineChartEventProps) => void  enableLegendSlider?: boolean  tickGap?: number  connectNulls?: boolean  xAxisLabel?: string  yAxisLabel?: string  legendPosition?: "left" | "center" | "right"  tooltipCallback?: (tooltipCallbackContent: TooltipProps) => void  customTooltip?: React.ComponentType<TooltipProps>}
   const LineChart = React.forwardRef<HTMLDivElement, LineChartProps>(  (props, ref) => {    const {      data = [],      categories = [],      index,      colors = AvailableChartColors,      valueFormatter = (value: number) => value.toString(),      startEndOnly = false,      showXAxis = true,      showYAxis = true,      showGridLines = true,      yAxisWidth = 56,      intervalType = "equidistantPreserveStart",      showTooltip = true,      showLegend = true,      autoMinValue = false,      minValue,      maxValue,      allowDecimals = true,      connectNulls = false,      className,      onValueChange,      enableLegendSlider = false,      tickGap = 5,      xAxisLabel,      yAxisLabel,      legendPosition = "right",      tooltipCallback,      customTooltip,      ...other    } = props    const CustomTooltip = customTooltip    const paddingValue =      (!showXAxis && !showYAxis) || (startEndOnly && !showYAxis) ? 0 : 20    const [legendHeight, setLegendHeight] = React.useState(60)    const [activeDot, setActiveDot] = React.useState<ActiveDot | undefined>(      undefined,    )    const [activeLegend, setActiveLegend] = React.useState<string | undefined>(      undefined,    )    const categoryColors = constructCategoryColors(categories, colors)
       const yAxisDomain = getYAxisDomain(autoMinValue, minValue, maxValue)    const hasOnValueChange = !!onValueChange    const prevActiveRef = React.useRef<boolean | undefined>(undefined)    const prevLabelRef = React.useRef<string | undefined>(undefined)
       function onDotClick(itemData: any, event: React.MouseEvent) {      event.stopPropagation()
         if (!hasOnValueChange) return      if (        (itemData.index === activeDot?.index &&          itemData.dataKey === activeDot?.dataKey) ||        (hasOnlyOneValueForKey(data, itemData.dataKey) &&          activeLegend &&          activeLegend === itemData.dataKey)      ) {        setActiveLegend(undefined)        setActiveDot(undefined)        onValueChange?.(null)      } else {        setActiveLegend(itemData.dataKey)        setActiveDot({          index: itemData.index,          dataKey: itemData.dataKey,        })        onValueChange?.({          eventType: "dot",          categoryClicked: itemData.dataKey,          ...itemData.payload,        })      }    }
       function onCategoryClick(dataKey: string) {      if (!hasOnValueChange) return      if (        (dataKey === activeLegend && !activeDot) ||        (hasOnlyOneValueForKey(data, dataKey) &&          activeDot &&          activeDot.dataKey === dataKey)      ) {        setActiveLegend(undefined)        onValueChange?.(null)      } else {        setActiveLegend(dataKey)        onValueChange?.({          eventType: "category",          categoryClicked: dataKey,        })      }      setActiveDot(undefined)    }
       return (      <div        ref={ref}        className={cx("h-80 w-full", className)}        tremor-id="tremor-raw"        {...other}      >        <ResponsiveContainer>          <RechartsLineChart            data={data}            onClick={              hasOnValueChange && (activeLegend || activeDot)                ? () => {                    setActiveDot(undefined)                    setActiveLegend(undefined)                    onValueChange?.(null)                  }                : undefined            }            margin={{              bottom: xAxisLabel ? 30 : undefined,              left: yAxisLabel ? 20 : undefined,              right: yAxisLabel ? 5 : undefined,              top: 5,            }}          >            {showGridLines ? (              <CartesianGrid                className={cx("stroke-gray-200 stroke-1 dark:stroke-gray-800")}                horizontal={true}                vertical={false}              />            ) : null}            <XAxis              padding={{ left: paddingValue, right: paddingValue }}              hide={!showXAxis}              dataKey={index}              interval={startEndOnly ? "preserveStartEnd" : intervalType}              tick={{ transform: "translate(0, 6)" }}              ticks={                startEndOnly                  ? [data[0][index], data[data.length - 1][index]]                  : undefined              }              fill=""              stroke=""              className={cx(                // base                "text-xs",                // text fill                "fill-gray-500 dark:fill-gray-500",              )}              tickLine={false}              axisLine={false}              minTickGap={tickGap}            >              {xAxisLabel && (                <Label                  position="insideBottom"                  offset={-20}                  className="fill-gray-800 text-sm font-medium dark:fill-gray-200"                >                  {xAxisLabel}                </Label>              )}            </XAxis>            <YAxis              width={yAxisWidth}              hide={!showYAxis}              axisLine={false}              tickLine={false}              type="number"              domain={yAxisDomain as AxisDomain}              tick={{ transform: "translate(-3, 0)" }}              fill=""              stroke=""              className={cx(                // base                "text-xs",                // text fill                "fill-gray-500 dark:fill-gray-500",              )}              tickFormatter={valueFormatter}              allowDecimals={allowDecimals}            >              {yAxisLabel && (                <Label                  position="insideLeft"                  style={{ textAnchor: "middle" }}                  angle={-90}                  offset={-15}                  className="fill-gray-800 text-sm font-medium dark:fill-gray-200"                >                  {yAxisLabel}                </Label>              )}            </YAxis>            <Tooltip              wrapperStyle={{ outline: "none" }}              isAnimationActive={true}              animationDuration={100}              cursor={{ stroke: "#d1d5db", strokeWidth: 1 }}              offset={20}              position={{ y: 0 }}              content={({ active, payload, label }) => {                const cleanPayload: TooltipProps["payload"] = payload                  ? payload.map((item: any) => ({                      category: item.dataKey,                      value: item.value,                      index: item.payload[index],                      color: categoryColors.get(                        item.dataKey,                      ) as AvailableChartColorsKeys,                      type: item.type,                      payload: item.payload,                    }))                  : []
                   if (                  tooltipCallback &&                  (active !== prevActiveRef.current ||                    label !== prevLabelRef.current)                ) {                  tooltipCallback({ active, payload: cleanPayload, label })                  prevActiveRef.current = active                  prevLabelRef.current = label                }
                   return showTooltip && active ? (                  CustomTooltip ? (                    <CustomTooltip                      active={active}                      payload={cleanPayload}                      label={label}                    />                  ) : (                    <ChartTooltip                      active={active}                      payload={cleanPayload}                      label={label}                      valueFormatter={valueFormatter}                    />                  )                ) : null              }}            />
               {showLegend ? (              <RechartsLegend                verticalAlign="top"                height={legendHeight}                content={({ payload }) =>                  ChartLegend(                    { payload },                    categoryColors,                    setLegendHeight,                    activeLegend,                    hasOnValueChange                      ? (clickedLegendItem: string) =>                          onCategoryClick(clickedLegendItem)                      : undefined,                    enableLegendSlider,                    legendPosition,                    yAxisWidth,                  )                }              />            ) : null}            {categories.map((category) => (              <Line                className={cx(                  getColorClassName(                    categoryColors.get(category) as AvailableChartColorsKeys,                    "stroke",                  ),                )}                strokeOpacity={                  activeDot || (activeLegend && activeLegend !== category)                    ? 0.3                    : 1                }                activeDot={(props: any) => {                  const {                    cx: cxCoord,                    cy: cyCoord,                    stroke,                    strokeLinecap,                    strokeLinejoin,                    strokeWidth,                    dataKey,                  } = props                  return (                    <Dot                      className={cx(                        "stroke-white dark:stroke-gray-950",                        onValueChange ? "cursor-pointer" : "",                        getColorClassName(                          categoryColors.get(                            dataKey,                          ) as AvailableChartColorsKeys,                          "fill",                        ),                      )}                      cx={cxCoord}                      cy={cyCoord}                      r={5}                      fill=""                      stroke={stroke}                      strokeLinecap={strokeLinecap}                      strokeLinejoin={strokeLinejoin}                      strokeWidth={strokeWidth}                      onClick={(_, event) => onDotClick(props, event)}                    />                  )                }}                dot={(props: any) => {                  const {                    stroke,                    strokeLinecap,                    strokeLinejoin,                    strokeWidth,                    cx: cxCoord,                    cy: cyCoord,                    dataKey,                    index,                  } = props
                     if (                    (hasOnlyOneValueForKey(data, category) &&                      !(                        activeDot ||                        (activeLegend && activeLegend !== category)                      )) ||                    (activeDot?.index === index &&                      activeDot?.dataKey === category)                  ) {                    return (                      <Dot                        key={index}                        cx={cxCoord}                        cy={cyCoord}                        r={5}                        stroke={stroke}                        fill=""                        strokeLinecap={strokeLinecap}                        strokeLinejoin={strokeLinejoin}                        strokeWidth={strokeWidth}                        className={cx(                          "stroke-white dark:stroke-gray-950",                          onValueChange ? "cursor-pointer" : "",                          getColorClassName(                            categoryColors.get(                              dataKey,                            ) as AvailableChartColorsKeys,                            "fill",                          ),                        )}                      />                    )                  }                  return <React.Fragment key={index}></React.Fragment>                }}                key={category}                name={category}                type="linear"                dataKey={category}                stroke=""                strokeWidth={2}                strokeLinejoin="round"                strokeLinecap="round"                isAnimationActive={false}                connectNulls={connectNulls}              />            ))}            {/* hidden lines to increase clickable target area */}            {onValueChange              ? categories.map((category) => (                  <Line                    className={cx("cursor-pointer")}                    strokeOpacity={0}                    key={category}                    name={category}                    type="linear"                    dataKey={category}                    stroke="transparent"                    fill="transparent"                    legendType="none"                    tooltipType="none"                    strokeWidth={12}                    connectNulls={connectNulls}                    onClick={(props: any, event) => {                      event.stopPropagation()                      const { name } = props                      onCategoryClick(name)                    }}                  />                ))              : null}          </RechartsLineChart>        </ResponsiveContainer>      </div>    )  },)
   LineChart.displayName = "LineChart"
   export { LineChart, type LineChartEventProps, type TooltipProps }
   ```

## Example with Axis Labels

Preview

Code

```
"use client"
import { LineChart } from "@/components/LineChart"
const chartdata = [  {    date: "Jan 23",    SolarPanels: 2890,    Inverters: 2338,  },  {    date: "Feb 23",    SolarPanels: 2756,    Inverters: 2103,  },  {    date: "Mar 23",    SolarPanels: 3322,    Inverters: 2194,  },  {    date: "Apr 23",    SolarPanels: 3470,    Inverters: 2108,  },  {    date: "May 23",    SolarPanels: 3475,    Inverters: 1812,  },  {    date: "Jun 23",    SolarPanels: 3129,    Inverters: 1726,  },  {    date: "Jul 23",    SolarPanels: 3490,    Inverters: 1982,  },  {    date: "Aug 23",    SolarPanels: 2903,    Inverters: 2012,  },  {    date: "Sep 23",    SolarPanels: 2643,    Inverters: 2342,  },  {    date: "Oct 23",    SolarPanels: 2837,    Inverters: 2473,  },  {    date: "Nov 23",    SolarPanels: 2954,    Inverters: 3848,  },  {    date: "Dec 23",    SolarPanels: 3239,    Inverters: 3736,  },]
export const LineChartAxisLabelsExample = () => (  <LineChart    className="h-80"    data={chartdata}    index="date"    categories={["SolarPanels", "Inverters"]}    valueFormatter={(number: number) =>      `$${Intl.NumberFormat("us").format(number).toString()}`    }    onValueChange={(v) => console.log(v)}    xAxisLabel="Month"    yAxisLabel="Spend Category"  />)
```

## Example with onValueChange

When you add onValueChange to the LineChart, it becomes clickable.

Preview

Code

```
null
```

```
"use client"
import React from "react"
import { LineChart, type LineChartEventProps } from "@/components/LineChart"
const chartdata = [  {    date: "Jan 23",    2022: 45,    2023: 78,  },  {    date: "Feb 23",    2022: 52,    2023: 71,  },  {    date: "Mar 23",    2022: 48,    2023: 80,  },  {    date: "Apr 23",    2022: 61,    2023: 65,  },  {    date: "May 23",    2022: 55,    2023: 58,  },  {    date: "Jun 23",    2022: 67,    2023: 62,  },  {    date: "Jul 23",    2022: 60,    2023: 54,  },  {    date: "Aug 23",    2022: 72,    2023: 49,  },  {    date: "Sep 23",    2022: 65,    2023: 52,  },  {    date: "Oct 23",    2022: 68,    2023: null,  },  {    date: "Nov 23",    2022: 74,    2023: null,  },  {    date: "Dec 23",    2022: 71,    2023: null,  },]
export const LineChartOnValueChangeExample = () => {  const [value, setValue] = React.useState<LineChartEventProps>(null)  return (    <>      <LineChart        className="mt-4 h-72"        data={chartdata}        index="date"        categories={["2022", "2023"]}        colors={["gray", "blue"]}        yAxisWidth={30}        onValueChange={(v) => setValue(v)}      />      <pre className="mt-8 rounded-md bg-gray-950 p-3 text-sm text-white dark:bg-gray-800">        {JSON.stringify(value, null, 2)}      </pre>    </>  )}
```

## Example with startEndOnly, custom yAxisWidth, no legend, and no tooltip

Preview

Code

```
"use client"
import { LineChart } from "@/components/LineChart"
const chartdata = [  { hour: "00:00", temperature: 12.8 },  { hour: "01:00", temperature: 12.4 },  { hour: "02:00", temperature: 12.2 },  { hour: "03:00", temperature: 11.9 },  { hour: "04:00", temperature: 11.7 },  { hour: "05:00", temperature: 11.5 },  { hour: "06:00", temperature: 11.3 },  { hour: "07:00", temperature: 11.2 },  { hour: "08:00", temperature: 11.5 },  { hour: "09:00", temperature: 12.0 },  { hour: "10:00", temperature: 13.0 },  { hour: "11:00", temperature: 14.2 },  { hour: "12:00", temperature: 15.5 },  { hour: "13:00", temperature: 16.8 },  { hour: "14:00", temperature: 17.5 },  { hour: "15:00", temperature: 18.1 },  { hour: "16:00", temperature: 18.2 },  { hour: "17:00", temperature: 17.8 },  { hour: "18:00", temperature: 17.2 },  { hour: "19:00", temperature: 16.5 },  { hour: "20:00", temperature: 15.8 },  { hour: "21:00", temperature: 14.9 },  { hour: "22:00", temperature: 14.2 },  { hour: "23:00", temperature: 13.5 },]
export const LineChartStartEndOnlyExample = () => (  <LineChart    className="h-56"    data={chartdata}    index="hour"    categories={["temperature"]}    valueFormatter={(number: number) =>      `${Intl.NumberFormat().format(number).toString()}°C`    }    yAxisWidth={40}    startEndOnly    connectNulls    showLegend={false}    showTooltip={false}    xAxisLabel="24H Temperature Readout (Zurich)"  />)
```

## Example with tooltipCallback

Preview

Code

Revenue by month

$4,900

```
"use client"
import React from "react"
import { LineChart, TooltipProps } from "@/components/LineChart"
interface DataItem {  date: string  revenue: number}
const data: DataItem[] = [Show  {    date: "Jan 23",    revenue: 2340,  },  {    date: "Feb 23",    revenue: 3110,  },  {    date: "Mar 23",    revenue: 4643,  },  {    date: "Apr 23",    revenue: 4650,  },  {    date: "May 23",    revenue: 3980,  },  {    date: "Jun 23",    revenue: 4702,  },  {    date: "Jul 23",    revenue: 5990,  },  {    date: "Aug 23",    revenue: 5700,  },  {    date: "Sep 23",    revenue: 4250,  },  {    date: "Oct 23",    revenue: 4182,  },  {    date: "Nov 23",    revenue: 3812,  },  {    date: "Dec 23",    revenue: 4900,  },]
function LineChartCallbackExample() {  const [datas, setDatas] = React.useState<TooltipProps | null>(null)  const currencyFormatter = (number: number) =>    `$${Intl.NumberFormat("us").format(number)}`
  const payload = datas?.payload?.[0]  const value = payload?.value
  const formattedValue = payload    ? currencyFormatter(value)    : currencyFormatter(data[data.length - 1].revenue)
  return (    <div>      <p className="text-sm text-gray-700 dark:text-gray-300">        Revenue by month      </p>      <p className="mt-2 text-xl font-semibold text-gray-900 dark:text-gray-50">        {formattedValue}      </p>
      <LineChart        data={data}        index="date"        categories={["revenue"]}        showLegend={false}        showYAxis={false}        startEndOnly={true}        className="-mb-2 mt-8 h-48"        tooltipCallback={(props) => {          if (props.active) {            setDatas((prev) => {              if (prev?.label === props.label) return prev              return props            })          } else {            setDatas(null)          }          return null        }}      />    </div>  )}
```

## Example with customTooltip

Preview

Code

```
import { cx } from "@/lib/utils"import { LineChart, TooltipProps } from "@/components/LineChart";
interface Issue {    status: "completed" | "in progress" | "on hold";    value: number;    percentage: number;}
interface DataEntry {    date: string;    issues: Issue[];}
const data: DataEntry[] = [Show    {        date: "Jun 1, 24",        issues: [            {                status: "completed",                value: 47,                percentage: 24.2,            },            {                status: "in progress",                value: 83,                percentage: 41.9,            },            {                status: "on hold",                value: 67,                percentage: 33.9,            },        ],    },    {        date: "Jun 2, 24",        issues: [            {                status: "completed",                value: 20,                percentage: 20.6,            },            {                status: "in progress",                value: 97,                percentage: 77.3,            },            {                status: "on hold",                value: 12,                percentage: 2.1,            },        ],    },    {        date: "Jun 3, 24",        issues: [            {                status: "completed",                value: 30,                percentage: 29.4,            },            {                status: "in progress",                value: 45,                percentage: 43.1,            },            {                status: "on hold",                value: 66,                percentage: 27.5,            },        ],    },    {        date: "Jun 4, 24",        issues: [            {                status: "completed",                value: 41,                percentage: 28.1,            },            {                status: "in progress",                value: 18,                percentage: 17.9,            },            {                status: "on hold",                value: 70,                percentage: 54.0,            },        ],    },    {        date: "Jun 5, 24",        issues: [            {                status: "completed",                value: 55,                percentage: 28.8,            },            {                status: "in progress",                value: 14,                percentage: 25.0,            },            {                status: "on hold",                value: 60,                percentage: 46.2,            },        ],    },    {        date: "Jun 6, 24",        issues: [            {                status: "completed",                value: 35,                percentage: 28.8,            },            {                status: "in progress",                value: 14,                percentage: 19.2,            },            {                status: "on hold",                value: 80,                percentage: 51.9,            },        ],    },    {        date: "Jun 7, 24",        issues: [            {                status: "completed",                value: 15,                percentage: 20.0,            },            {                status: "in progress",                value: 55,                percentage: 35.2,            },            {                status: "on hold",                value: 72,                percentage: 44.8,            },        ],    },    {        date: "Jun 8, 24",        issues: [            {                status: "completed",                value: 15,                percentage: 21.7,            },            {                status: "in progress",                value: 69,                percentage: 48.2,            },            {                status: "on hold",                value: 45,                percentage: 30.1,            },        ],    },];
// Transform data into a format suitable for LineChartconst formattedArray = data.map((entry) => {    return {        date: entry.date,        ...entry.issues.reduce(            (acc, issue) => {                acc[issue.status] = issue.value;                return acc;            },            {} as { [key in Issue["status"]]?: number }        ),    };});
const valueFormatter = (number: number) => {    return Intl.NumberFormat("us").format(number).toString();};
const status = {    "completed": "bg-blue-500 dark:bg-blue-500",    "in progress": "bg-cyan-500 dark:bg-cyan-500",    "on hold": "bg-violet-500 dark:bg-violet-500",};
const Tooltip = ({ payload, active, label }: TooltipProps) => {    if (!active || !payload || payload.length === 0) return null;
    const data = payload.map((item) => ({        status: item.category as Issue["status"],        value: item.value,        percentage: (            (item.value /                (item.payload.completed +                    item.payload["in progress"] +                    item.payload["on hold"])) *            100        ).toFixed(2),    }));
    return (        <>            <div className="w-60 rounded-md border border-gray-500/10  bg-blue-500 px-4 py-1.5 text-sm shadow-md dark:border-gray-400/20 dark:bg-gray-900">                <p className="flex items-center justify-between">                    <span className="text-gray-50 dark:text-gray-50">                        Date                    </span>                    <span className="font-medium text-gray-50 dark:text-gray-50">{label}</span>                </p>            </div>            <div className="mt-1 w-60 space-y-1 rounded-md border border-gray-500/10  bg-white px-4 py-2 text-sm shadow-md dark:border-gray-400/20 dark:bg-gray-900">                {data.map((item, index) => (                    <div key={index} className="flex items-center space-x-2.5">                        <span                            className={cx(                                status[item.status],                                "size-2.5 shrink-0 rounded-xs"                            )}                            aria-hidden={true}                        />                        <div className="flex w-full justify-between">                            <span className=" text-gray-700 dark:text-gray-300">                                {item.status}                            </span>                            <div className="flex items-center space-x-1">                                <span className="font-medium text-gray-900 dark:text-gray-50">                                    {item.value}                                </span>                                <span className="text-gray-500 dark:text-gray-500">                                    ({item.percentage}&#37;)                                </span>                            </div>                        </div>                    </div>                ))}            </div>        </>    );};
function LineChartCustomTooltipExample() {    return (        <div>            <LineChart                className="hidden h-72 sm:block"                data={formattedArray}                index="date"                categories={["completed", "in progress", "on hold"]}                colors={["blue", "cyan", "violet"]}                valueFormatter={valueFormatter}                yAxisWidth={35}                showLegend={false}                customTooltip={Tooltip}            />            <LineChart                className="h-80 sm:hidden"                data={formattedArray}                index="date"                categories={["completed", "in progress", "on hold"]}                colors={["blue", "cyan", "violet"]}                valueFormatter={valueFormatter}                showYAxis={false}                showLegend={false}                startEndOnly={true}                customTooltip={Tooltip}            />        </div>    );}
```

## API Reference: LineChart

data

Required

Record<string, any>[]

:   Data used to display the chart.

index

Required

string[]

:   Key of the data object to map the data to the x axis.

Default: []

categories

Required

string[]

:   Select the categories from your data. Also used to populate the legend and toolip.

Default: []

colors

AvailableChartColorsKeys[]

:   Change the colors of the categories. To add, update, or remove the colors, edit the 'chartColors' array in your chartUtils.ts file. The AvailableChartColorsKeys will be automatically updated.

Default: AvailableChartColors, which are by default: 'blue' | 'emerald' | 'violet' | 'amber' | 'gray' | 'cyan' | 'pink' | 'lime' | 'fuchsia'

valueFormatter

(value: number) => string

:   Controls the text formatting for the y-axis values. Also used in the Tooltip.

startEndOnly

boolean

:   Show only the first and last elements in the x-axis.

Default: false

showXAxis

boolean

:   Controls the visibility of the X axis.

Default: true

showYAxis

boolean

:   Controls the visibility of the Y axis.

Default: true

yAxisWidth

number

:   Controls the width of the y-axis.

Default: 56

showGridLines

boolean

:   Controls the visibility of the gridlines within the plotted area.

Default: true

intervalType

equidistantPreserveStart | preserveStartEnd

:   Controls the interval logic of the X axis and how ticks and labels are placed.

Default: equidistantPreserveStart

showTooltip

boolean

:   Controls the visibility of the tooltip.

Default: true

showLegend

boolean

:   Controls the visibility of the legend.

Default: true

autoMinValue

boolean

:   Adjusts the minimum value in relation to the magnitude of the data.

Default: false

minValue

number

:   Sets the minimum value of the shown chart data.

maxValue

number

:   Sets the maximum value of the shown chart data.

allowDecimals

boolean

:   Controls if the ticks of a numeric axis are displayed as decimals or not.

Default: true

onValueChange

(value: EventProps) => void

:   Callback function for when the value of the component changes.

enableLegendSlider

boolean

:   Adds a slider functionality to the legend instead of wrapping the legend items.

Default: false

tickGap

number

:   Sets the minimum gap between two adjacent labels.

Default: 5

connectNulls

boolean

:   Connects datapoints that have null values between them.

Default: false

xAxisLabel

string

:   Add a label to the x-axis.

yAxisLabel

string

:   Add a label to the y-axis.

tooltipCallback

(tooltipCallbackContent: TooltipCallbackProps) => void

:   Callback function that returns the active, payload, and label info when the tooltip changes.
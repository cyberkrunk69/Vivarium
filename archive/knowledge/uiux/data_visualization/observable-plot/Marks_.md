# Marks​

Source: https://observablehq.com/plot/features/marks

---

# Marks [​](#Marks)

TIP

If you aren’t yet up and running with Plot, please read our [getting started guide](./../getting-started) first. Tinkering with the code below will give a better sense of how Plot works.

Plot doesn’t have chart types; instead, you construct charts by layering **marks**.

## Marks are geometric shapes [​](#marks-are-geometric-shapes)

Plot provides a variety of mark types. Think of marks as the “visual vocabulary” — the painter’s palette 🎨, but of shapes instead of colors — that you pull from when composing a chart. Each mark type produces a certain type of geometric shape.

For example, the [dot mark](./../marks/dot) draws stroked circles (by default).

[Fork](https://observablehq.com/@observablehq/plot-temporal-scatterplot "Open on Observable")

js

```
Plot.dot(gistemp, {x: "Date", y: "Anomaly"}).plot()
```

The [line mark](./../marks/line) draws connected line segments (also known as a *polyline* or *polygonal chain*).

[Fork](https://observablehq.com/@observablehq/plot-temporal-line-chart "Open on Observable")

js

```
Plot.lineY(gistemp, {x: "Date", y: "Anomaly"}).plot()
```

And the [bar mark](./../marks/bar) draws rectangular bars in either a horizontal (barX→) or vertical (barY↑) orientation.

[Fork](https://observablehq.com/@observablehq/plot-alphabet-bar-chart "Open on Observable")

js

```
Plot.barX(alphabet, {x: "frequency", y: "letter"}).plot()
```

So instead of looking for a chart type, consider the shape of the primary graphical elements in your chart, and look for the corresponding mark type. If a chart has only a single mark, the mark type *is* effectively the chart type: the bar mark is used to make a bar chart, the area mark is used to make an area chart, and so on.

## Marks are layered [​](#marks-are-layered)

The big advantage of mark types over chart types is that you can compose multiple marks of different types into a single [plot](./plots). For example, below an [area](./../marks/area) and [line](./../marks/line) are used to plot the same sequence of values, while a [rule](./../marks/rule) emphasizes *y* = 0.

[Fork](https://observablehq.com/@observablehq/plot-layered-marks-2 "Open on Observable")

js

```
Plot.plot({
  marks: [
    Plot.ruleY([0]),
    Plot.areaY(aapl, {x: "Date", y: "Close", fillOpacity: 0.2}),
    Plot.lineY(aapl, {x: "Date", y: "Close"})
  ]
})
```

Each mark supplies its own data; a quick way to combine multiple datasets into a chart is to declare a separate mark for each. You can even use [*array*.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) to create multiple marks from nested data.

[Fork](https://observablehq.com/@observablehq/plot-layered-marks-2 "Open on Observable")

js

```
Plot.plot({
  marks: [
    [goog, aapl].map((stock) => Plot.lineY(stock, {x: "Date", y: "Close"}))
  ]
})
```

Marks may also be a function which returns an [SVG element](https://developer.mozilla.org/en-US/docs/Web/SVG/Element), if you wish to insert arbitrary content. (Here we use [Hypertext Literal](https://github.com/observablehq/htl) to generate an SVG gradient.)

[Fork](https://observablehq.com/@observablehq/plot-gradient-bars "Open on Observable")

js

```
Plot.plot({
  marks: [
    () => htl.svg`<defs>
      <linearGradient id="gradient" gradientTransform="rotate(90)">
        <stop offset="15%" stop-color="purple" />
        <stop offset="75%" stop-color="red" />
        <stop offset="100%" stop-color="gold" />
      </linearGradient>
    </defs>`,
    Plot.barY(alphabet, {x: "letter", y: "frequency", fill: "url(#gradient)"}),
    Plot.ruleY([0])
  ]
})
```

And marks may be null or undefined, which produce no output; this is useful for showing marks conditionally (*e.g.*, when a box is checked).

Show area:

[Fork](https://observablehq.com/@observablehq/plot-optional-marks "Open on Observable")

js

```
Plot.plot({
  marks: [
    Plot.ruleY([0]),
    area ? Plot.areaY(aapl, {x: "Date", y: "Close", fillOpacity: 0.2}) : null,
    Plot.lineY(aapl, {x: "Date", y: "Close"})
  ]
})
```

## Marks use scales [​](#marks-use-scales)

Marks are (typically) not positioned in literal pixels, or colored in literal colors, as in a conventional graphics system. Instead you provide abstract values such as time and temperature — marks are drawn “in data space” — and [scales](./scales) encode these into visual values such as position and color. And best of all, Plot automatically creates [axes](./../marks/axis) and [legends](./legends) to document the scales’ encodings.

Data is passed through scales automatically during rendering; the mark controls which scales are used. The **x** and **y** options are typically bound to the *x* and *y* scales, respectively, while the **fill** and **stroke** options are typically bound to the *color* scale. Changing a scale’s definition, say by overriding its **domain** (the extent of abstract input values) or **type**, affects the appearance of all marks that use the scale.

[Fork](https://observablehq.com/@observablehq/plot-aapl-log-scale "Open on Observable")

js

```
Plot.plot({
  y: {
    type: "log",
    domain: [30, 300],
    grid: true
  },
  marks: [
    Plot.lineY(aapl, {x: "Date", y: "Close"})
  ]
})
```

## Marks have tidy data [​](#marks-have-tidy-data)

A single mark can draw multiple shapes. A mark generally produces a shape — such as a rectangle or circle — for each element in the data.

[Fork](https://observablehq.com/@observablehq/plot-tidy-data "Open on Observable")

js

```
Plot.dot(aapl, {x: "Date", y: "Close"}).plot()
```

It’s more complicated than that, though, since some marks produce shapes that incorporate *multiple* data points. Pass the same data to a [line](./../marks/line) and you’ll get a single polyline.

[Fork](https://observablehq.com/@observablehq/plot-tidy-data "Open on Observable")

js

```
Plot.lineY(aapl, {x: "Date", y: "Close"}).plot()
```

And a line mark isn’t even guaranteed to produce a single polyline — there can be multiple polylines, as in a line chart with multiple series (using **z**).

[Fork](https://observablehq.com/@observablehq/plot-multiple-series-line-chart "Open on Observable")

js

```
Plot.lineY(bls, {x: "date", y: "unemployment", z: "division"}).plot()
```

Plot favors [tidy data](http://vita.had.co.nz/papers/tidy-data.html) structured as an array of objects, where each object represents an observation (a row), and each object property represents an observed value; all objects in the array should have the same property names (the columns).

For example, say we have hourly readings from two sensors *A* and *B*. You can represent the sensor log as an array of objects like so:

js

```
linedata = [
  {hour: 0, value: 8, sensor: "A"},
  {hour: 0, value: 6, sensor: "B"},
  {hour: 1, value: 7, sensor: "A"},
  {hour: 1, value: 5, sensor: "B"},
  {hour: 2, value: 3, sensor: "A"},
  {hour: 2, value: 0, sensor: "B"},
  {hour: 3, value: 9, sensor: "A"},
  {hour: 3, value: 2, sensor: "B"}
]
```

TIP

For larger datasets, you can more efficiently pass data using an [Apache Arrow](https://arrow.apache.org/docs/js/) table as a columnar data representation. [^0.6.16](https://github.com/observablehq/plot/releases/tag/v0.6.16 "added in v0.6.16")

Then you can pass the data to the line mark, and extract named columns from the data for the desired options:

[Fork](https://observablehq.com/@observablehq/plot-accessors "Open on Observable")

js

```
Plot.lineY(linedata, {x: "hour", y: "value", stroke: "sensor"}).plot()
```

Another common way to extract a column from tabular data is an accessor function. This function is invoked for each element in the data (each row), and returns the corresponding observed value, as with [*array*.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map).

[Fork](https://observablehq.com/@observablehq/plot-accessors "Open on Observable")

js

```
Plot.lineY(linedata, {
  x: (d) => d.hour,
  y: (d) => d.value,
  stroke: (d) => d.sensor
}).plot()
```

For greater efficiency, Plot also supports columnar data: you can use an [Apache Arrow](https://arrow.apache.org/docs/js/) table as data instead of an array of objects. [^0.6.16](https://github.com/observablehq/plot/releases/tag/v0.6.16 "added in v0.6.16") You can even pass parallel arrays of values, or Apache Arrow vectors, to each channel.

js

```
Plot.lineY({length: linedata.length}, {
  x: linedata.map((d) => d.hour),
  y: linedata.map((d) => d.value),
  stroke: linedata.map((d) => d.sensor)
}).plot()
```

TIP

Note that when accessor functions or parallel arrays are used instead of field names, automatic axis labels (*hour* and *value*) are lost. These can be restored using the **label** option on the *x* and *y* scales.

## Marks imply data types [​](#marks-imply-data-types)

Data comes in different types: quantitative (or temporal) values can be subtracted, ordinal values can be ordered, and nominal (or categorical) values can only be the same or different.

INFO

Because nominal values often need some arbitrary order for display purposes — often alphabetical — Plot uses the term *ordinal* to refer to both ordinal and nominal data.

Some marks work with any type of data, while other marks have certain requirements or assumptions of data. For example, a line should only be used when both *x* and *y* are quantitative or temporal, and when the data is in a meaningful order (such as chronological). This is because the line mark will interpolate between adjacent points to draw line segments. If *x* or *y* is nominal — say the names of countries — it doesn’t make sense to use a line because there is no half-way point between two nominal values.

[Fork](https://observablehq.com/@observablehq/plot-dont-do-this "Open on Observable")

js

```
Plot.lineY(["please", "don’t", "do", "this"]).plot() // 🌶️
```

WARNING

While Plot aspires to give good defaults and helpful warnings, Plot won’t prevent you from creating a meaningless chart. *Only you* can prevent bogus charts!

In particular, beware the simple “bar”! A bar mark is used for a bar chart, but a rect mark is needed for a histogram. Plot has four different mark types for drawing rectangles:

- use [rect](./../marks/rect) when both *x* and *y* are quantitative
- use [barX](./../marks/bar) when *x* is quantitative and *y* is ordinal
- use [barY](./../marks/bar) when *x* is ordinal and *y* is quantitative
- use [cell](./../marks/cell) when both *x* and *y* are ordinal

Plot encourages you to think about data types as you visualize because data types often imply semantics. For example, do you notice anything strange about the bar chart below?

[Fork](https://observablehq.com/@observablehq/plot-the-missing-bar "Open on Observable")

js

```
Plot
  .barY(timeseries, {x: "year", y: "population"}) // 🌶️
  .plot({x: {tickFormat: ""}})
```

Here’s the underlying data:

js

```
timeseries = [
  {year: 2014, population: 7295.290765},
  {year: 2015, population: 7379.797139},
  {year: 2016, population: 7464.022049},
  {year: 2017, population: 7547.858925},
  {year: 2019, population: 7713.468100},
  {year: 2020, population: 7794.798739}
]
```

The data is missing the population for the year 2018! Because the barY mark implies an ordinal *x* scale, the gap is hidden. Switching to the rectY mark (with the **interval** option to indicate that these are annual observations) reveals the missing data.

[Fork](https://observablehq.com/@observablehq/plot-the-missing-bar "Open on Observable")

js

```
Plot
  .rectY(timeseries, {x: "year", y: "population", interval: 1})
  .plot({x: {tickFormat: ""}})
```

Alternatively, you can keep the barY mark and apply the **interval** option to the *x* scale.

[Fork](https://observablehq.com/@observablehq/plot-the-missing-bar "Open on Observable")

js

```
Plot
  .barY(timeseries, {x: "year", y: "population"})
  .plot({x: {tickFormat: "", interval: 1}})
```

## Marks have options [​](#marks-have-options)

When constructing a mark, you can specify options to change the mark’s appearance. These options are passed as a second argument to the mark constructor. (The first argument is the required data.) For example, if you want filled dots instead of stroked ones, pass the desired color to the **fill** option:

[Fork](https://observablehq.com/@observablehq/plot-marks-have-options "Open on Observable")

js

```
Plot.dot(gistemp, {x: "Date", y: "Anomaly", fill: "red"}).plot()
```

As the name suggests, options are generally optional; Plot tries to provide good defaults for whatever you don’t specify. Plot even has [shorthand](./shorthand) for various common forms of data. Below, we extract an array of numbers from the `gistemp` dataset, and use the line mark shorthand to set *x* = index and *y* = identity.

[Fork](https://observablehq.com/@observablehq/plot-marks-have-options "Open on Observable")

js

```
Plot.lineY(gistemp.map((d) => d.Anomaly)).plot()
```

Some marks even provide default [transforms](./transforms), say for [stacking](./../transforms/stack)!

TIP

Because Plot strives to be concise, there are many default behaviors, some of which can be subtle. If Plot isn’t doing what you expect, try disabling the defaults by specifying options explicitly.

In addition to the standard options such as **fill** and **stroke** that are supported by all mark types, each mark type can support options unique to that type. For example, the dot mark takes a **symbol** option so you can draw things other than circles. See the documentation for each mark type to see what it supports.

## Marks have channels [​](#marks-have-channels)

Channels are mark options that can be used to encode data. These options allow the value to vary with the data, such as a different position or color for each dot. To use a channel, supply it with a column of data, typically as:

- a field (column) name,
- an accessor function, or
- an array of values of the same length and order as the data.

Not all mark options can be expressed as channels. For example, **stroke** can be a channel but **strokeDasharray** cannot. This is mostly a pragmatic limitation — it would be harder to implement Plot if every option were expressible as a channel — but it also serves to guide you towards options that are intended for encoding data.

TIP

To vary the definition of a constant option with data, create multiple marks with your different constant options, and then filter the data for each mark to achieve the desired result.

Some options can be either a channel or a constant depending on the provided value. For example, if you set the **fill** option to *purple*, Plot interprets it as a literal color.

[Fork](https://observablehq.com/@observablehq/plot-marks-have-channels "Open on Observable")

js

```
Plot
  .barX(timeseries, {x: "population", y: "year", fill: "purple"})
  .plot({y: {label: null, tickFormat: ""}})
```

Whereas if the **fill** option is a string but *not* a valid CSS color, Plot assumes you mean the corresponding column of the data and interprets it as a channel.

[Fork](https://observablehq.com/@observablehq/plot-marks-have-channels "Open on Observable")

js

```
Plot
  .barX(timeseries, {x: "population", y: "year", fill: "year"})
  .plot({y: {label: null, tickFormat: ""}})
```

If the **fill** option is a function, it is interpreted as a channel.

[Fork](https://observablehq.com/@observablehq/plot-marks-have-channels "Open on Observable")

js

```
Plot
  .barX(timeseries, {x: "population", y: "year", fill: (d) => d.year})
  .plot({y: {label: null, tickFormat: ""}})
```

Lastly, note that while channels are normally bound to a [scale](#marks-use-scales), you can bypass the *color* scale here by supplying literal color values to the **fill** channel.

[Fork](https://observablehq.com/@observablehq/plot-marks-have-channels "Open on Observable")

js

```
Plot
  .barX(timeseries, {x: "population", y: "year", fill: (d) => d.year & 1 ? "red" : "currentColor"})
  .plot({y: {label: null, tickFormat: ""}})
```

But rather than supplying literal values, it is more semantic to provide abstract values and use scales. In addition to centralizing the encoding definition (if used by multiple marks), it allows Plot to generate a legend.

evenodd

[Fork](https://observablehq.com/@observablehq/plot-marks-have-channels "Open on Observable")

js

```
Plot
  .barX(timeseries, {x: "population", y: "year", fill: (d) => d.year & 1 ? "odd" : "even"})
  .plot({y: {label: null, tickFormat: ""}, color: {legend: true}})
```

You can then specify the *color* scale’s **domain** and **range** to control the encoding.

## Mark options [​](#mark-options)

Mark constructors take two arguments: **data** and **options**. Together these describe a tabular dataset and how to visualize it. Option values that must be the same for all of a mark’s generated shapes are known as *constants*, whereas option values that may vary across a mark’s generated shapes are known as *channels*. Channels are typically bound to [scales](./scales) and encode abstract data values, such as time or temperature, as visual values, such as position or color. (Channels can also be used to order ordinal domains; see the [**sort** option](./scales#sort-mark-option).)

A mark’s data is most commonly an array of objects representing a tabular dataset, such as the result of loading a CSV file, while a mark’s options bind channels (such as *x* and *y*) to columns in the data (such as *units* and *fruit*).

js

```
sales = [
  {units: 10, fruit: "peach"},
  {units: 20, fruit: "pear"},
  {units: 40, fruit: "plum"},
  {units: 30, fruit: "plum"}
]
```

js

```
Plot.dot(sales, {x: "units", y: "fruit"})
```

While a column name such as `"units"` is the most concise way of specifying channel values, values can also be specified as functions for greater flexibility, say to transform data or derive a new column on the fly. Channel functions are invoked for each datum (*d*) in the data and return the corresponding channel value. (This is similar to how D3’s [*selection*.attr](https://d3js.org/d3-selection/modifying#selection_attr) accepts functions, though note that Plot channel functions should return abstract values, not visual values.)

js

```
Plot.dot(sales, {x: (d) => d.units * 1000, y: (d) => d.fruit})
```

Plot also supports columnar data for greater efficiency with bigger datasets; for example, data can be specified as any array of the appropriate length (or any iterable or value compatible with [Array.from](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from)), and then separate arrays of values can be passed as *options*.

js

```
index = [0, 1, 2, 3]
```

js

```
units = [10, 20, 40, 30]
```

js

```
fruits = ["peach", "pear", "plum", "plum"]
```

js

```
Plot.dot(index, {x: units, y: fruits})
```

Channel values can also be specified as numbers for constant values, say for a fixed baseline with an [area](./../marks/area).

js

```
Plot.area(aapl, {x1: "Date", y1: 0, y2: "Close"})
```

Missing and invalid data are handled specifically for each mark type and channel. In most cases, if the provided channel value for a given datum is null, undefined, or (strictly) NaN, the mark will implicitly filter the datum and not generate a corresponding output. In some cases, such as the radius (*r*) of a dot, the channel value must additionally be positive. Plot.line and Plot.area will stop the path before any invalid point and start again at the next valid point, thus creating interruptions rather than interpolating between valid points. Titles will only be added if they are non-empty.

All marks support the following style options:

- **fill** - fill color
- **fillOpacity** - fill opacity (a number between 0 and 1)
- **stroke** - stroke color
- **strokeWidth** - stroke width (in pixels)
- **strokeOpacity** - stroke opacity (a number between 0 and 1)
- **strokeLinejoin** - how to join lines (*bevel*, *miter*, *miter-clip*, or *round*)
- **strokeLinecap** - how to cap lines (*butt*, *round*, or *square*)
- **strokeMiterlimit** - to limit the length of *miter* joins
- **strokeDasharray** - a comma-separated list of dash lengths (typically in pixels)
- **strokeDashoffset** - the [stroke dash offset](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset) (typically in pixels)
- **opacity** - object opacity (a number between 0 and 1)
- **mixBlendMode** - the [blend mode](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode) (*e.g.*, *multiply*)
- **imageFilter** - a CSS [filter](https://developer.mozilla.org/en-US/docs/Web/CSS/filter) (*e.g.*, *blur(5px)*) [^0.6.7](https://github.com/observablehq/plot/releases/tag/v0.6.7 "added in v0.6.7")
- **shapeRendering** - the [shape-rendering mode](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/shape-rendering) (*e.g.*, *crispEdges*)
- **paintOrder** - the [paint order](https://developer.mozilla.org/en-US/docs/Web/CSS/paint-order) (*e.g.*, *stroke*)
- **dx** - horizontal offset (in pixels; defaults to 0)
- **dy** - vertical offset (in pixels; defaults to 0)
- **target** - link target (e.g., “\_blank” for a new window); for use with the **href** channel
- **className** - the [class attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class), if any (defaults to null) [^0.6.16](https://github.com/observablehq/plot/releases/tag/v0.6.16 "added in v0.6.16")
- **ariaDescription** - a textual description of the mark’s contents
- **ariaHidden** - if true, hide this content from the accessibility tree
- **pointerEvents** - the [pointer events](https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events) (*e.g.*, *none*)
- **clip** - whether and how to clip the mark
- **tip** - whether to generate an implicit [pointer](./../interactions/pointer) [tip](./../marks/tip) [^0.6.7](https://github.com/observablehq/plot/releases/tag/v0.6.7 "added in v0.6.7")

If the **clip** option is *frame* (or equivalently true), the mark is clipped to the frame’s dimensions. If the **clip** option is null (or equivalently false), the mark is not clipped. If the **clip** option is *sphere*, the mark will be clipped to the projected sphere (*e.g.*, the front hemisphere when using the orthographic projection); a [geographic projection](./projections) is required in this case. Lastly if the **clip** option is a GeoJSON object [^0.6.17](https://github.com/observablehq/plot/releases/tag/v0.6.17 "added in v0.6.17"), the mark will be clipped to the projected geometry.

If the **tip** option is true, a [tip mark](./../marks/tip) with the [pointer transform](./../interactions/pointer) will be derived from this mark and placed atop all other marks, offering details on demand. If the **tip** option is set to an options object, these options will be passed to the derived tip mark. If the **tip** option (or, if an object, its **pointer** option) is set to *x*, *y*, or *xy*, [pointerX](./../interactions/pointer#pointerX), [pointerY](./../interactions/pointer#pointerY), or [pointer](./../interactions/pointer#pointer) will be used, respectively; otherwise the pointing mode will be chosen automatically. (If the **tip** mark option is truthy, the **title** channel is no longer applied using an SVG title element as this would conflict with the tip mark.)

For all marks except [text](./../marks/text), the **dx** and **dy** options are rendered as a transform property, possibly including a 0.5px offset on low-density screens.

All marks support the following optional channels:

- **fill** - a fill color; bound to the *color* scale
- **fillOpacity** - a fill opacity; bound to the *opacity* scale
- **stroke** - a stroke color; bound to the *color* scale
- **strokeOpacity** - a stroke opacity; bound to the *opacity* scale
- **strokeWidth** - a stroke width (in pixels)
- **opacity** - an object opacity; bound to the *opacity* scale
- **title** - an accessible, short-text description (a string of text, possibly with newlines)
- **href** - a URL to link to
- **ariaLabel** - a short label representing the value in the accessibility tree

The **fill**, **fillOpacity**, **stroke**, **strokeWidth**, **strokeOpacity**, and **opacity** options can be specified as either channels or constants. When the fill or stroke is specified as a function or array, it is interpreted as a channel; when the fill or stroke is specified as a string, it is interpreted as a constant if a valid CSS color and otherwise it is interpreted as a column name for a channel. Similarly when the fill opacity, stroke opacity, object opacity, stroke width, or radius is specified as a number, it is interpreted as a constant; otherwise it is interpreted as a channel.

The scale associated with any channel can be overridden by specifying the channel as an object with a *value* property specifying the channel values and a *scale* property specifying the desired scale name or null for an unscaled channel. For example, to force the **stroke** channel to be unscaled, interpreting the associated values as literal color strings:

js

```
Plot.dot(data, {stroke: {value: "fieldName", scale: null}})
```

To instead force the **stroke** channel to be bound to the *color* scale regardless of the provided values, say:

js

```
Plot.dot(data, {stroke: {value: "fieldName", scale: "color"}})
```

The color channels (**fill** and **stroke**) are bound to the *color* scale by default, unless the provided values are all valid CSS color strings or nullish, in which case the values are interpreted literally and unscaled.

In addition to functions of data, arrays, and column names, channel values can be specified as an object with a *transform* method; this transform method is passed the mark’s array of data and must return the corresponding array of channel values. (Whereas a channel value specified as a function is invoked repeatedly for each element in the mark’s data, similar to *array*.map, the transform method is invoked only once being passed the entire array of data.) For example, to pass the mark’s data directly to the **x** channel, equivalent to [Plot.identity](./transforms#identity):

js

```
Plot.dot(numbers, {x: {transform: (data) => data}})
```

The **title**, **href**, and **ariaLabel** options can *only* be specified as channels. When these options are specified as a string, the string refers to the name of a column in the mark’s associated data. If you’d like every instance of a particular mark to have the same value, specify the option as a function that returns the desired value, *e.g.* `() => "Hello, world!"`.

For marks that support the **frameAnchor** option, it may be specified as one of the four sides (*top*, *right*, *bottom*, *left*), one of the four corners (*top-left*, *top-right*, *bottom-right*, *bottom-left*), or the *middle* of the frame.

All marks support the following [transform](./transforms) options:

- **filter** - apply the [filter transform](./../transforms/filter)
- **sort** - apply the [sort transform](./../transforms/sort)
- **reverse** - apply the [reverse transform](./../transforms/sort#reverse)
- **transform** - apply a [custom transform](./transforms#custom-transforms)
- **initializer** - apply a [custom initializer](./transforms#custom-initializers)

The **sort** option, when not specified as a channel value (such as a field name or an accessor function), can also be used to [impute ordinal scale domains](./scales#sort-mark-option).

### Insets [​](#insets)

Rect-like marks support insets: a positive inset moves the respective side in (towards the opposing side), whereas a negative inset moves the respective side out (away from the opposing side). Insets are specified in pixels using the following options:

- **inset** - shorthand for all four insets
- **insetTop** - inset the top edge
- **insetRight** - inset the right edge
- **insetBottom** - inset the bottom edge
- **insetLeft** - inset the left edge

Insets default to zero. Insets are commonly used to create a one-pixel gap between adjacent bars in histograms; the [bin transform](./../transforms/bin) provides default insets. (Note that the [band scale padding](./scales#position-scale-options) defaults to 0.1 as an alternative to insets.)

### Rounded corners [​](#rounded-corners)

Rect-like marks support rounded corners. Each corner (or side) is individually addressable [^0.6.16](https://github.com/observablehq/plot/releases/tag/v0.6.16 "added in v0.6.16") using the following options:

- **r** - the radius for all four corners
- **rx1** - the radius for the **x1**-**y1** and **x1**-**y2** corners
- **rx2** - the radius for the **x2**-**y1** and **x2**-**y2** corners
- **ry1** - the radius for the **x1**-**y1** and **x2**-**y1** corners
- **ry2** - the radius for the **x1**-**y2** and **x2**-**y2** corners
- **rx1y1** - the radius for the **x1**-**y1** corner
- **rx1y2** - the radius for the **x1**-**y2** corner
- **rx2y1** - the radius for the **x2**-**y1** corner
- **rx2y2** - the radius for the **x2**-**y2** corner
- **rx** - the [*x*-radius](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx) for elliptical corners
- **ry** - the [*y*-radius](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/ry) for elliptical corners

Corner radii are specified in either pixels or, for **rx** and **ry**, as percentages (strings) or the keyword *auto*. If the corner radii are too big, they are reduced proportionally.

## marks(...*marks*) [^0.2.0](https://github.com/observablehq/plot/releases/tag/v0.2.0 "added in v0.2.0") [​](#marks)

js

```
Plot.marks(
  Plot.ruleY([0]),
  Plot.areaY(data, {fill: color, fillOpacity, ...options}),
  Plot.lineY(data, {stroke: color, ...options})
)
```

A convenience method for composing a mark from a series of other marks. Returns an array of marks that implements the *mark*.plot function. See the [box mark](./../marks/box) implementation for an example.
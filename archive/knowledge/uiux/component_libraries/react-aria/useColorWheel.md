# useColorWheel

Source: https://react-spectrum.adobe.com/react-aria/useColorWheel.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ColorWheel).

# useColorWheel

Provides the behavior and accessibility implementation for a color wheel component.
Color wheels allow users to adjust the hue of an HSL or HSB color value on a circular track.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useColorWheel} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/slider/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/color "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/color "View package")

## API[#](#api)

---

`useColorWheel(
props: AriaColorWheelOptions,
state: ColorWheelState,
inputRef: RefObject<HTMLInputElement
|Â  |Â null>
): ColorWheelAria`

## Features[#](#features)

---

The [<input type="color">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color) HTML element
can be used to build a color picker, however it is very inconsistent across browsers and operating systems and consists
of a complete color picker rather than only a hue color wheel. `useColorWheel` helps achieve accessible and
touch-friendly color wheels that can be styled as needed.

- Support for adjusting the hue of an HSL or HSB color value
- Support for mouse, touch, and keyboard via the [useMove](../useMove) hook
- Multi-touch support
- Pressing on the track moves the thumb to that position
- Supports using the arrow keys, as well as page up/down, home, and end keys
- Support for disabling the color wheel
- Prevents text selection while dragging
- Exposed to assistive technology as a `slider` element via ARIA
- Uses a hidden native input element to support touch screen readers
- Automatic ARIA labeling using the localized channel name by default

## Anatomy[#](#anatomy)

---

A color wheel consists of a circular track and a thumb that the user can drag to change the color hue.
A visually hidden `<input>` element is used to represent the value to assistive technologies.

`useColorWheel` returns three sets of props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |

State is managed by the `useColorWheelState`
hook from `@react-stately/color`. The state object should be passed as an option to `useColorWheel`

By default, `useColorWheel` provides an `aria-label` for the localized string "Hue". If you wish to override this
with a more specific label, an `aria-label` or `aria-labelledby` prop may be passed instead to identify the element
to assistive technologies.

## Example[#](#example)

---

This example shows how to build a simple color wheel with a draggable thumb to adjust the hue value of a color. Styling for
the track background and positioning of the thumb are provided by `useColorWheel` in the returned `style` prop for each element.
The visually hidden `<input>` element inside the thumb is used to represent the color wheel to assistive technology. The thumb also
uses the [useFocusRing](../useFocusRing) hook to grow in size when it is keyboard focused (try tabbing to it).

```
import {useColorWheelState} from 'react-stately';
import {useColorWheel, useFocusRing} from 'react-aria';

const RADIUS = 100;
const TRACK_THICKNESS = 28;
const THUMB_SIZE = 20;

function ColorWheel(props) {
  let { isDisabled } = props;
  let state = useColorWheelState(props);
  let inputRef = React.useRef(null);
  let { trackProps, inputProps, thumbProps } = useColorWheel(
    {
      ...props,
      outerRadius: RADIUS,
      innerRadius: RADIUS - TRACK_THICKNESS
    },
    state,
    inputRef
  );

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <div
        {...trackProps}
        style={{
          ...trackProps.style,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : trackProps.style.background
        }}
      />
      <div
        {...thumbProps}
        style={{
          ...thumbProps.style,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : state.getDisplayColor().toString('css'),
          border: `2px solid ${isDisabled ? 'rgb(142, 142, 142)' : 'white'}`,
          boxShadow: '0 0 0 1px black, inset 0 0 0 1px black',
          width: isFocusVisible ? TRACK_THICKNESS + 4 : THUMB_SIZE,
          height: isFocusVisible ? TRACK_THICKNESS + 4 : THUMB_SIZE,
          borderRadius: '50%',
          boxSizing: 'border-box'
        }}
      >
        <input {...inputProps} {...focusProps} ref={inputRef} />
      </div>
    </div>
  );
}

<ColorWheel />
```

```
import {useColorWheelState} from 'react-stately';
import {useColorWheel, useFocusRing} from 'react-aria';

const RADIUS = 100;
const TRACK_THICKNESS = 28;
const THUMB_SIZE = 20;

function ColorWheel(props) {
  let { isDisabled } = props;
  let state = useColorWheelState(props);
  let inputRef = React.useRef(null);
  let { trackProps, inputProps, thumbProps } =
    useColorWheel(
      {
        ...props,
        outerRadius: RADIUS,
        innerRadius: RADIUS - TRACK_THICKNESS
      },
      state,
      inputRef
    );

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      style={{
        position: 'relative',
        display: 'inline-block'
      }}
    >
      <div
        {...trackProps}
        style={{
          ...trackProps.style,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : trackProps.style.background
        }}
      />
      <div
        {...thumbProps}
        style={{
          ...thumbProps.style,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : state.getDisplayColor().toString('css'),
          border: `2px solid ${
            isDisabled ? 'rgb(142, 142, 142)' : 'white'
          }`,
          boxShadow:
            '0 0 0 1px black, inset 0 0 0 1px black',
          width: isFocusVisible
            ? TRACK_THICKNESS + 4
            : THUMB_SIZE,
          height: isFocusVisible
            ? TRACK_THICKNESS + 4
            : THUMB_SIZE,
          borderRadius: '50%',
          boxSizing: 'border-box'
        }}
      >
        <input
          {...inputProps}
          {...focusProps}
          ref={inputRef}
        />
      </div>
    </div>
  );
}

<ColorWheel />
```

```
import {useColorWheelState} from 'react-stately';
import {
  useColorWheel,
  useFocusRing
} from 'react-aria';

const RADIUS = 100;
const TRACK_THICKNESS =
  28;
const THUMB_SIZE = 20;

function ColorWheel(
  props
) {
  let { isDisabled } =
    props;
  let state =
    useColorWheelState(
      props
    );
  let inputRef = React
    .useRef(null);
  let {
    trackProps,
    inputProps,
    thumbProps
  } = useColorWheel(
    {
      ...props,
      outerRadius:
        RADIUS,
      innerRadius:
        RADIUS -
        TRACK_THICKNESS
    },
    state,
    inputRef
  );

  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();

  return (
    <div
      style={{
        position:
          'relative',
        display:
          'inline-block'
      }}
    >
      <div
        {...trackProps}
        style={{
          ...trackProps
            .style,
          background:
            isDisabled
              ? 'rgb(142, 142, 142)'
              : trackProps
                .style
                .background
        }}
      />
      <div
        {...thumbProps}
        style={{
          ...thumbProps
            .style,
          background:
            isDisabled
              ? 'rgb(142, 142, 142)'
              : state
                .getDisplayColor()
                .toString(
                  'css'
                ),
          border:
            `2px solid ${
              isDisabled
                ? 'rgb(142, 142, 142)'
                : 'white'
            }`,
          boxShadow:
            '0 0 0 1px black, inset 0 0 0 1px black',
          width:
            isFocusVisible
              ? TRACK_THICKNESS +
                4
              : THUMB_SIZE,
          height:
            isFocusVisible
              ? TRACK_THICKNESS +
                4
              : THUMB_SIZE,
          borderRadius:
            '50%',
          boxSizing:
            'border-box'
        }}
      >
        <input
          {...inputProps}
          {...focusProps}
          ref={inputRef}
        />
      </div>
    </div>
  );
}

<ColorWheel />
```

## Usage[#](#usage)

---

The following examples show how to use the `ColorWheel` component created in the above example.

### Uncontrolled[#](#uncontrolled)

By default, `ColorWheel` is uncontrolled with a default value of red (hue = 0Ë). You can change the
default value using the `defaultValue` prop.

```
<ColorWheel defaultValue="hsl(80, 100%, 50%)" />
```

```
<ColorWheel defaultValue="hsl(80, 100%, 50%)" />
```

```
<ColorWheel defaultValue="hsl(80, 100%, 50%)" />
```

### Controlled[#](#controlled)

A `ColorWheel` can be made controlled using the `value` prop. The `parseColor`
function is used to parse the initial color from an HSL string, stored in state. The `onChange` prop
is used to update the value in state when the user drags the thumb.

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(parseColor('hsl(0, 100%, 50%)'));
  return (
    <>
      <ColorWheel value={color} onChange={setColor} />
      <p>Current color value: {color.toString('hsl')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(
    parseColor('hsl(0, 100%, 50%)')
  );
  return (
    <>
      <ColorWheel value={color} onChange={setColor} />
      <p>Current color value: {color.toString('hsl')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] =
    React.useState(
      parseColor(
        'hsl(0, 100%, 50%)'
      )
    );
  return (
    <>
      <ColorWheel
        value={color}
        onChange={setColor}
      />
      <p>
        Current color
        value:{' '}
        {color.toString(
          'hsl'
        )}
      </p>
    </>
  );
}
```

### onChangeEnd[#](#onchangeend)

The `onChangeEnd` prop can be used to handle when a user stops dragging the color wheel, whereas the `onChange`
prop is called as the user drags.

```
function Example() {
  let [color, setColor] = React.useState(parseColor('hsl(0, 100%, 50%)'));
  return (
    <>
      <ColorWheel defaultValue={color} onChangeEnd={setColor} />
      <p>Current color value: {color.toString('hsl')}</p>
    </>
  );
}
```

```
function Example() {
  let [color, setColor] = React.useState(
    parseColor('hsl(0, 100%, 50%)')
  );
  return (
    <>
      <ColorWheel
        defaultValue={color}
        onChangeEnd={setColor}
      />
      <p>Current color value: {color.toString('hsl')}</p>
    </>
  );
}
```

```
function Example() {
  let [color, setColor] =
    React.useState(
      parseColor(
        'hsl(0, 100%, 50%)'
      )
    );
  return (
    <>
      <ColorWheel
        defaultValue={color}
        onChangeEnd={setColor}
      />
      <p>
        Current color
        value:{' '}
        {color.toString(
          'hsl'
        )}
      </p>
    </>
  );
}
```

### Disabled[#](#disabled)

A `ColorWheel` can be disabled using the `isDisabled` prop. This prevents the thumb from being focused or dragged.
It's up to you to style your color wheel to appear disabled accordingly.

```
<ColorWheel defaultValue="hsl(80, 100%, 50%)" isDisabled />
```

```
<ColorWheel defaultValue="hsl(80, 100%, 50%)" isDisabled />
```

```
<ColorWheel
  defaultValue="hsl(80, 100%, 50%)"
  isDisabled
/>
```

### HTML forms[#](#html-forms)

ColorWheel supports the `name` prop for integration with HTML forms. The value will be submitted as a number between 0 and 360 degrees.

```
<ColorWheel name="hue" />
```

```
<ColorWheel name="hue" />
```

```
<ColorWheel name="hue" />
```

## Internationalization[#](#internationalization)

---

### Labeling[#](#labeling)

By default, a localized string for the "hue" channel name is used as the `aria-label` for the `ColorWheel`. When a custom `aria-label`
is provided, it should be localized accordingly. To get a localized channel name to use as a visual label,
you can use the `color.getChannelName` method.

### Value formatting[#](#value-formatting)

The `aria-valuetext` of the `<input>` element is formatted according to the user's locale automatically. If you wish to display this
value visually, you can use the `color.formatChannelValue` method.

### RTL[#](#rtl)

Color wheels should not be mirrored in right-to-left languages.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `outerRadius` | `number` | â | The outer radius of the color wheel. |
| `innerRadius` | `number` | â | The inner radius of the color wheel. |
| `isDisabled` | `boolean` | â | Whether the ColorWheel is disabled. |
| `onChange` | `( (value: Color )) => void` | â | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | â | Handler that is called when the user stops dragging. |
| `defaultValue` | `string |Â Color` | `'hsl(0, 100%, 50%)'` | The default value (uncontrolled). |
| `value` | `T` | â | The current value (controlled). |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

Represents a color value.

| Method | Description |
| --- | --- |
| `toFormat( (format: ColorFormat )): Color` | Converts the color to the given color format, and returns a new Color object. |
| `toString( (format?: ColorFormat |Â  |Â 'css' )): string` | Converts the color to a string in the given format. |
| `clone(): Color` | Returns a duplicate of the color value. |
| `toHexInt(): number` | Converts the color to hex, and returns an integer representation. |
| `getChannelValue( (channel: ColorChannel )): number` | Returns the numeric value for a given channel. Throws an error if the channel is unsupported in the current color format. |
| `withChannelValue( (channel: ColorChannel, , value: number )): Color` | Sets the numeric value for a given channel, and returns a new Color object. Throws an error if the channel is unsupported in the current color format. |
| `getChannelRange( (channel: ColorChannel )): ColorChannelRange` | Returns the minimum, maximum, and step values for a given channel. |
| `getChannelName( (channel: ColorChannel, , locale: string )): string` | Returns a localized color channel name for a given channel and locale, for use in visual or accessibility labels. |
| `getChannelFormatOptions( (channel: ColorChannel )): Intl.NumberFormatOptions` | Returns the number formatting options for the given channel. |
| `formatChannelValue( (channel: ColorChannel, , locale: string )): string` | Formats the numeric value for a given channel for display according to the provided locale. |
| `getColorSpace(): ColorSpace` | Returns the color space, 'rgb', 'hsb' or 'hsl', for the current color. |
| `getColorSpaceAxes( (xyChannels: { xChannel?: ColorChannel,  yChannel?: ColorChannel } )): ColorAxes` | Returns the color space axes, xChannel, yChannel, zChannel. |
| `getColorChannels(): [ ColorChannel, ColorChannel, ColorChannel ]` | Returns an array of the color channels within the current color space space. |
| `getColorName( (locale: string )): string` | Returns a localized name for the color, for use in visual or accessibility labels. |
| `getHueName( (locale: string )): string` | Returns a localized name for the hue, for use in visual or accessibility labels. |

A list of supported color formats.

`'hex'
|Â 'hexa'
|Â 'rgb'
|Â 'rgba'
|Â 'hsl'
|Â 'hsla'
|Â 'hsb'
|Â 'hsba'`

A list of color channels.

`'hue'
|Â 'saturation'
|Â 'brightness'
|Â 'lightness'
|Â 'red'
|Â 'green'
|Â 'blue'
|Â 'alpha'`

| Name | Type | Description |
| --- | --- | --- |
| `minValue` | `number` | The minimum value of the color channel. |
| `maxValue` | `number` | The maximum value of the color channel. |
| `step` | `number` | The step value of the color channel, used when incrementing and decrementing. |
| `pageSize` | `number` | The page step value of the color channel, used when incrementing and decrementing. |

`'rgb'
|Â 'hsl'
|Â 'hsb'`

`{

xChannel: ColorChannel,

yChannel: ColorChannel,

zChannel: ColorChannel

}`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `Color` | The current color value represented by the color wheel. |
| `defaultValue` | `Color` | The default color value. |
| `hue` | `number` | The current value of the hue channel displayed by the color wheel. |
| `isDragging` | `boolean` | Whether the color wheel is currently being dragged. |
| `step` | `number` | The step value of the hue channel, used when incrementing and decrementing. |
| `pageStep` | `number` | The page step value of the hue channel, used when incrementing and decrementing. |
| `isDisabled` | `boolean` | Whether the color wheel is disabled. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: string |Â  |Â Color )): void` | Sets the color value represented by the color wheel, and triggers `onChange`. |
| `setHue( (value: number )): void` | Sets the hue channel of the current color value and triggers `onChange`. |
| `setHueFromPoint( x: number, y: number, radius: number ): void` | Sets the hue channel of the current color value based on the given coordinates and radius of the color wheel, and triggers `onChange`. |
| `getThumbPosition( (radius: number )): { x: number,  y: number }` | Returns the coordinates of the thumb relative to the center point of the color wheel. |
| `increment( (stepSize?: number )): void` | Increments the hue by the given amount (defaults to 1). |
| `decrement( (stepSize?: number )): void` | Decrements the hue by the given amount (defaults to 1). |
| `setDragging( (value: boolean )): void` | Sets whether the color wheel is being dragged. |
| `getDisplayColor(): Color` | Returns the color that should be displayed in the color wheel instead of `value`. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

Provides state management for a color wheel component.
Color wheels allow users to adjust the hue of an HSL or HSB color value on a circular track.

`useColorWheelState(
(props: ColorWheelProps
)): ColorWheelState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDisabled` | `boolean` | â | Whether the ColorWheel is disabled. |
| `onChange` | `( (value: Color )) => void` | â | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | â | Handler that is called when the user stops dragging. |
| `defaultValue` | `string |Â Color` | `'hsl(0, 100%, 50%)'` | The default value (uncontrolled). |
| `value` | `T` | â | The current value (controlled). |

Parses a color from a string value. Throws an error if the string could not be parsed.

`parseColor(
(value: string
)): Color`
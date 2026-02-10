# useColorSlider

Source: https://react-spectrum.adobe.com/react-aria/useColorSlider.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ColorSlider).

# useColorSlider

Provides the behavior and accessibility implementation for a color slider component.
Color sliders allow users to adjust an individual channel of a color value.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useColorSlider} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/slider/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/color "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/color "View package")

## API[#](#api)

---

`useColorSlider(
(props: AriaColorSliderOptions,
, state: ColorSliderState
)): ColorSliderAria`

## Features[#](#features)

---

The [<input type="color">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color) HTML element
can be used to build a color picker, however it is very inconsistent across browsers and operating systems and consists
of a complete color picker rather than a single color channel slider. `useColorSlider` helps achieve accessible and
touch-friendly color sliders that can be styled as needed.

- Support for adjusting a single channel of RGBA, HSLA, and HSBA colors
- Support for mouse, touch, and keyboard via the [useMove](../useMove) hook
- Multi-touch support for dragging multiple sliders at once
- Pressing on the track moves the thumb to that position
- Supports using the arrow keys, as well as page up/down, home, and end keys
- Support for both horizontal and vertical orientations
- Support for disabling the color slider
- Prevents text selection while dragging
- Exposed to assistive technology as a `slider` element via ARIA
- Uses a hidden native input element to support touch screen readers
- Automatic ARIA labeling using localized channel names by default
- Support for visually labeling the slider
- Support for displaying the current value using an `<output>` element
- Internationalized number formatting based on the color channel type
- Support for mirroring in RTL locales

## Anatomy[#](#anatomy)

---

A color slider consists of a track element and a thumb that the user can drag to change a single channel of a color value.
It may also include optional label and `<output>` elements to display the color channel name and current numeric value, respectively.
A visually hidden `<input>` element is used to represent the value to assistive technologies.

`useColorSlider` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |
| `outputProps` | `DOMAttributes` | Props for the output element, displaying the value of the color slider. |

State is managed by the `useColorSliderState`
hook from `@react-stately/color`. The state object should be passed as an option to `useColorSlider`

By default, `useColorSlider` provides an `aria-label` for the localized color channel name. If you wish to display a visual
label, or override this with a more specific label, a `label`, `aria-label` or `aria-labelledby` prop may be passed instead.

## Example[#](#example)

---

This example shows how to build a horizontal color slider. It also includes a label which can be clicked to focus the thumb.
Styling for the track background and positioning of the thumb are provided by `useColorSlider` in the returned `style` prop for each element.

If no `label` prop is given, it uses the `Color` object to
get a localized string for the channel name using the `getChannelName` method. In addition, an `<output>` element is used
to display the current channel value as text. This is formatted using the Color object's `formatChannelValue` method, which
formats the value according to the channel type and locale settings.

The visually hidden `<input>` element inside the thumb is used to represent the color slider to assistive technology.
The thumb also uses the [useFocusRing](../useFocusRing) hook to grow in size when it is keyboard focused (try tabbing to it).

```
import {useColorSliderState} from 'react-stately';
import {useColorSlider, useFocusRing, useLocale} from 'react-aria';

const TRACK_THICKNESS = 28;
const THUMB_SIZE = 20;

function ColorSlider(props) {
  let { isDisabled } = props;
  let { locale } = useLocale();
  let state = useColorSliderState({ ...props, locale });
  let trackRef = React.useRef(null);
  let inputRef = React.useRef(null);

  // Default label to the channel name in the current locale
  let label = props.label || state.value.getChannelName(props.channel, locale);

  let { trackProps, thumbProps, inputProps, labelProps, outputProps } =
    useColorSlider({
      ...props,
      label,
      trackRef,
      inputRef
    }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: 300
      }}
    >
      {/* Create a flex container for the label and output element. */}
      <div style={{ display: 'flex', alignSelf: 'stretch' }}>
        <label {...labelProps}>{label}</label>
        <output {...outputProps} style={{ flex: '1 0 auto', textAlign: 'end' }}>
          {state.value.formatChannelValue(props.channel, locale)}
        </output>
      </div>
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps.style,
          height: TRACK_THICKNESS,
          width: '100%',
          borderRadius: 4,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : trackProps.style.background
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps.style,
            top: TRACK_THICKNESS / 2,
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
          <input ref={inputRef} {...inputProps} {...focusProps} />
        </div>
      </div>
    </div>
  );
}

<ColorSlider channel="hue" defaultValue="hsl(0, 100%, 50%)" />
```

```
import {useColorSliderState} from 'react-stately';
import {
  useColorSlider,
  useFocusRing,
  useLocale
} from 'react-aria';

const TRACK_THICKNESS = 28;
const THUMB_SIZE = 20;

function ColorSlider(props) {
  let { isDisabled } = props;
  let { locale } = useLocale();
  let state = useColorSliderState({ ...props, locale });
  let trackRef = React.useRef(null);
  let inputRef = React.useRef(null);

  // Default label to the channel name in the current locale
  let label = props.label ||
    state.value.getChannelName(props.channel, locale);

  let {
    trackProps,
    thumbProps,
    inputProps,
    labelProps,
    outputProps
  } = useColorSlider({
    ...props,
    label,
    trackRef,
    inputRef
  }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: 300
      }}
    >
      {/* Create a flex container for the label and output element. */}
      <div
        style={{ display: 'flex', alignSelf: 'stretch' }}
      >
        <label {...labelProps}>{label}</label>
        <output
          {...outputProps}
          style={{ flex: '1 0 auto', textAlign: 'end' }}
        >
          {state.value.formatChannelValue(
            props.channel,
            locale
          )}
        </output>
      </div>
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps.style,
          height: TRACK_THICKNESS,
          width: '100%',
          borderRadius: 4,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : trackProps.style.background
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps.style,
            top: TRACK_THICKNESS / 2,
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
            ref={inputRef}
            {...inputProps}
            {...focusProps}
          />
        </div>
      </div>
    </div>
  );
}

<ColorSlider
  channel="hue"
  defaultValue="hsl(0, 100%, 50%)"
/>
```

```
import {useColorSliderState} from 'react-stately';
import {
  useColorSlider,
  useFocusRing,
  useLocale
} from 'react-aria';

const TRACK_THICKNESS =
  28;
const THUMB_SIZE = 20;

function ColorSlider(
  props
) {
  let { isDisabled } =
    props;
  let { locale } =
    useLocale();
  let state =
    useColorSliderState({
      ...props,
      locale
    });
  let trackRef = React
    .useRef(null);
  let inputRef = React
    .useRef(null);

  // Default label to the channel name in the current locale
  let label =
    props.label ||
    state.value
      .getChannelName(
        props.channel,
        locale
      );

  let {
    trackProps,
    thumbProps,
    inputProps,
    labelProps,
    outputProps
  } = useColorSlider({
    ...props,
    label,
    trackRef,
    inputRef
  }, state);

  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();

  return (
    <div
      style={{
        display: 'flex',
        flexDirection:
          'column',
        alignItems:
          'center',
        width: 300
      }}
    >
      {/* Create a flex container for the label and output element. */}
      <div
        style={{
          display:
            'flex',
          alignSelf:
            'stretch'
        }}
      >
        <label
          {...labelProps}
        >
          {label}
        </label>
        <output
          {...outputProps}
          style={{
            flex:
              '1 0 auto',
            textAlign:
              'end'
          }}
        >
          {state.value
            .formatChannelValue(
              props
                .channel,
              locale
            )}
        </output>
      </div>
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps
            .style,
          height:
            TRACK_THICKNESS,
          width: '100%',
          borderRadius:
            4,
          background:
            isDisabled
              ? 'rgb(142, 142, 142)'
              : trackProps
                .style
                .background
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps
              .style,
            top:
              TRACK_THICKNESS /
              2,
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
            ref={inputRef}
            {...inputProps}
            {...focusProps}
          />
        </div>
      </div>
    </div>
  );
}

<ColorSlider
  channel="hue"
  defaultValue="hsl(0, 100%, 50%)"
/>
```

### Vertical[#](#vertical)

This example shows how to build a vertical color slider. The main difference from horizontal color sliders is the addition of the
`orientation: 'vertical'` option to `useColorSlider`. This automatically adjusts the internal positioning and dragging logic.
Additionally, this example does not have a visible label or `<output>` element. This can be done by simply not using the returned
`labelProps` and `outputProps`. The color slider will have a default `aria-label` using the localized channel name, which can be overridden
by passing an `aria-label` prop to `useColorSlider`.

```
function ColorSlider(props) {
  let { locale } = useLocale();
  let state = useColorSliderState({ ...props, locale });
  let trackRef = React.useRef(null);
  let inputRef = React.useRef(null);
  let { trackProps, thumbProps, inputProps } = useColorSlider({
    ...props,
    orientation: 'vertical',
    trackRef,
    inputRef
  }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      style={{
        height: 200
      }}
    >
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps.style,
          width: TRACK_THICKNESS,
          height: '100%',
          borderRadius: 4
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps.style,
            left: TRACK_THICKNESS / 2,
            border: '2px solid white',
            boxShadow: '0 0 0 1px black, inset 0 0 0 1px black',
            width: isFocusVisible ? TRACK_THICKNESS + 4 : THUMB_SIZE,
            height: isFocusVisible ? TRACK_THICKNESS + 4 : THUMB_SIZE,
            borderRadius: '50%',
            boxSizing: 'border-box',
            background: state.getDisplayColor().toString('css')
          }}
        >
          <input ref={inputRef} {...inputProps} {...focusProps} />
        </div>
      </div>
    </div>
  );
}

<ColorSlider channel="hue" defaultValue="hsl(0, 100%, 50%)" />
```

```
function ColorSlider(props) {
  let { locale } = useLocale();
  let state = useColorSliderState({ ...props, locale });
  let trackRef = React.useRef(null);
  let inputRef = React.useRef(null);
  let { trackProps, thumbProps, inputProps } =
    useColorSlider({
      ...props,
      orientation: 'vertical',
      trackRef,
      inputRef
    }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      style={{
        height: 200
      }}
    >
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps.style,
          width: TRACK_THICKNESS,
          height: '100%',
          borderRadius: 4
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps.style,
            left: TRACK_THICKNESS / 2,
            border: '2px solid white',
            boxShadow:
              '0 0 0 1px black, inset 0 0 0 1px black',
            width: isFocusVisible
              ? TRACK_THICKNESS + 4
              : THUMB_SIZE,
            height: isFocusVisible
              ? TRACK_THICKNESS + 4
              : THUMB_SIZE,
            borderRadius: '50%',
            boxSizing: 'border-box',
            background: state.getDisplayColor().toString(
              'css'
            )
          }}
        >
          <input
            ref={inputRef}
            {...inputProps}
            {...focusProps}
          />
        </div>
      </div>
    </div>
  );
}

<ColorSlider
  channel="hue"
  defaultValue="hsl(0, 100%, 50%)"
/>
```

```
function ColorSlider(
  props
) {
  let { locale } =
    useLocale();
  let state =
    useColorSliderState({
      ...props,
      locale
    });
  let trackRef = React
    .useRef(null);
  let inputRef = React
    .useRef(null);
  let {
    trackProps,
    thumbProps,
    inputProps
  } = useColorSlider({
    ...props,
    orientation:
      'vertical',
    trackRef,
    inputRef
  }, state);

  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();

  return (
    <div
      style={{
        height: 200
      }}
    >
      <div
        {...trackProps}
        ref={trackRef}
        style={{
          ...trackProps
            .style,
          width:
            TRACK_THICKNESS,
          height: '100%',
          borderRadius: 4
        }}
      >
        <div
          {...thumbProps}
          style={{
            ...thumbProps
              .style,
            left:
              TRACK_THICKNESS /
              2,
            border:
              '2px solid white',
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
              'border-box',
            background:
              state
                .getDisplayColor()
                .toString(
                  'css'
                )
          }}
        >
          <input
            ref={inputRef}
            {...inputProps}
            {...focusProps}
          />
        </div>
      </div>
    </div>
  );
}

<ColorSlider
  channel="hue"
  defaultValue="hsl(0, 100%, 50%)"
/>
```

## Usage[#](#usage)

---

The following examples show how to use the `ColorSlider` component created in the above example.

### RGBA[#](#rgba)

This example shows how you could build an RGBA color picker using four color sliders bound to the same
color value in state. The `parseColor`
function is used to parse the initial color from a hex value, stored in state. The `value` and `onChange` props
of `ColorSlider` are used to make the sliders controlled, so that they all update when the color is modified.

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(parseColor('#7f007f'));
  return (
    <>
      <ColorSlider channel="red" value={color} onChange={setColor} />
      <ColorSlider channel="green" value={color} onChange={setColor} />
      <ColorSlider channel="blue" value={color} onChange={setColor} />
      <ColorSlider channel="alpha" value={color} onChange={setColor} />
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(
    parseColor('#7f007f')
  );
  return (
    <>
      <ColorSlider
        channel="red"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="green"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="blue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
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
        '#7f007f'
      )
    );
  return (
    <>
      <ColorSlider
        channel="red"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="green"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="blue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
    </>
  );
}
```

### HSLA[#](#hsla)

This example shows how to build a similar color picker to the one above, using HSLA colors instead.

```
function Example() {
  let [color, setColor] = React.useState(parseColor('hsl(0, 100%, 50%)'));
  return (
    <>
      <ColorSlider channel="hue" value={color} onChange={setColor} />
      <ColorSlider channel="saturation" value={color} onChange={setColor} />
      <ColorSlider channel="lightness" value={color} onChange={setColor} />
      <ColorSlider channel="alpha" value={color} onChange={setColor} />
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
      <ColorSlider
        channel="hue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="saturation"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="lightness"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
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
      <ColorSlider
        channel="hue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="saturation"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="lightness"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
    </>
  );
}
```

### HSBA[#](#hsba)

This example shows how to build an HSBA color picker.

```
function Example() {
  let [color, setColor] = React.useState(parseColor('hsb(0, 100%, 50%)'));
  return (
    <>
      <ColorSlider channel="hue" value={color} onChange={setColor} />
      <ColorSlider channel="saturation" value={color} onChange={setColor} />
      <ColorSlider channel="brightness" value={color} onChange={setColor} />
      <ColorSlider channel="alpha" value={color} onChange={setColor} />
    </>
  );
}
```

```
function Example() {
  let [color, setColor] = React.useState(
    parseColor('hsb(0, 100%, 50%)')
  );
  return (
    <>
      <ColorSlider
        channel="hue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="saturation"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="brightness"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
    </>
  );
}
```

```
function Example() {
  let [color, setColor] =
    React.useState(
      parseColor(
        'hsb(0, 100%, 50%)'
      )
    );
  return (
    <>
      <ColorSlider
        channel="hue"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="saturation"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="brightness"
        value={color}
        onChange={setColor}
      />
      <ColorSlider
        channel="alpha"
        value={color}
        onChange={setColor}
      />
    </>
  );
}
```

### onChangeEnd[#](#onchangeend)

The `onChangeEnd` prop can be used to handle when a user stops dragging a color slider, whereas the `onChange`
prop is called as the user drags.

```
function Example() {
  let [color, setColor] = React.useState(parseColor('#7f007f'));
  return (
    <>
      <ColorSlider channel="red" defaultValue={color} onChangeEnd={setColor} />
      <p>Current color value: {color.toString('hex')}</p>
    </>
  );
}
```

```
function Example() {
  let [color, setColor] = React.useState(
    parseColor('#7f007f')
  );
  return (
    <>
      <ColorSlider
        channel="red"
        defaultValue={color}
        onChangeEnd={setColor}
      />
      <p>Current color value: {color.toString('hex')}</p>
    </>
  );
}
```

```
function Example() {
  let [color, setColor] =
    React.useState(
      parseColor(
        '#7f007f'
      )
    );
  return (
    <>
      <ColorSlider
        channel="red"
        defaultValue={color}
        onChangeEnd={setColor}
      />
      <p>
        Current color
        value:{' '}
        {color.toString(
          'hex'
        )}
      </p>
    </>
  );
}
```

### Disabled[#](#disabled)

A `ColorSlider` can be disabled using the `isDisabled` prop. This prevents the thumb from being focused or dragged.
It's up to you to style your color slider to appear disabled accordingly.

```
<ColorSlider channel="red" defaultValue="#7f007f" isDisabled />
```

```
<ColorSlider
  channel="red"
  defaultValue="#7f007f"
  isDisabled
/>
```

```
<ColorSlider
  channel="red"
  defaultValue="#7f007f"
  isDisabled
/>
```

### HTML forms[#](#html-forms)

ColorSlider supports the `name` prop for integration with HTML forms. The value will be submitted as a number between the minimum and maximum value for the displayed channel.

```
<ColorSlider
  defaultValue="#7f0000"
  channel="red"
  name="red" />
```

```
<ColorSlider
  defaultValue="#7f0000"
  channel="red"
  name="red" />
```

```
<ColorSlider
  defaultValue="#7f0000"
  channel="red"
  name="red" />
```

## Internationalization[#](#internationalization)

---

### Labeling[#](#labeling)

By default, a localized string for the channel name is used as the `aria-label` for the `ColorSlider`. When a custom `aria-label`
or visual `label` is provided, it should be localized accordingly. To get a localized channel name to use as the visual label,
you can use the `color.getChannelName` method.

### Value formatting[#](#value-formatting)

The `aria-valuetext` of the `<input>` element is formatted according to the user's locale automatically. If you wish to display this
value visually in the `<output>` element, you can use the `color.formatChannelValue` method.

### RTL[#](#rtl)

In right-to-left languages, color sliders should be mirrored. The label should be right aligned, and the value should be left aligned.
Ensure that your CSS accounts for this. Positioning of the thumb and dragging behavior is automatically mirrored by `useColorSlider`.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `trackRef` | `RefObject<Element |Â null>` | â | A ref for the track element. |
| `inputRef` | `RefObject<HTMLInputElement |Â null>` | â | A ref for the input element. |
| `channel` | `ColorChannel` | â | The color channel that the slider manipulates. |
| `colorSpace` | `ColorSpace` | â | The color space that the slider operates in. The `channel` must be in this color space. If not provided, this defaults to the color space of the `color` or `defaultColor` value. |
| `onChange` | `( (value: Color )) => void` | â | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | â | Handler that is called when the user stops dragging. |
| `orientation` | `Orientation` | `'horizontal'` | The orientation of the Slider. |
| `isDisabled` | `boolean` | â | Whether the whole Slider is disabled. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `label` | `ReactNode` | â | The content to display as the label. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

`'rgb'
|Â 'hsl'
|Â 'hsb'`

A list of color channels.

`'hue'
|Â 'saturation'
|Â 'brightness'
|Â 'lightness'
|Â 'red'
|Â 'green'
|Â 'blue'
|Â 'alpha'`

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

| Name | Type | Description |
| --- | --- | --- |
| `minValue` | `number` | The minimum value of the color channel. |
| `maxValue` | `number` | The maximum value of the color channel. |
| `step` | `number` | The step value of the color channel, used when incrementing and decrementing. |
| `pageSize` | `number` | The page step value of the color channel, used when incrementing and decrementing. |

`{

xChannel: ColorChannel,

yChannel: ColorChannel,

zChannel: ColorChannel

}`

`'horizontal' |Â 'vertical'`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `Color` | The current color value represented by the color slider. |
| `isDragging` | `boolean` | Whether the color slider is currently being dragged. |
| `values` | `number[]` | Values managed by the slider by thumb index. |
| `defaultValues` | `number[]` | The default values for each thumb. |
| `focusedThumb` | `number |Â undefined` | Currently-focused thumb index. |
| `step` | `number` | The step amount for the slider. |
| `pageSize` | `number` | The page size for the slider, used to do a bigger step. |
| `orientation` | `Orientation` | The orientation of the slider. |
| `isDisabled` | `boolean` | Whether the slider is disabled. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: string |Â  |Â Color )): void` | Sets the current color value. If a string is passed, it will be parsed to a Color. |
| `getDisplayColor(): Color` | Returns the color that should be displayed in the slider instead of `value` or the optional parameter. |
| `getThumbValue( (index: number )): number` | Get the value for the specified thumb. |
| `setThumbValue( (index: number, , value: number )): void` | Sets the value for the specified thumb. The actual value set will be clamped and rounded according to min/max/step. |
| `setThumbPercent( (index: number, , percent: number )): void` | Sets value for the specified thumb by percent offset (between 0 and 1). |
| `isThumbDragging( (index: number )): boolean` | Whether the specific thumb is being dragged. |
| `setThumbDragging( (index: number, , dragging: boolean )): void` | Set is dragging on the specified thumb. |
| `setFocusedThumb( (index: number |Â  |Â undefined )): void` | Set focused true on specified thumb. This will remove focus from any thumb that had it before. |
| `getThumbPercent( (index: number )): number` | Returns the specified thumb's value as a percentage from 0 to 1. |
| `getValuePercent( (value: number )): number` | Returns the value as a percent between the min and max of the slider. |
| `getThumbValueLabel( (index: number )): string` | Returns the string label for the specified thumb's value, per props.formatOptions. |
| `getFormattedValue( (value: number )): string` | Returns the string label for the value, per props.formatOptions. |
| `getThumbMinValue( (index: number )): number` | Returns the min allowed value for the specified thumb. |
| `getThumbMaxValue( (index: number )): number` | Returns the max allowed value for the specified thumb. |
| `getPercentValue( (percent: number )): number` | Converts a percent along track (between 0 and 1) to the corresponding value. |
| `isThumbEditable( (index: number )): boolean` | Returns if the specified thumb is editable. |
| `setThumbEditable( (index: number, , editable: boolean )): void` | Set the specified thumb's editable state. |
| `incrementThumb( (index: number, , stepSize?: number )): void` | Increments the value of the thumb by the step or page amount. |
| `decrementThumb( (index: number, , stepSize?: number )): void` | Decrements the value of the thumb by the step or page amount. |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |
| `outputProps` | `DOMAttributes` | Props for the output element, displaying the value of the color slider. |

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

Provides state management for a color slider component.
Color sliders allow users to adjust an individual channel of a color value.

`useColorSliderState(
(props: ColorSliderStateOptions
)): ColorSliderState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `locale` | `string` | â | The locale to use for formatting the color channel value. |
| `channel` | `ColorChannel` | â | The color channel that the slider manipulates. |
| `colorSpace` | `ColorSpace` | â | The color space that the slider operates in. The `channel` must be in this color space. If not provided, this defaults to the color space of the `color` or `defaultColor` value. |
| `onChange` | `( (value: Color )) => void` | â | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | â | Handler that is called when the user stops dragging. |
| `orientation` | `Orientation` | `'horizontal'` | The orientation of the Slider. |
| `isDisabled` | `boolean` | â | Whether the whole Slider is disabled. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `label` | `ReactNode` | â | The content to display as the label. |

Parses a color from a string value. Throws an error if the string could not be parsed.

`parseColor(
(value: string
)): Color`
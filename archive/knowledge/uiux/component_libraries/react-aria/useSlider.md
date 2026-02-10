# useSlider

Source: https://react-spectrum.adobe.com/react-aria/useSlider.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Slider).

# useSlider

Provides the behavior and accessibility implementation for a slider component representing one or more values.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useSlider, useSliderThumb} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/slider/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/slider "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/slider "View package")

## API[#](#api)

---

`useSlider<T extends number |Â number[]>(
props: AriaSliderProps<T>,
state: SliderState,
trackRef: RefObject<Element
|Â  |Â null>
): SliderAria`
`useSliderThumb(
(opts: AriaSliderThumbOptions,
, state: SliderState
)): SliderThumbAria`

## Features[#](#features)

---

The [<input type="range">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range)
HTML element can be used to build a slider, however it is
very difficult to style cross browser. `useSlider` and `useSliderThumb` help achieve accessible
sliders that can be styled as needed.

- Support for one or multiple thumbs
- Support for mouse, touch, and keyboard via the [useMove](../useMove) hook
- Multi-touch support for dragging multiple thumbs or multiple sliders at once
- Pressing on the track moves the nearest thumb to that position
- Supports using the arrow keys, as well as page up/down, home, and end keys
- Support for both horizontal and vertical orientations
- Support for custom min, max, and step values with handling for rounding errors
- Support for disabling the whole slider or individual thumbs
- Prevents text selection while dragging
- Exposed to assistive technology as a `group` of `slider` elements via ARIA
- Slider thumbs use hidden native input elements to support touch screen readers
- Support for labeling both the slider as a whole and individual thumbs
- Support for displaying the current thumb values using an `<output>` element
- Internationalized number formatting as a percentage or value
- Support for mirroring in RTL locales

## Anatomy[#](#anatomy)

---

Sliders consist of a track element showing the range of available values,
one or more thumbs showing the current values, an
optional [<output>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/output)
element displaying the current values textually, and a label.
The thumbs can be dragged to allow a user to change their value. In addition, the
track can be clicked to move the nearest thumb to that position.

### useSlider hook[#](#useslider-hook)

`useSlider` returns several sets of props and you should spread each one onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `groupProps` | `DOMAttributes` | Props for the root element of the slider component; groups slider inputs. |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `outputProps` | `OutputHTMLAttributes<HTMLOutputElement>` | Props for the output element, displaying the value of the slider thumbs. |

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify the element to screen readers.

### useSliderThumb hook[#](#usesliderthumb-hook)

`useSliderThumb` returns props that you should spread onto the appropriate elements, along with states for styling:

| Name | Type | Description |
| --- | --- | --- |
| `thumbProps` | `DOMAttributes` | Props for the root thumb element; handles the dragging motion. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element for this thumb (optional). |
| `isDragging` | `boolean` | Whether this thumb is currently being dragged. |
| `isFocused` | `boolean` | Whether the thumb is currently focused. |
| `isDisabled` | `boolean` | Whether the thumb is disabled. |

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify each thumb to screen readers.

Slider state is managed by the `useSliderState` hook.

## Examples[#](#examples)

---

### Single thumb[#](#single-thumb)

This example shows how to build a simple horizontal slider with a single thumb. In addition, it includes a label
which can be clicked to focus the slider thumb, and an `<output>` element to display the current slider value as
text. This is formatted using a locale aware number formatter provided by the [useNumberFormatter](../useNumberFormatter) hook.

The `<input>` element inside the thumb is used to represent the slider to assistive technology, and is hidden from view
using the [VisuallyHidden](../VisuallyHidden) component. The thumb also uses the [useFocusRing](../useFocusRing) hook to
display using a different color when it is keyboard focused (try tabbing to it).

```
import {useSliderState} from 'react-stately';

import {mergeProps, useFocusRing, useNumberFormatter, useSlider, useSliderThumb, VisuallyHidden} from 'react-aria';

function Slider(props) {
  let trackRef = React.useRef(null);
  let numberFormatter = useNumberFormatter(props.formatOptions);
  let state = useSliderState({ ...props, numberFormatter });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(props, state, trackRef);

  return (
    <div {...groupProps} className={`slider ${state.orientation}`}>
      {/* Create a container for the label and output element. */}
      {props.label &&
        (
          <div className="label-container">
            <label {...labelProps}>{props.label}</label>
            <output {...outputProps}>
              {state.getThumbValueLabel(0)}
            </output>
          </div>
        )}
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${state.isDisabled ? 'disabled' : ''}`}
      >
        <Thumb index={0} state={state} trackRef={trackRef} name={props.name} />
      </div>
    </div>
  );
}

function Thumb(props) {
  let { state, trackRef, index, name } = props;
  let inputRef = React.useRef(null);
  let { thumbProps, inputProps, isDragging } = useSliderThumb({
    index,
    trackRef,
    inputRef,
    name
  }, state);

  let { focusProps, isFocusVisible } = useFocusRing();
  return (
    <div
      {...thumbProps}
      className={`thumb ${isFocusVisible ? 'focus' : ''} ${
        isDragging ? 'dragging' : ''
      }`}
    >
      <VisuallyHidden>
        <input ref={inputRef} {...mergeProps(inputProps, focusProps)} />
      </VisuallyHidden>
    </div>
  );
}

<Slider label="Opacity" />
```

```
import {useSliderState} from 'react-stately';

import {
  mergeProps,
  useFocusRing,
  useNumberFormatter,
  useSlider,
  useSliderThumb,
  VisuallyHidden
} from 'react-aria';

function Slider(props) {
  let trackRef = React.useRef(null);
  let numberFormatter = useNumberFormatter(
    props.formatOptions
  );
  let state = useSliderState({ ...props, numberFormatter });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(props, state, trackRef);

  return (
    <div
      {...groupProps}
      className={`slider ${state.orientation}`}
    >
      {/* Create a container for the label and output element. */}
      {props.label &&
        (
          <div className="label-container">
            <label {...labelProps}>{props.label}</label>
            <output {...outputProps}>
              {state.getThumbValueLabel(0)}
            </output>
          </div>
        )}
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${
          state.isDisabled ? 'disabled' : ''
        }`}
      >
        <Thumb
          index={0}
          state={state}
          trackRef={trackRef}
          name={props.name}
        />
      </div>
    </div>
  );
}

function Thumb(props) {
  let { state, trackRef, index, name } = props;
  let inputRef = React.useRef(null);
  let { thumbProps, inputProps, isDragging } =
    useSliderThumb({
      index,
      trackRef,
      inputRef,
      name
    }, state);

  let { focusProps, isFocusVisible } = useFocusRing();
  return (
    <div
      {...thumbProps}
      className={`thumb ${isFocusVisible ? 'focus' : ''} ${
        isDragging ? 'dragging' : ''
      }`}
    >
      <VisuallyHidden>
        <input
          ref={inputRef}
          {...mergeProps(inputProps, focusProps)}
        />
      </VisuallyHidden>
    </div>
  );
}

<Slider label="Opacity" />
```

```
import {useSliderState} from 'react-stately';

import {
  mergeProps,
  useFocusRing,
  useNumberFormatter,
  useSlider,
  useSliderThumb,
  VisuallyHidden
} from 'react-aria';

function Slider(props) {
  let trackRef = React
    .useRef(null);
  let numberFormatter =
    useNumberFormatter(
      props.formatOptions
    );
  let state =
    useSliderState({
      ...props,
      numberFormatter
    });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(
    props,
    state,
    trackRef
  );

  return (
    <div
      {...groupProps}
      className={`slider ${state.orientation}`}
    >
      {/* Create a container for the label and output element. */}
      {props.label &&
        (
          <div className="label-container">
            <label
              {...labelProps}
            >
              {props
                .label}
            </label>
            <output
              {...outputProps}
            >
              {state
                .getThumbValueLabel(
                  0
                )}
            </output>
          </div>
        )}
      {/* The track element holds the visible track line and the thumb. */}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${
          state
              .isDisabled
            ? 'disabled'
            : ''
        }`}
      >
        <Thumb
          index={0}
          state={state}
          trackRef={trackRef}
          name={props
            .name}
        />
      </div>
    </div>
  );
}

function Thumb(props) {
  let {
    state,
    trackRef,
    index,
    name
  } = props;
  let inputRef = React
    .useRef(null);
  let {
    thumbProps,
    inputProps,
    isDragging
  } = useSliderThumb({
    index,
    trackRef,
    inputRef,
    name
  }, state);

  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();
  return (
    <div
      {...thumbProps}
      className={`thumb ${
        isFocusVisible
          ? 'focus'
          : ''
      } ${
        isDragging
          ? 'dragging'
          : ''
      }`}
    >
      <VisuallyHidden>
        <input
          ref={inputRef}
          {...mergeProps(
            inputProps,
            focusProps
          )}
        />
      </VisuallyHidden>
    </div>
  );
}

<Slider label="Opacity" />
```

 Show CSS

```
.slider {
  display: flex;
}

.slider.horizontal {
  flex-direction: column;
  width: 300px;
}

.slider.vertical {
  height: 150px;
}

.label-container {
  display: flex;
  justify-content: space-between;
}

.slider.horizontal .track {
  height: 30px;
  width: 100%;
}

/* track line */
.track:before {
  content: attr(x);
  display: block;
  position: absolute;
  background: gray;
}

.slider.horizontal .track:before {
  height: 3px;
  width: 100%;
  top: 50%;
  transform: translateY(-50%);
}

.slider.vertical .track {
  width: 30px;
  height: 100%;
}

.slider.vertical .track:before {
  width: 3px;
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: gray;
}

.thumb.dragging {
  background: dimgray;
}

.thumb.focus {
  background: orange;
}

.slider.horizontal .thumb {
  top: 50%;
}

.slider.vertical .thumb {
  left: 50%;
}

.track.disabled {
  opacity: 0.4;
}
```

```
.slider {
  display: flex;
}

.slider.horizontal {
  flex-direction: column;
  width: 300px;
}

.slider.vertical {
  height: 150px;
}

.label-container {
  display: flex;
  justify-content: space-between;
}

.slider.horizontal .track {
  height: 30px;
  width: 100%;
}

/* track line */
.track:before {
  content: attr(x);
  display: block;
  position: absolute;
  background: gray;
}

.slider.horizontal .track:before {
  height: 3px;
  width: 100%;
  top: 50%;
  transform: translateY(-50%);
}

.slider.vertical .track {
  width: 30px;
  height: 100%;
}

.slider.vertical .track:before {
  width: 3px;
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: gray;
}

.thumb.dragging {
  background: dimgray;
}

.thumb.focus {
  background: orange;
}

.slider.horizontal .thumb {
  top: 50%;
}

.slider.vertical .thumb {
  left: 50%;
}

.track.disabled {
  opacity: 0.4;
}
```

```
.slider {
  display: flex;
}

.slider.horizontal {
  flex-direction: column;
  width: 300px;
}

.slider.vertical {
  height: 150px;
}

.label-container {
  display: flex;
  justify-content: space-between;
}

.slider.horizontal .track {
  height: 30px;
  width: 100%;
}

/* track line */
.track:before {
  content: attr(x);
  display: block;
  position: absolute;
  background: gray;
}

.slider.horizontal .track:before {
  height: 3px;
  width: 100%;
  top: 50%;
  transform: translateY(-50%);
}

.slider.vertical .track {
  width: 30px;
  height: 100%;
}

.slider.vertical .track:before {
  width: 3px;
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
}

.thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: gray;
}

.thumb.dragging {
  background: dimgray;
}

.thumb.focus {
  background: orange;
}

.slider.horizontal .thumb {
  top: 50%;
}

.slider.vertical .thumb {
  left: 50%;
}

.track.disabled {
  opacity: 0.4;
}
```

### Multi thumb[#](#multi-thumb)

This example shows how to build a slider with multiple thumbs. The thumb component is the same one shown in the previous
example. The main difference in this example is that there are two `<Thumb>` elements rendered with different `index` props.
In addition, the `<output>` element uses `state.getThumbValueLabel` for each thumb to display the selected range.

```
function RangeSlider(props) {
  let trackRef = React.useRef(null);

  let numberFormatter = useNumberFormatter(props.formatOptions);
  let state = useSliderState({ ...props, numberFormatter });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(props, state, trackRef);

  return (
    <div {...groupProps} className={`slider ${state.orientation}`}>
      {props.label &&
        (
          <div className="label-container">
            <label {...labelProps}>{props.label}</label>
            <output {...outputProps}>
              {`${state.getThumbValueLabel(0)} - ${
                state.getThumbValueLabel(1)
              }`}
            </output>
          </div>
        )}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${state.isDisabled ? 'disabled' : ''}`}
      >
        <Thumb index={0} state={state} trackRef={trackRef} />
        <Thumb index={1} state={state} trackRef={trackRef} />
      </div>
    </div>
  );
}

<RangeSlider
  label="Price Range"
  formatOptions={{ style: 'currency', currency: 'USD' }}
  maxValue={500}
  defaultValue={[100, 350]}
  step={10}
/>
```

```
function RangeSlider(props) {
  let trackRef = React.useRef(null);

  let numberFormatter = useNumberFormatter(
    props.formatOptions
  );
  let state = useSliderState({ ...props, numberFormatter });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(props, state, trackRef);

  return (
    <div
      {...groupProps}
      className={`slider ${state.orientation}`}
    >
      {props.label &&
        (
          <div className="label-container">
            <label {...labelProps}>{props.label}</label>
            <output {...outputProps}>
              {`${state.getThumbValueLabel(0)} - ${
                state.getThumbValueLabel(1)
              }`}
            </output>
          </div>
        )}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${
          state.isDisabled ? 'disabled' : ''
        }`}
      >
        <Thumb
          index={0}
          state={state}
          trackRef={trackRef}
        />
        <Thumb
          index={1}
          state={state}
          trackRef={trackRef}
        />
      </div>
    </div>
  );
}

<RangeSlider
  label="Price Range"
  formatOptions={{ style: 'currency', currency: 'USD' }}
  maxValue={500}
  defaultValue={[100, 350]}
  step={10}
/>
```

```
function RangeSlider(
  props
) {
  let trackRef = React
    .useRef(null);

  let numberFormatter =
    useNumberFormatter(
      props.formatOptions
    );
  let state =
    useSliderState({
      ...props,
      numberFormatter
    });
  let {
    groupProps,
    trackProps,
    labelProps,
    outputProps
  } = useSlider(
    props,
    state,
    trackRef
  );

  return (
    <div
      {...groupProps}
      className={`slider ${state.orientation}`}
    >
      {props.label &&
        (
          <div className="label-container">
            <label
              {...labelProps}
            >
              {props
                .label}
            </label>
            <output
              {...outputProps}
            >
              {`${
                state
                  .getThumbValueLabel(
                    0
                  )
              } - ${
                state
                  .getThumbValueLabel(
                    1
                  )
              }`}
            </output>
          </div>
        )}
      <div
        {...trackProps}
        ref={trackRef}
        className={`track ${
          state
              .isDisabled
            ? 'disabled'
            : ''
        }`}
      >
        <Thumb
          index={0}
          state={state}
          trackRef={trackRef}
        />
        <Thumb
          index={1}
          state={state}
          trackRef={trackRef}
        />
      </div>
    </div>
  );
}

<RangeSlider
  label="Price Range"
  formatOptions={{
    style: 'currency',
    currency: 'USD'
  }}
  maxValue={500}
  defaultValue={[
    100,
    350
  ]}
  step={10}
/>
```

## Usage[#](#usage)

---

The following examples show how to use the `Slider` and `RangeSlider` components created in the above examples.

### Vertical orientation[#](#vertical-orientation)

Sliders are horizontally oriented by default. The `orientation` prop can be set to `"vertical"` to create a vertical slider.
This example also uses `aria-label` rather than `label` to create a slider with no visible label.

```
<Slider
  orientation="vertical"
  aria-label="Opacity"
  maxValue={1}
  step={0.01} />
```

```
<Slider
  orientation="vertical"
  aria-label="Opacity"
  maxValue={1}
  step={0.01} />
```

```
<Slider
  orientation="vertical"
  aria-label="Opacity"
  maxValue={1}
  step={0.01} />
```

### Controlled value[#](#controlled-value)

The `value` prop paired with the `onChange` event can be used to make a slider controlled. The value must fall between the Slider's minimum and maximum values, which default to 0 and 100 respectively. The `onChange` event receives the new slider value as a parameter, which can be used to update state.

```
function Example() {
  let [value, setValue] = React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        value={value}
        onChange={setValue} />
      <p>Current value: {value}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] = React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        value={value}
        onChange={setValue} />
      <p>Current value: {value}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] =
    React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        value={value}
        onChange={setValue}
      />
      <p>
        Current value:
        {' '}
        {value}
      </p>
    </>
  );
}
```

Multi thumb sliders specify their values as an array rather than a single number.

```
function Example() {
  let [value, setValue] = React.useState([25, 75]);
  return (
    <>
      <RangeSlider
        label="Range"
        value={value}
        onChange={setValue} />
      <p>Current value: {value.join(' â ')}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] = React.useState([25, 75]);
  return (
    <>
      <RangeSlider
        label="Range"
        value={value}
        onChange={setValue} />
      <p>Current value: {value.join(' â ')}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] =
    React.useState([
      25,
      75
    ]);
  return (
    <>
      <RangeSlider
        label="Range"
        value={value}
        onChange={setValue}
      />
      <p>
        Current value:
        {' '}
        {value.join(
          ' â '
        )}
      </p>
    </>
  );
}
```

### onChangeEnd[#](#onchangeend)

The `onChangeEnd` prop can be used to handle when a user stops dragging a slider, whereas the `onChange` prop is called as the user drags.

```
function Example() {
  let [value, setValue] = React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        defaultValue={value}
        onChangeEnd={setValue} />
      <p>Current value: {value}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] = React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        defaultValue={value}
        onChangeEnd={setValue} />
      <p>Current value: {value}</p>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] =
    React.useState(25);
  return (
    <>
      <Slider
        label="Cookies to buy"
        defaultValue={value}
        onChangeEnd={setValue}
      />
      <p>
        Current value:
        {' '}
        {value}
      </p>
    </>
  );
}
```

### Custom value scale[#](#custom-value-scale)

By default, slider values are percentages between 0 and 100. A different scale can be used by setting the `minValue` and `maxValue` props.

```
<Slider
  label="Cookies to buy"
  minValue={50}
  maxValue={150}
  defaultValue={100} />
```

```
<Slider
  label="Cookies to buy"
  minValue={50}
  maxValue={150}
  defaultValue={100} />
```

```
<Slider
  label="Cookies to buy"
  minValue={50}
  maxValue={150}
  defaultValue={100} />
```

### Value formatting[#](#value-formatting)

Values are formatted as a percentage by default, but this can be modified by using the `formatOptions` prop to specify a different format.
`formatOptions` is compatible with the option parameter of [Intl.NumberFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NumberFormat) and is applied based on the current locale.

```
<Slider
  label="Currency"
  formatOptions={{style: 'currency', currency: 'JPY'}}
  defaultValue={60} />
```

```
<Slider
  label="Currency"
  formatOptions={{style: 'currency', currency: 'JPY'}}
  defaultValue={60} />
```

```
<Slider
  label="Currency"
  formatOptions={{
    style: 'currency',
    currency: 'JPY'
  }}
  defaultValue={60}
/>
```

### Step values[#](#step-values)

The `step` prop can be used to snap the value to certain increments. The steps are calculated
starting from the minimum. For example, if `minValue={2}`, and `step={3}`, the valid step values would be 2, 5, 8, 11, etc.
This example allows increments of 5 between 0 and 100.

```
<Slider
  label="Amount"
  formatOptions={{style: 'currency', currency: 'USD'}}
  minValue={0}
  maxValue={100}
  step={5} />
```

```
<Slider
  label="Amount"
  formatOptions={{style: 'currency', currency: 'USD'}}
  minValue={0}
  maxValue={100}
  step={5} />
```

```
<Slider
  label="Amount"
  formatOptions={{
    style: 'currency',
    currency: 'USD'
  }}
  minValue={0}
  maxValue={100}
  step={5}
/>
```

### Disabled[#](#disabled)

A slider can be disabled using the `isDisabled` prop.

```
<Slider
  label="Cookies to share"
  defaultValue={25}
  isDisabled />
```

```
<Slider
  label="Cookies to share"
  defaultValue={25}
  isDisabled />
```

```
<Slider
  label="Cookies to share"
  defaultValue={25}
  isDisabled
/>
```

### HTML forms[#](#html-forms)

useSliderThumb supports the `name` prop for integration with HTML forms.

```
<Slider
  label="Opacity"
  defaultValue={50}
  name="opacity" />
```

```
<Slider
  label="Opacity"
  defaultValue={50}
  name="opacity" />
```

```
<Slider
  label="Opacity"
  defaultValue={50}
  name="opacity" />
```

## Internationalization[#](#internationalization)

---

### Value formatting[#](#value-formatting-1)

Formatting the value that should be displayed in the value label or `aria-valuetext`
is handled by `useSliderState`.
The formatting can be controlled using the `formatOptions` prop.
If you want to change locales, the `I18nProvider`
must be somewhere in the hierarchy above the Slider.
This will tell the formatter what locale to use.

### RTL[#](#rtl)

In right-to-left languages, the slider should be mirrored. The label is right-aligned,
the value is left-aligned. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `orientation` | `Orientation` | `'horizontal'` | The orientation of the Slider. |
| `isDisabled` | `boolean` | â | Whether the whole Slider is disabled. |
| `onChangeEnd` | `( (value: T )) => void` | â | Fired when the slider stops moving, due to being let go. |
| `minValue` | `number` | `0` | The slider's minimum value. |
| `maxValue` | `number` | `100` | The slider's maximum value. |
| `step` | `number` | `1` | The slider's step value. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

`'horizontal' |Â 'vertical'`

### Properties

| Name | Type | Description |
| --- | --- | --- |
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
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `groupProps` | `DOMAttributes` | Props for the root element of the slider component; groups slider inputs. |
| `trackProps` | `DOMAttributes` | Props for the track element. |
| `outputProps` | `OutputHTMLAttributes<HTMLOutputElement>` | Props for the output element, displaying the value of the slider thumbs. |

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

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `trackRef` | `RefObject<Element |Â null>` | â | A ref to the track element. |
| `inputRef` | `RefObject<HTMLInputElement |Â null>` | â | A ref to the thumb input element. |
| `isDisabled` | `boolean` | â | Whether the Thumb is disabled. |
| `index` | `number` | `0` | Index of the thumb within the slider. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |

`'valid' |Â 'invalid'`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `thumbProps` | `DOMAttributes` | Props for the root thumb element; handles the dragging motion. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden range input element. |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element for this thumb (optional). |
| `isDragging` | `boolean` | Whether this thumb is currently being dragged. |
| `isFocused` | `boolean` | Whether the thumb is currently focused. |
| `isDisabled` | `boolean` | Whether the thumb is disabled. |

Provides state management for a slider component. Stores values for all thumbs,
formats values for localization, and provides methods to update the position
of any thumbs.

`useSliderState<T extends number |Â number[]>(
(props: SliderStateOptions<T>
)): SliderState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `numberFormatter` | `Intl.NumberFormat` | â |  |
| `orientation` | `Orientation` | `'horizontal'` | The orientation of the Slider. |
| `isDisabled` | `boolean` | â | Whether the whole Slider is disabled. |
| `onChangeEnd` | `( (value: T )) => void` | â | Fired when the slider stops moving, due to being let go. |
| `minValue` | `number` | `0` | The slider's minimum value. |
| `maxValue` | `number` | `100` | The slider's maximum value. |
| `step` | `number` | `1` | The slider's step value. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `label` | `ReactNode` | â | The content to display as the label. |

Provides the locale for the application to all child components.

| Name | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode` | Contents that should have the locale applied. |
| `locale` | `string` | The locale to apply to the children. |
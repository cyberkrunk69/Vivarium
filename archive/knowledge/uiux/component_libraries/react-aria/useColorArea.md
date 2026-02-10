# useColorArea

Source: https://react-spectrum.adobe.com/react-aria/useColorArea.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ColorArea).

# useColorArea

Provides the behavior and accessibility implementation for a color area component.
Color area allows users to adjust two channels of an RGB, HSL or HSB color value against a two-dimensional gradient background.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useColorArea} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/slider/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/color "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/color "View package")

## API[#](#api)

---

`useColorArea(
(props: AriaColorAreaOptions,
, state: ColorAreaState
)): ColorAreaAria`

## Features[#](#features)

---

The [<input type="color">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color) HTML element
can be used to build a color picker, however it is very inconsistent across browsers and operating systems and consists
of a complete color picker rather than a color area. `useColorArea` helps achieve accessible and
touch-friendly color areas that can be styled as needed.

- Support for adjusting two-channel values of an HSL, HSB or RGB color value
- Support for mouse, touch, and keyboard via the [useMove](../useMove) hook
- Multi-touch support
- Pressing on the color area background moves the thumb to that position
- Supports using the arrow keys, for changing value by step, as well as shift + arrow key, page up/down, home, and end keys, for changing the value by page step.
- Support for disabling the color area
- Prevents text selection while dragging
- Exposed to assistive technology as a `2D slider` element via ARIA
- Uses two hidden native input elements within a group to support touch screen readers
- Automatic ARIA labeling using the localized channel names by default
- Support for mirroring in RTL locales

## Anatomy[#](#anatomy)

---

A color area consists of a rectangular background area that provides, using a two-dimensional gradient,
a visual representation of the range of color values from which a user can select, and a thumb that the user can drag
to change the selected color value. Two visually hidden `<input>` elements are used to represent the color channel
values to assistive technologies.

`useColorArea` returns five sets of props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `colorAreaProps` | `DOMAttributes` | Props for the color area container element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `xInputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden horizontal range input element. |
| `yInputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden vertical range input element. |

State is managed by the `useColorAreaState`
hook from `@react-stately/color`. The state object should be passed as an option to `useColorArea`.

By default, `useColorArea` provides an `aria-label` for the localized string "Color Picker",
which labels the visually hidden `<input>` elements for the two color channels, or on mobile devices,
the group containing them. If you wish to override this with a more specific label, an `aria-label` or
`aria-labelledby` prop may be passed to further to identify the element to assistive technologies.

The `aria-valuetext` for each `<input>` will include the localized color channel name and current value for each
channel.

## Example[#](#example)

---

This example shows how to build a color area with a draggable thumb to adjust two color channel values of a color. Styling for
the background gradient and positioning of the thumb are provided by `useColorArea` in the returned props for each element.
The two `<input>` elements inside the thumb represent the color channel values to assistive technologies, and are hidden
from view. The thumb also uses the
[useFocusRing](../useFocusRing) hook to grow in size when it is keyboard focused (try tabbing to it).

```
import {useColorAreaState} from 'react-stately';
import {useColorArea, useFocusRing} from 'react-aria';

const SIZE = 192;
const FOCUSED_THUMB_SIZE = 28;
const THUMB_SIZE = 20;
const BORDER_RADIUS = 4;

function ColorArea(props) {
  let inputXRef = React.useRef(null);
  let inputYRef = React.useRef(null);
  let containerRef = React.useRef(null);

  let state = useColorAreaState(props);

  let { isDisabled } = props;

  let {
    colorAreaProps,
    xInputProps,
    yInputProps,
    thumbProps
  } = useColorArea({ ...props, inputXRef, inputYRef, containerRef }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      ref={containerRef}
      {...colorAreaProps}
      style={{
        ...colorAreaProps.style,
        width: SIZE,
        height: SIZE,
        borderRadius: BORDER_RADIUS,
        background: isDisabled
          ? 'rgb(142, 142, 142)'
          : colorAreaProps.style.background,
        opacity: isDisabled ? 0.3 : undefined
      }}
    >
      <div
        {...thumbProps}
        style={{
          ...thumbProps.style,
          background: isDisabled
            ? 'rgb(142, 142, 142)'
            : state.getDisplayColor().toString('css'),
          border: `2px solid ${isDisabled ? 'rgb(142, 142, 142)' : 'white'}`,
          borderRadius: '50%',
          boxShadow: '0 0 0 1px black, inset 0 0 0 1px black',
          boxSizing: 'border-box',
          height: isFocusVisible ? FOCUSED_THUMB_SIZE + 4 : THUMB_SIZE,
          width: isFocusVisible ? FOCUSED_THUMB_SIZE + 4 : THUMB_SIZE
        }}
      >
        <input ref={inputXRef} {...xInputProps} {...focusProps} />
        <input ref={inputYRef} {...yInputProps} {...focusProps} />
      </div>
    </div>
  );
}

<ColorArea />
```

```
import {useColorAreaState} from 'react-stately';
import {useColorArea, useFocusRing} from 'react-aria';

const SIZE = 192;
const FOCUSED_THUMB_SIZE = 28;
const THUMB_SIZE = 20;
const BORDER_RADIUS = 4;

function ColorArea(props) {
  let inputXRef = React.useRef(null);
  let inputYRef = React.useRef(null);
  let containerRef = React.useRef(null);

  let state = useColorAreaState(props);

  let { isDisabled } = props;

  let {
    colorAreaProps,
    xInputProps,
    yInputProps,
    thumbProps
  } = useColorArea({
    ...props,
    inputXRef,
    inputYRef,
    containerRef
  }, state);

  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      ref={containerRef}
      {...colorAreaProps}
      style={{
        ...colorAreaProps.style,
        width: SIZE,
        height: SIZE,
        borderRadius: BORDER_RADIUS,
        background: isDisabled
          ? 'rgb(142, 142, 142)'
          : colorAreaProps.style.background,
        opacity: isDisabled ? 0.3 : undefined
      }}
    >
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
          borderRadius: '50%',
          boxShadow:
            '0 0 0 1px black, inset 0 0 0 1px black',
          boxSizing: 'border-box',
          height: isFocusVisible
            ? FOCUSED_THUMB_SIZE + 4
            : THUMB_SIZE,
          width: isFocusVisible
            ? FOCUSED_THUMB_SIZE + 4
            : THUMB_SIZE
        }}
      >
        <input
          ref={inputXRef}
          {...xInputProps}
          {...focusProps}
        />
        <input
          ref={inputYRef}
          {...yInputProps}
          {...focusProps}
        />
      </div>
    </div>
  );
}

<ColorArea />
```

```
import {useColorAreaState} from 'react-stately';
import {
  useColorArea,
  useFocusRing
} from 'react-aria';

const SIZE = 192;
const FOCUSED_THUMB_SIZE =
  28;
const THUMB_SIZE = 20;
const BORDER_RADIUS = 4;

function ColorArea(
  props
) {
  let inputXRef = React
    .useRef(null);
  let inputYRef = React
    .useRef(null);
  let containerRef =
    React.useRef(null);

  let state =
    useColorAreaState(
      props
    );

  let { isDisabled } =
    props;

  let {
    colorAreaProps,
    xInputProps,
    yInputProps,
    thumbProps
  } = useColorArea({
    ...props,
    inputXRef,
    inputYRef,
    containerRef
  }, state);

  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();

  return (
    <div
      ref={containerRef}
      {...colorAreaProps}
      style={{
        ...colorAreaProps
          .style,
        width: SIZE,
        height: SIZE,
        borderRadius:
          BORDER_RADIUS,
        background:
          isDisabled
            ? 'rgb(142, 142, 142)'
            : colorAreaProps
              .style
              .background,
        opacity:
          isDisabled
            ? 0.3
            : undefined
      }}
    >
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
          borderRadius:
            '50%',
          boxShadow:
            '0 0 0 1px black, inset 0 0 0 1px black',
          boxSizing:
            'border-box',
          height:
            isFocusVisible
              ? FOCUSED_THUMB_SIZE +
                4
              : THUMB_SIZE,
          width:
            isFocusVisible
              ? FOCUSED_THUMB_SIZE +
                4
              : THUMB_SIZE
        }}
      >
        <input
          ref={inputXRef}
          {...xInputProps}
          {...focusProps}
        />
        <input
          ref={inputYRef}
          {...yInputProps}
          {...focusProps}
        />
      </div>
    </div>
  );
}

<ColorArea />
```

## Usage[#](#usage)

---

The following examples show how to use the `ColorArea` component created in the above example.

### Uncontrolled[#](#uncontrolled)

By default, color area is uncontrolled, with a default value of white using the RGB color space (`rgb(255, 255, 255)`).
You can change the default value using the `defaultValue` prop, and the color area will use the color space of the provided value.
If no `xChannel` or `yChannel` is provided, for the RGB color space, the `red` color channel maps to the horizontal axis or `xChannel`,
and the `green` color channel maps to the vertical axis or `yChannel`. Similarly, for the HSL and HSB color spaces, the `hue` color
channel maps to the horizontal axis or `xChannel`, and the `saturation` color channel maps to the vertical axis or `yChannel`.

```
<label id="hsb-label-id">x: Hue, y: Saturation</label>
<ColorArea
  aria-labelledby="hsb-label-id"
  defaultValue="hsb(219, 58%, 93%)" />
```

```
<label id="hsb-label-id">x: Hue, y: Saturation</label>
<ColorArea
  aria-labelledby="hsb-label-id"
  defaultValue="hsb(219, 58%, 93%)" />
```

```
<label id="hsb-label-id">
  x: Hue, y: Saturation
</label>
<ColorArea
  aria-labelledby="hsb-label-id"
  defaultValue="hsb(219, 58%, 93%)"
/>
```

### Controlled[#](#controlled)

A color area can be made controlled using the `value` prop.
The `parseColor`
function is used to parse the initial color from an RGB, HSL or HSB string, stored in state.

The `onChange` prop is used to update the value in the state when the user drags the thumb.
This is the more common usage because it allows to adjust the third color channel using a separate control,
like a color slider using the [useColorSlider](../ColorSlider/useColorSlider) hook or a color wheel using the
[useColorWheel](../ColorWheel/useColorWheel) hook, or to display the color value stored in a state using a preview swatch.

The `onChangeEnd` prop can be used to handle when a user stops dragging the color area.

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('hsba(219, 58%, 93%, 0.75)'));
  let [
    endColor,
    setEndColor
  ] = React.useState(color);
  let [
    xChannel,
    yChannel,
    zChannel
  ] = color.getColorChannels();
  return (
    <>
      <label id="hsb-label-id-1">
        x: {color.getChannelName(xChannel, 'en-US')}, y:{' '}
        {color.getChannelName(yChannel, 'en-US')}
      </label>
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '1rem'
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}
        >
          <ColorArea
            aria-labelledby="hsb-label-id-1"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
            xChannel={xChannel}
            yChannel={yChannel}
          />
          <ColorSlider
            channel={zChannel}
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
          <ColorSlider
            channel="alpha"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}
        >
          <div
            style={{
              display: 'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={color.withChannelValue('alpha', 1)}
              aria-label={`current color swatch: ${color.toString('hsl')}`}
            />
            <ColorSwatch
              color={color}
              aria-label={`current color swatch with alpha channel: ${
                color.toString('hsla')
              }`}
            />
          </div>
          <div
            style={{
              display: 'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={endColor.withChannelValue('alpha', 1)}
              aria-label={`end color swatch: ${endColor.toString('hsb')}`}
            />
            <ColorSwatch
              color={endColor}
              aria-label={`end color swatch with alpha channel: ${
                endColor.toString('hsba')
              }`}
            />
          </div>
        </div>
      </div>
      <p>Current color value: {color.toString('hsba')}</p>
      <p>End color value: {endColor.toString('hsba')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(
    parseColor('hsba(219, 58%, 93%, 0.75)')
  );
  let [
    endColor,
    setEndColor
  ] = React.useState(color);
  let [
    xChannel,
    yChannel,
    zChannel
  ] = color.getColorChannels();
  return (
    <>
      <label id="hsb-label-id-1">
        x: {color.getChannelName(xChannel, 'en-US')}, y:
        {' '}
        {color.getChannelName(yChannel, 'en-US')}
      </label>
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '1rem'
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}
        >
          <ColorArea
            aria-labelledby="hsb-label-id-1"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
            xChannel={xChannel}
            yChannel={yChannel}
          />
          <ColorSlider
            channel={zChannel}
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
          <ColorSlider
            channel="alpha"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}
        >
          <div
            style={{
              display: 'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={color.withChannelValue('alpha', 1)}
              aria-label={`current color swatch: ${
                color.toString('hsl')
              }`}
            />
            <ColorSwatch
              color={color}
              aria-label={`current color swatch with alpha channel: ${
                color.toString('hsla')
              }`}
            />
          </div>
          <div
            style={{
              display: 'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={endColor.withChannelValue('alpha', 1)}
              aria-label={`end color swatch: ${
                endColor.toString('hsb')
              }`}
            />
            <ColorSwatch
              color={endColor}
              aria-label={`end color swatch with alpha channel: ${
                endColor.toString('hsba')
              }`}
            />
          </div>
        </div>
      </div>
      <p>Current color value: {color.toString('hsba')}</p>
      <p>End color value: {endColor.toString('hsba')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(
    parseColor(
      'hsba(219, 58%, 93%, 0.75)'
    )
  );
  let [
    endColor,
    setEndColor
  ] = React.useState(
    color
  );
  let [
    xChannel,
    yChannel,
    zChannel
  ] = color
    .getColorChannels();
  return (
    <>
      <label id="hsb-label-id-1">
        x:{' '}
        {color
          .getChannelName(
            xChannel,
            'en-US'
          )}, y:{' '}
        {color
          .getChannelName(
            yChannel,
            'en-US'
          )}
      </label>
      <div
        style={{
          display:
            'flex',
          flexWrap:
            'wrap',
          gap: '1rem'
        }}
      >
        <div
          style={{
            display:
              'flex',
            flexDirection:
              'column',
            gap: '1rem'
          }}
        >
          <ColorArea
            aria-labelledby="hsb-label-id-1"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
            xChannel={xChannel}
            yChannel={yChannel}
          />
          <ColorSlider
            channel={zChannel}
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
          <ColorSlider
            channel="alpha"
            value={color}
            onChange={setColor}
            onChangeEnd={setEndColor}
          />
        </div>
        <div
          style={{
            display:
              'flex',
            flexDirection:
              'column',
            gap: '1rem'
          }}
        >
          <div
            style={{
              display:
                'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={color
                .withChannelValue(
                  'alpha',
                  1
                )}
              aria-label={`current color swatch: ${
                color
                  .toString(
                    'hsl'
                  )
              }`}
            />
            <ColorSwatch
              color={color}
              aria-label={`current color swatch with alpha channel: ${
                color
                  .toString(
                    'hsla'
                  )
              }`}
            />
          </div>
          <div
            style={{
              display:
                'flex',
              gap: '6px'
            }}
          >
            <ColorSwatch
              color={endColor
                .withChannelValue(
                  'alpha',
                  1
                )}
              aria-label={`end color swatch: ${
                endColor
                  .toString(
                    'hsb'
                  )
              }`}
            />
            <ColorSwatch
              color={endColor}
              aria-label={`end color swatch with alpha channel: ${
                endColor
                  .toString(
                    'hsba'
                  )
              }`}
            />
          </div>
        </div>
      </div>
      <p>
        Current color
        value:{' '}
        {color.toString(
          'hsba'
        )}
      </p>
      <p>
        End color value:
        {' '}
        {endColor
          .toString(
            'hsba'
          )}
      </p>
    </>
  );
}
```

### ColorSlider[#](#colorslider)

The `ColorSlider` component used in the example above controls the channel value not controlled by the `ColorArea`, in this case, the `brightness` channel, or the `alpha` channel.
It is built using the [useColorSlider](../ColorSlider/useColorSlider.html) hook, and can be shared with other color components.

 Show code

```
import {useColorSliderState} from 'react-stately';
import {useColorSlider, useFocusRing, useLocale, VisuallyHidden} from 'react-aria';

function ColorSlider(props) {
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
        width: SIZE
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
        className="color-slider-track"
        {...trackProps}
        ref={trackRef}
        style={{
          height: FOCUSED_THUMB_SIZE
        }}
      >
        <div className="color-slider-track-background"></div>
        <div
          className="color-slider-track-color"
          style={{
            ...trackProps.style
          }}
        >
        </div>
        <div
          className={`color-slider-thumb${isFocusVisible ? ' is-focused' : ''}`}
          {...thumbProps}
          style={{
            ...thumbProps.style
          }}
        >
          <div className="color-slider-thumb-background"></div>
          <div
            className="color-slider-thumb-color"
            style={{
              background: state.getDisplayColor().toString('css')
            }}
          >
          </div>
          <VisuallyHidden>
            <input ref={inputRef} {...inputProps} {...focusProps} />
          </VisuallyHidden>
        </div>
      </div>
    </div>
  );
}
```

```
import {useColorSliderState} from 'react-stately';
import {
  useColorSlider,
  useFocusRing,
  useLocale,
  VisuallyHidden
} from 'react-aria';

function ColorSlider(props) {
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
        width: SIZE
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
        className="color-slider-track"
        {...trackProps}
        ref={trackRef}
        style={{
          height: FOCUSED_THUMB_SIZE
        }}
      >
        <div className="color-slider-track-background">
        </div>
        <div
          className="color-slider-track-color"
          style={{
            ...trackProps.style
          }}
        >
        </div>
        <div
          className={`color-slider-thumb${
            isFocusVisible ? ' is-focused' : ''
          }`}
          {...thumbProps}
          style={{
            ...thumbProps.style
          }}
        >
          <div className="color-slider-thumb-background">
          </div>
          <div
            className="color-slider-thumb-color"
            style={{
              background: state.getDisplayColor().toString(
                'css'
              )
            }}
          >
          </div>
          <VisuallyHidden>
            <input
              ref={inputRef}
              {...inputProps}
              {...focusProps}
            />
          </VisuallyHidden>
        </div>
      </div>
    </div>
  );
}
```

```
import {useColorSliderState} from 'react-stately';
import {
  useColorSlider,
  useFocusRing,
  useLocale,
  VisuallyHidden
} from 'react-aria';

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
        width: SIZE
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
        className="color-slider-track"
        {...trackProps}
        ref={trackRef}
        style={{
          height:
            FOCUSED_THUMB_SIZE
        }}
      >
        <div className="color-slider-track-background">
        </div>
        <div
          className="color-slider-track-color"
          style={{
            ...trackProps
              .style
          }}
        >
        </div>
        <div
          className={`color-slider-thumb${
            isFocusVisible
              ? ' is-focused'
              : ''
          }`}
          {...thumbProps}
          style={{
            ...thumbProps
              .style
          }}
        >
          <div className="color-slider-thumb-background">
          </div>
          <div
            className="color-slider-thumb-color"
            style={{
              background:
                state
                  .getDisplayColor()
                  .toString(
                    'css'
                  )
            }}
          >
          </div>
          <VisuallyHidden>
            <input
              ref={inputRef}
              {...inputProps}
              {...focusProps}
            />
          </VisuallyHidden>
        </div>
      </div>
    </div>
  );
}
```

 Show CSS

```
  .color-slider-track,
  .color-slider-track-background,
  .color-slider-track-color {
    width: 100%;
    border-radius: 4px;
    forced-color-adjust: none;
    position: relative;
  }

  .color-slider-track-background,
  .color-slider-track-color {
    position: absolute;
    height: 100%;
  }

  .color-slider-thumb {
    position: absolute;
    top: 14px;
    border: 2px solid white;
    box-shadow:
      0 0 0 1px black,
      inset 0 0 0 1px black;
    border-radius: 50%;
    box-sizing: border-box;
    width: 20px;
    height: 20px;
  }

  .color-slider-thumb.is-focused {
    width: 32px;
    height: 32px;
  }

  .color-slider-track-background,
  .color-slider-thumb-background {
    background-size: 16px 16px;
    background-position:
      -2px -2px,
      -2px 6px,
      6px -10px,
      -10px -2px;
    background-color: white;
    background-image:
      linear-gradient(-45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(-45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%),
      linear-gradient(45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%);
  }

  .color-slider-thumb-background,
  .color-slider-thumb-color {
    position: absolute;
    border-radius: 50%;
    width: 100%;
    height: 100%;
  }
```

```
  .color-slider-track,
  .color-slider-track-background,
  .color-slider-track-color {
    width: 100%;
    border-radius: 4px;
    forced-color-adjust: none;
    position: relative;
  }

  .color-slider-track-background,
  .color-slider-track-color {
    position: absolute;
    height: 100%;
  }

  .color-slider-thumb {
    position: absolute;
    top: 14px;
    border: 2px solid white;
    box-shadow:
      0 0 0 1px black,
      inset 0 0 0 1px black;
    border-radius: 50%;
    box-sizing: border-box;
    width: 20px;
    height: 20px;
  }

  .color-slider-thumb.is-focused {
    width: 32px;
    height: 32px;
  }

  .color-slider-track-background,
  .color-slider-thumb-background {
    background-size: 16px 16px;
    background-position:
      -2px -2px,
      -2px 6px,
      6px -10px,
      -10px -2px;
    background-color: white;
    background-image:
      linear-gradient(-45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(-45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%),
      linear-gradient(45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%);
  }

  .color-slider-thumb-background,
  .color-slider-thumb-color {
    position: absolute;
    border-radius: 50%;
    width: 100%;
    height: 100%;
  }
```

```
  .color-slider-track,
  .color-slider-track-background,
  .color-slider-track-color {
    width: 100%;
    border-radius: 4px;
    forced-color-adjust: none;
    position: relative;
  }

  .color-slider-track-background,
  .color-slider-track-color {
    position: absolute;
    height: 100%;
  }

  .color-slider-thumb {
    position: absolute;
    top: 14px;
    border: 2px solid white;
    box-shadow:
      0 0 0 1px black,
      inset 0 0 0 1px black;
    border-radius: 50%;
    box-sizing: border-box;
    width: 20px;
    height: 20px;
  }

  .color-slider-thumb.is-focused {
    width: 32px;
    height: 32px;
  }

  .color-slider-track-background,
  .color-slider-thumb-background {
    background-size: 16px 16px;
    background-position:
      -2px -2px,
      -2px 6px,
      6px -10px,
      -10px -2px;
    background-color: white;
    background-image:
      linear-gradient(-45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(45deg, transparent 75.5%, rgb(188, 188, 188) 75.5%),
      linear-gradient(-45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%),
      linear-gradient(45deg, rgb(188, 188, 188) 25.5%, transparent 25.5%);
  }

  .color-slider-thumb-background,
  .color-slider-thumb-color {
    position: absolute;
    border-radius: 50%;
    width: 100%;
    height: 100%;
  }
```

### ColorSwatch[#](#colorswatch)

The `ColorSwatch` component used in the example above implements an image preview of the color with the [useColorSwatch](../ColorSwatch/useColorSwatch.html) hook.

 Show code

```
import {useColorSwatch} from 'react-aria';

function ColorSwatch(props) {
  let { colorSwatchProps, color } = useColorSwatch(props);

  return (
    <span
      {...colorSwatchProps}
      style={{
        ...colorSwatchProps.style,
        display: 'inline-block',
        width: 32,
        height: 32,
        borderRadius: 4,
        background: `linear-gradient(${color}, ${color}),
          repeating-conic-gradient(#CCC 0% 25%, white 0% 50%) 50% / 16px 16px`,
        ...props.style
      }}
    />
  );
}
```

```
import {useColorSwatch} from 'react-aria';

function ColorSwatch(props) {
  let { colorSwatchProps, color } = useColorSwatch(props);

  return (
    <span
      {...colorSwatchProps}
      style={{
        ...colorSwatchProps.style,
        display: 'inline-block',
        width: 32,
        height: 32,
        borderRadius: 4,
        background: `linear-gradient(${color}, ${color}),
          repeating-conic-gradient(#CCC 0% 25%, white 0% 50%) 50% / 16px 16px`,
        ...props.style
      }}
    />
  );
}
```

```
import {useColorSwatch} from 'react-aria';

function ColorSwatch(
  props
) {
  let {
    colorSwatchProps,
    color
  } = useColorSwatch(
    props
  );

  return (
    <span
      {...colorSwatchProps}
      style={{
        ...colorSwatchProps
          .style,
        display:
          'inline-block',
        width: 32,
        height: 32,
        borderRadius: 4,
        background:
          `linear-gradient(${color}, ${color}),
          repeating-conic-gradient(#CCC 0% 25%, white 0% 50%) 50% / 16px 16px`,
        ...props.style
      }}
    />
  );
}
```

### xChannel and yChannel[#](#xchannel-and-ychannel)

The color channel for each axis of a color area can be specified using the `xChannel` and `yChannel` props.
An array of channel names for a color can be returned using the `color.getColorChannels` method.
To get a localized channel name to use as a label, you can use the `color.getChannelName` method.

#### RGB[#](#rgb)

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('rgb(100, 149, 237)'));
  let [
    rChannel,
    gChannel,
    bChannel
  ] = color.getColorChannels();
  return (
    <>
      <div style={{ display: 'inline-flex', flexWrap: 'wrap' }}>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="gbr-label-id-1">
            x: {color.getChannelName(gChannel, 'en-US')}, y:{' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="gbr-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={gChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={rChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="brg-label-id-1">
            x: {color.getChannelName(bChannel, 'en-US')}, y:{' '}
            {color.getChannelName(rChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="brg-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={bChannel}
            yChannel={rChannel}
          />
          <ColorSlider
            channel={gChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="rgb-label-id-1">
            x: {color.getChannelName(rChannel, 'en-US')}, y:{' '}
            {color.getChannelName(gChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="rgb-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={rChannel}
            yChannel={gChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current RGB color value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('rgb')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('rgb(100, 149, 237)'));
  let [
    rChannel,
    gChannel,
    bChannel
  ] = color.getColorChannels();
  return (
    <>
      <div
        style={{ display: 'inline-flex', flexWrap: 'wrap' }}
      >
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="gbr-label-id-1">
            x: {color.getChannelName(gChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="gbr-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={gChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={rChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="brg-label-id-1">
            x: {color.getChannelName(bChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(rChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="brg-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={bChannel}
            yChannel={rChannel}
          />
          <ColorSlider
            channel={gChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="rgb-label-id-1">
            x: {color.getChannelName(rChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(gChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="rgb-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={rChannel}
            yChannel={gChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current RGB color value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('rgb')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(
    parseColor(
      'rgb(100, 149, 237)'
    )
  );
  let [
    rChannel,
    gChannel,
    bChannel
  ] = color
    .getColorChannels();
  return (
    <>
      <div
        style={{
          display:
            'inline-flex',
          flexWrap:
            'wrap'
        }}
      >
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="gbr-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                gChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                bChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="gbr-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={gChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={rChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="brg-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                bChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                rChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="brg-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={bChannel}
            yChannel={rChannel}
          />
          <ColorSlider
            channel={gChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="rgb-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                rChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                gChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="rgb-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={rChannel}
            yChannel={gChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current RGB color
        value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width:
              '16px',
            height:
              '16px',
            verticalAlign:
              'text-bottom'
          }}
        />{' '}
        {color.toString(
          'rgb'
        )}
      </p>
    </>
  );
}
```

#### HSL[#](#hsl)

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('hsl(219, 79%, 66%)'));
  let [
    hChannel,
    sChannel,
    lChannel
  ] = color.getColorChannels();
  return (
    <>
      <div style={{ display: 'inline-flex', flexWrap: 'wrap' }}>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="slh-label-id-1">
            x: {color.getChannelName(sChannel, 'en-US')}, y:{' '}
            {color.getChannelName(lChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="slh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="lhs-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:{' '}
            {color.getChannelName(lChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="lhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="hsl-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:{' '}
            {color.getChannelName(sChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="hsl-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={lChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSL color value:{' '}
        <ColorSwatch
          color={color}
          aria-hidden="true"
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('hsl')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('hsl(219, 79%, 66%)'));
  let [
    hChannel,
    sChannel,
    lChannel
  ] = color.getColorChannels();
  return (
    <>
      <div
        style={{ display: 'inline-flex', flexWrap: 'wrap' }}
      >
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="slh-label-id-1">
            x: {color.getChannelName(sChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(lChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="slh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="lhs-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(lChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="lhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="hsl-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(sChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="hsl-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={lChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSL color value:{' '}
        <ColorSwatch
          color={color}
          aria-hidden="true"
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('hsl')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(
    parseColor(
      'hsl(219, 79%, 66%)'
    )
  );
  let [
    hChannel,
    sChannel,
    lChannel
  ] = color
    .getColorChannels();
  return (
    <>
      <div
        style={{
          display:
            'inline-flex',
          flexWrap:
            'wrap'
        }}
      >
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="slh-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                sChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                lChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="slh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="lhs-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                hChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                lChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="lhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={lChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="hsl-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                hChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                sChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="hsl-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={lChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSL color
        value:{' '}
        <ColorSwatch
          color={color}
          aria-hidden="true"
          style={{
            width:
              '16px',
            height:
              '16px',
            verticalAlign:
              'text-bottom'
          }}
        />{' '}
        {color.toString(
          'hsl'
        )}
      </p>
    </>
  );
}
```

#### HSB[#](#hsb)

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('hsb(219, 58%, 93%)'));
  let [
    hChannel,
    sChannel,
    bChannel
  ] = color.getColorChannels();
  return (
    <>
      <div style={{ display: 'inline-flex', flexWrap: 'wrap' }}>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="sbh-label-id-1">
            x: {color.getChannelName(sChannel, 'en-US')}, y:{' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="sbh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="bhs-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:{' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="bhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div style={{ marginRight: '2rem', marginBottom: '2rem' }}>
          <label id="hsb-label-id-2">
            x: {color.getChannelName(hChannel, 'en-US')}, y:{' '}
            {color.getChannelName(sChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="hsb-label-id-2"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSB color value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('hsb')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(parseColor('hsb(219, 58%, 93%)'));
  let [
    hChannel,
    sChannel,
    bChannel
  ] = color.getColorChannels();
  return (
    <>
      <div
        style={{ display: 'inline-flex', flexWrap: 'wrap' }}
      >
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="sbh-label-id-1">
            x: {color.getChannelName(sChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="sbh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="bhs-label-id-1">
            x: {color.getChannelName(hChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(bChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="bhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight: '2rem',
            marginBottom: '2rem'
          }}
        >
          <label id="hsb-label-id-2">
            x: {color.getChannelName(hChannel, 'en-US')}, y:
            {' '}
            {color.getChannelName(sChannel, 'en-US')}
          </label>
          <ColorArea
            aria-labelledby="hsb-label-id-2"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSB color value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width: '16px',
            height: '16px',
            verticalAlign: 'text-bottom'
          }}
        />{' '}
        {color.toString('hsb')}
      </p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [
    color,
    setColor
  ] = React.useState(
    parseColor(
      'hsb(219, 58%, 93%)'
    )
  );
  let [
    hChannel,
    sChannel,
    bChannel
  ] = color
    .getColorChannels();
  return (
    <>
      <div
        style={{
          display:
            'inline-flex',
          flexWrap:
            'wrap'
        }}
      >
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="sbh-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                sChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                bChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="sbh-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={sChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={hChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="bhs-label-id-1">
            x:{' '}
            {color
              .getChannelName(
                hChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                bChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="bhs-label-id-1"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={bChannel}
          />
          <ColorSlider
            channel={sChannel}
            value={color}
            onChange={setColor}
          />
        </div>
        <div
          style={{
            marginRight:
              '2rem',
            marginBottom:
              '2rem'
          }}
        >
          <label id="hsb-label-id-2">
            x:{' '}
            {color
              .getChannelName(
                hChannel,
                'en-US'
              )}, y:{' '}
            {color
              .getChannelName(
                sChannel,
                'en-US'
              )}
          </label>
          <ColorArea
            aria-labelledby="hsb-label-id-2"
            value={color}
            onChange={setColor}
            xChannel={hChannel}
            yChannel={sChannel}
          />
          <ColorSlider
            channel={bChannel}
            value={color}
            onChange={setColor}
          />
        </div>
      </div>
      <p>
        Current HSB color
        value:{' '}
        <ColorSwatch
          color={color}
          style={{
            width:
              '16px',
            height:
              '16px',
            verticalAlign:
              'text-bottom'
          }}
        />{' '}
        {color.toString(
          'hsb'
        )}
      </p>
    </>
  );
}
```

### Disabled[#](#disabled)

A color area can be disabled using the `isDisabled` prop. This prevents the thumb from being focused or dragged.
It's up to you to style your color area to appear disabled accordingly.

```
<ColorArea
  defaultValue="hsl(0, 100%, 50%)"
  xChannel="saturation"
  yChannel="lightness"
  isDisabled />
```

```
<ColorArea
  defaultValue="hsl(0, 100%, 50%)"
  xChannel="saturation"
  yChannel="lightness"
  isDisabled />
```

```
<ColorArea
  defaultValue="hsl(0, 100%, 50%)"
  xChannel="saturation"
  yChannel="lightness"
  isDisabled
/>
```

### HTML forms[#](#html-forms)

ColorArea supports the `xName` and `yName` props for integration with HTML forms. The values will be submitted as numbers between the minimum and maximum value for the corresponding channel in the X and Y direction.

```
<ColorArea xName="red" yName="green" />
```

```
<ColorArea xName="red" yName="green" />
```

```
<ColorArea
  xName="red"
  yName="green"
/>
```

## Internationalization[#](#internationalization)

---

### Labeling[#](#labeling)

By default, `useColorArea` provides an `aria-label` for the localized string "Color Picker",
which labels the visually hidden `<input>` elements for the two color channels, or on mobile devices,
the group containing them. If you wish to override this with a more specific label, an `aria-label` or
`aria-labelledby` prop may be passed to further to identify the element to assistive technologies.
For example, for a color area that adjusts a text color you might pass the `aria-label` prop,
"Text color", which `useColorArea` will return as the `aria-label` prop "Text color, Color picker". When a custom `aria-label`
is provided, it should be localized accordingly.

### Role description[#](#role-description)

In order to communicate to a screen reader user that the color area adjusts in two dimensions,
`useColorArea` provides an `aria-roledescription`, using the localized string "2D Slider", on each of the
visually hidden `<input>` elements.

### Value formatting[#](#value-formatting)

The `aria-valuetext` of each `<input>` element is formatted according to the user's locale automatically.
It includes the localized color channel name and current value for each channel, with the channel name
and value that the `<input>` element controls coming before the channel name and value for the adjacent
`<input>` element. For example, for an RGB color area where the `xChannel` is "blue", the `yChannel`
is "green", when the current selected color is yellow (`rgb(255, 255, 0)`), the `<input>` representing the
blue channel will have `aria-valuetext` to announce as "Blue: 0, Green: 255", and the `<input>`
representing the green channel will have `aria-valuetext` to announce as "Green: 255, Blue: 0".

### RTL[#](#rtl)

In right-to-left languages, color areas should be mirrored.
Orientation of the gradient background, positioning of the thumb,
and dragging behavior is automatically mirrored by `useColorArea`.

| Name | Type | Description |
| --- | --- | --- |
| `inputXRef` | `RefObject<HTMLInputElement |Â null>` | A ref to the input that represents the x axis of the color area. |
| `inputYRef` | `RefObject<HTMLInputElement |Â null>` | A ref to the input that represents the y axis of the color area. |
| `containerRef` | `RefObject<Element |Â null>` | A ref to the color area containing element. |
| `xName` | `string` | The name of the x channel input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `yName` | `string` | The name of the y channel input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | The `<form>` element to associate the ColorArea with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `colorSpace` | `ColorSpace` | The color space that the color area operates in. The `xChannel` and `yChannel` must be in this color space. If not provided, this defaults to the color space of the `color` or `defaultColor` value. |
| `xChannel` | `ColorChannel` | Color channel for the horizontal axis. |
| `yChannel` | `ColorChannel` | Color channel for the vertical axis. |
| `isDisabled` | `boolean` | Whether the ColorArea is disabled. |
| `onChange` | `( (value: Color )) => void` | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | Handler that is called when the user stops dragging. |
| `value` | `T` | The current value (controlled). |
| `defaultValue` | `T` | The default value (uncontrolled). |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |

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

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `Color` | The current color value displayed by the color area. |
| `defaultValue` | `Color` | The default value of the color area. |
| `xValue` | `number` | The current value of the horizontal axis channel displayed by the color area. |
| `yValue` | `number` | The current value of the vertical axis channel displayed by the color area. |
| `isDragging` | `boolean` | Whether the color area is currently being dragged. |
| `channels` | `{ xChannel: ColorChannel,  yChannel: ColorChannel,  zChannel: ColorChannel }` | Returns the xChannel, yChannel and zChannel names based on the color value. |
| `xChannelStep` | `number` | The step value of the xChannel, used when incrementing and decrementing. |
| `yChannelStep` | `number` | The step value of the yChannel, used when incrementing and decrementing. |
| `xChannelPageStep` | `number` | The page step value of the xChannel, used when incrementing and decrementing. |
| `yChannelPageStep` | `number` | The page step value of the yChannel, used when incrementing and decrementing. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: string |Â  |Â Color )): void` | Sets the current color value. If a string is passed, it will be parsed to a Color. |
| `setXValue( (value: number )): void` | Sets the value for the horizontal axis channel displayed by the color area, and triggers `onChange`. |
| `setYValue( (value: number )): void` | Sets the value for the vertical axis channel displayed by the color area, and triggers `onChange`. |
| `setColorFromPoint( (x: number, , y: number )): void` | Sets the x and y channels of the current color value based on a percentage of the width and height of the color area, and triggers `onChange`. |
| `getThumbPosition(): { x: number,  y: number }` | Returns the coordinates of the thumb relative to the upper left corner of the color area as a percentage. |
| `incrementX( (stepSize?: number )): void` | Increments the value of the horizontal axis channel by the channel step or page amount. |
| `decrementX( (stepSize?: number )): void` | Decrements the value of the horizontal axis channel by the channel step or page amount. |
| `incrementY( (stepSize?: number )): void` | Increments the value of the vertical axis channel by the channel step or page amount. |
| `decrementY( (stepSize?: number )): void` | Decrements the value of the vertical axis channel by the channel step or page amount. |
| `setDragging( (value: boolean )): void` | Sets whether the color area is being dragged. |
| `getDisplayColor(): Color` | Returns the color that should be displayed in the color area thumb instead of `value`. |

| Name | Type | Description |
| --- | --- | --- |
| `colorAreaProps` | `DOMAttributes` | Props for the color area container element. |
| `thumbProps` | `DOMAttributes` | Props for the thumb element. |
| `xInputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden horizontal range input element. |
| `yInputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the visually hidden vertical range input element. |

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

Provides state management for a color area component.
Color area allows users to adjust two channels of an HSL, HSB or RGB color value against a two-dimensional gradient background.

`useColorAreaState(
(props: ColorAreaProps
)): ColorAreaState`

| Name | Type | Description |
| --- | --- | --- |
| `colorSpace` | `ColorSpace` | The color space that the color area operates in. The `xChannel` and `yChannel` must be in this color space. If not provided, this defaults to the color space of the `color` or `defaultColor` value. |
| `xChannel` | `ColorChannel` | Color channel for the horizontal axis. |
| `yChannel` | `ColorChannel` | Color channel for the vertical axis. |
| `isDisabled` | `boolean` | Whether the ColorArea is disabled. |
| `onChange` | `( (value: Color )) => void` | Handler that is called when the value changes, as the user drags. |
| `onChangeEnd` | `( (value: Color )) => void` | Handler that is called when the user stops dragging. |
| `value` | `T` | The current value (controlled). |
| `defaultValue` | `T` | The default value (uncontrolled). |

Parses a color from a string value. Throws an error if the string could not be parsed.

`parseColor(
(value: string
)): Color`
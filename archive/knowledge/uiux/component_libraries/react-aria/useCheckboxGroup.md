# useCheckboxGroup

Source: https://react-spectrum.adobe.com/react-aria/useCheckboxGroup.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../CheckboxGroup).

# useCheckboxGroup

Provides the behavior and accessibility implementation for a checkbox group component.
Checkbox groups allow users to select multiple items from a list of options.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useCheckboxGroup, useCheckboxGroupItem} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/checkbox "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/checkbox "View package")

## API[#](#api)

---

`useCheckboxGroup(
(props: AriaCheckboxGroupProps,
, state: CheckboxGroupState
)): CheckboxGroupAria`
`useCheckboxGroupItem(
props: AriaCheckboxGroupItemProps,
state: CheckboxGroupState,
inputRef: RefObject<HTMLInputElement
|Â  |Â null>
): CheckboxAria`

## Features[#](#features)

---

Checkbox groups can be built in HTML with the
[<fieldset>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/fieldset)
and [<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) elements,
however these can be difficult to style. `useCheckboxGroup` and `useCheckboxGroupItem` help achieve accessible
checkbox groups that can be styled as needed.

- Checkbox groups are exposed to assistive technology via ARIA
- Each checkbox is built with a native HTML `<input>` element, which can be optionally visually
  hidden to allow custom styling
- Full support for browser features like form autofill and validation
- Keyboard focus management and cross browser normalization
- Group and checkbox labeling support for assistive technology

## Anatomy[#](#anatomy)

---

A checkbox group consists of a set of checkboxes, and a label. Each checkbox
includes a label and a visual selection indicator. Zero or more checkboxes
within the group can be selected at a time. Users may click or touch a checkbox
to select it, or use the `Tab` key to navigate to it
and the `Space` key to toggle it.

`useCheckboxGroup` returns props for the group and its label, which you should spread
onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `groupProps` | `DOMAttributes` | Props for the checkbox group wrapper element. |
| `labelProps` | `DOMAttributes` | Props for the checkbox group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the checkbox group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the checkbox group error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

`useCheckboxGroupItem` returns props for an individual checkbox:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isSelected` | `boolean` | Whether the checkbox is selected. |
| `isPressed` | `boolean` | Whether the checkbox is in a pressed state. |
| `isDisabled` | `boolean` | Whether the checkbox is disabled. |
| `isReadOnly` | `boolean` | Whether the checkbox is read only. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

Selection state is managed by the `useCheckboxGroupState`
hook in `@react-stately/checkbox`. The state object should be passed as an option to `useCheckboxGroup`
and `useCheckboxGroupItem`.

Individual checkboxes must have a visual label. If the checkbox group does not have a visible label,
an `aria-label` or `aria-labelledby` prop must be passed instead to identify the element to assistive
technology.

**Note:** `useCheckboxGroupItem` should only be used when it is contained within a checkbox group. For a
standalone checkbox, use the [useCheckbox](../Checkbox/useCheckbox.html) hook instead.

## Example[#](#example)

---

This example uses native input elements for the checkboxes, and React context to share state from the group
to each checkbox. An HTML `<label>` element wraps the native input and the text to provide an implicit label
for the checkbox.

```
import {useCheckboxGroupState} from 'react-stately';
import {useCheckboxGroup, useCheckboxGroupItem} from 'react-aria';

let CheckboxGroupContext = React.createContext(null);

function CheckboxGroup(props) {
  let { children, label, description } = props;
  let state = useCheckboxGroupState(props);
  let {
    groupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useCheckboxGroup(props, state);

  return (
    <div {...groupProps}>
      <span {...labelProps}>{label}</span>
      <CheckboxGroupContext.Provider value={state}>
        {children}
      </CheckboxGroupContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>{description}</div>
      )}
      {isInvalid &&
        (
          <div {...errorMessageProps} style={{ color: 'red', fontSize: 12 }}>
            {validationErrors.join(' ')}
          </div>
        )}
    </div>
  );
}

function Checkbox(props) {
  let { children } = props;
  let state = React.useContext(CheckboxGroupContext);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckboxGroupItem(props, state, ref);

  let isDisabled = state.isDisabled || props.isDisabled;
  let isSelected = state.isSelected(props.value);

  return (
    <label
      {...labelProps}
      style={{
        display: 'block',
        color: (isDisabled && 'var(--gray)') || (isSelected && 'var(--blue)')
      }}
    >
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<CheckboxGroup label="Favorite sports">
  <Checkbox value="soccer" isDisabled>Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
import {useCheckboxGroupState} from 'react-stately';
import {
  useCheckboxGroup,
  useCheckboxGroupItem
} from 'react-aria';

let CheckboxGroupContext = React.createContext(null);

function CheckboxGroup(props) {
  let { children, label, description } = props;
  let state = useCheckboxGroupState(props);
  let {
    groupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useCheckboxGroup(props, state);

  return (
    <div {...groupProps}>
      <span {...labelProps}>{label}</span>
      <CheckboxGroupContext.Provider value={state}>
        {children}
      </CheckboxGroupContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>
          {description}
        </div>
      )}
      {isInvalid &&
        (
          <div
            {...errorMessageProps}
            style={{ color: 'red', fontSize: 12 }}
          >
            {validationErrors.join(' ')}
          </div>
        )}
    </div>
  );
}

function Checkbox(props) {
  let { children } = props;
  let state = React.useContext(CheckboxGroupContext);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckboxGroupItem(
    props,
    state,
    ref
  );

  let isDisabled = state.isDisabled || props.isDisabled;
  let isSelected = state.isSelected(props.value);

  return (
    <label
      {...labelProps}
      style={{
        display: 'block',
        color: (isDisabled && 'var(--gray)') ||
          (isSelected && 'var(--blue)')
      }}
    >
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<CheckboxGroup label="Favorite sports">
  <Checkbox value="soccer" isDisabled>Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
import {useCheckboxGroupState} from 'react-stately';
import {
  useCheckboxGroup,
  useCheckboxGroupItem
} from 'react-aria';

let CheckboxGroupContext =
  React.createContext(
    null
  );

function CheckboxGroup(
  props
) {
  let {
    children,
    label,
    description
  } = props;
  let state =
    useCheckboxGroupState(
      props
    );
  let {
    groupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useCheckboxGroup(
    props,
    state
  );

  return (
    <div {...groupProps}>
      <span
        {...labelProps}
      >
        {label}
      </span>
      <CheckboxGroupContext.Provider
        value={state}
      >
        {children}
      </CheckboxGroupContext.Provider>
      {description && (
        <div
          {...descriptionProps}
          style={{
            fontSize: 12
          }}
        >
          {description}
        </div>
      )}
      {isInvalid &&
        (
          <div
            {...errorMessageProps}
            style={{
              color:
                'red',
              fontSize:
                12
            }}
          >
            {validationErrors
              .join(' ')}
          </div>
        )}
    </div>
  );
}

function Checkbox(
  props
) {
  let { children } =
    props;
  let state = React
    .useContext(
      CheckboxGroupContext
    );
  let ref = React.useRef(
    null
  );
  let {
    inputProps,
    labelProps
  } =
    useCheckboxGroupItem(
      props,
      state,
      ref
    );

  let isDisabled =
    state.isDisabled ||
    props.isDisabled;
  let isSelected = state
    .isSelected(
      props.value
    );

  return (
    <label
      {...labelProps}
      style={{
        display: 'block',
        color:
          (isDisabled &&
            'var(--gray)') ||
          (isSelected &&
            'var(--blue)')
      }}
    >
      <input
        {...inputProps}
        ref={ref}
      />
      {children}
    </label>
  );
}

<CheckboxGroup label="Favorite sports">
  <Checkbox
    value="soccer"
    isDisabled
  >
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

## Styling[#](#styling)

---

See the [useCheckbox](../Checkbox/useCheckbox.html#styling) docs for details on how to customize the styling of checkbox elements.

## Styled examples[#](#styled-examples)

---

[![](/buttongroup-example.2ca88afe.png)

Button Group

A multi-selectable segmented ButtonGroup component.](https://codesandbox.io/s/magical-bose-l7z36b?file=/src/ButtonGroup.js)

## Usage[#](#usage)

---

The following examples show how to use the `CheckboxGroup` component created in the above example.

### Default value[#](#default-value)

An initial, uncontrolled value can be provided to the CheckboxGroup using the `defaultValue` prop, which accepts an array of selected items that map to the
`value` prop on each Checkbox.

```
<CheckboxGroup
  label="Favorite sports (uncontrolled)"
  defaultValue={['soccer', 'baseball']}
>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports (uncontrolled)"
  defaultValue={['soccer', 'baseball']}
>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports (uncontrolled)"
  defaultValue={[
    'soccer',
    'baseball'
  ]}
>
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

### Controlled value[#](#controlled-value)

A controlled value can be provided using the `value` prop, which accepts an array of selected items, which map to the
`value` prop on each Checkbox. The `onChange` event is fired when the user checks or unchecks an option. It receives a new array
containing the updated selected values.

```
function Example() {
  let [selected, setSelected] = React.useState(['soccer', 'baseball']);

  return (
    <CheckboxGroup
      label="Favorite sports (controlled)"
      value={selected}
      onChange={setSelected}
    >
      <Checkbox value="soccer">Soccer</Checkbox>
      <Checkbox value="baseball">Baseball</Checkbox>
      <Checkbox value="basketball">Basketball</Checkbox>
    </CheckboxGroup>
  );
}
```

```
function Example() {
  let [selected, setSelected] = React.useState([
    'soccer',
    'baseball'
  ]);

  return (
    <CheckboxGroup
      label="Favorite sports (controlled)"
      value={selected}
      onChange={setSelected}
    >
      <Checkbox value="soccer">Soccer</Checkbox>
      <Checkbox value="baseball">Baseball</Checkbox>
      <Checkbox value="basketball">Basketball</Checkbox>
    </CheckboxGroup>
  );
}
```

```
function Example() {
  let [
    selected,
    setSelected
  ] = React.useState([
    'soccer',
    'baseball'
  ]);

  return (
    <CheckboxGroup
      label="Favorite sports (controlled)"
      value={selected}
      onChange={setSelected}
    >
      <Checkbox value="soccer">
        Soccer
      </Checkbox>
      <Checkbox value="baseball">
        Baseball
      </Checkbox>
      <Checkbox value="basketball">
        Basketball
      </Checkbox>
    </CheckboxGroup>
  );
}
```

### Description[#](#description)

The `description` prop can be used to associate additional help text with a checkbox group.

```
<CheckboxGroup
  label="Favorite sports"
  description="Select your favorite sports."
>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  description="Select your favorite sports."
>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  description="Select your favorite sports."
>
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

### Group validation[#](#group-validation)

CheckboxGroup supports the `isRequired` prop to ensure the user selects at least one item, as well as custom client and server-side validation. Individual checkboxes also support validation, and errors from all checkboxes are aggregated at the group level. CheckboxGroup can also be integrated with other form libraries. See the [Forms](../forms) guide to learn more.

When a CheckboxGroup has the `validationBehavior="native"` prop, validation errors block form submission. The `isRequired` prop at the `CheckboxGroup` level requires that at least one item is selected. To display validation errors, use the `validationErrors` and `errorMessageProps` returned by `useCheckboxGroup`. This allows you to render error messages from all of the above sources with consistent custom styles.

```
<form>
  <CheckboxGroup
    label="Sandwich condiments"
    name="condiments"
    isRequired
    validationBehavior="native"  >
    <Checkbox value="lettuce">Lettuce</Checkbox>
    <Checkbox value="tomato">Tomato</Checkbox>
    <Checkbox value="onion">Onion</Checkbox>
    <Checkbox value="sprouts">Sprouts</Checkbox>
  </CheckboxGroup>
  <input type="submit" style={{marginTop: 8}} />
</form>
```

```
<form>
  <CheckboxGroup
    label="Sandwich condiments"
    name="condiments"
    isRequired
    validationBehavior="native"  >
    <Checkbox value="lettuce">Lettuce</Checkbox>
    <Checkbox value="tomato">Tomato</Checkbox>
    <Checkbox value="onion">Onion</Checkbox>
    <Checkbox value="sprouts">Sprouts</Checkbox>
  </CheckboxGroup>
  <input type="submit" style={{marginTop: 8}} />
</form>
```

```
<form>
  <CheckboxGroup
    label="Sandwich condiments"
    name="condiments"
    isRequired
    validationBehavior="native"  >
    <Checkbox value="lettuce">
      Lettuce
    </Checkbox>
    <Checkbox value="tomato">
      Tomato
    </Checkbox>
    <Checkbox value="onion">
      Onion
    </Checkbox>
    <Checkbox value="sprouts">
      Sprouts
    </Checkbox>
  </CheckboxGroup>
  <input
    type="submit"
    style={{
      marginTop: 8
    }}
  />
</form>
```

### Individual Checkbox validation[#](#individual-checkbox-validation)

To require that specific checkboxes are checked, set the `isRequired` prop at the `Checkbox` level instead of the `CheckboxGroup`. The following example shows how to require that all items are selected.

```
<form>
  <CheckboxGroup label="Agree to the following" validationBehavior="native">
    <Checkbox value="terms" isRequired>Terms and conditions</Checkbox>
    <Checkbox value="privacy" isRequired>Privacy policy</Checkbox>
    <Checkbox value="cookies" isRequired>Cookie policy</Checkbox>  </CheckboxGroup>
  <input type="submit" style={{marginTop: 8}} />
</form>
```

```
<form>
  <CheckboxGroup
    label="Agree to the following"
    validationBehavior="native"
  >
    <Checkbox value="terms" isRequired>
      Terms and conditions
    </Checkbox>
    <Checkbox value="privacy" isRequired>
      Privacy policy
    </Checkbox>
    <Checkbox value="cookies" isRequired>
      Cookie policy
    </Checkbox>  </CheckboxGroup>
  <input type="submit" style={{ marginTop: 8 }} />
</form>
```

```
<form>
  <CheckboxGroup
    label="Agree to the following"
    validationBehavior="native"
  >
    <Checkbox
      value="terms"
      isRequired
    >
      Terms and
      conditions
    </Checkbox>
    <Checkbox
      value="privacy"
      isRequired
    >
      Privacy policy
    </Checkbox>
    <Checkbox
      value="cookies"
      isRequired
    >
      Cookie policy
    </Checkbox>  </CheckboxGroup>
  <input
    type="submit"
    style={{
      marginTop: 8
    }}
  />
</form>
```

### Disabled[#](#disabled)

The entire CheckboxGroup can be disabled with the `isDisabled` prop.

```
<CheckboxGroup label="Favorite sports" isDisabled>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup label="Favorite sports" isDisabled>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  isDisabled
>
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

To disable an individual checkbox, pass `isDisabled` to the `Checkbox` instead.

```
<CheckboxGroup label="Favorite sports">
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball" isDisabled>Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup label="Favorite sports">
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball" isDisabled>Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup label="Favorite sports">
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox
    value="baseball"
    isDisabled
  >
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

### Read only[#](#read-only)

The `isReadOnly` prop makes the selection immutable. Unlike `isDisabled`, the CheckboxGroup remains focusable.
See the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<CheckboxGroup label="Favorite sports" defaultValue={['baseball']} isReadOnly>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  defaultValue={['baseball']}
  isReadOnly
>
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  defaultValue={[
    'baseball'
  ]}
  isReadOnly
>
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

### HTML forms[#](#html-forms)

CheckboxGroup supports the `name` prop, paired with the Checkbox `value` prop, for integration with HTML forms.

```
<CheckboxGroup label="Favorite sports" name="sports">
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup label="Favorite sports" name="sports">
  <Checkbox value="soccer">Soccer</Checkbox>
  <Checkbox value="baseball">Baseball</Checkbox>
  <Checkbox value="basketball">Basketball</Checkbox>
</CheckboxGroup>
```

```
<CheckboxGroup
  label="Favorite sports"
  name="sports"
>
  <Checkbox value="soccer">
    Soccer
  </Checkbox>
  <Checkbox value="baseball">
    Baseball
  </Checkbox>
  <Checkbox value="basketball">
    Basketball
  </Checkbox>
</CheckboxGroup>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `string[]` | â | The current value (controlled). |
| `defaultValue` | `string[]` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string[] )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

`'valid' |Â 'invalid'`

`string |Â string[]`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `readonly string[]` | Current selected values. |
| `defaultValue` | `readonly string[]` | Default selected values. |
| `isDisabled` | `boolean` | Whether the checkbox group is disabled. |
| `isReadOnly` | `boolean` | Whether the checkbox group is read only. |
| `isInvalid` | `boolean` | Whether the checkbox group is invalid. |
| `isRequired` | `boolean` | Whether the checkboxes in the group are required. This changes to false once at least one item is selected. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `isSelected( (value: string )): boolean` | Returns whether the given value is selected. |
| `setValue( (value: string[] )): void` | Sets the selected values. |
| `addValue( (value: string )): void` | Adds a value to the set of selected values. |
| `removeValue( (value: string )): void` | Removes a value from the set of selected values. |
| `toggleValue( (value: string )): void` | Toggles a value in the set of selected values. |
| `setInvalid( (value: string, , validation: ValidationResult )): void` | Sets whether one of the checkboxes is invalid. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

| Name | Type | Description |
| --- | --- | --- |
| `groupProps` | `DOMAttributes` | Props for the checkbox group wrapper element. |
| `labelProps` | `DOMAttributes` | Props for the checkbox group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the checkbox group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the checkbox group error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

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
| `value` | `string` | â |  |
| `isIndeterminate` | `boolean` | â | Indeterminism is presentational only. The indeterminate visual representation remains regardless of user interaction. |
| `children` | `ReactNode` | â | The label for the element. |
| `onChange` | `( (isSelected: boolean )) => void` | â | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: boolean )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` | The type of press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Methods

| Method | Description |
| --- | --- |
| `continuePropagation(): void` | By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. |

`'mouse'
|Â 'pen'
|Â 'touch'
|Â 'keyboard'
|Â 'virtual'`

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isSelected` | `boolean` | Whether the checkbox is selected. |
| `isPressed` | `boolean` | Whether the checkbox is in a pressed state. |
| `isDisabled` | `boolean` | Whether the checkbox is disabled. |
| `isReadOnly` | `boolean` | Whether the checkbox is read only. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

Provides state management for a checkbox group component. Provides a name for the group,
and manages selection and focus state.

`useCheckboxGroupState(
(props: CheckboxGroupProps
)): CheckboxGroupState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `string[]` | â | The current value (controlled). |
| `defaultValue` | `string[]` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string[] )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
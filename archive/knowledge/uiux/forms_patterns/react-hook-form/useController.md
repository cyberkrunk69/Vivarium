# useController

Source: https://react-hook-form.com/docs/usecontroller

---

Select page...controller`## useController: (props?: UseControllerProps) => { field: object, fieldState: object, formState: object }`

This custom hook powers [`Controller`](/docs/usecontroller/controller). Additionally, it shares the same props and methods as `Controller`. It's useful for creating reusable Controlled input.

## Props

The following table contains information about the arguments for `useController`.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | [`FieldPath`](/ts#FieldPath "FieldPath type") | ✓ | Unique name of your input. |
| `control` | [`Control`](/ts#Control "Control type") |  | [`control`](/docs/useform/control) object provided by invoking `useForm`. Optional when using `FormProvider`. |
| `rules` | `Object` |  | Validation rules in the same format for `register`, which includes:  required, min, max, minLength, maxLength, pattern, validate  [CodeSandbox TS](https://codesandbox.io/s/controller-rules-8pd7z?file=/src/App.tsx)  ```  rules={{ required: true }} ``` |
| `shouldUnregister` | `boolean = false` |  | Input will be unregistered after unmount and defaultValues will be removed as well.  **Note:** this prop should be avoided when using with `useFieldArray` as `unregister` function gets called after input unmount/remount and reorder. |
| `disabled` | `boolean = false` |  | `disabled` prop will be returned from `field` prop. Controlled input will be disabled and its value will be omitted from the submission data. |
| `defaultValue` | `unknown` |  | **Important:** Can not apply `undefined` to `defaultValue` or `defaultValues` at `useForm`.   - You need to either set `defaultValue` at the field-level or `useForm`'s `defaultValues`. `undefined` is not a valid value. If you used `defaultValues` at `useForm`, skip using this prop. - If your form will invoke `reset` with default values, you will need to provide `useForm` with `defaultValues`. |
| `exact` | `boolean = false` |  | This prop will enable an exact match for input name subscriptions, default to true. |

## Return

The following table contains information about properties which `useController` produces.

| Object Name | Name | Type | Description |
| --- | --- | --- | --- |
| `field` | `onChange` | `(value: any) => void` | A function which sends the input's value to the library.   - It should be assigned to the `onChange` prop of the input and value should **not be `undefined`**. - This prop update [formState](/docs/useform/formstate) and you should avoid manually invoke [setValue](/docs/useform/setvalue) or other API related to field update. |
| `field` | `onBlur` | `() => void` | A function which sends the input's onBlur event to the library. It should be assigned to the input's `onBlur` prop. |
| `field` | `value` | `unknown` | The current value of the controlled component. |
| `field` | `disabled` | `boolean` | The disabled state of the input. |
| `field` | `name` | `string` | Input's name being registered. |
| `field` | `ref` | `React.Ref` | A ref used to connect hook form to the input. Assign `ref` to component's input ref to allow hook form to focus the error input. |
| `fieldState` | `invalid` | `boolean` | Invalid state for current input. |
| `fieldState` | `isTouched` | `boolean` | Touched state for current controlled input. |
| `fieldState` | `isDirty` | `boolean` | Dirty state for current controlled input. |
| `fieldState` | `error` | `object` | error for this specific input. |
| [`formState`](/docs/useform/formstate) | `isDirty` | `boolean` | Set to `true` after the user modifies any of the inputs.   - **Important:** Make sure to provide all inputs' defaultValues at the useForm, so hook form can have a single source of truth to compare whether the form is dirty.  Copy  ```    const {  formState: { isDirty, dirtyFields },  setValue,  } = useForm({ defaultValues: { test: "" } });    // isDirty: true  setValue('test', 'change')    // isDirty: false because there getValues() === defaultValues  setValue('test', '')   ``` - File typed input will need to be managed at the app level due to the ability to cancel file selection and [FileList](https://developer.mozilla.org/en-US/docs/Web/API/FileList) object. - Do not support custom object, Class or File object. |
| `formState` | `dirtyFields` | `object` | An object with the user-modified fields. Make sure to provide all inputs' defaultValues via useForm, so the library can compare against the `defaultValues`.   - **Important:** Make sure to provide defaultValues at the useForm, so hook form can have a single source of truth to compare each field's dirtiness. - Dirty fields will **not** represent as `isDirty` formState, because dirty fields are marked field dirty at field level rather the entire form. If you want to determine the entire form state use `isDirty` instead. |
| `formState` | `touchedFields` | `object` | An object containing all the inputs the user has interacted with. |
| `formState` | `defaultValues` | `object` | The value which has been set at [useForm](/docs/useform)'s defaultValues or updated defaultValues via [reset](/docs/useform/reset) API. |
| `formState` | `isSubmitted` | `boolean` | Set to `true` after the form is submitted. Will remain `true` until the `reset` method is invoked. |
| `formState` | `isSubmitSuccessful` | `boolean` | Indicate the form was successfully submitted without any runtime error. |
| `formState` | `isSubmitting` | `boolean` | `true` if the form is currently being submitted. `false` otherwise. |
| `formState` | `isLoading` | `boolean` | `true` if the form is currently loading async default values.  **Important:** this prop is only applicable to async `defaultValues`  Copy  ```  const {  formState: { isLoading }  } = useForm({  defaultValues: async () => await fetch('/api')  }); ``` |
| `formState` | `submitCount` | `number` | Number of times the form was submitted. |
| `formState` | `isValid` | `boolean` | Set to `true` if the form doesn't have any errors.  `setError` has no effect on `isValid` formState, `isValid` will always derived via the entire form validation result. |
| `formState` | `isValidating` | `boolean` | Set to `true` during validation. |
| `formState` | `validatingFields` | `object` | Capture fields which are getting async validation. |
| `formState` | `errors` | `object` | An object with field errors. There is also an [ErrorMessage](/docs/useformstate/errormessage) component to retrieve error message easily. |
| `formState` | `disabled` | `boolean` | Set to `true` if the form is disabled via the `disabled` prop in [useForm](/docs/useform#disabled). |

## Examples

TextFieldCheckboxes

JSTSCopy [CodeSandbox JS](https://codesandbox.io/s/usecontroller-i0ywh)

```
import { TextField } from "@material-ui/core";

import { useController, useForm } from "react-hook-form";

function Input({ control, name }) {

const {

field,

fieldState: { invalid, isTouched, isDirty },

formState: { touchedFields, dirtyFields }

} = useController({

name,

control,

rules: { required: true },

});

return (

<TextField

onChange={field.onChange} // send value to hook form

onBlur={field.onBlur} // notify when input is touched/blur

value={field.value} // input value

name={field.name} // send down the input name

inputRef={field.ref} // send input ref, so we can focus on input when error appear

/>

);

}
```

Copy [CodeSandbox TS](https://codesandbox.io/s/usecontroller-checkboxes-99ld4)

```
import * as React from "react";

import { useController, useForm } from "react-hook-form";

const Checkboxes = ({ options, control, name }) => {

const { field } = useController({

control,

name

});

const [value, setValue] = React.useState(field.value || []);

return (

<>

{options.map((option, index) => (

<input

onChange={(e) => {

const valueCopy = [...value];

// update checkbox value

valueCopy[index] = e.target.checked ? e.target.value : null;

// send data to react hook form

field.onChange(valueCopy);

// update local state

setValue(valueCopy);

}}

key={option}

checked={value.includes(option)}

type="checkbox"

value={option}

/>

))}

</>

);

};

export default function App() {

const { register, handleSubmit, control } = useForm({

defaultValues: {

controlled: [],

uncontrolled: []

}

});

const onSubmit = (data) => console.log(data);

return (

<form onSubmit={handleSubmit(onSubmit)}>

<section>

<h2>uncontrolled</h2>

<input {...register("uncontrolled")} type="checkbox" value="A" />

<input {...register("uncontrolled")} type="checkbox" value="B" />

<input {...register("uncontrolled")} type="checkbox" value="C" />

</section>

<section>

<h2>controlled</h2>

<Checkboxes

options={["a", "b", "c"]}

control={control}

name="controlled"

/>

</section>

<input type="submit" />

</form>

);

}
```

## Tips

- It's important to be aware of each prop's responsibility when working with external controlled components, such as MUI, AntD, Chakra UI. Its job is to spy on the input, report, and set its value.

  - **onChange**: send data back to hook form
  - **onBlur**: report input has been interacted (focus and blur)
  - **value**: set up input initial and updated value
  - **ref**: allow input to be focused with error
  - **name**: give input an unique name

  It's fine to host your state and combined with `useController`.

  Copy [CodeSandbox TS](https://codesandbox.io/s/usecontroller-own-state-wncet2?file=/src/App.tsx)

  ```
  const { field } = useController();

  const [value, setValue] = useState(field.value);

  onChange={(event) => {

  field.onChange(parseInt(event.target.value)) // data send back to hook form

  setValue(event.target.value) // UI state

  }}
  ```
- Do not `register` input again. This custom hook is designed to take care of the registration process.

  Copy

  ```
  const { field } = useController({ name: 'test' })

  <input {...field} /> // ✅

  <input {...field} {...register('test')} /> // ❌ double up the registration
  ```
- It's ideal to use a single `useController` per component. If you need to use more than one, make sure you rename the prop. May want to consider using `Controller` instead.

  Copy

  ```
  const { field: input } = useController({ name: 'test' })

  const { field: checkbox } = useController({ name: 'test1' })

  <input {...input} />

  <input {...checkbox} />
  ```

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub
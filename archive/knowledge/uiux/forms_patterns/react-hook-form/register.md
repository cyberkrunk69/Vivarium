# register

Source: https://react-hook-form.com/docs/useform/register

---

## </> `register:` `(name: string, options?: RegisterOptions) => ({ ref, name, onChange, onBlur })`

This method allows you to register an input or select element and apply validation rules to React Hook Form. Validation rules are all based on the HTML standard and also allow for custom validation methods.

### Props

---

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Input's name. |
| `options` | RegisterOptions | Input's behavior. |

### Return

---

| Name | Type | Description |
| --- | --- | --- |
| `ref` | React.ref | React element ref used to connect hook form to the input. |
| `name` | string | Input's name being registered. |
| `onChange` | ChangeHandler | `onChange` prop to subscribe the input change event. |
| `onBlur` | ChangeHandler | `onBlur` prop to subscribe the input blur event. |

**NOTE**

This is how submitted values will look like:

| Input Name | Submit Result |
| --- | --- |
| register("firstName") | `{ firstName: value }` |
| register("name.firstName") | `{ name: { firstName: value } }` |
| register("name.firstName.0") | `{ name: { firstName: [ value ] } }` |

### Options

---

By selecting the register option, the API table below will get updated.

validationvalidation and error message

| Name | Description |
| --- | --- |
| `ref`  ``` React.Ref ``` | React element `ref` |
| `required`  ``` boolean ``` | Indicates that the input must have a value before the form can be submitted.  **Note:** This config aligns with web constrained API for required input validation, for object or array type of input use validate function instead. |
| `maxLength`  ``` number ``` | The maximum length of the value to accept for this input. |
| `minLength`  ``` number ``` | The minimum length of the value to accept for this input. |
| `max`  ``` number ``` | The maximum value to accept for this input. |
| `min`  ``` number ``` | The minimum value to accept for this input. |
| `pattern`  ``` RegExp ``` | The regex pattern for the input.  **Note:** `RegExp` with the `/g` flag keeps track of the last index where a match occurred. |
| `validate`  ``` Function | Record<string, Function> ``` | Validate function will be executed on its own without depending on other validation rules included in the required attribute.  **Note:** for object or array input data, it's recommended to use the validate function for validation as the other rules mostly apply to string, array of strings, number and boolean. |
| `valueAsNumber`  ``` boolean ``` | Returns `Number` normally. If something goes wrong `NaN` will be returned.   - `valueAs` process is happening **before** validation. - Only applies to number input, but without any data manipulation. - Does not transform `defaultValue` or `defaultValues`. |
| `valueAsDate`  ``` boolean ``` | Returns `Date` normally. If something goes wrong `Invalid Date` will be returned.   - `valueAs` process is happening **before** validation. - Only applies to input. - Does not transform `defaultValue` or `defaultValues`. |
| `setValueAs`  ``` <T>(value: any) => T ``` | Return input value by running through the function.   - `valueAs` process is happening **before** validation. Also, `setValueAs` is ignored if either `valueAsNumber` or `valueAsDate` are true. - Only applies to text input. - Does not transform `defaultValue` or `defaultValues`. |
| `disabled`  ``` boolean = false ``` | Set `disabled` to `true` will lead input value to be `undefined` and input control to be disabled.   - `disabled` prop will also omit built-in validation rules. - For schema validation, you can leverage the `undefined` value returned from input or context object. |
| `onChange`  ``` (e: SyntheticEvent) => void ``` | `onChange` function event to be invoked in the change event. |
| `onBlur`  ``` (e: SyntheticEvent) => void ``` | `onBlur` function event to be invoked in the blur event. |
| `value`  ``` unknown ``` | Set up `value` for the registered input. This prop should be utilised inside `useEffect` or invoke once, each re-run will update or overwrite the input value which you have supplied. |
| `shouldUnregister`  ``` boolean ``` | Input will be unregistered after unmount and `defaultValues` will be removed as well.  **Note:** this prop should be avoided when using with `useFieldArray` as unregister function gets called after input unmount/remount and reorder. |
| `deps`  ``` string | string[] ``` | Validation will be triggered for the dependent inputs, it only limited to register api not trigger. |

| Name | Description |
| --- | --- |
| `ref`  ``` React.Ref ``` | React element `ref` |
| `required`  ``` string | {   value: boolean,   message: string } ``` | Indicates that the input must have a value before the form can be submitted.   **Note:** This config aligns with web constrained API for required input validation, for object or array type of input use validate function instead. |
| `maxLength`  ``` {   value: number,   message: string } ``` | The maximum length of the value to accept for this input. |
| `minLength`  ``` {   value: number,   message: string } ``` | The minimum length of the value to accept for this input. |
| `max`  ``` {   value: number,   message: string } ``` | The maximum value to accept for this input. |
| `min`  ``` {   value: number,   message: string } ``` | The minimum value to accept for this input. |
| `pattern`  ``` {   value: RegExp,   message: string } ``` | The regex pattern for the input.  **Note:** `RegExp` with the `/g` flag keeps track of the last index where a match occurred. |
| `validate`  ``` Function | Record<string, Function> ``` | Validate function will be executed on its own without depending on other validation rules included in the required attribute.  **Note:** for object or array input data, it's recommended to use the validate function for validation as the other rules mostly apply to string, array of strings, number and boolean. |
| `valueAsNumber`  ``` boolean ``` | Returns `Number` normally. If something goes wrong `NaN` will be returned.   - `valueAs` process is happening **before** validation. - Only applies to number input, but without any data manipulation. - Does not transform `defaultValue` or `defaultValues`. |
| `valueAsDate`  ``` boolean ``` | Returns `Date` normally. If something goes wrong `Invalid Date` will be returned.   - `valueAs` process is happening **before** validation. - Only applies to input. - Does not transform `defaultValue` or `defaultValues`. |
| `setValueAs`  ``` <T>(value: any) => T ``` | Return input value by running through the function.   - `valueAs` process is happening **before** validation. Also, `setValueAs` is ignored if either `valueAsNumber` or `valueAsDate` are true. - Only applies to text input. - Does not transform `defaultValue` or `defaultValues`. |
| `disabled`  ``` boolean = false ``` | Set `disabled` to `true` will lead input value to be `undefined` and input control to be disabled.   - `disabled` prop will also omit built-in validation rules. - For schema validation, you can leverage the `undefined` value returned from input or context object. |
| `onChange`  ``` (e: SyntheticEvent) => void ``` | `onChange` function event to be invoked in the change event. |
| `onBlur`  ``` (e: SyntheticEvent) => void ``` | `onBlur` function event to be invoked in the blur event. |
| `value`  ``` unknown ``` | Set up `value` for the registered input. This prop should be utilised inside `useEffect` or invoke once, each re-run will update or overwrite the input value which you have supplied. |
| `shouldUnregister`  ``` boolean ``` | Input will be unregistered after unmount and `defaultValues` will be removed as well.  **Note:** this prop should be avoided when using with `useFieldArray` as unregister function gets called after input unmount/remount and reorder. |
| `deps`  ``` string | string[] ``` | Validation will be triggered for the dependent inputs, it only limited to register api not trigger. |

**RULES**

- Name is **required** and **unique** (except native radio and checkbox).
  Input name supports both dot and bracket syntax, which allows you to easily
  create nested form fields.
- Name can neither start with a number nor use number as key name. Please
  avoid special characters as well.
- We are using dot syntax only for typescript usage consistency, so bracket `[]`
  will not work for array form value.

  ```
  register('test.0.firstName'); // ✅

  register('test[0]firstName'); // ❌
  ```
- Disabled input will result in an undefined form value. If you want to prevent users from updating the input, you can use `readOnly` or `disable` the entire `fieldset`. Here is an [example](https://codesandbox.io/s/react-hook-form-disabled-inputs-oihxx).
- To produce an array of fields, input names should be followed by a dot and number. For example: `test.0.data`
- Changing the name on each render will result in new inputs being registered. It's recommended to keep static names for each registered input.
- Input value and reference will no longer gets removed based on unmount. You can invoke unregister to remove that value and reference.
- Individual register option can't be removed by `undefined` or `{}`. You can update individual attribute instead.

  ```
  register('test', { required: true });

  register('test', {}); // ❌

  register('test', undefined); // ❌

  register('test', { required: false });  // ✅
  ```
- There are certain keyword which need to avoid before conflicting with type check. They are `ref`, `_f`.

**Examples**

---

**Register input or select**

[CodeSandbox JS](https://codesandbox.io/s/register-is0sfo)

```
import { useForm } from "react-hook-form"

export default function App() {

const { register, handleSubmit } = useForm({

defaultValues: {

firstName: "",

lastName: "",

category: "",

checkbox: [],

radio: "",

},

})

return (

<form onSubmit={handleSubmit(console.log)}>

<input

{...register("firstName", { required: true })}

placeholder="First name"

/>

<input

{...register("lastName", { minLength: 2 })}

placeholder="Last name"

/>

<select {...register("category")}>

<option value="">Select...</option>

<option value="A">Category A</option>

<option value="B">Category B</option>

</select>

<input {...register("checkbox")} type="checkbox" value="A" />

<input {...register("checkbox")} type="checkbox" value="B" />

<input {...register("checkbox")} type="checkbox" value="C" />

<input {...register("radio")} type="radio" value="A" />

<input {...register("radio")} type="radio" value="B" />

<input {...register("radio")} type="radio" value="C" />

<input type="submit" />

</form>

)

}
```

**Custom async validation**

```
import { useForm } from "react-hook-form"

import { checkProduct } from "./service"

export default function App() {

const { register, handleSubmit } = useForm()

return (

<form onSubmit={handleSubmit(console.log)}>

<select

{...register("category", {

required: true,

})}

>

<option value="">Select...</option>

<option value="A">Category A</option>

<option value="B">Category B</option>

</select>

<input

type="text"

{...register("product", {

validate: {

checkAvailability: async (product, { category }) => {

if (!category) return "Choose a category"

if (!product) return "Specify your product"

const isInStock = await checkProduct(category, product)

return isInStock || "There is no such product"

},

},

})}

/>

<input type="submit" />

</form>

)

}
```

### Video

---

### Tips

---

#### Destructuring assignment

```
const { onChange, onBlur, name, ref } = register('firstName');

// include type check against field path with the name you have supplied.

<input

onChange={onChange} // assign onChange event

onBlur={onBlur} // assign onBlur event

name={name} // assign name prop

ref={ref} // assign ref prop

/>

// same as above

<input {...register('firstName')} />
```

#### Custom Register

You can also register inputs with `useEffect` and treat them as virtual inputs. For controlled components, we provide a custom hook [useController](/docs/usecontroller) and [Controller](/docs/usecontroller/controller) component to take care this process for you.

If you choose to manually register fields, you will need to update the input value with [setValue](/docs/useform/setvalue).

```
register('firstName', { required: true, min: 8 });

<TextInput onTextChange={(value) => setValue('lastChange', value))} />
```

#### How to work with `innerRef`, `inputRef`?

When the custom input component didn't expose ref correctly, you can get it working via the following.

```
// not working, because ref is not assigned

<TextInput {...register('test')} />

const firstName = register('firstName', { required: true })

<TextInput

name={firstName.name}

onChange={firstName.onChange}

onBlur={firstName.onBlur}

inputRef={firstName.ref} // you can achieve the same for different ref name such as innerRef

/>
```

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub
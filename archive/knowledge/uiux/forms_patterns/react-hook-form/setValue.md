# setValue

Source: https://react-hook-form.com/docs/useform/setvalue

---

## </> `setValue:` (name: string, value: unknown, config?: SetValueConfig) => void

This function allows you to dynamically set the value of a **registered** field and have the options to validate and update the form state. At the same time, it tries to avoid unnecessary rerender.

### Props

---

| Name |  | Description |
| --- | --- | --- |
| `name` string |  | Target a single field or field array by name. |
| `value` unknown |  | The value for the field. This argument is required and can not be `undefined`. |
| `options` | `shouldValidate` boolean | - Whether to compute if your input is valid or not (subscribed to errors). - Whether to compute if your entire form is valid or not (subscribed to isValid). This option will update `touchedFields` at the specified field level not the entire form touched fields. |
|  | `shouldDirty` boolean | - Whether to compute if your input is dirty or not against your `defaultValues` (subscribed to dirtyFields). - Whether to compute if your entire form is dirty or not against your `defaultValues` (subscribed to isDirty). - This option will update `dirtyFields` at the specified field level not the entire form dirty fields. |
|  | `shouldTouch` boolean | Whether to set the input itself to be touched. |

**RULES**

- You can use methods such as [replace](/docs/usefieldarray#replace) or [update](/docs/usefieldarray#update) for field array, however, they will cause the component to unmount and remount for the targeted field array.

  ```
  const { update } = useFieldArray({ name: "array" })

  // unmount fields and remount with updated value

  update(0, { test: "1", test1: "2" })

  // will directly update input value

  setValue("array.0.test1", "1")

  setValue("array.0.test2", "2")
  ```
- The method will not create a new field when targeting a non-existing field.

  ```
  const { replace } = useFieldArray({ name: "test" })

  // ❌ doesn't create new input

  setValue("test.101.data")

  // ✅ work on refresh entire field array

  replace([{ data: "test" }])
  ```
- Only the following conditions will trigger a re-render:

  - When an error is triggered or corrected by a value update.
  - When `setValue` cause state update, such as dirty and touched.
- It's recommended to target the field's name rather than make the second argument a nested object.

  ```
  setValue("yourDetails.firstName", "value") // ✅ performant

  setValue("yourDetails", { firstName: "value" }) ❌ // less performant

  register("nestedValue", { value: { test: "data" } }) // register a nested value input

  setValue("nestedValue.test", "updatedData") // ❌ failed to find the relevant field

  setValue("nestedValue", { test: "updatedData" }) // ✅ setValue find input and update
  ```
- It's recommended to register the input's name before invoking `setValue`. To update the entire `FieldArray`, make sure the `useFieldArray` hook is being executed first.

  **Important:** use `replace` from `useFieldArray` instead, update entire field array with `setValue` will be removed in the next major version.

  ```
  // you can update an entire Field Array,

  setValue("fieldArray", [{ test: "1" }, { test: "2" }]) // ✅

  // you can setValue to a unregistered input

  setValue("notRegisteredInput", "value") // ✅ prefer to be registered

  // the following will register a single input (without register invoked)

  setValue("resultSingleNestedField", { test: "1", test2: "2" }) // 🤔

  // with registered inputs, the setValue will update both inputs correctly.

  register("notRegisteredInput.test", "1")

  register("notRegisteredInput.test2", "2")

  setValue("notRegisteredInput", { test: "1", test2: "2" }) // ✅ sugar syntax to setValue twice
  ```

### Examples

---

**Basic**

[CodeSandbox JS](https://codesandbox.io/s/react-hook-form-v7-ts-setvalue-8z9hx)

```
import { useForm } from "react-hook-form"

const App = () => {

const { register, setValue } = useForm({

firstName: "",

})

return (

<form>

<input {...register("firstName", { required: true })} />

<button onClick={() => setValue("firstName", "Bill")}>setValue</button>

<button

onClick={() =>

setValue("firstName", "Luo", {

shouldValidate: true,

shouldDirty: true,

})

}

>

setValue options

</button>

</form>

)

}
```

**Dependant Fields**

[CodeSandbox TS](https://codesandbox.io/s/dependant-field-dwin1)

```
import * as React from "react"

import { useForm } from "react-hook-form"

type FormValues = {

a: string

b: string

c: string

}

export default function App() {

const { watch, register, handleSubmit, setValue, formState } =

useForm<FormValues>({

defaultValues: {

a: "",

b: "",

c: "",

},

})

const onSubmit = (data: FormValues) => console.log(data)

const [a, b] = watch(["a", "b"])

React.useEffect(() => {

if (formState.touchedFields.a && formState.touchedFields.b && a && b) {

setValue("c", `${a} ${b}`)

}

}, [setValue, a, b, formState])

return (

<form onSubmit={handleSubmit(onSubmit)}>

<input {...register("a")} placeholder="a" />

<input {...register("b")} placeholder="b" />

<input {...register("c")} placeholder="c" />

<input type="submit" />

<button

type="button"

onClick={() => {

setValue("a", "what", { shouldTouch: true })

setValue("b", "ever", { shouldTouch: true })

}}

>

trigger value

</button>

</form>

)

}
```

### Video

---

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub
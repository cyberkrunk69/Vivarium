# watch

Source: https://react-hook-form.com/docs/useform/watch

---

## </> `watch:` UseFormWatch

This method will watch specified inputs and return their values. It is useful to render input value and for determining what to render by condition.

### Overloads

This function mainly serves **two purposes**:

- `watch(name: string, defaultValue?: unknown): unknown`
- `watch(names: string[], defaultValue?: {[key:string]: unknown}): unknown[]`
- `watch(): {[key:string]: unknown}`

The explanation of each of these four overloads follows below.

#### 1-a. Watching single field `watch(name: string, defaultValue?: unknown): unknown`

---

Watch and subscribe to a single field used outside of render.

**Params**

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | the field name |
| `defaultValue` | `unknown` | *optional*. default value for field |

**Returns** the single field value.

```
const name = watch("name")
```

#### 1-b. Watching some fields `watch(names: string[], defaultValue?: {[key:string]: unknown}): unknown[]`

---

Watch and subscribe to an array of fields used outside of render.

**Params**

| Name | Type | Description |
| --- | --- | --- |
| `names` | `string[]` | the field names |
| `defaultValue` | `{[key:string]: unknown}` | *optional*. default values for fields |

**Returns** an array of field values.

```
const [name, name1] = watch(["name", "name1"])
```

#### 1-c. Watching the entire form `watch(): {[key:string]: unknown}`

---

Watch and subscribe to the entire form update/change based on onChange and re-render at the useForm.

**Params** None

**Returns** the entire form values.

```
const formValues = watch()
```

#### 2. **Deprecated:** consider use or migrate to [subscribe](/docs/useform/subscribe). Watching with callback fn `watch(callback: (data, { name, type }) => void, defaultValues?: {[key:string]: unknown}): { unsubscribe: () => void }`

---

Subscribe to field update/change without trigger re-render.

**Params**

| Name | Type | Description |
| --- | --- | --- |
| `callback` | `(data, { name, type }) => void` | callback function to subscribe to all fields changes |
| `defaultValues` | `{[key:string]: unknown}` | *optional*. defaultValues for the entire form |

**Returns** object with `unsubscribe` function.

### Rules

---

- When `defaultValue` is not defined, the first render of `watch` will return `undefined` because it is called before `register`. It's **recommended** to provide `defaultValues` at `useForm` to avoid this behaviour, but you can set the inline `defaultValue` as the second argument.
- When both `defaultValue` and `defaultValues` are supplied, `defaultValue` will be returned.
- This API will trigger re-render at the root of your app or form, consider using a callback or the [useWatch](/docs/usewatch) api if you are experiencing performance issues.
- `watch` result is optimised for render phase instead of `useEffect`'s deps, to detect value update you may want to use an external custom hook for value comparison.

### Examples:

---

#### Watch in a Form

TSJS

Copy [CodeSandbox TS](https://codesandbox.io/s/react-hook-form-watch-v7-ts-8et1d)

```
import { useForm } from "react-hook-form"

interface IFormInputs {

name: string

showAge: boolean

age: number

}

function App() {

const {

register,

watch,

formState: { errors },

handleSubmit,

} = useForm<IFormInputs>()

const watchShowAge = watch("showAge", false) // you can supply default value as second argument

const watchAllFields = watch() // when pass nothing as argument, you are watching everything

const watchFields = watch(["showAge", "age"]) // you can also target specific fields by their names

const onSubmit = (data: IFormInputs) => console.log(data)

return (

<>

<form onSubmit={handleSubmit(onSubmit)}>

<input {...register("name", { required: true, maxLength: 50 })} />

<input type="checkbox" {...register("showAge")} />

{/* based on yes selection to display Age Input*/}

{watchShowAge && (

<input type="number" {...register("age", { min: 50 })} />

)}

<input type="submit" />

</form>

</>

)

}
```

Copy [CodeSandbox JS](https://codesandbox.io/s/react-hook-form-watch-v7-qbxd7)

```
import { useForm } from "react-hook-form"

function App() {

const {

register,

watch,

formState: { errors },

handleSubmit,

} = useForm()

const watchShowAge = watch("showAge", false) // you can supply default value as second argument

const watchAllFields = watch() // when pass nothing as argument, you are watching everything

const watchFields = watch(["showAge", "number"]) // you can also target specific fields by their names

const onSubmit = (data) => console.log(data)

return (

<>

<form onSubmit={handleSubmit(onSubmit)}>

<input type="checkbox" {...register("showAge")} />

{/* based on yes selection to display Age Input*/}

{watchShowAge && (

<input type="number" {...register("age", { min: 50 })} />

)}

<input type="submit" />

</form>

</>

)

}
```

#### Watch in Field Array

TSJS

Copy [CodeSandbox TS](https://codesandbox.io/s/watch-with-usefieldarray-z54xwd)

```
import * as React from "react"

import { useForm, useFieldArray } from "react-hook-form"

type FormValues = {

test: {

firstName: string

lastName: string

}[]

}

function App() {

const { register, control, handleSubmit, watch } = useForm<FormValues>()

const { fields, remove, append } = useFieldArray({

name: "test",

control,

})

const onSubmit = (data: FormValues) => console.log(data)

console.log(watch("test"))

return (

<form onSubmit={handleSubmit(onSubmit)}>

{fields.map((field, index) => {

return (

<div key={field.id}>

<input

defaultValue={field.firstName}

{...register(`test.${index}.firstName`)}

/>

<input

defaultValue={field.lastName}

{...register(`test.${index}.lastName`)}

/>

<button type="button" onClick={() => remove(index)}>

Remove

</button>

</div>

)

})}

<button

type="button"

onClick={() =>

append({

firstName: "bill" + renderCount,

lastName: "luo" + renderCount,

})

}

>

Append

</button>

</form>

)

}
```

Copy [CodeSandbox JS](https://codesandbox.io/s/watch-with-usefieldarray-52yy3z)

```
import * as React from "react"

import { useForm, useFieldArray } from "react-hook-form"

function App() {

const { register, control, handleSubmit, watch } = useForm()

const { fields, remove, append } = useFieldArray({

name: "test",

control,

})

const onSubmit = (data) => console.log(data)

console.log(watch("test"))

return (

<form onSubmit={handleSubmit(onSubmit)}>

{fields.map((field, index) => {

return (

<div key={field.id}>

<input

defaultValue={field.firstName}

{...register(`test.${index}.firstName`)}

/>

<input

defaultValue={field.lastName}

{...register(`test.${index}.lastName`)}

/>

<button type="button" onClick={() => remove(index)}>

Remove

</button>

</div>

)

})}

<button

type="button"

onClick={() =>

append({

firstName: "bill" + renderCount,

lastName: "luo" + renderCount,

})

}

>

Append

</button>

</form>

)

}
```

## Video

---

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub
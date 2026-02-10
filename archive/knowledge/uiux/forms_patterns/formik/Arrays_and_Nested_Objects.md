# Arrays and Nested Objects

Source: https://formik.org/docs/guides/arrays

---

# Arrays and Nested Objects

Formik has support for nested objects and arrays out of the box. These subjects are somewhat related because they both leverage the same syntax.

## Nested Objects

The `name` props in Formik can use lodash-like dot paths to reference nested Formik values. This means that you do not need to flatten out your form's values anymore.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3

4 export const NestedExample = () => (

5   <div>

6     <h1>Social Profiles</h1>

7     <Formik

8       initialValues={{

9         social: {

10           facebook: '',

11           twitter: '',

12         },

13       }}

14       onSubmit={values => {

15         // same shape as initial values

16         console.log(values);

17       }}

18     >

19       <Form>

20         <Field name="social.facebook" />

21         <Field name="social.twitter" />

22         <button type="submit">Submit</button>

23       </Form>

24     </Formik>

25   </div>

26 );
```

## Arrays

Formik also has support for arrays and arrays of objects out of the box. Using lodash-like bracket syntax for `name` string you can quickly build fields for items in a list.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3

4 export const BasicArrayExample = () => (

5   <div>

6     <h1>Friends</h1>

7     <Formik

8       initialValues={{

9         friends: ['jared', 'ian'],

10       }}

11       onSubmit={values => {

12         // same shape as initial values

13         console.log(values);

14       }}

15     >

16       <Form>

17         <Field name="friends[0]" />

18         <Field name="friends[1]" />

19         <button type="submit">Submit</button>

20       </Form>

21     </Formik>

22   </div>

23 );
```

For more information around manipulating (add/remove/etc) items in lists, see the API reference section on the `<FieldArray>` component.

## Avoid nesting

If you want to avoid this default behavior Formik also has support for it to have fields with dots.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3

4 export const NestedExample = () => (

5   <div>

6     <h1>Social Profiles</h1>

7     <Formik

8       initialValues={{

9         'owner.fullname': '',

10       }}

11       onSubmit={values => {

12         // same shape as initial values

13         console.log(values);

14       }}

15     >

16       <Form>

17         <Field name="['owner.fullname']" />

18         <button type="submit">Submit</button>

19       </Form>

20     </Formik>

21   </div>

22 );
```

[PreviousValidation](/docs/guides/validation)[NextTypeScript](/docs/guides/typescript)

Was this page helpful?

![](/twemoji/1f62d.svg)![](/twemoji/1f615.svg)![](/twemoji/1f600.svg)![](/twemoji/1f929.svg)

[Edit this page on GitHub](https://github.com/formik/formik/edit/main/docs/guides/arrays.md)

#### On this page
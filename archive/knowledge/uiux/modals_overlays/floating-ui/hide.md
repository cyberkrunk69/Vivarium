# hide

Source: https://floating-ui.com/docs/hide

---

# hide

A data provider that allows you to hide the floating element in
applicable situations.

*Data Provider*

```
import {hide} from '@floating-ui/dom';
```

This is useful for situations where you want to hide the floating
element because it appears detached from the reference element
(or attached to nothing).

Scroll up

In the above example, the floating element turns partially
transparent once it has `escaped` the reference element’s
clipping context. Once the reference element is hidden, it hides
itself.

## [Usage](#usage)

Apply a hidden visibility style to the floating element based on
the data in `middlewareData.hide`:

```
computePosition(referenceEl, floatingEl, {
  middleware: [hide()],
}).then(({middlewareData}) => {
  if (middlewareData.hide) {
    Object.assign(floatingEl.style, {
      visibility: middlewareData.hide.referenceHidden
        ? 'hidden'
        : 'visible',
    });
  }
});
```

## [Order](#order)

`hide()` should generally be placed at the end of your
middleware array.

## [Options](#options)

These are the options you can pass to `hide()`.

```
interface HideOptions extends DetectOverflowOptions {
  strategy?: 'referenceHidden' | 'escaped';
}
```

### [`strategy`](#strategy)

default: `'referenceHidden'`

The strategy used to determine when to hide the floating element.

```
hide({
  strategy: 'escaped', // 'referenceHidden' by default
});
```

If you’d like to use multiple strategies, call `hide()`
multiple times in your middleware array with different options.

### […detectOverflowOptions](#detectoverflowoptions)

All of [`detectOverflow`](/docs/detectOverflow#options)’s options
can be passed. For instance:

```
hide({
  padding: 5, // 0 by default
});
```

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
hide((state) => ({
  padding: state.rects.reference.width,
}));
```

## [Data](#data)

```
interface Data {
  referenceHidden?: boolean;
  referenceHiddenOffsets?: SideObject;
  escaped?: boolean;
  escapedOffsets?: SideObject;
}
```

Depending on the strategy used, these options may exist in the
data object.

### [`referenceHidden`](#referencehidden)

Determines whether the reference element is fully clipped, and is
therefore hidden from view.

Note that “hidden” means clipping, `visibility` and `opacity`
styles are not considered.

### [`referenceHiddenOffsets`](#referencehiddenoffsets)

A side object containing overflow offsets.

### [`escaped`](#escaped)

Determines whether the floating element has “escaped” the
reference’s clipping context and appears fully detached from it.

### [`escapedOffsets`](#escapedoffsets)

A side object containing overflow offsets.
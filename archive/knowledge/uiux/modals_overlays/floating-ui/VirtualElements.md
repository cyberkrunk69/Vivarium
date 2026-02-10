# VirtualElements

Source: https://floating-ui.com/docs/virtual-elements

---

# Virtual Elements

Position a floating element relative to a custom reference area,
useful for context menus, range selections, following the cursor,
and more.

## [Usage](#usage)

The most basic virtual element is a plain object that has a
`getBoundingClientRect` method, which mimics a real
element’s one:

```
// A virtual element that is 20 x 20 px starting from (0, 0)
const virtualEl = {
  getBoundingClientRect() {
    return {
      x: 0,
      y: 0,
      top: 0,
      left: 0,
      bottom: 20,
      right: 20,
      width: 20,
      height: 20,
    };
  },
};
```

```
computePosition(virtualEl, floatingEl);
```

A point reference, such as a mouse event, is one such use case:

```
function onClick({clientX, clientY}) {
  const virtualEl = {
    getBoundingClientRect() {
      return {
        width: 0,
        height: 0,
        x: clientX,
        y: clientY,
        top: clientY,
        left: clientX,
        right: clientX,
        bottom: clientY,
      };
    },
  };
 
  computePosition(virtualEl, floatingEl).then(({x, y}) => {
    // Position the floating element relative to the click
  });
}
 
document.addEventListener('click', onClick);
```

## [`contextElement`](#contextelement)

This property is useful if your
`getBoundingClientRect` method is derived from a real
element, to ensure clipping and position update detection works
as expected.

```
const virtualEl = {
  getBoundingClientRect() {
    return {
      // ...
    };
  },
  contextElement: document.querySelector('#context'),
};
```

## [`getClientRects`](#getclientrects)

This property is useful when using range selections and the
[`inline`](/docs/inline) middleware.

```
const virtualEl = {
  getBoundingClientRect: () => range.getBoundingClientRect(),
  getClientRects: () => range.getClientRects(),
};
```
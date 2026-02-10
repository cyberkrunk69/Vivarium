# Middleware

Source: https://floating-ui.com/docs/middleware

---

# Middleware

Objects that change the positioning of the floating element,
executed in order as a queue.

Middleware allow you to customize the behavior of the positioning
and be as granular as you want, adding your own custom logic.

`computePosition()` starts with initial positioning via
`placement` — then middleware are executed as an
in-between “middle” step of the initial placement computation and
eventual return of data for rendering.

Each middleware is executed in order:

```
computePosition(referenceEl, floatingEl, {
  placement: 'right',
  middleware: [],
});
```

## [Example](#example)

```
const shiftByOnePixel = {
  name: 'shiftByOnePixel',
  fn({x, y}) {
    return {
      x: x + 1,
      y: y + 1,
    };
  },
};
```

This (not particularly useful) middleware adds `1` pixel to
the coordinates. To use this middleware, add it to your
`middleware` array:

```
computePosition(referenceEl, floatingEl, {
  placement: 'right',
  middleware: [shiftByOnePixel],
});
```

Here, `computePosition()` will compute coordinates that will
place the floating element to the `right` center of the
reference element, lying flush with it.

Middleware are then executed, resulting in these coordinates
getting shifted by one pixel. Then that data is returned for
rendering.

### [Shape](#shape)

A middleware is an object that has a `name` property and a
`fn` property. The `fn` property provides
the logic of the middleware, which returns new positioning
coordinates or useful data.

### [Data](#data)

Any data can be passed via an optional `data` property of
the object that is returned from `fn`. This will be
accessible to the consumer via the `middlewareData` property:

```
const shiftByOnePixel = {
  name: 'shiftByOnePixel',
  fn({x, y}) {
    return {
      x: x + 1,
      y: y + 1,
      data: {
        amount: 1,
      },
    };
  },
};
```

```
computePosition(referenceEl, floatingEl, {
  middleware: [shiftByOnePixel],
}).then(({middlewareData}) => {
  console.log(middlewareData.shiftByOnePixel);
});
```

### [Function](#function)

You may notice that Floating UI’s packaged middleware are
actually functions. This is so you can pass options in, changing
how the middleware behaves:

```
const shiftByAmount = (amount = 0) => ({
  name: 'shiftByAmount',
  options: amount,
  fn: ({x, y}) => ({
    x: x + amount,
    y: y + amount,
  }),
});
```

It returns an object and uses a closure to pass the configured
behavior:

```
const middleware = [shiftByAmount(10)];
```

The `options` key on a middleware object holds the
dependencies, allowing deep comparison reactivity.

### [Always return an object](#always-return-an-object)

Inside `fn` make sure to return an object. It doesn’t
need to contain properties, but to remind you that it should be
pure, you must return an object. Never mutate any values that get
passed in from `fn`.

## [MiddlewareState](#middlewarestate)

An object is passed to `fn` containing useful data
about the middleware lifecycle being executed.

In the previous examples, we destructured `x` and
`y` out of the `fn` parameter object. These
are only two properties that get passed into middleware, but
there are many more.

The properties passed are below:

```
interface MiddlewareState {
  x: number;
  y: number;
  initialPlacement: Placement;
  placement: Placement;
  strategy: Strategy;
  middlewareData: MiddlewareData;
  elements: Elements;
  rects: ElementRects;
  platform: Platform;
}
```

### [`x`](#x)

This is the x-axis coordinate to position the floating element
to.

### [`y`](#y)

This is the y-axis coordinate to position the floating element
to.

### [`elements`](#elements)

This is an object containing the reference and floating elements.

### [`rects`](#rects)

This is an object containing the `Rect`s of the
reference and floating elements, an object of shape
`{width, height, x, y}`.

### [`middlewareData`](#middlewaredata)

This is an object containing all the data of any middleware at
the current step in the lifecycle. The lifecycle loops over the
`middleware` array, so later middleware have access to
data from any middleware run prior.

### [`strategy`](#strategy)

The positioning strategy.

### [`initialPlacement`](#initialplacement)

The initial (or preferred) placement passed in to
`computePosition()`.

### [`placement`](#placement)

The stateful resultant placement. Middleware like
`flip` change `initialPlacement` to a new one.

### [`platform`](#platform)

An object containing methods to make Floating UI work on the
current platform, e.g. DOM or React Native.

## [Ordering](#ordering)

The order in which middleware are placed in the array matters, as
middleware **use** the coordinates that were returned from
previous ones. This means they perform their work based on the
current positioning state.

Three `shiftByOnePixel` in the middleware array means
the coordinates get shifted by 3 pixels in total:

```
const shiftByOnePixel = {
  name: 'shiftByOnePixel',
  fn: ({x, y}) => ({x: x + 1, y: y + 1}),
};
const middleware = [
  shiftByOnePixel,
  shiftByOnePixel,
  shiftByOnePixel,
];
```

If the later `shiftByOnePixel` implementations had a condition
based on the current value of `x` and `y`, the
condition can change based on their placement in the array.

Understanding this can help in knowing which order to place
middleware in, as placing a middleware before or after another
can produce a different result.

In general, `offset()` should always go at the beginning of
the middleware array, while `arrow()` and `hide()` at
the end. The other core middleware can be shifted around
depending on the desired behavior.

```
const middleware = [
  offset(),
  // ...
  arrow({element: arrowElement}),
  hide(),
];
```

## [Resetting the lifecycle](#resetting-the-lifecycle)

There are use cases for needing to reset the middleware lifecycle
so that other middleware perform fresh logic.

- When `flip()` and `autoPlacement()` change the
  placement, they reset the lifecycle so that other middleware
  that modify the coordinates based on the current
  `placement` do not perform stale logic.
- `size()` resets the lifecycle with the newly applied
  dimensions, as many middleware read the dimensions to perform
  their logic.
- `inline()` resets the lifecycle when it changes the
  reference rect to a custom implementation, similar to a
  [Virtual Element](/docs/virtual-elements).

In order to do this, add a `reset` property to the
returned object from `fn`.

```
type Reset =
  | true
  | {
      placement?: Placement;
      // `true` will compute the new `rects` if the
      // dimensions were mutated. Otherwise, you can
      // return your own new rects.
      rects?: true | ElementRects;
    };
```

```
const middleware = {
  name: 'middleware',
  fn() {
    if (someCondition) {
      return {
        reset: {
          placement: nextPlacement,
        },
      };
    }
 
    return {};
  },
};
```

Data supplied to `middlewareData` is preserved by doing
this, so you can read it at any point after you’ve reset the
lifecycle.
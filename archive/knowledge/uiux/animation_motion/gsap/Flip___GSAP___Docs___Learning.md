# Flip | GSAP | Docs & Learning

Source: https://gsap.com/docs/v3/Plugins/Flip/

---

On this page

info

Flip involves a whole different way of thinking about animation. Once you get it, you'll be wowed.

Flip plugin lets you seamlessly transition between two states even if there are sweeping changes to the structure of the DOM that would normally cause elements to jump.

Flip records the current position/size/rotation of your elements, you make whatever changes you want, and then Flip applies offsets to make them ***look*** like they never moved... Lastly FLIP animates the **removal** of those offsets! UI transitions become remarkably simple to code. Flip does all the heavy lifting.

## What people are saying:

> *Experimenting more with GSAP's flip plugin and I'm blown away by how much this accelerates development! What a powerful tool!*ðª*"* - Manoela Ilic, Codrops

> *"HOW DOES IT KNOW WHAT TO DO?* ð¤¯*"* - @georgedoescode

> *"I'm truly amazed at the power of GSAP and FLIP."* - @Alex.Marti

> *"My 'Wow' of the week goes to the Flip Plugin. Star-struck. It's soooo smart!"* - @PeHaa

## Video[â](#video "Direct link to Video")

Detailed walkthrough

Of course like all GreenSock tools, there's a rich API for finessing effects and getting exactly the look you want.

"**FLIP**" is an animation technique that stands for "**F**irst", "**L**ast", "**I**nvert", "**P**lay" and was coined [by Paul Lewis](https://aerotwist.com/blog/flip-your-animations/). Here's a demo of how it works:

#### loading...

## Features[â](#features "Direct link to Features")

Feature Highlights

- **Nested transforms? No problem!** Most FLIP libraries only calculate basic offsets assuming no transforms beyond x/y, so a scaled parent breaks things. Rotations certainly aren't allowed. GSAP's Flip plugin **just works**!
- Set `absolute: true` to **make elements use `position: absolute` during the flip**. This solves layout challenges with flexbox, grid, etc. You can even define a subset of targets, like `absolute: ".box"`
- One flip can handle **multiple elements** and even stagger them.
- **Resize via width/height properties** (default) **or scaleX/scaleY** (`scale: true`)
- You get the **full power of GSAP under the hood**, so you can use any `ease`, define special properties like `onComplete`, `onUpdate`, `repeat`, `yoyo`, and even `add()` other animations with total control of timing, etc.

**read more...**

- **Apply a CSS class during the flip with `toggleClass`**. It'll be removed at the end of the flip.
- **[Flip.fit()](/docs/v3/Plugins/Flip/static.fit()) repositions/resizes one element to fit perfectly on top another (or even a previous state of the same element)**.
- **Compensate for nested offsets**. If a container element is getting flipped along with some of its children, set `nested: true` to prevent the offsets from compounding.
- **Smoothly handles interruptions**.
- **Flip one element to another**; even have them cross-fade (`fade: true`). Just give them the same `data-flip-id` attribute to correlate them.
- **`onEnter` and `onLeave` callbacks** for when elements enter or leave (like if the flip senses a `display: none` toggle and there's no matching target to swap), making it easy to elegantly animate on/off elements.
- **Batch** multiple Flip animations so they don't step on each other's toes, like in a React app with multiple independent components that need to work together.

## How does Flip work?[â](#how-does-flip-work "Direct link to How does Flip work?")

There are typically 3 steps to a "FLIP" animation:

1. ### Get the current state[â](#get-the-current-state "Direct link to Get the current state")

   ```
   // returns a state object containing data about the elements' current position/size/rotation in the viewport  
   const state = Flip.getState(".targets");
   ```

   This merely captures some data about the current state. Use selector text, an Element, an Array of Elements, or NodeList. [Flip.getState()](/docs/v3/Plugins/Flip/static.getState()) doesn't alter anything (unless there's an active flip animation affecting any of the targets in which case it will force it to completion to capture the final state accurately). By default, Flip only concerns itself with position, size, rotation, and skew. If you want your Flip animations to affect other CSS properties, you can define a configuration object with a comma-delimited list of `props`, like:

   ```
   // record some extra properties (optional)  
   const state = Flip.getState(".targets", { props: "backgroundColor,color" });
   ```
2. ### Make your state changes[â](#make-your-state-changes "Direct link to Make your state changes")

   Perform DOM edits, styling updates, add/remove classes, or whatever is necessary to get things in their final state. There's no need to do that through the plugin (unless you're [batching](/docs/v3/Plugins/Flip/static.batch())). For example, we'll toggle a class:

   ```
   // make state changes. We'll toggle a class, for example:  
   element.classList.toggle("full-screen");
   ```
3. ### Call `Flip.from(state, options)`[â](#call-flipfromstate-options "Direct link to call-flipfromstate-options")

   Flip will look at the `state` object, compare the recorded positions/sizes to the current ones, immediately reposition/resize them to *appear* where they were in that previous state, and then animate the *removal* of those offsets. You can specify almost any standard tween special properties like `duration`, `ease`, `onComplete`, etc. [Flip.from()](/docs/v3/Plugins/Flip/static.from()) returns a timeline that you can `add()` things to or control in any way:

   ```
   // animate from the previous state to the current one:  
   Flip.from(state, {  
     duration: 1,  
     ease: "power1.inOut",  
     absolute: true,  
     onComplete: myFunc,  
   });
   ```

   ***That's it!***

## Simple example[â](#simple-example "Direct link to Simple example")

#### loading...

## Flex example[â](#flex-example "Direct link to Flex example")

#### loading...

## Advanced example[â](#advanced-example "Direct link to Advanced example")

#### loading...

## **Config Object**[â](#config-object "Direct link to config-object")

The [Flip.from()](/docs/v3/Plugins/Flip/static.from()) options object (2nd parameter) can contain any of the following optional properties **in addition to any standard tween properties like `duration`, `ease`, `onComplete`**, etc. as described [here](/docs/v3/GSAP/gsap.to()):

### Property

### Description

- #### absolute

  Boolean | String | Array | NodeList | Element - specifies which of the targets should have `position: absolute` applied during the course of the FLIP animation. If `true`, **all** of the targets are affected, or use selector text like `".box"` (or an Array/NodeList of Elements, or even a single Element) to specify a subset of the targets. This can solve layout challenges with flex and grid layouts, for example. If things aren't behaving in a seamless way, try setting `absolute: true`. Beware, that `position: absolute` removes the elements from document flow, so things below can collapse. In that case, just define a subset that doesn't include the container element so it props the layout open. *(added in 3.9.0)*
- #### absoluteOnLeave

  Boolean - if `true`, any "leaving" Elements (ones passed to the `onLeave()`) will be set to `position: absolute` during the flip animation. This can be very useful when you set elements to `display: none` to hide them in the final state, but you want to animate them out (fade, scale, whatever). It's critical that they not affect layout but you still want them visible during the animation. *(added in 3.9.0)*
- #### fade

  Boolean - by default, if the target element associated with a particular `data-flip-id` in the previous state is a **different element** than the one with the same `data-flip-id` in the end state, it will get swapped immediately but if you'd prefer that they cross-fade, set `fade: true`. Again, this only applies when swapping elements. If the "swapping out" (leaving) element is `display: none` (CSS), obviously it won't be visible for fading but if you set the Flip to `absolute: true`, it will force the element to the previous display state *during* the flip so that it can cross-fade. The reason `absolute: true` is necessary in this case is because otherwise the element would affect document flow and throw off the positioning of other elements but if it is `position: absolute` (CSS), it's removed from the document flow and won't contaminate positioning.
- #### nested

  Boolean - if the Flip has any *nested* targets (like a parent and its child are both in the `targets`), set `nested: true` to have Flip perform extra calculations to prevent those movements from compounding. A parent's movement affects its children, so if both are mapped to end up 200px from their original position and Flip moves them both 200px, the child would end up moving 400px unless `nested: true` is set.
- #### onEnter

  Function - A callback that's called if/when a target either isn't found in the original `state` or it was not in the document flow in that original state (like `display: none`), but it *IS* in the document flow in the **end** state. Since there is no position/size data to compare to in the original state, it won't be included in the flip animation, but the callback receives an Array of the entering elements as a parameter so that you can animate them as you please (like fade them in). Any animation returned by this callback will get added to the flip timeline so that it gets forced to completion if a competing flip interrupts it. For example: 

  ```
  onEnter: elements => gsap.fromTo(elements, {opacity: 0}, {opacity: 1})
  ```
- #### onLeave

  Function - A callback that's called if/when a target is in the original `state` but not the end state, or if it isn't in the document flow in the end state (like `display: none`). Since there is no position/size data to compare to in the end state, it won't be included in the flip animation, but the callback receives an Array of the leaving elements as a parameter so that you can animate them as you please (like fade them out). **IMPORTANT:** these elements won't be visible unless you also set `absolute: true` (otherwise, it'd throw off document flow). If `absolute: true` is set, it will force `display` to whatever it was in the previous state and then revert it back at the end of the flip. Any animation returned by this callback will get added to the flip timeline so that it gets forced to completion if a competing flip interrupts it. For example:

  ```
  onLeave: elements => gsap.fromTo(elements, {opacity: 1}, {opacity: 0})
  ```
- #### props

  String - a comma-delimited list of *camelCased* CSS properties that should be included in the flip animation beyond the standard positioning/size/rotation/skew ones. For example, `"backgroundColor,color"`. This will only work, however, if the props exist in the `state` object (first parameter) because otherwise there's no corresponding data to pull from. By default, Flip will use the `props` that were captured in the state with [Flip.getState(targets, props)](/docs/v3/Plugins/Flip/static.getState()), so it's very rare that you'd need to define `props` in [Flip.from()](/docs/v3/Plugins/Flip/static.from()). It's only useful if you want to *LIMIT* them to a subset of the ones captured in the state.
- #### prune

  Boolean - if `true`, Flip will remove any targets from the animation that match the previous state (position/size) in order to conserve resources. This requires a little more processing up-front, but it may improve performance during the animation when several get removed, plus it also makes staggering more intuitive since you may not want non-animating targets to be factored into the staggering. *(added in 3.9.0)*
- #### scale

  Boolean - by default, Flip will affect the `width` and `height` CSS properties to alter the size, but if you'd rather scale the element instead (typically better performance), set `scale: true`.
- #### simple

  Boolean - if `true`, Flip will skip the extra calculations that would be necessary to accommodate rotation/scale/skew in determining positions. It's like telling Flip *"I promise that there aren't any rotated/scaled/skewed containers for the Flipping elements"* which makes things **faster**. In most cases, the performance difference isn't noticeable, but if you're flipping a lot of elements it can help keep things snappy.
- #### spin

  Boolean | Number | Function - 

  if `true`, the elements will spin an extra 360 degrees during the flip animation which makes it look a little more fun. Or you can define a **number** of full rotations, including a negative number, so `-1` would spin in the opposite direction once. If you provide a **function**, it will be called once for each target so that you can return whatever value you'd like for each individual element's spin. This allows you to, for example, have certain targets spin one direction, other elements spin another direction, or return 0 to not spin at all. Sample code: ...

   

  ```
  Flip.from(state, {  
    spin: (index, target) => {  
      if (target.classList.contains("clockwise")) {  
        return 1;  
      } else if (target.classList.contains("counter-clockwise")) {  
        return -1;  
      } else {  
        return 0;  
      }  
    },  
  })
  ```
- #### targets

  String | Element | Array | NodeList - by default, Flip will use the targets from the `state` object (first parameter), but you can specify a subset of those as either selector text (`".class, #id"`), an Element, an Array of Elements, or a NodeList. If any of the targets provided is NOT found in the `state` object, it will be passed to the `onEnter` and *not* included in the flip animation because there's no previous state from which to pull position/size data.
- #### toggleClass

  String - adds a CSS class to the targets while the flip animation is in progress. For example `"flipping"`.
- #### zIndex

  Number - immediately sets the zIndex CSS property to this value for the entire course of the flip animation and then reverts at the end. This makes it easy to ensure that your flipping elements are on top of other elements during the animation, for example.

## How do I flip between two *different* elements?[â](#how-do-i-flip-between-two-different-elements "Direct link to how-do-i-flip-between-two-different-elements")

Flip looks for a `data-flip-id` attribute on every element it interacts with (via [Flip.getState()](/docs/v3/Plugins/Flip/static.getState()) or [Flip.from()](/docs/v3/Plugins/Flip/static.from()), etc.) and if one isn't found, Flip assigns an incremented one automatically ("auto-1", "auto-2", etc.). It lets you correlate targets (the target with the `data-flip-id` of `"5"` in the "from" state gets matched up with the target with a `data-flip-id` of `"5"` in the end state). The `data-flip-id` can be any string, not just a number.

So if you want to flip between two different targets, make sure the data-flip-id attribute in the end state matches the one in the "from" state. When Flip sees that there are two with the same value in the from/end state, it will automatically figure out which one is disappearing (typically with `display: none`) and base things off of that to "swap" the elements. If you want them to crossfade, simply set `fade: true`, otherwise they'll immediately swap. And it is typically best to set `absolute: true` so that when Flip alters the `display` value, it doesn't affect the document flow.

#### loading...

## Batching[â](#batching "Direct link to Batching")

What if you need to create **multiple** coordinated Flip animations (perhaps in various React components)? They'd need to all [.getState()](/docs/v3/Plugins/Flip/static.getState()) *BEFORE* any of them make their changes to the DOM/styling because doing so could alter the position/size of the other elements. See the docs for [Flip.batch()](/docs/v3/Plugins/Flip/static.batch()) for details.

## Caveats & Tips[â](#caveats--tips "Direct link to Caveats & Tips")

warning

- Flip does not accommodate 3D transforms (like rotationX, rotationY, or z).
- It is strongly recommended that you use `box-sizing: border-box` on your elements to ensure accurate width/height calculations.
- When `absolute: true` is set, remember that coordinates will be calculated based on the current viewport, so if the viewport size changes or the user scrolls DURING the flip, it may affect positioning (but once the flip is done and the offsets are removed, things will be where they should be). In other words, in-progress flipping isn't always responsive.
- Set any transform-related values (x, y, scale, rotation, etc.) [directly via GSAP](/resources/mistakes#transforms) whenever possible (instead of just in CSS classes or inline) because GSAP caches transform-related data to supercharge performance and maximize accuracy. To clear GSAP's cache on a particular element (which you'd never need to do if you're making all your changes via GSAP), `gsap.set(element, {clearProps: "transform"});`

 Deep Dive - Using a framework like Vue, React or Angular? 

Beware that frameworks often **DON'T** render changes immediately, so you should wait until the render occurs *before* initiating the [Flip.from()](/docs/v3/Plugins/Flip/static.from()). [Batching](/docs/v3/Plugins/Flip/static.batch()) may be an excellent option because you can `batch.getState(true)` and then perhaps a `useLayoutEffect(() => batch.run(true), [...])` in React. Another hack would be to use requestAnimationFrame() to wait one tick: `requestAnimationFrame(() => Flip.from(...));`

When you `Flip.getState(".your-class")`, it records position/size data for the elements with ".your-class" at that time, remembering **those particular elements** and their `data-flip-id` attribute values. Then, if you `Flip.from(yourState)`, and don't specify any `targets`, it will default to using the elements that were captured in the getState() but your framework may have re-rendered entirely new element instances (even if they look the same), thus they won't animate because Flip doesn't know to look at those new elements. The original ones were completely removed from the DOM, hence the need to tell the Flip *"use these new targets and search the state object for the IDs that match..."*. So make sure you define `targets` like this:

```
// BAD  
Flip.from(state, {  
  duration: 1,  
});  
  
// GOOD  
Flip.from(state, {  
  targets: ".your-class", // <-- BINGO!  
  duration: 1,  
});
```

And don't forget that you'll probably need to set a `data-flip-id` on those elements to make sure Flip knows which target matches up with which one from the captured state.

## **Methods**[â](#methods "Direct link to methods")

|  |  |
| --- | --- |
| [Flip.batch](/docs/v3/Plugins/Flip/static.batch())( id:String ) : FlipBatch | Coordinates the creation of multiple Flip animations in the properly sequenced set of steps to avoid cross-contamination. |
| [Flip.fit](/docs/v3/Plugins/Flip/static.fit())( targetToResize:String | Element, destinationTargetOrState:String | Element | FlipState, vars:Object ) ; | Repositions/resizes one element so that it appears to fit exactly into the same area as another element. Using the `fitChild` special property, you can even scale/reposition an element so that one if its *child* elements is used for the fitting calculations instead! By default it alters the transforms (x, y, rotation, and skewX) as well as the width and height of the element, but if you set `scale: true` it will use scaleX and scaleY instead of width and height. |
| [Flip.from](/docs/v3/Plugins/Flip/static.from())( state:FlipState, vars:Object ) : Timeline | Immediately moves/resizes the targets to match the provided `state` object, and then animates backwards to remove those offsets to end up at the current state. By default, `width` and `height` properties are used for the resizing, but you can set `scale: true` to scale instead (transform). It returns a timeline animation, so you can control it or add() other animations. |
| [Flip.getState](/docs/v3/Plugins/Flip/static.getState())( targets:String | Element | Array, vars:Object ) : Object | Captures information about the current state of the `targets` so that they can be Flipped later. By default, this information includes the dimensions, rotation, skew, opacity, and the position of the targets in the viewport. Other properties can be captured by configuring the `vars` parameter. |
| [Flip.isFlipping](/docs/v3/Plugins/Flip/static.isFlipping())( target:String | Element ) : Boolean | Returns `true` if the given target is currently being Flipped. Otherwise returns `false`. |
| [Flip.killFlipsOf](/docs/v3/Plugins/Flip/static.killFlipsOf())( targets:String | Array | NodeList | Element, complete:boolean ) ; | Immediately kills the Flip animation associated with any of the targets provided. |
| [Flip.makeAbsolute](/docs/v3/Plugins/Flip/static.makeAbsolute())( targets:String | Element | Array | NodeList | FlipState ) : Array | Sets all of the provided target elements to `position: absolute` while retaining their current positioning. |
| [Flip.to](/docs/v3/Plugins/Flip/static.to())( state:FlipState, vars:Object ) : Timeline | Identical to [Flip.from()](/docs/v3/Plugins/Flip/static.from()) except inverted, so this would animate **to** the provided state (from the current one). |

## **Demos**[â](#demos "Direct link to demos")

Check out the full collection of [How-to demos](https://codepen.io/collection/4a605f253549434210c139fa331704cb) and our favourite [inspiring community demos](https://codepen.io/collection/d725bcacb2f44bbdf0f44718f7ebbf55) on CodePen.

## Contents

- [Video](#video)
- [Features](#features)
- [How does Flip work?](#how-does-flip-work)
  - [Get the current state](#get-the-current-state)
  - [Make your state changes](#make-your-state-changes)
  - [Call `Flip.from(state, options)`](#call-flipfromstate-options)
- [Simple example](#simple-example)
- [Flex example](#flex-example)
- [Advanced example](#advanced-example)
- [**Config Object**](#config-object)
- [How do I flip between two *different* elements?](#how-do-i-flip-between-two-different-elements)
- [Batching](#batching)
- [Caveats & Tips](#caveats--tips)
- [**Methods**](#methods)
- [**Demos**](#demos)
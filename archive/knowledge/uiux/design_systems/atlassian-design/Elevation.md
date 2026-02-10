# Elevation

Source: https://atlassian.design/foundations/elevation

---

# Elevation

Elevations are layered surfaces that form the foundation of UI.

![Banner for Elevation page](/static/hero.light-d85ccb7060c6f276474f4824e958d4a20bdd39c1c7b94bfdb3034c41ac2f0bdc.png)

Elevations are the layered surfaces that form the foundation of the UI. They create a blank canvas
where other UI will be placed, such as text, icons, backgrounds, and borders.

![](/f4aed3271e20b0423fbd349472e97fbc/elevation-layers.png)

Most elevations consist of surfaces and shadows. Together, surfaces and shadows give the impression
of lift or depth. Elevations can guide focus through layering, or indicate that the UI can be
scrolled, slid, or dragged.

## Applying elevations

The elevations use [design tokens](https://atlassian.design/tokens/design-tokens) to apply different
surface levels. The highest two elevation surfaces, raised and overlay, are paired with shadows to
create more depth.

![](/44d63d6590027c301eb5ee946e966628/applying-elevations-light.png)

### Elevations in dark theme

Shadows can be harder to see in dark mode, so dark mode elevations also rely on different surface
colors. Imagine that the surfaces are distantly lit from the front — the higher the elevation, the
lighter the surface looks.

![](/0af5348364096744ecb7c559d0f71448/applying-elevations-dark-1.png)

Raised and overlay surfaces are still paired with shadows for added depth and consistency in dark
mode.

![](/1bc0e1a207079167a14fe50bdb958a08/applying-elevations-dark-2.png)

## Types of elevations

There are four basic elevation levels:

1. [Sunken](#sunken)
2. [Default](#default)
3. [Raised](#raised)
4. [Overlay](#overlay)

There is also one "[overflow](#overflow)" elevation for special cases.

### Sunken

Sunken is the lowest elevation available. The sunken surface creates a backdrop (or well) where
other content sits. Columns on a Kanban board are a good example of the sunken elevation.

Only use sunken surfaces on the default surface level. Don’t apply sunken elevations on raised or
overlay elevations. To differentiate areas of the UI in other ways, use whitespace or borders
instead.

![](/90ab780d11a1bab005340c179710bcbe/elevation-sunken-1.png)

#### Using `elevation.surface.sunken` vs `color.background.neutral`

Although `elevation.surface.sunken` and `color.background.neutral` tokens may appear similar in
light mode, they behave differently in dark mode. Here are the main differences between the two:

`elevation.surface.sunken` is an opaque (solid) token that darkens in both light and dark modes. Use
this token as a backdrop to group content or elements together (such as a kanban board) on the
default surface.

![](/5f297d74b73f577681e4442e039979f6/elevation-sunken-2.png)

`color.background.neutral` is a token that uses a transparent color. It darkens in light mode and
lightens in dark mode. Use this token when you need the background to adapt to different elevations,
which is relevant in dark mode since surfaces change depending on what elevation you’re on.

![](/a1c6bd3d190941910f596b6665ebbf00/elevation-sunken-3.png)

### Default

The default elevation is the baseline with respect to all other layers. It represents a flat UI
surface with no visual lift, such as a Confluence page.

Use `elevation.surface` as the starting point for body content when building a UI. To create flat
cards, pair with a border.

![](/4f0bfb7dd130c2b6d273aa8964aa13dc/elevation-surface-1.png)

### Raised

Raised elevations sit slightly higher than default elevations. They are reserved for cards that can
be moved, such as Jira and Trello cards. In special circumstances, they can be used for cards as a
way to provide additional heirarchy or emphasis.

Always pair `elevation.surface.raised` with `elevation.shadow.raised`. This is particularly
important in dark mode, where raised surfaces are lighter to help differentiate elevations.

![](/cd9d38755ac86a080b139bf636b096af/elevation-raised-1.png)

#### Do

Use raised elevations intentionally. If using for emphasis, limit to one section or focal point of the screen.

#### Don’t

Raised elevations can create visual noise, so don’t use to group content when a border or white space would suffice.

### Overlay

Overlay is the highest elevation available. It is reserved for a UI that sits over another UI, such
as modals, dialogs, dropdown menus, floating toolbars, and floating single-action buttons.

Always pair `elevation.surface.overlay` with `elevation.shadow.overlay`. This is important in dark
mode, where overlay surfaces are lighter to help differentiate elevations.

Overlays can stack on top of other overlays.

![](/3921f0bc4c09891e16865f19cf26bf27/elevation-overlay-1.png)

### Overflow

Overflow is a shadow indicating content has [scrolled](#scrolled) outside a view. It can be used for
vertical or horizontal scroll. An example of overflow shadows is the horizontal scroll in tables on
a Confluence page.

![](/b0c9c3dc331c09109beab37d3f868923/elevation-overflow-1.png)

If box shadows are not technically feasible, use the combination of
`elevation.shadow.overflow.spread` and `elevation.shadow.overflow.perimeter` to replicate the
overflow shadow.

## Interaction states

### Hovered and pressed

Elevations use surface color changes to communicate hovered and pressed states. Use the hovered and
pressed elevation tokens to create these visual changes.

![](/22031d7d141b6e350e24a2a3f186adeb/elevation-hovered.png)

Transitions between elevations can be used as an alternative to hovered and pressed tokens, but only
for default and raised elevations (not overlays):

- Transition to overlay elevation on hover
- Transition to raised elevation on press

This approach should be used sparingly to avoid excessive animation. It should not be used for very
small UI, as elevation changes are harder to see than surface color changes at this size.

#### Do

Use the recommended hovered and pressed tokens for interaction states on elevations.

#### Don’t

Don’t combine elevation transitions and hovered and pressed tokens for interactive states. Use one or the other.

#### Background change example

DefaultDefault (bordered)

RaisedOverlay

Styles

`// Default:
Background color: elevation.surface
Hovered background color: elevation.surface.hovered
Pressed background color: elevation.surface.pressed
// Default (bordered):
Background color: elevation.surface
Hovered background color: elevation.surface.hovered
Pressed background color: elevation.surface.pressed
Border: 1px solid color.border
// Raised:
Background color: elevation.surface.raised
Hovered background color: elevation.surface.raised.hovered
Pressed background color: elevation.surface.raised.pressed
Shadow: elevation.shadow.raised
// Overlay
Background color: elevation.surface.overlay
Hovered background color: elevation.surface.overlay.hovered
Pressed background color: elevation.surface.overlay.pressed
Shadow: elevation.shadow.overlay`

Show more

#### Elevation change example

DefaultDefault (bordered)Raised

Styles

`// Default:
Background color: elevation.surface
Hovered background color: elevation.surface.overlay
Pressed background color: elevation.surface.raised
Hovered shadow: elevation.shadow.overlay
Pressed shadow: elevation.shadow.raised
// Default (with border)
Background color: elevation.surface
Hovered background color: elevation.surface.overlay
Pressed background color: elevation.surface.raised
Border: 1px solid color.border
Hovered shadow: elevation.shadow.overlay
Pressed shadow: elevation.shadow.raised
// Raised
Background color: elevation.surface.raised
Hovered background color: elevation.surface.overlay
Pressed background color: elevation.surface.raised
Shadow: elevation.shadow.raised
Hovered shadow: elevation.shadow.overlay
Pressed shadow: elevation.shadow.raised`

Show more

### Dragged

Use the overlay elevation for any UI that is being dragged. Once moved, it returns to its original
elevation.

![](/1febaf074b27ac29440ced9f749954b4/elevation-dragged-1.png)

### Scrolled

When scrollable content exceeds the available area, a border or [overflow](#overflow) shadow can be
applied at the point the content is cut off to indicate there is hidden content that can be scrolled
back into view.

A border is the default approach for scrolled content and can be seen in modal sticky headers and
footers, and top and side navigation.

![](/970641e0961309ee791c5a27bf6347c3/elevation-scrolled.png)

[Overflow](#overflow) shadows are reserved for experiences where a border might be easily missed,
such as in very small UI or tables that use borders to separate cells.

Both approaches should apply the appropriate surface token where the content is being hidden.

## All elevation tokens and values

For the full list of elevation design tokens and their values, see our
[design token reference list](https://atlassian.design/components/tokens/all-tokens). Every token
comes with a description to help you ensure you’re using the correct one.

## Best practices

### Follow the recommended surface and shadow pairings

Raised and overlay elevations have dedicated surface and shadow pairings.

![](/static/pairing-do-4875990101aede1d4740f26c834dd1599b6b1e22ba09176a63f1aa0c008a80ce.png)

#### Do

When creating elevations, always pair matching surface and shadow tokens.

![](/static/pairing-dont-a43d62d77698e3c5da7f71cabddb9efced227f322eabc88e901ba20a8eacd59e.png)

#### Don’t

Don't mix different shadow and surface elevation tokens.

### Replace elevation surfaces with background colors only when required

Elevation surfaces use our
[neutral palettes](https://atlassian.design/foundations/color#neutral-colors). If a different color
is needed, surface tokens can be swapped for any solid background token. When using background
tokens, align to the behavior of
[interaction states for color tokens](https://atlassian.design/foundations/color#interaction-states).

![](/f521c1c5394fedf423a4e637f753adc0/background-colors.png)

### Avoid excessive use of raised and overlay elevations

The shadows and surfaces of raised and overlay elevations can create busy UI if not applied
intentionally. Follow the recommended guidance when considering these elevations.

![](/static/grouping-do-7ec44ede7c54a20ecf95a0d3d3be927a4beb2b00f984919c47c58c00701b8e9a.png)

#### Do

Limit the use of overlay elevations by grouping related buttons together in a floating toolbar if they are required to sit over another UI.

![](/static/grouping-dont-630f50e20def932838c75e7c90541bc897ff5e30985a3fb3dba4de1afb436da5.png)

#### Don’t

Don’t have more than one floating button next to each other.

### Check contrast ratios

Always make sure your elevation and background choices are accessible.

#### Do

Check the contrast ratio for UI on overlay surfaces in dark mode to ensure it meets accessibility requirements.

#### Don’t

Don't assume that because UI is accessible in light mode, it will be in dark mode. Some UI may need tweaking.

## Z-index

The z-index determines the stacking order of elements. Elements with a higher z-index always sit in
front of elements with a lower z-index.

Different UI can have the same elevation style, but each UI should apply a different z-index to
indicate the layer(s) order in a stack (or where the elements touch).

| Z-index | Example usage | Elevation level |
| --- | --- | --- |
| 100 | None | None |
| 200 | [Atlassian navigation](https://atlassian.design/components/atlassian-navigation/) | Default |
| 300 | [Inline dialog](https://atlassian.design/components/inline-dialog/) | Overlay |
| 400 | [Popup](https://atlassian.design/components/popup/) | Overlay |
| 500 | [Blanket](https://atlassian.design/components/blanket/) | None |
| 510 | [Modal](https://atlassian.design/components/modal-dialog/) | Overlay |
| 600 | [Flag](https://atlassian.design/components/flag/) | Overlay |
| 700 | [Spotlight](https://atlassian.design/components/onboarding/) | Overlay |
| 800 | [Tooltip](https://atlassian.design/components/tooltip/) | None |

## Related

- Learn about the basics of [design tokens](https://atlassian.design/tokens/design-tokens).
- See the list of [all design tokens](https://atlassian.design/components/tokens/all-tokens) for
  full descriptions and values for all tokens.

---

##### Was this page helpful?

YesNo

We use this feedback to improve our documentation.
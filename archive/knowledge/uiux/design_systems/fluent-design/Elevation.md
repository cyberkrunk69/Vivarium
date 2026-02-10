# Elevation

Source: https://fluent2.microsoft.design/elevation

---

# Elevation

Elevation is the perceived distance between an object and the surface behind it using shadows and light. Elevate UI elements to create visual cues, aid scannability, and convey levels of importance.

![](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-hero-01.CcJFfP4_.webp&w=1536&h=940&f=png)

---

## Depth, shadow, and light

Fluent interfaces mimic three dimensional space by placing components at different elevations along the z-axis to increase the visual prominence of certain UI elements. This creates a clear hierarchy and sense of focus within an experience.

Elevation uses the interplay of shadow and light to imply the distance between two surfaces and illustrate how far an object appears from the surface behind it.

![Shadow](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-depthshadowandlight-01.DSIuZ5xG.webp&w=1536&h=962&f=png)

![Shadow direction](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-depthshadowandlight-02.0viE1ah5.webp&w=728&h=490&f=png)

Shadow direction

Consistent shadow direction conveys a perceived light source.

![Shadow size](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-depthshadowandlight-03.DXsskPLj.webp&w=728&h=480&f=png)

Shadow size

Just like in the physical world, sharp and crisp shadows indicate closeness to a surface, while larger, softer shadows indicate a greater distance.

---

## Shadow system

Fluent uses a set of equations to generate consistent, cohesive shadows based on any given value. The shadow ramp references increasing blur values to indicate shadow size and, thereby, distance. For example, shadow 2 has 2 pixel blur and shadow 64 has 64 pixel blur. The six shadow types, token values, and use cases are listed in the following elevation tables.

![Shadow system](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsystem-01.DYESe50L.webp&w=1536&h=940&f=png)

Fluent shadows are created by combining sharp, directional shadows (key) to define the edges of an element and soft, diffused shadows (ambient) to imply distance.

![Key shadows and ambient shadows](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsystem-02.DooC1oM-.webp&w=1536&h=860&f=png)

**Platform distinction**

Windows uses strokes instead of key shadows to outline an object.

![Key shadows and storke](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsystem-03.DSL226Kd.webp&w=1536&h=860&f=png)

---

## Low elevation ramp

![Low elevation ramp](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-01.xOb21Bwn.webp&w=1536&h=440&f=png)

Light

**Shadow 1**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 14%

**Shadow 2**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 14%

**Dark**

**Shadow 1**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 28%

**Shadow 2**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 14%

![Light Shadow 2](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-02.BcIy3mcS.webp&w=728&h=480&f=png)

Light Shadow 2

Cards without an edge and floating action buttons when pressed

`$shadow2`

![Dark Shadow 2](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-03.CHF0xIFW.webp&w=728&h=480&f=png)

Dark Shadow 2

Ribbon, icons, and hero buttons

`$shadow2`

![Light Shadow 4](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-04.CTWiWHLQ.webp&w=728&h=480&f=png)

Light Shadow 4

Cards without an edge

`$shadow4`

![Dark Shadow 4](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-05.PbMmAA1x.webp&w=728&h=480&f=png)

**Dark Shadow 4**

Cards, grid items, and list items

`$shadow4`

![Light Shadow 8](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-06.CFH3qgtt.webp&w=728&h=480&f=png)

Light Shadow 8

Floating action buttons, raised cards, and raised app bars

`$shadow8`

![Dark Shadow 8](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-07.B5LPUD1P.webp&w=728&h=480&f=png)

Dark Shadow 8

Command bars, command dropdowns, and tooltips

`$shadow8`

![Light Shadow 16](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-08.DoUtoZkF.webp&w=728&h=480&f=png)

Light Shadow 16

Cards without edge and floating action buttons when pressed

`$shadow16`

![Dark Shadow 16](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-09.Df9mC4w2.webp&w=728&h=480&f=png)

Dark Shadow 16

Callouts and hover cards

`$shadow16`

---

## High elevation ramp

![High elevation ramp](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-01.xOb21Bwn.webp&w=1536&h=440&f=png)

Light

**Shadow 1**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 24%

**Shadow 2**

Blur = 8

X Axis = 0

Y Axis = 0

Opacity = 20%

Dark

**Shadow 1**

Blur = 1 \* n

X Axis = 0

Y Axis = 0.5 \* n

Opacity = 28%

**Shadow 2**

Blur = 2

X Axis = 0

Y Axis = 0

Opacity = 20%

![Light Shadow 28](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-highelevationramp-02.DYucAF9w.webp&w=728&h=480&f=png)

Light Shadow 28

Bottom sheet, side navigation, and raised tab bars

`$shadow28`

![Dark Shadow 28](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-highelevationramp-03.Cvz811dR.webp&w=728&h=480&f=png)

Dark Shadow 28

Bottom sheet, side navigation, and raised tab bars

`$shadow28`

![Light Shadow 64](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-highelevationramp-04.BLvRjLUi.webp&w=728&h=480&f=png)

Light Shadow 64

Pop-up dialogs

`$shadow64`

![Dark Shadow 64](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-lowelevationramp-05.PbMmAA1x.webp&w=728&h=480&f=png)

Dark Shadow 64

Panels and pop-up dialogs

`$shadow64`

[Windows elevation system   
 Learn about how Windows applies elevation](https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/layering "Windows elevation system")

---

## Shadows on color surfaces

To convey the same level of elevation on color surfaces, we adjust the shadows using the luminosity equation. Use the provided brand shadow tokens to apply shadows to colors in an interface.

### Luminosity equation

When compared to neutrals, the same shadow value on brand colors may not give the impression of the same elevation levels. To bring elements to the same level of elevation visually, we use the luminosity equation to calculate the shadow opacity based on the colorâs luminosity.

Use the brand shadow tokens to ensure consistent shadows throughout interfaces.

![Shadows on color surfaces](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsoncolorsurfaces-01.BkNo-Fq2.webp&w=1536&h=440&f=png)

Luminosity

0.2126 \* R + 0.7152 \* G + 0.0722 \* B

Shadow 1 opacity

Round ( 42 - 0.116 \* luminosity )

Â

Â

Shadow 2 opacity

Round ( 34 - 0.09 \* luminosity )

![Adjust shadow opacity based on the luminosity of the surface color](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsoncolorsurfaces-02.AIpGFNIZ.webp&w=728&h=440&f=png)

Adjust shadow opacity based on the luminosity of the surface color

![Donât use the main shadow ramp on colored surfaces](/_image?href=https%3A%2F%2Ffluent2websitecdn.azureedge.net%2Fcdn%2Fdesignlanguage-elevation-shadowsoncolorsurfaces-03.DcgljPfF.webp&w=728&h=440&f=png)

Donât use the main shadow ramp on colored surfaces
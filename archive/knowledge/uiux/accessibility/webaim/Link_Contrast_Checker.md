# Link Contrast Checker

Source: https://webaim.org/resources/linkcontrastchecker/

---

# Link Contrast Checker

You are here: [Home](/) > [Resources](/resources/) > Link Contrast Checker

Link Color

Please enter a valid [hex triplet](http://en.wikipedia.org/wiki/Web_colors#Hex_triplet), or use the color picker.

Hex

color picker

Lightness

Body Text Color

Please enter a valid [hex triplet](http://en.wikipedia.org/wiki/Web_colors#Hex_triplet), or use the color picker.

Hex

color picker

Lightness

Background Color

Please enter a valid [hex triplet](http://en.wikipedia.org/wiki/Web_colors#Hex_triplet), or use the color picker.

Hex

color picker

Lightness

The five [boxing wizards](/) jump quickly.

## Link to Body Text

WCAG A:

## Link to Background

WCAG AA:

## Body Text to Background

WCAG AA:

[permalink](./?fcolor=000000&bcolor=FFFFFF)

WebAIM Accessibility Testing Services

The experts at WebAIM can audit your web site and provide a detailed report to help you remediate accessibility and WCAG compliance issues.

[Learn more about WebAIM Evaluation Services](/services/evaluation)

## Explanation

For usability and accessibility, links should be underlined by default. Otherwise, [link text must have at least 3:1 contrast with surrounding body text](/articles/contrast/#only), and must present a non-color indicator (typically underline) on mouse hover and keyboard focus.

In addition, both links and body text must have at least 4.5:1 contrast with the background (3:1 for large text) to meet WCAG 2 Level AA.

Enter link, body text, and background colors in RGB hexadecimal format (e.g., #FD3 or #F7DA39) or use the color pickers. The Lightness sliders can be used to adjust the selected color. Feedback will be presented for all three required contrast calculations.

To check the contrast of large text, or to check against Level AAA contrast requirements, use [our standard contrast checker](/resources/contrastchecker/).

New!

This tool also functions as a basic API. Simply append `&api` to any permalink to get a JSON object with the contrast ratios. For example: <https://webaim.org/resources/contrastchecker/?fcolor=FF0000&bcolor=FFFFFF&api>.
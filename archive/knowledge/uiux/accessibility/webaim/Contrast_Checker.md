# Contrast Checker

Source: https://webaim.org/resources/contrastchecker/

---

# Contrast Checker

You are here: [Home](/) > [Resources](/resources/) > Contrast Checker

Foreground

Please enter a valid [hex value](http://en.wikipedia.org/wiki/Web_colors#Hex_triplet) (alpha value optional) or use the color picker.

Hex Value

#

Color Picker

Alpha

Lightness

Background

Please enter a valid [hex value](//en.wikipedia.org/wiki/Web_colors#Hex_triplet) or use the color picker.

Hex Value

#

Color Picker

Lightness

Contrast Ratio
[permalink](./?fcolor=0000FF&bcolor=FFFFFF)

## Normal Text

WCAG AA:

WCAG AAA:

The five boxing wizards jump quickly.

## Large Text

WCAG AA:

WCAG AAA:

The five boxing wizards jump quickly.

## Graphical Objects and User Interface Components

WCAG AA:

★

WebAIM Accessibility Testing Services

Web accessibility testing can be difficult! The experts at WebAIM can audit your web site and provide a detailed report to help you remediate accessibility and WCAG compliance issues.

[Learn more about WebAIM Evaluation Services](/services/evaluation)

## Explanation

Enter a foreground and background color in RGB hexadecimal format or choose a color using the Color Picker. Enter an Alpha value to adjust the transparency of the foreground color. Use the Lightness slider to adjust the perceived lightness of the color.

WCAG 2.0 level AA requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text. WCAG 2.1 requires a contrast ratio of at least 3:1 for graphics and user interface components (such as form input borders). WCAG Level AAA requires a contrast ratio of at least 7:1 for normal text and 4.5:1 for large text.

Large text is defined as 14 point (typically 18.66px) and bold or larger, or 18 point (typically 24px) or larger.

**Hint:** Use the eye dropper tool in the Color Picker to extract the color value from any element on screen. Additionally, [WAVE](http://wave.webaim.org/) can analyze contrast ratios for all page text elements at once.

Use [our link contrast checker](/resources/linkcontrastchecker/) to evaluate links that are identified using color alone.

Contrast Checker API and Bookmarklet

This tool also functions as a basic API. Simply append `&api` to any [permalink](./?fcolor=0000FF&bcolor=FFFFFF) to get a JSON object with the contrast ratio and the AA/AAA pass/fail states. For example: <https://webaim.org/resources/contrastchecker/?fcolor=0000FF&bcolor=EEEEEE&api>.

A miniature version of this Contrast Checker can be initiated within any web page by installing and using the [Contrast Checker Bookmarklet](bookmarklet). This tool allows easy contrast testing of any content on your screen by using the foreground and background eyedropper tools.
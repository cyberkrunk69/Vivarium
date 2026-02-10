# Typefaces and Fonts

Source: https://webaim.org/techniques/fonts/

---

# Typefaces and Fonts

You are here: [Home](/) > [Articles](/articles/) > Fonts

## Introduction

![](media/fonts.jpg)

Typefaces are groups of designed text characters, such as Arial, Helvetica, and Times New Roman. Fonts are sub-sets of typefaces that have a consistent appearance, such as a 14 point and bold font in the Arial typeface. Typography—how typefaces and fonts present text—is very impactful on reading, which is a core component of visual accessibility.

This article primarily focuses on typefaces and fonts. To learn more about other aspects of typography and layout, please see [Text/Typographical Layout](/techniques/textlayout/).

## Typeface Readability

When reading text, most people do not read or parse individual characters or even words. Instead, the eye quickly scans through text and parses patterns and groups of characters (typically 6-9 characters at a time) which are nearly instantaneously converted into meaning by the human brain. This subconscious process allows us to read and understand text content very quickly with high degrees of understanding, even though we aren't even seeing or thinking of characters and words.

It is only when characters or words are unfamiliar or introduce a barrier to that direct pattern-to-meaning process that we must pause to more closely examine or process characters or words. For optimal readability and understandability, the key is to avoid those interruptions.

Some principles to consider:

1. Use simple, familiar, and easily-parsed fonts.
2. Avoid character complexity
3. Avoid character ambiguity
4. Use a limited number of typefaces, fonts, and font variations.
5. Consider spacing and weight.
6. Ensure sufficient, but not too much, contrast between the text and the background.
7. Avoid small font sizes and other anti-patterns.

### Use simple, familiar, and easily-parsed fonts

Simple, familiar typefaces are easiest to parse and read because the mind already has or can quickly generate a model for the shapes and patterns of text. Unfamiliar or complex typefaces require additional time and orientation, resulting in character or word parsing (which is slow and cognitively intense) rather than pattern/block parsing (which is fast and less burdensome).

![](media/common_fonts.jpg)**There is not a *best* typeface or font.** Experts disagree on which typefaces provide the best readability. Some people indicate that sans-serif fonts are better for viewing on a screen and serif fonts are better for print, but this is becoming less of a concern due to the prevalence of high resolution displays and higher quality typefaces. Regardless, simplicity in typefaces is critical. The typeface should be familiar or easily-parsed so that it quickly becomes familiar. Many common and standard fonts available in modern operating systems meet these requirements.

Similarly, there is not one typeface that will be optimal for all users with dyslexia.

Typefaces should be chosen to align with the tone, messaging, and brand of the content. A cartoon font used on a bank web site, for example, would likely undermine the sense of trust and professionalism the user expects. Consider the differences between these two logos with the same text, but different typefaces.

![Two logos with text of WebAIM Bank and Trust. We take your money seriously. We promise! The first uses a chalkboard and cartoonish font. The second uses sans-serif fonts that are more common to bank logos.](media/WebAIMbank.png)

Which of these banks would you trust more with your money?

### Avoid character complexity

Simpler shapes and patterns of typographical text are more quickly and accurately analyzed by the human mind. Be careful with complex fonts, especially for long sections of text.

![An illustration of a complex, decorative typeface vs a simpler, serif typeface.](media/complexvssimple.png)

### Avoid character ambiguity

When glyphs or characters within a typeface appear similar to another, this can introduce ambiguity which must be processed by the brain, thus impacting reading speed and understanding.

![An illustration of letter C vs O in different typefaces.](media/ambiguity.png)

The texts above illustrate common ambiguities. The capital letters "C" and "O" and lowercase letters "e" and "o" in the Arial typeface look very similar due to the very narrow opening in the letters. This is contrasted with the wider opening and more distinct differences between "C" and "O" and "e" and "o" in the Open Sans typeface.

![An illustration of capital I vs lowercase l vs number 1 in different typefaces.](media/ambiguity2.png)

Similarly, capital "I", lowercase "l", and numeral "1" appear almost identical in Gill Sans, but are much more easily distinguished from each other in Verdana. Even though Verdana is a bit more complex, this minor complexity helps with disambiguation of characters.

### Use a limited number of typefaces, fonts, and font variations

Each time you encounter a new typeface, font, or font variation, your mind must build a map or model of the characters and patterns to then more quickly parse words and process meaning. This requires cognitive effort and time. If the typeface is already familiar, this overhead is reduced.

![An illustration showing the words 'Each new typeface introduces additional cognitive overhead' in multiple typefaces.](media/multiple.png)

Be cautious when using multiple typefaces in the same document or web page. Ensure that typefaces/fonts align with types of content, such as one typeface or font for headings and another for body text.

### Consider spacing and weight

Adequate letter and word spacing can improve readability by providing greater separation and clarity between adjacent characters and words. When letters or words appear very close to each other, confusion can be introduced.

![An illustration showing very closely spaced characters. Is the word 'cod' or 'cool'?](media/spacing.png)

Additionally, the weight (meaning the thickness of the glyphs) can also impact perceivability and readability.

![An illustration over a very thin/light font weight compared to standard font weight.](media/weight.png)

WCAG Text Spacing

WCAG requires that no loss of content or functionality occurs when the end user overrides page styles for paragraph spacing to 200% of the font size, text line height/spacing to 150% of the font size, word spacing to 16% of the font size, and letter spacing to 12% of the font size. Ensure that your page text can be modified without it disappearing or overlapping other page content.

### Ensure sufficient, but not too much, contrast between the text and the background

Text is much easier to read when there is a sufficient contrast or brightness difference between the text and the background. The [Web Content Accessibility Guidelines](/standards/wcag/checklist) define measures for sufficient text contrast. Tools such as [WebAIM's Color Contrast Checker](/resources/contrastchecker/) make it easy to check contrast and determine WCAG compliance.

![An illustration showing text with too little, too much, and adequate contrasts.](media/contrast.png)

Black text on a white background is the default for web content, but this combination can feel stark and fatiguing, especially for long sections of text. Too much contrast may introduce halos or echos of text characters which can impact readability, especially for some with dyslexia. While WCAG does not have a maximum contrast threshold, you may want to style text with slightly lower contrast. This page, for example, uses a very dark grey body text color on white for slightly reduced contrast.

### Avoid small font sizes and other anti-patterns.

In addition to text spacing, weight, and contrast, the size of text has a significant impact on readability. Although WCAG has no minimum font size requirement, it is still a valid usability consideration.

Relative font sizes (such as percents or ems) provide more flexibility in modifying the visual presentation compared to absolute units (such as pixels or points).

The font size chosen also impacts line length—the number of characters that appear per line. Line length and other text layout considerations are covered in WebAIM's [Text/Typographical Layout article](/techniques/textlayout/#line).

![An illustration showing small, all bold, all italic, and all capitalized texts.](media/antipatterns.png)

Be careful with longer sections of text that are entirely bold, italicized, capitalized, or styled in atypical ways. These font variations can make text more difficult to read—and each new variation requires some orientation by the user.

## Real Text vs. Text Within Graphics

Real text provides many advantages over text within images. When content is presented as real text—meaning rendered a text characters in a web page—it is very adaptable. The user can customize it for better readability, such as by adjusting the line, word, and character spacing, changing the font face, changing text colors, increasing the text size without loss of fidelity, and translating to other languages. Additionally, true text can be copied and pasted, adapts to various screen sizes, is more compatible with search engines and low bandwidth environments, etc.

When text is instead defined within an image, it loses most of that adaptability. The [Web Content Accessibility Guidelines](/standards/wcag/) require that [if the same visual presentation can be made using text alone, an image is not used to present that text.](/standards/wcag/checklist#sc1.4.5)

Text within images can become more pixelated, blocky, and difficult to read when enlarged, such as may be necessary by users with some visual disabilities.

Example

![A pixelated image of the word 'university,' which is difficult to read](media/pixelated.jpg)

The enlarged image of the word "University" above is difficult to read because it has become pixelated.

## Embedded fonts

Modern browsers allow font embedding, a CSS technique that allows the browser to download fonts and then display text in those font faces. While most system-level typefaces are designed for some level of readability, many custom-designed typefaces are not. Care should be taken to use typefaces and fonts that maintain high levels of readability. Simply changing the font face has no impact on screen reader or other types of accessibility, so long as the actual underlying text is maintained in an accessible format.
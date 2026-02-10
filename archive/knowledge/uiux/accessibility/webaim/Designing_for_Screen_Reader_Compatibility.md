# Designing for Screen Reader Compatibility

Source: https://webaim.org/techniques/screenreader/

---

# Designing for Screen Reader Compatibility

You are here: [Home](/) > [Articles](/articles/) > Designing for Screen Reader Compatibility

## Overview

![](media/screen.jpg) Screen readers convert digital text into synthesized speech. They empower users to hear content and navigate with the keyboard. The technology helps people who are blind or who have low vision to use information technology with the same level of independence and privacy as anyone else. Screen readers are also used by people with certain cognitive or learning disabilities, or users who simply prefer audio content over text. Beyond the web, screen readers also work with documents, spreadsheets, and the user’s operating system.

Screen readers read content differently from humans. The voice may sound somewhat robotic and monotone. Experienced users often like to speed up the reading rate to 300 words per minute or more—well beyond what an inexperienced listener can easily understand. It takes time to get used to a screen reader, but once users become accustomed to it, they can race through content at speeds that awe sighted individuals.

## Document Language

Since every language has its own pronunciation rules, the screen reader needs to know which language it should "speak." Web pages specify document language with a `lang` attribute on the `<html>` tag, in order to encompass the entire document. The page you are reading right now uses `<html lang="en">`, with "en" being the code for English. This also facilitates automatic translation of content.

Sometimes text is interspersed with foreign phrases. For example:

> “C’est la vie,” Harold sighed, as he watched his Volvo tumble off the cliff.

In such cases, the `lang` attribute (in this case `lang="fr"`) is typically applied to a `<span>` tag surrounding the other-language content. This flags a temporary departure from the previously-specified document language.

Note

You can learn much more about choosing and implementing proper lang attribute values in the [Document and Content Language](/techniques/language/) article.

## Content Linearization

Audio interfaces present content linearly to users, one item at a time. This contrasts with the way in which most people use visual interfaces. Sighted users can scan an entire screen almost instantaneously, comprehending the overall layout, the artistic style, and other macro-level aspects of the content. Screen reader users cannot comprehend these macro-level aspects as quickly. The linear progression through the content from beginning to end is somewhat like automated telephone menu systems which do not reveal all of the options at once. Users must progress through such systems in a step-wise manner. The insight that audio interfaces are linearized versions of web content is an important one that should guide web developers during the engineering and design process.

## Navigating Content

Despite the linear nature of audio interfaces, screen readers do provide ways for users to navigate content quickly.

### Links and Form Controls

One way is to use the Tab key to jump from link to link. This gives the user an idea of where the page links to, and can be a useful way to run through the content if the user is looking for a specific link. A related technique is to obtain a list of the links on the page, arranged alphabetically. The drawback of these methods is that the user does not hear any of the non-link content, and may miss important information this way. See [http://webaim.org/techniques/hypertext/](../hypertext/).

**Implication:** Links should make sense when read out of context.

### Headings

Another way to get an overall impression of a page's content is to jump from heading to heading. Users can hear an outline of the page's main ideas, then backtrack to read the parts they are most interested in. The main drawback to this technique is that it relies on headings—which too many pages lack. See [http://webaim.org/techniques/semanticstructure/](../semanticstructure/).

**Implication:** Authors should organize content with headings. To the extent possible, the headings should represent an accurate outline of the content.

### Landmarks and page sections

Users can navigate via [ARIA landmarks](/techniques/aria/#landmarks) and HTML5 sectioning elements, such as `<main>`, `<nav>`, `<header>`, etc.

**Implication:** Define appropriate ARIA landmarks and use HTML5 elements appropriately.

### Paragraphs and page elements

Users can jump from paragraph to paragraph, listening to the first sentence or two before moving on to the next paragraph. This technique resembles the way visual users explore the page before focusing on an area of interest. Users can also jump from element to element, such as `<div>` tags, links, form elements, list items, or other units of content.

**Implication:** When possible, place the distinguishing information of a paragraph in the first sentence.

### “Skip navigation” links

[Skip links](/techniques/skipnav/) at the top of the page allow users to bypass the main navigation and go directly to the main content. They speed up the reading process and help users distinguish between the main navigation and the main content.

**Implication:** Where appropriate, allow users to skip over repetitive navigation links.

### Others

In addition to the methods above, screen reader users can also navigate by tables, lists, buttons, forms, links, images, etc.

**Implication:** Use proper HTML [semantic structure](/techniques/semanticstructure/) with elements marked up appropriately.

## Accommodating Differences Between Screen Readers

All screen readers share similar functionality and capabilities. However, keyboard shortcuts, voices, and ways of calling out links, images, and so on, vary between them. Since users will be accustomed to their preferred screen reader’s conventions, these differences don’t typically impact coding practices. The key is to adhere to accessibility standards and generally-accepted accessibility techniques.

## How Screen Readers Read Content

In general:

- Screen readers pause for:
  - periods
  - semi-colons
  - commas
  - question marks
  - exclamation points
  - paragraph endings
- Screen readers try to pronounce acronyms, if there are sufficient vowels/consonants to be pronounceable. Otherwise, they spell out the letters.
  - NASA is pronounced as a word.
  - SQL is pronounced “sequel” even though some humans say “S. Q. L.”
  - NSF is pronounced “N. S. F.”
  - URL is pronounced “U. R. L.”
- Users can pause screen readers and go back to repeat a word or passage. They can even have the screen reader read words letter by letter, with the screen reader shouting/emphasizing the uppercase letters.
- Screen readers read letters out loud as you type them, but say “star” or “asterisk” for password fields.
- Screen readers announce the page title (the `<title>` element in the HTML markup) when first loading a web page.
- Screen readers will read the [alternative text](/techniques/alttext/) of images, if alt text is present. JAWS precedes the alternative text with the word “graphic.” If the image is a link, JAWS precedes the alternative text with “graphic link."
- Screen readers ignore images without alternative text and say nothing, but users can set their preferences to read the file name.
- If an image without alternative text is a link, screen readers will generally read the link destination (the `href` attribute in the HTML markup) or may read the image file name.
- Screen readers announce [headings and identify the heading level](/techniques/semanticstructure/). NVDA and JAWS, for example, precede `<h1>` headings with “heading level 1.”
- Some screen readers announce the number of links on a page as soon as the page finishes loading in the browser.
- JAWS says “same page link” if the link destination is on the same page as the link itself and “visited link” for links that have been previously accessed.
- Screen readers in table navigation mode inform the user how many rows and columns are in a [data table](/techniques/tables/data).
- Users can navigate in any direction from cell to cell in table navigation mode. If the table is marked up correctly, the screen reader will read the column and/or row heading as the user enters each new cell.
- Screen readers inform users when they have entered into a form. Users have the option to enter form navigation mode.
- Screen readers can be thrown off by homographs. For example, the word *read* can be pronounced “reed” or “red,” depending on the context: “I’m going to read the newspaper” vs. “I already read the newspaper.” A sentence such as “I read the newspaper every day” is ambiguous to all readers—humans and screen readers alike. The word *content* is another example: “I feel content” (meaning *satisfied*, with the emphasis on the second syllable [con-**TENT**]) vs. “WebAIM.org has some really awesome content” (meaning the *subject matter*, with the emphasis on the first syllable [**CON**-tent]).
- Screen readers may or may not read out punctuation, depending on the user’s verbosity setting. Ensure that your intended meaning will be conveyed in either case. To appreciate the value of punctuation, consider these sentences:
  - Let’s eat, grandpa!
  - I’d like to thank my parents, the pope, and Mother Teresa.
  - He finds inspiration in cooking, his children, and his cat.

Note

Some browsers seem to work better with certain screen readers. Here are our recommended pairings:

- [Firefox](//mozilla.org/firefox/) with [NVDA](//nvaccess.org/download/)
- [Chrome](//google.com/chrome/browser/) or [Internet Explorer](//windows.microsoft.com/internet-explorer/) with [JAWS](//freedomscientific.com/JAWSHQ/JAWSHeadquarters01)
- [Safari](//apple.com/safari/) with [VoiceOver](//apple.com/accessibility/)
- [Edge](//microsoft.com/windows/microsoft-edge) with [Narrator](//microsoft.com/accessibility/windows)

Important

Using any screen reader for the first time can be a confusing and discouraging experience. Using an audio interface is almost always a little disorienting for sighted users. Also, much of the content on a web page will seem to be inaccessible, when in fact the problem may be that the new user simply does not know how to use the screen reader.

Developers who are serious about wanting to know how their content sounds on screen readers will need to either work closely with people who use screen readers on a regular basis or else devote the time to learn how to use a screen reader effectively. However, testing accessibility with a screen reader is best conducted using the default or minimally customized settings and limited navigation techniques. This allows the basic accessibility of the page to be analyzed without relying on strategies employed by screen reader power users.
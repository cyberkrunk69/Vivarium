# Truncate String with Ellipsis | CSS-Tricks

Source: https://css-tricks.com/snippets/css/truncate-string-with-ellipsis/

---

Things have changed quite a bit since this article was published in 2011! If you’re looking for a more modern approach to truncating a string of content, check out the CSS [`line-clamp` property](https://css-tricks.com/almanac/properties/l/line-clamp/) as well as [this tutorial](https://css-tricks.com/recreating-mdns-truncated-text-effect/) that uses it along with a fading effect.

All the following are required, so the text must be in a single straight line that overflows a box where that overflow is hidden.

```
.truncate {
  width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

Note the fixed width in use here. The gist is that the element needs some kind of determinate width, which you have to be particularly careful about with flexbox:

---

Looking for [truncating to a particular number of lines](https://css-tricks.com/line-clampin/)? You might also dig [this neat fading truncation effect](https://css-tricks.com/recreating-mdns-truncated-text-effect/).
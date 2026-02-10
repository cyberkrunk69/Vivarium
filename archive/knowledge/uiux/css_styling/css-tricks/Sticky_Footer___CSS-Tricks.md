# Sticky Footer | CSS-Tricks

Source: https://css-tricks.com/snippets/css/sticky-footer/

---

Works great if you can apply a fixed height to the footer.

```
<div class="page-wrap">
  
  Content!
      
</div>

<footer class="site-footer">
  I'm the Sticky Footer.
</footer>
```

```
* {
  margin: 0;
}
html, body {
  height: 100%;
}
.page-wrap {
  min-height: 100%;
  /* equal to footer height */
  margin-bottom: -142px; 
}
.page-wrap:after {
  content: "";
  display: block;
}
.site-footer, .page-wrap:after {
  height: 142px; 
}
.site-footer {
  background: orange;
}
```

See the Pen [Sticky Footer](http://codepen.io/chriscoyier/pen/uwJjr/) by Chris Coyier ([@chriscoyier](http://codepen.io/chriscoyier)) on [CodePen](http://codepen.io).
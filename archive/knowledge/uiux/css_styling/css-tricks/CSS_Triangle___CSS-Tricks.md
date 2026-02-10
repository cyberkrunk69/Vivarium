# CSS Triangle | CSS-Tricks

Source: https://css-tricks.com/snippets/css/css-triangle/

---

#### HTML

You can make them with a single div. It’s nice to have classes for each direction possibility.

```
<div class="arrow-up"></div>
<div class="arrow-down"></div>
<div class="arrow-left"></div>
<div class="arrow-right"></div>
```

#### CSS

The idea is a box with zero width and height. The actual width and height of the arrow is determined by the width of the border. In an up arrow, for example, the bottom border is colored while the left and right are transparent, which forms the triangle.

```
.arrow-up {
  width: 0; 
  height: 0; 
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  
  border-bottom: 5px solid black;
}

.arrow-down {
  width: 0; 
  height: 0; 
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  
  border-top: 20px solid #f00;
}

.arrow-right {
  width: 0; 
  height: 0; 
  border-top: 60px solid transparent;
  border-bottom: 60px solid transparent;
  
  border-left: 60px solid green;
}

.arrow-left {
  width: 0; 
  height: 0; 
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent; 
  
  border-right:10px solid blue; 
}
```

#### Demo

See the Pen [Animation to Explain CSS Triangles](http://codepen.io/chriscoyier/pen/lotjh/) by Chris Coyier ([@chriscoyier](http://codepen.io/chriscoyier)) on [CodePen](http://codepen.io).

#### Examples

---

Dave Everitt writes in:

> For an equilateral triangle it’s worth pointing out that the height is 86.6% of the width so (border-left-width + border-right-width) \* 0.866% = border-bottom-width
# JavaScript Grid: Quick Start | AG Grid

Source: https://www.ag-grid.com/javascript-data-grid/getting-started/

---

AG Grid is a high-performance JavaScript Data Grid library for building JavaScript Tables with unbeatable performance and hundreds of features. Available in Community and Enterprise editions. Visit [Community vs. Enterprise](/javascript-data-grid/community-vs-enterprise/) to learn more.

[![JavaScript Data Grid quick start video tutorial thumbnail](https://img.youtube.com/vi/Ww7-LC6rU6U/0.jpg)](https://www.youtube.com/watch?v=Ww7-LC6rU6U&list=PLsZlhayVgqNxijfRQxg5Mc6W4MzZHQ9MK)

## Create a JavaScript Data Grid [Copy Link](#create-a-javascript-data-grid)

Add AG Grid to your application in 60 seconds:

1

### Provide a Container [Copy Link](#provide-a-container)

Load the AG Grid library and create a container div. The div should have a height because the Data Grid will fill the size of the parent container:

```
<html lang="en">
    <head>
        <!-- Includes all JS & CSS for the JavaScript Data Grid -->
        <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js"></script>
    </head>
    <body>
        <!-- Your Data Grid container -->
        <div id="myGrid" style="height: 500px"></div>
    </body>
</html>
```

If you're using TypeScript you need to import and register the modules you want to use. See the [NPM Installation](/javascript-data-grid/installation/#npm-installation) docs for more information.

2

### Instantiating the JavaScript Data Grid [Copy Link](#instantiating-the-javascript-data-grid)

Create the Data Grid inside of your container div using `createGrid`.

```
// Grid Options: Contains all of the Data Grid configurations
const gridOptions = {};

// Your Javascript code to create the Data Grid
const myGridElement = document.querySelector('#myGrid');
agGrid.createGrid(myGridElement, gridOptions);
```

3

### Define Rows and Columns [Copy Link](#define-rows-and-columns)

```
// Grid Options: Contains all of the Data Grid configurations
const gridOptions = {
    // Row Data: The data to be displayed.
    rowData: [
        { make: "Tesla", model: "Model Y", price: 64950, electric: true },
        { make: "Ford", model: "F-Series", price: 33850, electric: false },
        { make: "Toyota", model: "Corolla", price: 29600, electric: false },
    ],
    // Column Definitions: Defines the columns to be displayed.
    columnDefs: [
        { field: "make" },
        { field: "model" },
        { field: "price" },
        { field: "electric" }
    ]
};
```

4

### Example JavaScript Data Grid [Copy Link](#example-javascript-data-grid)

Below is a live example of the application running. Click `</> Code` to see the code.

To live-edit the code, open the example in CodeSandbox or Plunker using the buttons to the lower-right.

## Next Steps [Copy Link](#next-steps)

Now that you have a basic JavaScript Data Grid running, choose one of the following options to continue your learning journey:

[### Key Features

Browse an overview of our commonly used features](/react-data-grid/key-features/)[### Tutorials

Get started with our step-by-step tutorials](/react-data-grid/deep-dive/)[### Community vs. Enterprise

Understand the differences between each version](/react-data-grid/community-vs-enterprise/)
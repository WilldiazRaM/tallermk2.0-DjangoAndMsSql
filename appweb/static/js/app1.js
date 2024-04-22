const jsonData = '{ "book": { "name": "JSON Primer", "price": 29.99, "inStock": true, "rating": null } }';

const jsObject = JSON.parse(jsonData);

console.log(jsObject);
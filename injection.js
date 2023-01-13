Object.setPrototypeOf(document, Object.getPrototypeOf(document.implementation.createDocument('http://www.w3.org/1999/xhtml', 'html', null)));
var element = document.createElement('iframe');
element.setAttribute('id', 'cleanContext');
element.setAttribute('sandbox', 'allow-scripts allow-same-origin');
element.setAttribute('src', 'https://fakku.net');
document.head.insertBefore(element, document.head.children[0]);

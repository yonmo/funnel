var script = document.createElement('script');
script.type = 'text/javascript';
var src = 'var cureCanvas = Object.create(HTMLCanvasElement);';
var element = document.createTextNode(src);
script.appendChild(element);
document.head.insertBefore(script, document.head.children[0]);
window.top.cureCanvas = cureCanvas;

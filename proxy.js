var script = document.createElement('script');
script.type = 'text/javascript';
var src = ``; // Put The Proxy Script Here And Use This Script Inside funnel.py Or Another Selenium WebDriver Setup
var element = document.createTextNode(src);
script.appendChild(element);
document.head.insertBefore(script, document.head.children[0]);
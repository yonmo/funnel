// ==UserScript==
// @name         shiny-octo-potato
// @version      1.0
// @description  to get seed and edges
// @author       yonmo
// @grant        GM_xmlhttpRequest
// @match        *://*.fakku.net/*
// @run-at       document-start
// ==/UserScript==

(function() {
    //'use strict';
    console.log(Object.create(HTMLCanvasElement));
    window.addEventListener('load',() => {runtime();});

    function runtime() {
        var code;

        // Prototype Poison The DOM to Allow Me To Create Elements
        Object.setPrototypeOf(document, Object.getPrototypeOf(document.implementation.createDocument('http://www.w3.org/1999/xhtml', 'html', null)));

        // Inject My Code
        var src = `const handler = {
                        get(target, prop) {
                            if (typeof target[prop] === 'function') {
                                return new Proxy(target[prop], {
                                    apply: (target, thisArg, argumentsList) => {
                                        console.log(thisArg);
                                        console.log(argumentsList);
                                        return Reflect.apply(target, thisArg, argumentsList);
                                    }
                                });
                            } else if (target[prop] == 'prototype') {
                                console.log(Object.prototype);
                                return Object.prototype;
                            } else {
                                return Reflect.get(target, prop);
                            }
                        },
                        consructor(target, args) {
                            console.log(target);
                            console.log(args);
                            return new target(...args);
                        }
                    };

                    Object = new Proxy(Object, handler);`

        var inject = document.createElement('script');

        inject.type = 'text/javascript';
        code = document.createTextNode(src);
        inject.appendChild(code);
        document.head.insertBefore(inject, document.head.children[0]);
    }
})();
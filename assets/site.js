"use strict";
for (const element of document.querySelectorAll("#y, #year")) {
  element.textContent = new Date().getFullYear();
}

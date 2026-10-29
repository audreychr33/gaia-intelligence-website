"use strict";
for (const element of document.querySelectorAll("#y, #year")) {
  element.textContent = new Date().getFullYear();
}
for (const button of document.querySelectorAll("[data-copy]")) {
  const label = button.textContent;
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = button.dataset.done;
      setTimeout(() => { button.textContent = label; }, 2000);
    } catch (error) {
      window.getSelection().selectAllChildren(button.previousElementSibling);
    }
  });
}

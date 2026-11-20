"use strict";
for (const element of document.querySelectorAll("#y, #year")) {
  element.textContent = new Date().getFullYear();
}
for (const button of document.querySelectorAll("[data-copy]")) {
  // An icon button: on success it shows a tick for two seconds and announces "Copied" to screen readers.
  const label = button.getAttribute("aria-label");
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.classList.add("done");
      button.setAttribute("aria-label", button.dataset.done);
      button.title = button.dataset.done;
      setTimeout(() => { button.classList.remove("done"); button.setAttribute("aria-label", label); button.title = label; }, 2000);
    } catch (error) {
      window.getSelection().selectAllChildren(button.previousElementSibling);
    }
  });
}

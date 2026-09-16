const status = document.querySelector("#status");

if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("./sw.js")
    .then((reg) => {
      status.textContent = "sw: registered " + reg.scope;
    })
    .catch((err) => {
      status.textContent = "sw: " + err;
    });
} else {
  status.textContent = "sw: not supported";
}

const form = document.querySelector("#echo-form");
const output = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = new FormData(form).get("message");
  output.textContent = `ローカル: ${message}`;
  try {
    const res = await fetch("https://httpbin.org/post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    output.textContent += `\nfetch: ${JSON.stringify(data.json)}`;
  } catch (error) {
    output.textContent += `\nfetch failed: ${error}`;
  }
});

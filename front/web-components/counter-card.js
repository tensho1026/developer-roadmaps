const template = document.createElement("template");
template.innerHTML = `
  <style>
    :host {
      display: inline-block;
      font-family: system-ui, sans-serif;
      border: 1px solid #444;
      padding: 1rem 1.25rem;
      border-radius: 8px;
    }
    button { font: inherit; padding: 0.4rem 0.8rem; }
  </style>
  <p part="label"></p>
  <button type="button">increment</button>
`;

class CounterCard extends HTMLElement {
  #count = 0;

  constructor() {
    super();
    this.attachShadow({ mode: "open" }).appendChild(template.content.cloneNode(true));
  }

  connectedCallback() {
    const label = this.shadowRoot.querySelector("p");
    const button = this.shadowRoot.querySelector("button");
    const render = () => {
      label.textContent = `${this.getAttribute("label") ?? "count"}: ${this.#count}`;
    };
    render();
    button.addEventListener("click", () => {
      this.#count += 1;
      render();
    });
  }
}

customElements.define("counter-card", CounterCard);

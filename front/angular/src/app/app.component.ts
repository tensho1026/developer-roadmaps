import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";

@Component({
  selector: "app-root",
  imports: [RouterOutlet],
  template: `
    <main>
      <h1>Angular playground</h1>
      <p>Frontend roadmap: Learn a Framework → Angular</p>
      <router-outlet />
    </main>
  `,
  styles: `
    main {
      padding: 2rem;
    }
  `,
})
export class AppComponent {}

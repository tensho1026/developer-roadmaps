import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import { expect, test } from "vitest";
import App from "./App";

test("renders heading", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>,
  );
  expect(screen.getByText(/React playground/)).toBeTruthy();
});

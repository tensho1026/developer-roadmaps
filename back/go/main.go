package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]any{"ok": true, "language": "go"})
	})
	log.Println("go listening on http://localhost:8090")
	log.Fatal(http.ListenAndServe(":8090", mux))
}

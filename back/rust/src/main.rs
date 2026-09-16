use axum::{routing::get, Json, Router};
use serde_json::{json, Value};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3006").await.unwrap();
    println!("rust listening on http://localhost:3006");
    axum::serve(listener, app).await.unwrap();
}

async fn health() -> Json<Value> {
    Json(json!({ "ok": true, "language": "rust" }))
}

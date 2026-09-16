var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/health", () => Results.Json(new { ok = true, language = "csharp" }));
app.Run("http://localhost:5080");

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public class App {
  public static void main(String[] args) throws IOException {
    HttpServer server = HttpServer.create(new InetSocketAddress(8081), 0);
    server.createContext("/health", exchange -> {
      byte[] body = "{\"ok\":true,\"language\":\"java\"}".getBytes(StandardCharsets.UTF_8);
      exchange.getResponseHeaders().add("Content-Type", "application/json");
      exchange.sendResponseHeaders(200, body.length);
      exchange.getResponseBody().write(body);
      exchange.close();
    });
    server.start();
    System.out.println("java listening on http://localhost:8081");
  }
}

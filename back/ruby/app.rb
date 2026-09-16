require "json"
require "webrick"

server = WEBrick::HTTPServer.new(Port: 4567, BindAddress: "0.0.0.0")
server.mount_proc "/health" do |_req, res|
  res["Content-Type"] = "application/json"
  res.body = { ok: true, language: "ruby", framework: "webrick" }.to_json
end

trap("INT") { server.shutdown }
puts "ruby listening on http://localhost:4567"
server.start

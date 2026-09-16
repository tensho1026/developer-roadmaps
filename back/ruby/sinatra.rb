require "sinatra"
require "json"

set :port, 4568
set :bind, "0.0.0.0"

get "/health" do
  content_type :json
  { ok: true, language: "ruby", framework: "sinatra" }.to_json
end

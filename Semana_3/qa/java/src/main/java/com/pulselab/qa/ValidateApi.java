package com.pulselab.qa;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ValidateApi {
    public static void main(String[] args) throws IOException, InterruptedException {
        String baseUrl = System.getenv().getOrDefault("API_BASE_URL", "http://localhost:8000");
        HttpClient client = HttpClient.newHttpClient();

        String health = get(client, baseUrl + "/api/health");
        String cached = get(client, baseUrl + "/api/lab?mode=cached&locale=es");
        String nocache = get(client, baseUrl + "/api/lab?mode=nocache&locale=es");

        requireContains(health, "\"status\":\"UP\"", "health status");

        int cachedTtfb = extractInt(cached, "\"ttfbMs\":");
        int nocacheTtfb = extractInt(nocache, "\"ttfbMs\":");

        if (cachedTtfb >= nocacheTtfb) {
            throw new IllegalStateException("JAVA validate_api expected cached ttfb lower than nocache");
        }

        System.out.println("JAVA validate_api OK");
        System.out.println("cached ttfb=" + cachedTtfb + " ms");
        System.out.println("nocache ttfb=" + nocacheTtfb + " ms");
    }

    private static String get(HttpClient client, String url) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url)).GET().build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new IllegalStateException("Request failed: " + url + " status=" + response.statusCode());
        }
        return response.body();
    }

    private static void requireContains(String value, String required, String label) {
        if (!value.contains(required)) {
            throw new IllegalStateException("Missing " + label);
        }
    }

    private static int extractInt(String json, String marker) {
        int start = json.indexOf(marker);
        if (start < 0) {
            throw new IllegalStateException("Marker not found: " + marker);
        }

        int index = start + marker.length();
        int end = index;
        while (end < json.length() && Character.isDigit(json.charAt(end))) {
            end++;
        }

        return Integer.parseInt(json.substring(index, end));
    }
}

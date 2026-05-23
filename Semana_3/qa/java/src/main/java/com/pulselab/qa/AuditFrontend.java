package com.pulselab.qa;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class AuditFrontend {
    public static void main(String[] args) throws Exception {
        String frontendBaseUrl = System.getenv().getOrDefault("FRONTEND_BASE_URL", "http://localhost:4173");
        HttpClient client = HttpClient.newHttpClient();

        String index = get(client, frontendBaseUrl + "/");
        String robots = get(client, frontendBaseUrl + "/robots.txt");
        String sitemap = get(client, frontendBaseUrl + "/sitemap.xml");

        requireContains(index, "<meta name=\"description\"", "description meta");
        requireContains(index, "<link rel=\"canonical\"", "canonical link");
        requireContains(index, "application/ld+json", "json ld");
        requireContains(robots, "Sitemap:", "robots sitemap");
        requireContains(sitemap, "<loc>http://localhost:4173/</loc>", "sitemap root URL");

        System.out.println("JAVA audit_frontend OK");
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
}

package com.pulselab.qa;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ProfileCache {
    public static void main(String[] args) throws Exception {
        String baseUrl = System.getenv().getOrDefault("API_BASE_URL", "http://localhost:8000");
        HttpClient client = HttpClient.newHttpClient();

        double cachedAvg = averageMode(client, baseUrl, "cached");
        double nocacheAvg = averageMode(client, baseUrl, "nocache");

        if (cachedAvg >= nocacheAvg) {
            throw new IllegalStateException("JAVA profile_cache expected cached avg lower than nocache avg");
        }

        System.out.println("JAVA profile_cache OK");
        System.out.printf("cached avg=%.2f ms%n", cachedAvg);
        System.out.printf("nocache avg=%.2f ms%n", nocacheAvg);
    }

    private static double averageMode(HttpClient client, String baseUrl, String mode) throws IOException, InterruptedException {
        double sum = 0;
        for (int i = 0; i < 5; i++) {
            long started = System.nanoTime();
            get(client, baseUrl + "/api/lab?mode=" + mode + "&locale=es");
            sum += (System.nanoTime() - started) / 1_000_000.0;
        }
        return sum / 5;
    }

    private static void get(HttpClient client, String url) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url)).GET().build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new IllegalStateException("Request failed: " + url + " status=" + response.statusCode());
        }
    }
}

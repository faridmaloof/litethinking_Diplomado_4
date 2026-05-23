using System.Diagnostics;

namespace QaChecks;

public sealed class QaCommands(QaConfiguration configuration, QaHttpClient client)
{
    private readonly QaConfiguration _configuration = configuration;
    private readonly QaHttpClient _client = client;

    public async Task RunAsync(string command)
    {
        switch (command.ToLowerInvariant())
        {
            case "validate":
                await ValidateApiAsync();
                return;
            case "profile":
                await ProfileCacheAsync();
                return;
            case "audit":
                await AuditFrontendAsync();
                return;
            default:
                throw new InvalidOperationException($"Unknown command: {command}");
        }
    }

    private async Task ValidateApiAsync()
    {
        using var health = await _client.GetJsonAsync($"{_configuration.ApiBaseUrl}/api/health");
        using var cached = await _client.GetJsonAsync($"{_configuration.ApiBaseUrl}/api/lab?mode=cached&locale=es");
        using var nocache = await _client.GetJsonAsync($"{_configuration.ApiBaseUrl}/api/lab?mode=nocache&locale=es");

        if (health.RootElement.GetProperty("status").GetString() != "UP")
        {
            throw new InvalidOperationException("CSHARP validate_api health check failed");
        }

        var cachedTtfb = cached.RootElement.GetProperty("performance").GetProperty("ttfbMs").GetInt32();
        var nocacheTtfb = nocache.RootElement.GetProperty("performance").GetProperty("ttfbMs").GetInt32();

        if (cachedTtfb >= nocacheTtfb)
        {
            throw new InvalidOperationException("CSHARP validate_api expected cached ttfb lower than nocache");
        }

        Console.WriteLine("CSHARP validate_api OK");
        Console.WriteLine($"cached ttfb={cachedTtfb} ms");
        Console.WriteLine($"nocache ttfb={nocacheTtfb} ms");
    }

    private async Task ProfileCacheAsync()
    {
        var cachedAvg = await AverageForModeAsync("cached");
        var nocacheAvg = await AverageForModeAsync("nocache");

        if (cachedAvg >= nocacheAvg)
        {
            throw new InvalidOperationException("CSHARP profile_cache expected cached avg lower than nocache avg");
        }

        Console.WriteLine("CSHARP profile_cache OK");
        Console.WriteLine($"cached avg={cachedAvg:F2} ms");
        Console.WriteLine($"nocache avg={nocacheAvg:F2} ms");
    }

    private async Task AuditFrontendAsync()
    {
        var indexHtml = await _client.GetTextAsync($"{_configuration.FrontendBaseUrl}/");
        var robots = await _client.GetTextAsync($"{_configuration.FrontendBaseUrl}/robots.txt");
        var sitemap = await _client.GetTextAsync($"{_configuration.FrontendBaseUrl}/sitemap.xml");

        Require(indexHtml.Contains("<meta name=\"description\""), "description meta");
        Require(indexHtml.Contains("<link rel=\"canonical\""), "canonical link");
        Require(indexHtml.Contains("application/ld+json"), "json ld");
        Require(robots.Contains("Sitemap:"), "robots sitemap");
        Require(sitemap.Contains("<loc>http://localhost:4173/</loc>"), "sitemap root URL");

        Console.WriteLine("CSHARP audit_frontend OK");
    }

    private async Task<double> AverageForModeAsync(string mode)
    {
        var samples = new List<double>();

        for (var i = 0; i < 5; i++)
        {
            var stopwatch = Stopwatch.StartNew();
            await _client.GetTextAsync($"{_configuration.ApiBaseUrl}/api/lab?mode={mode}&locale=es");
            stopwatch.Stop();
            samples.Add(stopwatch.Elapsed.TotalMilliseconds);
        }

        return samples.Average();
    }

    private static void Require(bool condition, string label)
    {
        if (!condition)
        {
            throw new InvalidOperationException($"Missing {label}");
        }
    }
}

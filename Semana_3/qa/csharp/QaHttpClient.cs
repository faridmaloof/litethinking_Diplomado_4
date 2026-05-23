using System.Text.Json;

namespace QaChecks;

public sealed class QaHttpClient(HttpClient httpClient)
{
    private readonly HttpClient _httpClient = httpClient;

    public async Task<JsonDocument> GetJsonAsync(string url)
    {
        using var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        return JsonDocument.Parse(content);
    }

    public async Task<string> GetTextAsync(string url)
    {
        using var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadAsStringAsync();
    }
}

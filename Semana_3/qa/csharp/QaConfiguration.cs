namespace QaChecks;

public sealed class QaConfiguration
{
    public string ApiBaseUrl { get; }
    public string FrontendBaseUrl { get; }

    public QaConfiguration()
    {
        ApiBaseUrl = (Environment.GetEnvironmentVariable("API_BASE_URL") ?? "http://localhost:8000").TrimEnd('/');
        FrontendBaseUrl = (Environment.GetEnvironmentVariable("FRONTEND_BASE_URL") ?? "http://localhost:4173").TrimEnd('/');
    }
}

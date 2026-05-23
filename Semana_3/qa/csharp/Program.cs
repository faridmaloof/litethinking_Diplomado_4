using QaChecks;

var command = args.Length > 0 ? args[0] : "validate";
var configuration = new QaConfiguration();

using var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(15) };

var qaCommands = new QaCommands(configuration, new QaHttpClient(httpClient));
await qaCommands.RunAsync(command);

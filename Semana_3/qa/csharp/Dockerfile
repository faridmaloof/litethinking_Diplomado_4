FROM mcr.microsoft.com/dotnet/sdk:8.0

WORKDIR /qa-csharp

COPY QaChecks.csproj ./
RUN dotnet restore

COPY . ./
RUN dotnet publish -c Release -o /app

CMD ["dotnet", "/app/QaChecks.dll", "validate"]

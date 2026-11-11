# Stage 1: Build & Publish
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["UniChristBackend.csproj", "./"]
RUN dotnet restore "UniChristBackend.csproj"
COPY . .
RUN dotnet publish "UniChristBackend.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 2: Runtime Environment
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5000
ENV PORT=5000
EXPOSE 5000
ENTRYPOINT ["dotnet", "UniChristBackend.dll"]


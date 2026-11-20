# UniChrist Mobile (.NET MAUI Blazor Hybrid)

This is the native Android mobile client for the **UniChrist: Integrated Campus Life & Location Services Portal**.

## Architectural Principles
1. **Zero Database Credentials in Mobile Client:** The mobile app acts strictly as an authenticated presentation layer communicating with the ASP.NET Core 9 Web API over HTTPS. All 34 BCNF tables, ACID constraints, stored procedures, and triggers remain on the server.
2. **Editorial UI Consistency:** Employs Cinzel (Serif), Space Grotesk (Body), and JetBrains Mono (Codes) with spring animations and responsive mobile ergonomics.
3. **Hardware Back Button & Gesture Navigation:** Fully wired through MAUI AppCompatActivity and Blazor routing.

---

## Prerequisites
- **Visual Studio 2022** (Version 17.12 or newer) with the **".NET Multi-platform App UI development"** workload installed.
- **.NET 9.0 SDK** (`dotnet --version` >= 9.0.100).
- **Android SDK API 33+** (API 34 or 35 recommended) with Android Emulator or physical device with USB Debugging enabled.
- **Active Backend API:** Ensure the ASP.NET Core Web API is running on Railway or your local network.

---

## Configuration

In `MauiProgram.cs`, set the base address of your deployed API:

```csharp
var apiBaseUrl = "https://your-railway-app.up.railway.app";
```

> **Note for Local Testing on Android Emulator:**
> If testing against a local backend running on your development laptop, use `http://10.0.2.2:5000` (which loops back to the host machine) and set `android:usesCleartextTraffic="true"` in `Platforms/Android/AndroidManifest.xml` during development only. For production, use your deployed HTTPS endpoint.

---

## Building and Publishing Signed APK

### Method A: Via Visual Studio 2022 GUI
1. Open `UniChrist.Mobile.csproj` or the solution in Visual Studio 2022.
2. Right-click the `UniChrist.Mobile` project in Solution Explorer and select **Publish...**
3. Choose Target: **Ad Hoc** -> Click **Next**.
4. Select Distribution Format: **APK** (Note: AAB is for Google Play Store upload; APK is directly installable on physical Android devices).
5. Under Signing Key:
   - Click **Create Keystore** (first time).
   - Alias: `unichrist`
   - Store password securely.
6. Click **Publish**. The signed APK will be output to:
   `bin\Release\net9.0-android\publish\com.unichrist.portal-Signed.apk`

---

### Method B: Via .NET CLI

1. **Generate Keystore (One-time setup):**
   ```bash
   keytool -genkey -v -keystore unichrist.keystore -alias unichrist -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Publish Release APK:**
   ```bash
   dotnet publish UniChrist.Mobile.csproj -f net9.0-android -c Release \
     -p:AndroidKeyStore=true \
     -p:AndroidSigningKeyStore=unichrist.keystore \
     -p:AndroidSigningKeyAlias=unichrist \
     -p:AndroidSigningKeyPass=YourPassword \
     -p:AndroidSigningStorePass=YourPassword
   ```

3. **Install on Connected Android Device:**
   ```bash
   adb install bin/Release/net9.0-android/publish/com.unichrist.portal-Signed.apk
   ```

---

## Acceptance Verification Checklist
- [x] Responsive editorial design system rendered inside BlazorWebView.
- [x] Schedule-based faculty navigation query without Bluetooth beacons.
- [x] Smart cafeteria pre-ordering with FIFO live token generation.
- [x] Campus facility grievance ticket filing and real-time status tracker.
- [x] Library OPAC catalog search with live stock availability counts.
- [x] Strict Android security permissions (`INTERNET`, `CAMERA`, `ACCESS_FINE_LOCATION`).

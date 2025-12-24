PRD – Swish CSV to PDF Converter

1. Översikt

Swish CSV to PDF Converter är en lokal desktopapplikation utvecklad i Python som används för att omvandla Swish-transaktionsrapporter (CSV) till strukturerade, bokföringsredo PDF-dokument. Applikationen är avsedd för redovisningsunderlag och arkivering och fokuserar på korrekt datahantering, tydlig presentation och låg användarfriktion.

Applikationen används främst för intern bokföring där Swish-rapporter exporteras från extern källa och behöver konverteras till ett standardiserat PDF-format.

2. Mål och syfte

Primärt mål

Skapa ett tillförlitligt PDF-underlag för bokföring baserat på Swish CSV-rapporter.

Sekundära mål

Minimera manuell hantering

Minska risken för felaktiga exporter

Säkerställa konsekvent layout och struktur mellan rapporter

3. Målgrupp

Småföretagare

Enskilda näringsidkare

Intern redovisning / bokföring

Användare utan teknisk bakgrund

4. Antaganden och datakontrakt

Applikationen utgår från att CSV-filer alltid följer ett känt och konsekvent format, med tre logiska sektioner:

4.1 Metadata

Exempel:

"Skapad av:";"TIMMERLID OLIVER"
"Datum:";"2025-10-26"
"Sökbegrepp:";"Datum, Transaktionstyp, Swish nummer"
"Sök:";"2025-09-07 00:00:00 - 2025-09-07 23:59:59, ..."
"Swish-nummer:";"123 200 36 71"
"Antal resultat";"1"

4.2 Sammanfattning (översikt)

Identifieras via header:

"MARKNADSNAMN";"SWISH NUMMER"; ... ;"NETTO"

Följs av:

Total-rad

En eller flera marknadsrader

4.3 Transaktioner

Identifieras via header:

"DATUM";"TID";"MARKNADSNAMN"; ... ;"BELOPP"

5. Funktionella krav
   5.1 Filinmatning

Användaren ska kunna dra och släppa en CSV-fil i applikationsfönstret.

Endast .csv accepteras.

Ogiltiga filer ska avvisas med användarvänligt felmeddelande.

5.2 CSV-parsning

CSV-filer ska parsas konsekvent med Python csv-modulen eller pandas.

Ingen manuell strängsplit (split(';')) ska användas i produktion.

Applikationen ska korrekt hantera:

Semikolon-separerade värden

Tomma fält

Svenska decimalformat

5.3 Validering

Applikationen ska validera att:

Obligatoriska headers finns

Minst en transaktion existerar

Filens struktur matchar förväntat Swish-format

Vid fel:

Visa tydligt felmeddelande

Ingen PDF ska genereras

5.4 Förhandsgranskning

Efter lyckad inläsning ska användaren se en förhandsgranskning innehållande:

Datumintervall (från metadata)

Antal transaktioner

Totalbelopp

Marknadsnamn

Ingen PDF skapas förrän användaren bekräftar.

5.5 PDF-generering

PDF ska innehålla:

Översikt

Sökdatum

Antal betalningar

Totalt inbetalat belopp

Transaktionstabell

Alla relevanta kolumner

Sidbrytning med repeterad header

Högerjusterade belopp

Layout ska vara konsekvent och läsbar för bokföring.

5.6 Automatisk filnamngivning

Standardnamn ska genereras automatiskt enligt format:

Swish_YYYY-MM-DD.pdf

Användaren ska kunna ändra namn och plats innan export.

5.7 Exportinställningar

Användaren ska kunna justera:

Sidformat (A4 / Letter)

Orientering (stående / liggande)

Kolumnval (visa/dölj)

Textstorlek (liten / normal)

6. Icke-funktionella krav
   6.1 Logging

All intern status och fel ska loggas via Python logging

Ingen användning av print

Loggfil ska sparas lokalt för felsökning

6.2 Användarupplevelse

Applikationen ska fungera utan konfiguration

Alla fel ska kommuniceras via dialogrutor

Ingen terminal krävs

6.3 Plattform

Windows (primärt)

Python-baserad desktopapp (Tkinter / CustomTkinter)

7. Begränsningar

Applikationen är offline-only

Endast Swish CSV-format stöds

Ingen databas eller historiklagring

8. Framgångskriterier

PDF används direkt som bokföringsunderlag

Ingen manuell redigering krävs efter export

Felaktiga CSV-filer fångas innan PDF skapas

9. Applikationsstruktur och navigationsflöde

9.1 Fönsterbaserad arkitektur

Applikationen är en single-window desktop application. All funktionalitet presenteras inom ett och samma huvudfönster, utan externa dialoger för navigation mellan huvudsakliga vyer.

Fönstret innehåller logiskt separerade views/frames som byts baserat på applikationens tillstånd.

9.2 Navigationsmodell

Navigation sker genom intern state-hantering snarare än nya fönster. Användaren rör sig mellan följande huvudsakliga vyer:

Preview View (Startläge)

File Selection View

Settings View

Export / Confirmation State

Navigationen ska vara linjär och intuitiv, utan möjlighet att hamna i ett inkonsekvent tillstånd.

9.3 Startläge – Preview State

När applikationen startar:

Användaren möts av en preview state

Ingen fil är initialt vald

UI:t visar:

Instruktion om att välja eller dra in CSV-fil

Tom eller inaktiv förhandsgranskningsyta

Preview state fungerar som både:

Startvy

Neutral fallback om fil avmarkeras eller laddning misslyckas

9.4 Filval (File Selection)

Applikationen ska erbjuda två sätt att välja fil:

Drag-and-drop av CSV-fil

Manuell filväljare (”Välj fil”)

Efter lyckat filval:

CSV-filen parsas och valideras

Preview View uppdateras automatiskt

Metadata, sammanfattning och totals visas

Ogiltig fil leder till:

Felmeddelande

Applikationen stannar kvar i preview state

9.5 Förhandsgranskning (Preview View)

Preview View ska visa:

Sökdatum / datumintervall

Swish-nummer

Antal transaktioner

Totalbelopp

Eventuellt marknadsnamn

Syftet är att:

Ge användaren visuell verifiering innan export

Fånga upp felaktiga rapporter tidigt

Ingen PDF genereras i detta steg.

9.6 Inställningar (Settings View)

Applikationen ska innehålla en separat inställningsvy som kan nås från preview-läget.

Inställningarna ska omfatta:

PDF-layout (A4 / Letter)

Orientering (stående / liggande)

Kolumnval (visa/dölj)

Textstorlek

Automatisk filnamngivning (på/av)

Inställningar:

Ska kunna ändras innan export

Ska påverka både preview och slutlig PDF

Ska inte kräva omstart av applikationen

9.7 Exportflöde

När användaren bekräftar export:

Applikationen använder aktuella inställningar

PDF genereras

Filnamn föreslås automatiskt enligt standard

Användaren kan bekräfta eller ändra sparplats

Efter lyckad export:

Bekräftelse visas

Applikationen återgår till preview state

9.8 State-översikt (sammanfattning)
State Beskrivning
Preview (Initial) Ingen fil vald, väntar på input
Preview (Loaded) CSV inläst och förhandsgranskad
Settings Export- och layoutinställningar
Export PDF genereras och sparas

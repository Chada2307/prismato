# 02. Wymagania Funkcjonalne i Niefunkcjonalne

## 1. Konwencja oznaczeń i priorytetyzacja (MoSCoW)
Każde wymaganie posiada unikalny identyfikator oraz priorytet:
- **[MUST]** – Funkcjonalność krytyczna, bez której system nie może działać ani zostać obroniony.
- **[SHOULD]** – Funkcjonalność wysoce pożądana, istotna dla pełnej wartości użytkowej.
- **[COULD]** – Funkcjonalność dodatkowa, realizowana tylko w przypadku rezerwy czasowej.
- **[WONT]** – Funkcjonalność świadomie odłożona na przyszłe wersje (poza zakresem inżynierki).

---

## 2. Wymagania Funkcjonalne (Functional Requirements – FR)

### 2.1. Moduł Autentykacji i Zarządzania Użytkownikami (AUTH)
- **FR-AUTH-01 [MUST]:** Rejestracja nowego użytkownika z walidacją danych (login, silne hasło).
- **FR-AUTH-02 [MUST]:** Logowanie użytkownika z użyciem bezpiecznych tokenów lub sesji.
- **FR-AUTH-03 [MUST]:** Bezpieczne haszowanie haseł przed zapisem do bazy danych.
- **FR-AUTH-04 [SHOULD]:** Możliwość edycji profilu oraz zmiany hasła przez zalogowanego użytkownika.
- **FR-AUTH-05 [COULD]:** Mechanizm resetowania hasła.

### 2.2. Moduł Zarządzania Zasobami i Kolekcjami (MEDIA)
- **FR-MEDIA-01 [MUST]:** Przesyłanie pojedynczych oraz wielu plików graficznych jednocześnie (Multi-upload).
- **FR-MEDIA-02 [MUST]:** Walidacja przesyłanych plików po stronie serwera (format MIME, dopuszczalne rozszerzenia, maksymalny rozmiar).
- **FR-MEDIA-03 [MUST]:** Usuwanie zasobów przez właściciela (zarówno wpisu w bazie, jak i fizycznego pliku ze storage).
- **FR-MEDIA-04 [SHOULD]:** Tworzenie, edycja i usuwanie albumów/kolekcji oraz przypisywanie do nich zdjęć.
- **FR-MEDIA-05 [SHOULD]:** System tagowania zdjęć (dodawanie/usuwanie etykiet) w celu łatwej kategoryzacji.

### 2.3. Moduł Przetwarzania i Ekstrakcji Metadanych (PROC)
- **FR-PROC-01 [MUST]:** Automatyczne generowanie miniatur (thumbnails) o zoptymalizowanym rozmiarze i formacie (np. WebP) podczas uploadu.
- **FR-PROC-02 [MUST]:** Odczyt i parsowanie metadanych EXIF (np. data wykonania zdjęcia, model aparatu/obiektywu, ISO, czas naświetlania, przysłona).
- **FR-PROC-03 [SHOULD]:** Asynchroniczne przetwarzanie zadań ciężkich (np. kolejkowanie generowania miniatur w tle, aby nie blokować odpowiedzi HTTP).
- **FR-PROC-04 [COULD]:** Ekstrakcja i zapis współrzędnych GPS z metadanych do późniejszej geolokalizacji.

### 2.4. Moduł Przeglądania, Wyszukiwania i Prezentacji (UI/SEARCH)
- **FR-UI-01 [MUST]:** Responsywny widok siatki (Gallery Grid) z leniwym ładowaniem (Lazy Loading) miniatur.
- **FR-UI-02 [MUST]:** Widok pełnoekranowy/podgląd pojedynczego zdjęcia wraz z wyświetlaniem odczytanych metadanych technicznych.
- **FR-UI-03 [SHOULD]:** Filtrowanie i sortowanie kolekcji (po dacie wykonania/dodania, rozmiarze, tagach, albumach).
- **FR-UI-04 [COULD]:** Wyszukiwarka pełnotekstowa po nazwach, opisach i tagach.

---

## 3. Wymagania Niefunkcjonalne (Non-Functional Requirements – NFR)

### 3.1. Wydajność i Skalowalność (NFR-PERF)
- **NFR-PERF-01:** Czas odpowiedzi API dla zapytań odczytu listy miniatur nie powinien przekraczać 200 ms przy standardowym obciążeniu.
- **NFR-PERF-02:** Przetwarzanie plików (skalowanie, generowanie miniatur) nie może blokować operacji I/O ani głównego wątku serwera aplikacji.
- **NFR-PERF-03:** Paginacja lub kursorowe pobieranie danych dla dużych zbiorów zdjęć.

### 3.2. Bezpieczeństwo i Izolacja Danych (NFR-SEC)
- **NFR-SEC-01:** Pełna izolacja danych – użytkownik ma dostęp wyłącznie do własnych zasobów (chyba że zostały jawnie udostępnione).
- **NFR-SEC-02:** Zabezpieczenie przed atakami typu SQL Injection, XSS oraz CSRF.
- **NFR-SEC-03:** Bezpieczne przechowywanie nazw plików (generowanie unikalnych identyfikatorów UUID dla zapisywanych plików na dysku, aby zapobiec Path Traversal).

### 3.3. Architektura i Utrzymanie (NFR-ARCH)
- **NFR-ARCH-01:** Konteneryzacja całego środowiska (Backend, Frontend, Baza danych, ewentualne kolejki/storage) za pomocą Docker i Docker Compose.
- **NFR-ARCH-02:** Architektura oparta o REST API ze standaryzowanymi kodami odpowiedzi HTTP i automatyczną dokumentacją (OpenAPI/Swagger).
- **NFR-ARCH-03:** Modułowa struktura kodu umożliwiająca łatwe dopisanie testów jednostkowych i integracyjnych.

---

## 4. Przykładowe Scenariusze Użycia (Use Cases)

### UC-01: Przesłanie nowej partii zdjęć
1. **Aktor:** Użytkownik zalogowany.
2. **Warunek początkowy:** Użytkownik znajduje się w widoku dodawania plików.
3. **Przebieg główny:**
   1. Użytkownik wybiera pliki metodą Drag & Drop.
   2. Frontend sprawdza wstępnie format i rozmiar plików.
   3. Pliki są wysyłane równolegle/strumieniowo na backend.
   4. Backend zapisuje oryginalny plik z unikalnym UUID, zleca generowanie miniatury i odczytuje dane EXIF.
   5. Do bazy danych trafia rekord z powiązanymi metadanymi.
   6. Frontend otrzymuje potwierdzenie i odświeża galerię.
4. **Warunek końcowy:** Zdjęcia są zarchiwizowane i widoczne w siatce jako miniatury.

### UC-02: Usunięcie zdjęcia
1. **Aktor:** Użytkownik zalogowany.
2. **Warunek początkowy:** Użytkownik znajduje się w widoku wyświetlenia galerii zdjęć.
3. **Przebieg główny:**
   1. Użytkownik wybiera zdjęcie z intencją usunięcia.
   2. Użytkownik klika ikonkę kosza na śmieci.
   3. Zdjęcie znika z GUI, frontend zostaje przeładowany.
   4. Backend otrzymuje żądanie zmiany stausu flagi zdjęcia w bazie danych.
   5. W bazie danych rekord powiązany z danym zdjęciem, zostaje zmodyfikowany poprzez ustawienie flagi is_deleted
   6. Użytkownik weryfikuje na GUI zakładkę *"Trash"*
   7. Użytkownik widzi usunięte przez siebie zdjęcie.
   8. Użytkownik weryfikuje czy poprawne zdjęcie zostało przeniesione do kosza oraz ponownie klika ikonkę kosa na śmieci.
   9. Zdjęcie znika z GUI, frontend zostaje przeładowany.
   10. Backend otrzymuje żądanie usunięcia zdjęcia z katalogów oraz rekordu w bazie danych
4. **Warunek końcowy:** Zdjęcie zostało usunięte, wszelkie informacje odnośnie pliku zostały usunięte z bazy danych oraz sam plik nie isnieje w przestrzeni dyskowej aplikacji.
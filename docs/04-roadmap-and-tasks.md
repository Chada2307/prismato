# 04. Roadmapa, Inwentaryzacja i Harmonogram Prac

## 1. Stan Obecny Projektu (Inwentaryzacja AS-IS)

### 1.1. Moduły wdrożone i działające (Done):
- [x] **Środowisko i Konteneryzacja:** Pełny build w Docker Compose (FastAPI + SvelteKit/Vite + PostgreSQL z `pgvector`).
- [x] **Logowanie jednokontowe (Demo Auth):** Prosty mechanizm logowania na zahardcodowanego użytkownika (`admin`/`admin`).
- [x] **Upload zasobów:** Obsługa przesyłania pojedynczego i masowego (Multi-upload) za pomocą metody Drag & Drop oraz tradycyjnego okna wyboru plików.
- [x] **Ekstrakcja metadanych EXIF:** Zczytywanie parametrów z pliku; w przypadku braku daty wykonania w EXIF następuje automatyczny fallback do daty przesłania pliku (`created_at`).
- [x] **Zarządzanie stanem zdjęć (Soft & Hard Delete):** 
  - Przenoszenie zdjęć z widoku głównego do kosza (`is_deleted = true`).
  - Trwałe usuwanie plików fizycznych i rekordów z poziomu kosza.
- [x] **Główny UI / Layout (Svelte):**
  - Panel boczny (Sidebar) ze skrótami do sekcji: `Photos`, `Search`, `Map`, `Favourites`, `Albums`, `Trash`.
  - Widok siatki kafelków (`Photos`) z podglądem miniaturek, datą i akcjami szybkimi (polubienie, przeniesienie do kosza).

---

### 1.2. Elementy do zrobienia (Backlog / TO-DO):
- [ ] **Pełna Autentykacja (Multi-user):** Rejestracja, haszowanie haseł w bazie, generowanie tokenów i dynamiczny `owner_id`.
- [ ] **Moduł Ulubione (`Favourites`):** Dodanie flagi/relacji `is_favorite` i podpięcie widoku pod przycisk serduszka na kafelku.
- [ ] **Moduł Kosz (`Trash`):** Dedykowany widok z opcją przywracania zdjęć (`Restore`) lub trwałego czyszczenia kosza.
- [ ] **Moduł Wyszukiwarki (`Search`):** Wyszukiwanie po dacie, nazwie, modelu aparatu oraz po wykrytych twarzach.
- [ ] **Moduł Mapy (`Map`):** Prezentacja zdjęć na mapie kafelkowej (np. Leaflet) w oparciu o współrzędne `latitude` i `longitude`.
- [ ] **Moduł Albumów (`Albums`):** Tworzenie kolekcji i grupowanie zdjęć.
- [ ] **Moduł AI / Wektorowy (Detekcja twarzy):** Integracja biblioteki do wektorowania twarzy (128D) i powiązanie z tabelami `faces` i `people` w `pgvector`.

---

## 2. Podział na Sprinty i Kamienie Milowe

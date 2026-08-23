# 01. Przegląd i Zakres Projektu

## 1. Nazwa i geneza projektu
- **Nazwa robocza:** Prismato
- **Krótki opis:** Projekt i implementacja systemu do archiwizacji i zarządzania cyfrowymi zbiorami fotograficznymi.  

---

## 2. Problem biznesowy i motywacja
- **Identyfikacja problemu:** System ma być alternatywą dla rozwiązań istniejących na rynku przypisanych głównie do urządzeń i ich systemów operacyjnych, ma on pozwalać na użytkownikowi budować własną prywatną chmurę oraz kontrolować swoje osobiste dane, bez zbędnych modeli subskrypcyjnych za przestrzeń w chmurze czy rezygnowania z prywatności.
- **Cel projektu:** Celem jest zaprojektowanie i budowa aplikacji służącej do centralizacji i porządkowania zasobów fotograficznych. Projekt ma na celu stworzenie narzędzia wspomagającego użytkownika w katalogowaniu dużych zbiorow danych wizualnych oraz optymalizację procesu ich przeglądania i wyszukiwania.

---

## 3. Aktorzy systemu

| Rola | Opis | Główne uprawnienia |
| :--- | :--- | :--- |
| **Gość (Niezalogowany)** | Użytkownik przeglądający stronę | Dostęp do strony logowania, rejestracji oraz publicznej dokumentacji API |
| **Użytkownik standardowy** | Zarejestrowany właściciel konta | Upload plików, tworzenie albumów/tagów, przeglądanie i pobieranie własnych zasobów |
| **Administrator** (opcjonalnie) | Zarządca platformy | Podgląd statystyk systemu, zarządzanie użytkownikami, monitorowanie zasobów dyskowych |

---

## 4. Zakres projektu

### 4.1. W zakresie
- Bezpieczna autoryzacja i zarządzanie kontem użytkownika.
- Asynchroniczny upload wielu plików z walidacją formatów i rozmiarów.
- Automatyczne generowanie miniatur oraz odczyt metadanych (np. EXIF: data wykonania, parametry aparatu, geolokalizacja).
- Kategoryzacja, tworzenie kolekcji/albumów oraz tagowanie zasobów.
- Wyszukiwarka i zaawansowane filtrowanie po dacie, tagach i parametrach technicznych.

### 4.2. Poza zakresem
- *Zaawansowane rozpoznawanie twarzy i obiektów AI*.
- *Wyszukiwanie osób na zdjęciach na podstawie zebranych danych z modułu sztucznej inteligencji*
- *Wyszukiwanie i kategoryzowanie zbiorów na podstawie geolokalizacji zdjęć - oraz w przypadku jej braku - możliwość dodawania lokalizacji do zdjęcia*

---

## 5. Główne kryteria sukcesu projektu
1. Działające, w pełni zintegrowane środowisko (Frontend + Backend + Baza danych / Storage).
2. Sprawny proces przetwarzania i serwowania multimediów bez blokowania głównego wątku aplikacji.
3. Kompletna dokumentacja techniczna.
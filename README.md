# Program do tworzenia quizu z podanymi informacjami

## Opis
Program tworzy quiz na podstawie podanych pytaniami i odpowiedziami.
Po zatwierdzeniu odpowiedzi wysyła na email użytkownika informacje o poprawnych i niepoprawnych odpowiedziach oraz czas w którym użytkownik rozpoczął i zakończył quiz.
Użytkownik ma do wyboru 4 odpowiedzi na każde pytanie.
Pytania i odpowiedzi mogą zawierać zdjęcia.

## Instalacja i uruchomienie
Należy skolonować repozytarium i jej zawartość
By skorzystać z programu należy zainstalować podane niżej biblioteki:
-pygame
-io
-typing
-time
-sys
-smtplib
-email.mime.multipart
-email.mime.text
-Sub.Time
-dotenv
By quiz używał właściwych pytań i odpowiedzi należy utworzyć plik pytania.txt w folderze Data w którym pytanie będzie rozpoczynało plik pytania.txt a odpowiedzi będą podawane w następnych liniach pliku(4 odpowiedzi), jeśli chcemy dodać obrazki do pytań i odpowiedzi należy podać link do zdjęcia koło danego pytania lub odpowiedzi po spacji.
Jeśli chcemy włączyć quiz należy uruchomić plik zatytułowany Quiz.py

# Zastosowanie poszczególnych plików
plik .env zawiera hasło do emaila
plik Time.py zlicza czas w którym użytkownik zakończył quiz
plik Quiz.py zawiera kod programu
plik Elements.py tworzy obiekty
plik Send.py przesyła odpowiedzi na pytania i czas w którym użytkownik zakończył quiz na email użytkownika
plik Data.py pobiera dane z pliku pytania.txt
plik pytania.txt zawiera pytania i odpowiedzi


# Licencja
Projekt jest dostępny na licencji MIT


# Autorzy
Mikołaj Mak
Bartek Turek
Dominik Matuszyk

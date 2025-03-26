# Program do tworzenia quizu z podanymi informacjami

## Opis
Program tworzy quiz na podstawie podanych pytaniach z odpowiedziach.
Po zatwierdzeniu odpowiedzi wysyła na email użytkownika informacje o zaznaczonych odpowiedziach oraz czas w którym użytkownik rozpoczął i zakończył quiz.
Użytkownik ma do wyboru 4 odpowiedzi na każde pytanie.
Pytania i odpowiedzi mogą zawierać zdjęcia.

## Instalacja i uruchomienie
Należy skolonować repozytarium i jej zawartość
Projekt był tworzony na najnowszej wersji pythona 3.14
By skorzystać z programu należy zainstalować podane niżej biblioteki:
-pygame<br>
-io<br>
-typing<br>
-time<br>
-sys<br>
-smtplib<br>
-email.mime.multipart<br>
-email.mime.text<br>
-Sub.Time<br>
-dotenv<br>
Aby wysłać odpowiedzi na wskazany e-mail, należy zmienić go w pliku Settings.config.
Aby quiz używał właściwych pytań i odpowiedzi, należy utworzyć plik pytania.txt w folderze ProjectData, w którym pytanie będzie rozpoczynało plik, a odpowiedzi będą podawane w następnych liniach (4 odpowiedzi). Jeśli chcemy dodać obrazek do pytań lub odpowiedzi, należy podać link do zdjęcia obok danego pytania lub odpowiedzi, po spacji.
Aby uruchomić quiz, należy włączyć plik zatytułowany Quiz.py.

# Zastosowanie poszczególnych plików
plik .env zawiera hasło do emaila<br>
plik Time.py zlicza czas w którym użytkownik zakończył quiz<br>
plik Quiz.py zawiera kod programu<br>
plik Elements.py tworzy obiekty<br>
plik Send.py przesyła odpowiedzi na pytania i czas w którym użytkownik zakończył quiz na email użytkownika<br>
plik Data.py pobiera dane z pliku pytania.txt<br>
plik pytania.txt zawiera pytania i odpowiedzi<br>
w pliku Settings.config można ustawić limit czasowy<br>


# Licencja
Projekt jest dostępny na licencji MIT


# Autorzy
Mikołaj Mak<br>
Bartek Turek<br>
Dominik Matuszyk<br>


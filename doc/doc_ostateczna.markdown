Dokumentacja  do projektu z PSZT

Grupa projektowa MK.AE.2 w składzie:

1. Radosław Załuska
2. Konrad Czarnota
3. Maciej Zaborek

## Opis problemu

Problem podziału kart za pomocą algorytmu ewolucyjnego.
Algorytm ewolucyjny ma pomóc nam efektywnie rozwiązać problem podziału kart,
specyfikacja problemu sprowadza się do dwóch punktów: Dysponujemy 10
kartami ponumerowanymi od 1 do 10. Celem jest podział kart na dwie
grupy takie, że: suma pierwsze grupy jest jak najbliższa 36, a produkt
(iloczyn) drugiej grupy jest jak najbliższy 360.

## Opis rozwiązania
Do rozwiązania problemu został użyty algorytm genetyczny. Rozwiązanie zostało
uogólnione dla przypadku n – kart. Jeśli istnieje taka suma i taki iloczyn
podziału n kart na 2 grupy to algorytm taki podział znajdzie. Aby ułatwić
generowanie możliwych przypadków testowych została opracowana funkcja generująca
potencjalne możliwe do rozwiązania problemy. W ramach rozwiązania zostały
zaimplementowane 3 algorytmy w celu porównania ich możliwości rozwiązania tego
problemu.

### Opis genotypu
Każdy osobnik będzie opisany przez zestaw n bitów, gdzie n będzie liczbą kart w
rozpatrywanym przypadku. Każdy z bitów będzie odpowiadał na pytanie do której
grupy należy dana karta. Dla przykładu został podany wektor opisujący osobnika
10 bitowego (problem podziału 10 kart)

-  -  -----  -  -  -  -  -  -  --  -  
0  0  **1**  0  1  1  0  1  1   0  bity opisujące osobnika
1  2  **3**  4  5  6  7  8  9  10  numery kart której odpowiada dany bit
1  1  **2**  1  2  2  1  2  2   1  grupa do której należy dana karta
---------------------------------------------------------------------------

Przykładowo z wyróżnionej kolumny wynika że karta z numerem 3 będzie należała do
grupy 2.

Karty należące do grupy 1 będą sumowane, a karty należące do grupy 2 będą
mnożone przez siebie. W ten sposób będzie można danego osobnika w populacji
jednoznacznie przypisać do jakiegoś przykładowego podziału kart. Zostanie więc
spełniona zasada jednoznaczność przypisania wymagana przez metodykę
projektowania algorytmów genetycznych.

###Opis funkcji celu
Każdy z osobników będzie oceniany za pomocą funkcji przystosowania określonej
wzorem:
$$f(osobnik) = f(s, i) = \frac{|\xi - s|}{\xi} + \frac{|\eta - i|}{\eta}$$
gdzie:  
$s$ - to suma wartości kart w grupie 1 dla danego osobnika  
$i$ - to iloczyn wartości kart w grupie 2 dla danego osobnika  
$\xi$ - suma kart w rozwiązaniu do którego dążymy  
$\eta$ - iloczyn kart w rozwiązaniu do którego dążymy

W miarę poprawy rozwiązania w kolejnych pokoleniach algorytmu wartość funkcji
przystosowania zbiega do zera.

$$\lim_{generation \to \infty} f(s, i) = 0$$

Poszukując rozwiązania będziemy zbliżać się z wartością funkcji do 0.
Osiągnięcie tej wartości będzie oznaczać, że znaleźliśmy rozwiązanie i jest ono
optymalne. Osobnik będzie tym lepiej przystosowany im wartość f. przystosowania
będzie bliższa 0. Za pomocą funkcji przystosowania będzie dokonywana selekcja
najlepiej przystosowanych osobników i odrzucanie słabszych.

###Opis operatorów genetycznych
W algorytmie będą wykorzystywane dwa operatory genetyczne:

1. mutacja - polegający na losowej zmianie któregoś z bitów (losowego)
   opisujących danego osobnika. Mutacja w tym problemie jest specyficzna
   ponieważ każdy gen ma inne prawdopodobieństwo zmutowania. Geny o mniejszych
   wartościach mają większe prawdopodobieństwo zmutowania, ponieważ ich zmiana
   nie wpływa znacząco na wartość funkcji dopasowania. Geny dalsze kodujące
   większe numery kart są mutowane z mniejszym prawdopodobieństwem, ponieważ ich
   zmiana wpływa znacząco na wartość funkcji dopasowania. Gdybyśmy je za często
   zmieniali to populacja stała by się niestabilna. Dzięki uzależnieniu wartości
   prawdopodobieństwa mutacji danego genu od jego pozycji w genotypie
   dopasowanie średnie populacji zmienia się łagodnie a nie skokowo.
2. krzyżowanie - łączenie 2 osobników poprzez zamianę fragmentów ciągów bitowych
   między sobą i tworzenie nowych osobników. Miejsce podziału jest wybierane
   losowo Tutaj może dodatkowo pojawić się mutacja jako dopełnienie tego
   procesu.

Przykład krzyżowania (przedstawiono tu bity reprezentujące osobników):

--- ---   --- --- ---
*1* *0* | *1* *0* *1* | rodzic 1
1   1   | 1    1   0  | rodzic 2
*1* *0* | 1    1   0  | dziecko 1
1   1   | *1* *0* *1* | dziecko 2
---------------------------------------------------------------------------

###Opisy algorytmów
Wszystkie algorytmy korzystają z tej samej reprezentacji osobnika.

####Algorytm doboru podobnych osobników

1. Losujemy początkową populację o rozmiarze n.
2. Wprowadzamy do populacji losowe zaburzenie mutacją o sile zależnej od
   odległość najlepszego osobnika od rozwiązania optymalnego
3. Sortujemy populację po wartość funkcji dopasowania
4. Upewniamy się że w populacji jest dokładnie n osobników nadmiarowe osobniki
   najgorsze odrzucamy
5. Dokonujemy dobierania w pary i krzyżowania
    1. i = 0
    2. jeśli i < ilość osobników oraz i < 10*dopasowanie najlepszego osobnika
        1. osobnik_a = populacja[i]
        2. i = i + 1
        3. osobnik_b = populacja[i]
        4. i = i + 1
        5. potomstwo = osobnik_a x osobnik_b
        6. mutacja(potmostwo)
        7. dodajemy potomków do populacji
6. Powrót do kroku 2

####Odmiana algorytmu turniejowego (Microbal GA)

1. Losujemy początkową populację o rozmiarze n.
2. Losujemy 2 osobników z populacji
3. Obliczmy ich dopasowanie
4. Porównujemy ich ze sobą na podstawie funkcji dopasowania
    1. Lepszy z nich wraca do populacji niezmieniony
    2. Gorszy z nich przejmuje z pewnym prawdopodobieństwem część genów lepszego
       i dokonywana jest na nim mutacja
5. Powrót do kroku 2


####Algorytm Differential Evolution
1. Losujemy początkową populację o rozmiarze n.
2. Ustalamy F = 1 i CR = 0.5
3. Losujemy 4 różnych osobników z populacji oznaczamy je przez X,a,b,c
4. Losujemy liczbę R będącą jedną z pozycji w genie
5. Tworzymy nowego osobnika, który na początku ma taki sam genotyp jak X
6. Przechodzimy po wszystkich bitach nowego osobnika
    1. Losujemy liczbę będącą jedną z pozycji w genie oznaczamy ją prze i
    2. Losujemy liczbę rzeczywistą C z zakresu 0..1
    3. Jeśli i == R i C < CR
        1. Na pozycji bitu nowego osobnika na której jesteśmy teraz ustawiamy
        nowy_osobnik[bit]  = a[bit]  + F * (b[bit]  - c[bit])
7. Jeśli nowy osobnik jest lepszy od X to dodajemy go do populacji a X z niej
   usuwamy
8. Powrót do kroku 3

##Porównanie algorytmów

###Algorytm doboru podobnych osobników
![Alt text](a6.png)\

Ilość osobników 200, ilość kart 100

![Alt text](a5.png)\

Ilość osobników 200, ilość kart 200

![Alt text](a4.png)\

Ilość osobników 100, ilość kart 60

![Alt text](a3.png)\

Ilość osobników 300, ilość kart 100

![Alt text](a2.png)\

Ilość osobników 100, ilość kart 40

![Alt text](a1.png)\

Ilość osobników 50, ilość kart 100

###Odmiana algorytmu turniejowego (Microbal GA)
![Alt text](ma1.png)\

Ilość osobników 100, ilość kart 40

![Alt text](ma2.png)\

Ilość osobników 100, ilość kart 100

![Alt text](ma3.png)\

Liczba osobników 5, ilość kart 200

![Alt text](ma4.png)\

Liczba osobników 30, ilość kart 200

![Alt text](ma5.png)\

Liczba osobników 3, ilość kart 60

###Algorytm Differential Evolution
![Alt text](da1.png)\

Liczba osobników 100, ilość kart 60

![Alt text](da2.png)\

Ilość osobników 300, ilość kart 60


##Wnioski
Najlepszym z badanych algorytmów okazał się algorytm z doborem podobnych
osobników. Znajduje on rozwiązanie w stabilny sposób i równomiernie ulepsza całą
populację, jednocześnie ją stabilizując. Algorytm Turniejowy lepiej radzi sobie
z poprawą najlepszego osobnika populacji gdy jest w nim mała liczba osobników.
Dzieje się tak dlatego, bo rośnie prawdopodobieństwo na to, że najlepszy osobnik
zostanie wybrany do turnieju i przekaże swoje dobre cechy innym, a następnie
inne osobniki rozprzestrzenią dobre cechy osobnika najlepszego bardzo szybko po
populacji bo jest mało osobników. Niestety powoduje zawężenie przestrzeni
poszukiwań rozwiązania. Najgorszym z badanych algorytmów jest algorytm
Differential Evolution. Został on pierwotnie zaprojektowany do optymalizacji
funkcji zmiennej rzeczywistej i bardzo słabo radzi sobie z problemami
dyskretnymi. Żaden z badanych algorytmów nie daje gwarancji znalezienia
rozwiązania optymalnego w zadanym czasie. Najczęściej po około 300 pokoleniach
odchylenie od rozwiązania optymalnego jest w granicach 10% co jest wynikiem
dobrym ale nie  dokładnym. Przy małej ilość kart mamy bardzo duże
prawdopodobieństwo na to że otrzymamy dokładny wynik w krótkim czasie.
Prawdopodobieństwo to rośnie dodatkowo gdy stosunek ilości osobników do ilość
kart jest dużo większy od 1, bo wtedy mogą się trafić od razu osobniki, które są
bardzo blisko rozwiązania.

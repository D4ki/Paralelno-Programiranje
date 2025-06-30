# Paralelno-Programiranje
Seminarski rad iz paralelnog programiranja
Da bi proces mogao učitat sliku slika se mora nalaziti u istoj datoteci kao i program. Pozivanjem slike u program (npr. "Gauss.jpg") jako je bitno da navedemo koju vrstu slike smo ubacili.
Za Python kod:
Jednostavno samo pokrenemo proces i onda će ispisati sva vremena u terminalu i snimit će nam sliku kao Output.

Za C kod:
C kod je malo kompliciran pošto ne možemo samo pokrenuti proces u VScode-u pošto on ne pokreće sa -fopenMP. Morat ćemo onda u terminalu otvoriti gdje se nalazi naš proces npr. ako se nalazi u C: / Desktop / C kod upisat ćemo u terminalu cd "C:"\\"Desktop"\\"C kod"
kada nam u terminalu unosimo gcc -fopenmp -Wall -o GausovFilter.exe GausovFilter.c i dobit ćemo exe file koji je naš proces. njega pokrećemo u terminalu sa naredbom ./GausovFilter.

Za Javu:
isto kao i python potrebno je samo da imamo slike u istom folderu i program će raditi. 

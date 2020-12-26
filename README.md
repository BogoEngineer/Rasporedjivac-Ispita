# Rasporedjivac ispita

Programu se dostavljaju 2 json fajla kao ulaz, koji predstavljaju sale koje je moguce iskoristiti za potrebe ispitnog roka i sam ispitni rok, respektivno.
Pomocu CSP (backtracking sa forward checking-om) algoritma se ispiti iz ispitnog roka rasporedjuju po salama tako da fakultet snosi sto manje finansijske troskove (minimalan broj dezurnih u sali i da se sala nalazi u prostorijama fakulteta, ukoliko je to moguce).
Restrikcije koje algoritam treba da ispostuje:
  - Jedan ispit zauzima tacno jedan termin i odrzava se u potrebnom broju sala (u jednom terminu moze biti rasporedjeno vise razlicitih ispita)
  - Broj rasporedjenih studenata u jednoj sali ne moze premasiti kapacitet te sale
  - Ispit pocinju u jednom od 4 navedena termina (8:00, 11:30, 15:00, 18:30). Smatrati da svaki ispit traje najduze 3h.
  - U jednoj sali u jednom trenutku moze da se odrzava samo jedan ispit
  - Ispiti koji se polazu na racunarima mogu da se raspodele samo u sale koje poseduju racunare
  - Za svaki odsek vazi da se u jednom danu ne mogu rasporediti dva ili vise ispita sa iste godine studija koji se na tom odseku nude
  - Za svaki odsek vazi da se u jednom terminu ne mogu rasporediti dva ili vise ispita sa susednih godina studija (prva i druga, druga i treca, treca i cetvrta) koji se na tom odseku nude
  
Izlaz programa se ispisuje u raspored.csv fajl.
Format izlaza se moze videti u raspored.csv fajlu, dok se format ulaza moze naci u folderu "javni_testovi"

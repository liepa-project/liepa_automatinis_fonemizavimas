Apie
===============================

transcriber_re.py yra automatinis transkribavimo įrankis. Įėjimo duomenys yra tekstas. Jis vėliau skaidomas į atskirus žodžius. Unikalūs žodžiai paverčiami į fonemų sekas. Transkribavimas vyksta regulariomis išraiškomis (RegExp). Išėjimo duomenys yra žodis išreikštas poromis: grafemomis ir fonemomis.

Naudojimas  
===============================

h2. Pagalbinė informacija:

    ```
    transcriber_re.py --help
    ```
    


h2. Transkscribuoti pavienį žodį:

    ```
    transcriber_re.py <ŽODIS>
    ```

, kur <ŽODIS> - yra transcribuojamas žodis

pvz.
    ```
    transcriber_re.py besikiškiakopūstaudavome
    besikiškiakopūstaudavome	B E S I K I S2 K E K O_ P U_ S T A U D A V O_ M E
    ```
    

h2. Transcribuoti failus

    ```
    transcriber_re.py -i <NUSKAITYMO_TXT_FAILAS>
    ```

, kur <TXT_FAILAS> - yra tekstinis failas UTF-8 koduotės, kuriame yra žodžiai atskirti tarpais arba nauja eilute

pvz.

    ```
    transcriber_re.py -i in_file.txt 
    du	D U
    trys	T R I_ S
    vienas	V I E N A S
    ```

h2. Įrašyti transcripcijas į žodyno failą



    ```
    transcriber_re.py -i <NUSKAITYMO_TXT_FAILAS> -o <ĮRAŠYMO_TXT_FAILAS>
    ```
    
pvz.
    ```
    transcriber_re.py -i in_file.txt -o out_file.dic
    ```
    


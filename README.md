# Un simple emulator de load balancer si scheduling

Programul emuleaza un mediu de lucru asemanator unui centru de servere sau cluster
avand mai multi "muncitori" la care va impartii diverse sarcini

## Exeutare

```
python3 main.py
```

## Sarcini

Fiecare sarcina are un nume, timp de sosire, durata si prioritate

## Muncitori

Muncitorii (workers) sunt emulati folosind thread-uri, acestia primesc o lista de
sarcini pe care le vor "executa" folosind unul din algoritmi de scheduling disponibili

Muncitorii vor primi noi sarcini pe parcurs ce astea ajung la load balancer

## Algoritmi

Pentru scheduling sunt prezenti:

* FCFS - primul venit, priml servit (cel mai simplu)
* round robin (cel mai corect)
* SJF - shortest job first (imposibil de implementat in practica)
* priority based - executa prima data sarciniile mai importante

Pentru partea de balancing:

* round robin - se impart sarcinile dupa cum sosesc pe rand la fiecare muncitor
* least used first - noile sarcini vor fi executate de muncitorul cu cele mai putine

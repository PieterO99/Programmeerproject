# Programmeerproject# project-PieterO99

### Onderzoeksvraag: 
***"Hoe bewegen mensenmassa's zich als de individuen verschillende bestemmingen hebben?"***

### Minimal Viable Product:
Ik heb al een goede basis van een boid klasse met een visualisatie erbij. Zie [Shoutout naar Ewout](https://github.com/projectmesa/mesa/tree/main/examples/boid_flockers).
Ik wil de volgende elementen implementeren:
- [ ] ik wil agents een bepaalde bestemming meegeven. Bijvoorbeeld een student die van lokaal naar lokaal gaat. Dan wil ik verschillende agents verschillende bestemmingen geven en kijken hoe dit eruit ziet. [^1]

### Extra's:
- [ ] het lijkt me mooi om obstakels toe te voegen en misschien zelfs een plattegrond van een klaslokaal of van het sciencepark te gebruiken. En als we dan toch op schaal gaan werken, de afstand die individuen willen houden (`boid.separation`) op anderhalve meter te zetten.

- [ ] ik zou ook nog kunnen kijken naar gedrag van studenten. Dat ik een bepaalde agressiviteit meegeef die de kans bepaalt dat ze in de personal space van een andere student komen.


[^1]: (Hiervoor moet ik dus ook onderzoeken in hoeverre je richting wordt bepaald door de drie klassieke elementen van een boid: **separation**, **alignment** en **cohesion** aan de ene kant en de **bestemming** aan de andere kant.)
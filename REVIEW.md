## Review door Victor en Viola

### Verbeterpunten

- *snelheid*: agents de mogelijkheid geven om hun snelheid te veranderen
- *schaal*: de plattegrond op schaal uitwerken en realistische snelheden meegeven
- *verdeling startposities en bestemmingen*: de bestemmingen en startposities realistischer verdelen over de studenten
- *stijl*
- *onderzoeksvraag*

# snelheid

Het model zou realistischer zijn als we agents niet alleen van richting laten veranderen om buren en obstakels te ontwijken, maar ook zouden laten veranderen van snelheid. Dit lijkt een complex probleem waar we nog geen oplossing voor konden vinden. Als ik meer tijd zou hebben, zou ik eerst een implementatie hiervan proberen waar een agent elke stap óf met constante snelheid een bepaalde richting in gaat óf stopt op zijn plaats. 

In eerste instantie zou ik dan de agent laten vergelijken wat de voorspelde afstand van al zijn buren (de som) is voor de volgende stap als hij stil blijft staan of juist doorloopt. Dan kiest de agent (evt met een bepaalde kans) de actie die de voorspelde afstand maximaliseert.
Vervolgens zou ik moeten kijken hoe ik de `destination_vector` mee laat wegen in de keuze tussen stilstaan en doorlopen.
Dan zou ik ook nog kunnen overwegen om studenten een bepaalde haast mee te geven die steeds meer wordt en hun keuze beïnvloedt.

Een volgende stap zou nog kunnen zijn om dan naast stilstaan nog het veranderen van snelheid als actie mee te geven waar we blijven doorlopen voor verschillende snelheden vergelijken of de voorspelde afstand als functie van de snelheid **v** zien en die maximaliseren naar **v**.

# schaal

Een simpelere verbetering zou zijn om de plattegrond die ik heb gemaakt van de hal van het sciencepark op schaal te krijgen. Dit zou ook duidelijkheid geven over welke snelheden we moeten kiezen voor studenten en de afstand die ze willen houden. Al met al zou het leiden tot beter interpreteerbare resultaten. We hebben nu een `mesa.space` met `width=100` en `height=100`. Door de afmetingen van de hal op te vragen zouden we bijvoorbeeld de `height` gelijk kunnen houden aan 100 en er de juiste width bij kiezen en alle deuren en de student helpdesk op schaal maken. Ook zouden we de `separation_dist` op schaal kunnen doen, bijvoorbeeld overeenkomend met 1.5 meter.

# verdeling startposities en bestemmingen

Ik laat nu de studenten met evenveel kans bij elke deur starten en met evenveel kansen elke deur als bestemming hebben. In de praktijk weet ik dat er afhankelijk van het tijdstip vooral heel veel studenten door de bovenste draaideuren gaan en eigenlijk alleen naar binnen mogen door de linker en eigenlijk alleen naar buiten mogen door de rechter. In mijn model was er veel ontstopping bij studenten die tussen de deuren linksboven bewogen, terwijl in de praktijk bijna niemand de deur van de studentenraad (de normale deur linksboven) gebruikt. Dit zou wel moeten worden meegenomen in een goede analyse van het loopgedrag in de hal.

# stijl

Omdat ik uiteindelijk best ver van het boid model ben afgestapt zou het wat duidelijker zijn om alle namen waarin boid of flock voorkomt te vervangen door iets dat meer overeenkomt met wat ik modelleer. Dus bijvoorbeeld de class `Student` in plaats van `Boid`.

# onderzoeksvraag

De huidige onderzoeksvraag is misschien een beetje vaag, dit kwam doordat ik me verloor in het modelleren van realistisch loopgedrag en gaandeweg mijn idee veranderde van wat ik kon programmeren. Uiteindelijk bleek `distance_factor` veel invloed te hebben op het loopgedrag en ben ik dit gaan onderzoeken. 

Een nadeel is dat het een vrij vaag resultaat geeft: je kan niet tegen mensen zeggen dat ze in hun ontwijkgedrag de afstand van buren kwadratisch moeten wegen. Hierom denk ik dat het interessanter zou zijn om een vaste `distance_factor` te kiezen die realistisch lijkt en de `separation` te variëren. Dan zou een resultaat kunnen zijn dat mensen misschien beter afstand houden als je ze een hogere of juist lagere afstand probeert te laten houden. Ook zou je kunnen kijken welke afstand mensen van nature houden en hoe het (proberen te) houden aan anderhalve meter afstand de flow op het science park beïnvloedt.
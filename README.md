# ScrapingTweetsProject

Ceci est un projet qui a pour but de récupérer des données(tweets) relatives à la cryptomonaie sur twitter et les enregistrer dans une base de donnée.

Les données sont obtenues en faisant des recherches se basant sur un certains nombre de mots clé contenus dans les tweets ou hashtags. Des mots clé comme 
`#cryptomonaie`, `#blockchain`, `bitcoin`, `cryptoconcurency` etc.

Par ailleurs, j'ai fait de telle sorte que le script s'exécute chaque 6h au niveau du serveur. De ce fait chaque 06h de temps, 
il recherche de nouvelles données et les enregistre automatique dans la base de donnée et en même temps un commit/push se fera une minute après contenant le résultat de l'exécution du script

J'ai fait le projet avec la supervision de Mr. Mbacké, professeur en Administration de Base de Donnée à l'Ecole Supérieure Polytechnique de Dakar.

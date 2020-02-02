# Classification supervisée à base de motifs de graphes 
 
Code en python + utilisation de Networkx : https://networkx.github.io/  
Base de donnée de graphe MUTAG : https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets  

**Maître de stage : Dominique Gay (enseignant/chercheur à L'université de la Réunion)**  
Stagiaires : Chien Kan Foon Brandon - Corre Stanislas - Chien Kan Foon Corentin ( étudiants à l'université de la Réunion )  

_____________________________________________________________________________________________________________________________________


## Introduction

La **Classification supervisée** a pour but d'étiquetter une donnée , en ayant au préalable établi des règles par le biais  d'une étude d'échantillon d'apprentissage dont la catégorisation est connue.

> Exemples : Attribuer une rubrique à un article, Evaluer la toxicité d'une molécule etc...

_Note : La Classification dîtes non-supervisée, elle, vise à trouver des ressemblances entre des éléments de données pour établir des groupes_

Pour établir ces règles de classification, l'on procéde à une fouille de donnée qui a pour but de découvrir de l'information utile.
La fouille de graphes permet de traiter des données complexes:

> Exemples : Molécules, réseaux etc...

Mais si les graphes sont efficaces en terme de représentation de données, il est difficile d'étendre les méthodes de fouille de données ensemblistes à ces derniers. Notamment, l'appariement entre graphes/graphes ou graphes/sous-graphes qui s'avère être plus compliqué que celui entre motifs ensemblistes ( Problème de l'isomorphisme de graphes/sous-graphes )

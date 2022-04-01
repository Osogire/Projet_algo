Lancer une résolution d'instance:

Pour résoudre une instance, il suffit de la créer : instance = Instance.Instance(9,6,4,2,3)
de créer un solver : solver = Solver_exact.Solver_exact(copy.deepcopy(instance))
et de lancer la résolution : solver.attribute_courses(2)

Les méthodes 0 et 1 ne sont plus utilisées, elles ont aidées dans le raisonnement et dans la vérification de l'exactitude de la solution 2 mais il se peut qu'elle ne donne même pas de résultat.

Lecture des résultats :

Lors de la résolution de l'instance le fichier instance.txt est modifié, c'est l'instance précomplétée avec l'attribution des cours principaux pour tous les élèves.

Lecture d'un cours :
Course 6:                                                                                                   --> Le numéro du cours
None                                                                                                        --> Liste des élèves ayant ce cours dans leurs voeux (inutilisé dans la résolution 2)        
[1,3,5,8,10,11,16,21,27,30,37,41,43,44,50,51,52,54,55,56,57,67,68,72,73,75,76,83,86,87,89,90]               --> Les élèves inscrits dans ce cours


Lecture d'un élève :
Student 124:            --> Le numéro de l'élève
[3,9,4,6,7]             --> Les voeux de l'élève
[3,6,7]                 --> La liste des cours non attribués
[9,4]                   --> La liste des cours attribués
100.0%                  --> La satisfaction (si un cours de remplacement est choisi la satisfaction diminue, si le bon nombre de cours n'est pas encore attribué la satisfaction n'est pas impactée)

Il est possible d'enregistrer la solution retourner dans par la résolution d'instance : solver._best_result[2].save_as_txt('exact\solution2.txt')
La lecture de l'instance se fait alors exactement comme décrit précedemment


Les fichiers présents dans resultat sont les résultats des temps des tests effectués 
Le nom du fichier correspond à l'instance créée
si le suffixe __2 apparait c'est que l'amélioration en fonction de la meilleure solution calculée mathématiquement a été ajoutée

nbr total : 100                                 --> nombre total d'instances résolues
temps total : 0.3081636428833008                --> temps total pour la résolution de ces instances
temps moyen total : 0.0030816364288330077       --> temps moyen pour la résolution de ces instances
-------------0-------------                     --> nombre de cours devant être attribués après la première attribution systématique des meilleurs cours aux élèves (visible dans instance.txt)
nbr : 56                                        --> nombre d'instance avec (ici) 0 cours devant être attribués
temps min : 0.0009965896606445312               --> temps minimum pour la résolution d'une des (ici) 56 instances
temps moyen : 0.0017386980272353183             --> temps moyen pour la résolution des instances
temps max : 0.005981922149658203                --> temps maximum pour la résolution d'une des (ici) 56 instances
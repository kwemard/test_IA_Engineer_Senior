"""Point d’entrée à compléter. Le mode par défaut doit déployer le vrai modèle local."""
import argparse

def deploy(ci=False, image=None):
    """TODO : prérequis, acquisition/cache, build ou image reçue, tests, démarrage et smoke.

    ci=False : vrai modèle local, acquisition automatique si nécessaire, services laissés actifs.
    ci=True : réponse simulée, pas de poids ni de modèle réel ; nettoyage en fin d’exécution.
    image : utiliser cette image déjà construite, sans la reconstruire.
    Utiliser le même chemin d’orchestration pour les deux modes, hors service/réponse du modèle.
    """
    raise NotImplementedError('Déploiement automatisé à implémenter')

def stop():
    """TODO : arrêter uniquement les services/ressources du projet, sans effacer les poids en cache."""
    raise NotImplementedError('Arrêt à implémenter')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ci',action='store_true')
    parser.add_argument('--image')
    parser.add_argument('--stop',action='store_true')
    args=parser.parse_args()
    if args.stop: stop()
    else: deploy(ci=args.ci,image=args.image)

if __name__=='__main__': main()

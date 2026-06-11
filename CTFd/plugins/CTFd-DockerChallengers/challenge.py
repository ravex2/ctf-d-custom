from CTFd.models import Challenges

class DynamicDockerChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "dynamic_docker"}
    
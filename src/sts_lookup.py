from .classes.docker_service import DockerService
from .log import LOGGER

STS_NODES = []
s = DockerService()
#sts_list = s.list({ "ancestor": "dmi7ry/significant-trades-server" })
sts_list = s.list(regex=r".*dmi7ry/significant-trades-server.*")
for sts in sts_list:
    LOGGER.warning("Found contanier = { id=%s, name=%s, image=%s }" % (sts.id, sts.name, sts.attrs["Config"]["Image"]) )

    #zero by default, but can be overrided via STS_MIN_AMOUNT
    sts_config = { "min": 0 }

    for env in [ env.split("=") for env in sts.attrs["Config"]["Env"] ]:
        if env[0] == "STS_DEFAULT_PAIR":
            sts_config["pair"]  = env[1].lower().replace("/", "")
            sts_config["s1"]    = env[1].split("/")[0]
            sts_config["s2"]    = env[1].split("/")[1]
        if env[0] == "STS_DEFAULT_PORT":
            sts_config["port"]  = env[1]
        if env[0] == "STS_MIN_AMOUNT":
            sts_config["min"]   = int(env[1])

    LOGGER.info("found container: %s" % sts_config)

    if not sts_config.get("port", None) or not sts_config.get("pair", None):
        raise Exception("Cannot find necessary Env vars from container %s, Envs=%s" % ( sts.name,sts.attrs["Config"]["Env"]  ) )
    STS_NODES += [ sts_config ]

LOGGER.warning("Found instances of significant trades server: %s" % STS_NODES)

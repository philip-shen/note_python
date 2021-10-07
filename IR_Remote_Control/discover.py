import broadlink
#broadlink.setup('IGO-Test-3', '51007907', 2)
#dev = broadlink.discover(timeout=10)
dev = broadlink.discover(timeout=5)#, local_ip_address='192.168.6.130')
net=[]
for d in dev:
    d.auth()
    n=dict(type=d.get_type(),ip=d.host[0],port =d.host[1],
             mac = "-".join([format(x,"02x") for x in [x for x in reversed(d.mac)]]),
             timeout = d.timeout)
    net.append(n)
print(net)
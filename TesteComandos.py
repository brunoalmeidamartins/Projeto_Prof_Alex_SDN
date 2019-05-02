import os
qos = os.popen("ovs-vsctl list qos | grep _uuid | awk '{print $3}'").read().strip('\n')

print(type(qos))
print(qos)


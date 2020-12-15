from wakeonlan      import send_magic_packet
from app.models     import Hosts

def wakeup(host_idx):
    # Get host object
    host    = Hosts.query.filter_by(idx=host_idx).one_or_none()

    send_magic_packet(  host.mac,
                        ip_address=host.ip,
                        port=7)

    return host.name
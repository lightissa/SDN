from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import re
import sys
from mininet.link import Intf
from mininet.topolib import TreeTopo
from mininet.util import quietRun

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
ef checkIntf( intf ):
    "Make sure intf exists and is not configured."
    if ( ' %s:' % intf ) not in quietRun( 'ip link show' ):
        error( 'Error:', intf, 'does not exist!\n' )
        exit( 1 )
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf ) )
    if ips:
        error( 'Error:', intf, 'has an IP address,'
               'and is probably in use!\n' )
        exit( 1 )

if __name__ == '__main__':
    setLogLevel( 'info' )

    # try to get hw intf from the command line; by default, use eth1
    intfName = sys.argv[ 3 ] if len( sys.argv ) > 1 else 'wlan0'
    info( '*** Connecting to hw intf: %s' % intfName )

    info( '*** Checking', intfName, '\n' )
    checkIntf( intfName )
    

    def build( self, **_opts ):
        router = self.addNode( 'r0', cls=LinuxRouter, ip='192.168.1.1/24')


        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        h2 = self.addHost('h2', ip='192.168.1.101/24',
                           defaultRoute='via 192.168.1.1' )
        h3 = self.addHost( 'h3', ip='172.16.0.100/12',
                           defaultRoute='via 172.16.0.1' )
        h4 = self.addHost( 'h4', ip='172.16.0.101/12',
                           defaultRoute='via 172.16.0.1' )

        h5 = self.addHost( 'h5', ip='10.0.0.100/8',
                           defaultRoute='via 10.0.0.1' )
        h6 = self.addHost ( 'h6', ip='10.0.0.101/8',
                           defaultRoute='via 10.0.0.1' )

        s1  =  self.addSwitch(  's1'  )
        s2  =  self.addSwitch(  's2'  )
        s3  =  self.addSwitch(  's3'  )

        self.addLink(h1,s1)
        self.addLink(h2,s1)  
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        self.addLink(h5,s3)
        self.addLink(h6,s3)
        self.addLink( s1, router, intfName1='s1-eth1',intfName2='r0-eth1',
                      params2={ 'ip' : '192.168.1.1/24' } )
        self.addLink( s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '172.16.0.1/12' } )
        self.addLink( s3, router, intfName2='r0-eth3',
                      params2={ 'ip' : '10.0.0.1/8' } )
topos = { 'custom': ( lambda: NetworkTopo() ) }


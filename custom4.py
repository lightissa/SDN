from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI

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
    

    def build( self, **_opts ):
        router = self.addNode( 'r0', cls=LinuxRouter, ip='194.12.230.1/24')
        router1= self.addNode( 'r1', cls=LinuxRouter, ip='172.10.0.1/16') 
        " 1er sous-reseau du routeur 1"
        h1 = self.addHost( 'h1', ip='194.12.230.2/26',
                           defaultRoute='via 194.12.230.1' )
        h2 = self.addHost('h2', ip='194.12.230.3/26',
                           defaultRoute='via 194.12.230.1' )
        " 2em sous-reseau du routeur 1"
        h3 = self.addHost( 'h3', ip='194.12.230.66/26',
                           defaultRoute='via 194.12.230.65' )
        h4 = self.addHost( 'h4', ip='194.12.230.67/26',
                           defaultRoute='via 194.12.230.65' )
        h5 = self.addHost( 'h5', ip='194.12.230.68/26',
                           defaultRoute='via 194.12.230.65' )

        " 3em sous-reseau du routeur 1"
        h6 = self.addHost( 'h6', ip='194.12.230.130/26',
                           defaultRoute='via 194.12.230.129' )
        h7 = self.addHost( 'h7', ip='194.12.230.131/26',
                           defaultRoute='via 194.12.230.129' )
        h8 = self.addHost( 'h8', ip='194.12.230.132/26',
                           defaultRoute='via 194.12.230.129' )
        h9 = self.addHost( 'h9', ip='194.12.230.133/26',
                           defaultRoute='via 194.12.230.129' )
        " reseau du routeur 2"
        " 1er sous-reseau"
        h10 = self.addHost('h10', ip='172.10.0.2/18',
                           defaultRoute='via 172.10.0.1')
        h11 = self.addHost('h11', ip='172.10.0.3/18',
                           defaultRoute='via 172.10.0.1')
        h12 = self.addHost('h12', ip='172.10.17.4/18',
                           defaultRoute='via 172.10.0.1')   
        "2eme sous reseau"
        h13 = self.addHost('h13', ip='172.10.64.1/18',
                           defaultRoute='via 172.10.64.1')
        h14 = self.addHost('h14', ip='172.10.64.3/18',
                           defaultRoute='via 172.10.64.1')
        h15 = self.addHost('h15', ip='172.10.64.4/18',
                           defaultRoute='via 172.10.64.1')
        " 3eme sous reseau"
        h16 = self.addHost('h16', ip='172.10.128.2/18',
                           defaultRoute='via 172.10.128.1')
        h17 = self.addHost('h17', ip='172.10.128.3/18',
                           defaultRoute='via 172.10.128.1')
        h18 = self.addHost('h18', ip='172.10.128.4/18',
                           defaultRoute='via 172.10.128.1') 
        "3eme reseau"
        h19= self.addHost( 'h19', ip='10.0.0.100/8',
                           defaultRoute='via 10.0.0.1' )
        h20= self.addHost ( 'h20', ip='10.0.0.101/8',
                           defaultRoute='via 10.0.0.1' ) 
        "switchs du reseau 1"
        s1  =  self.addSwitch(  's1'  )
        s2  =  self.addSwitch(  's2'  )
        s3  =  self.addSwitch(  's3'  )
        "switchs du reseau 2"
        s4 =   self.addSwitch( 's4'  )
        s5 =   self.addSwitch( 's5'  )
        s6 =   self.addSwitch( 's6'  )
        "switch du 3eme reseau"
        s7=    self.addSwitch( 's7' )
        "liaisons reseau 1"
        "A0"
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        "A1"  
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        self.addLink(h5,s2)
        "A2"
        self.addLink(h6,s3)
        self.addLink(h7,s3)
        self.addLink(h8,s3)
        self.addLink(h9,s3)
        " liasons reseau 2"
        "B0"
        self.addLink(h10,s4)
        self.addLink(h11,s4)
        self.addLink(h12,s4)
        "B1"
        self.addLink(h13,s5)
        self.addLink(h14,s5)
        self.addLink(h15,s5)
        "B2"
        self.addLink(h16,s6)
        self.addLink(h17,s6)
        self.addLink(h18,s6)
        "C1"
        self.addLink(h19,s7)
        self.addLink(h20,s7)
        " generations des liens"
        self.addLink( s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : '194.12.230.1/26' } )
        self.addLink( s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '194.12.230.65/26' } )
        self.addLink( s3, router, intfName2='r0-eth3',
                      params2={ 'ip' : '194.12.230.129/26' } )
        self.addLink( s4, router1, intfName2='r1-eth1',
                      params2={ 'ip' : '172.10.0.1/18' } )
        self.addLink( s5, router1, intfName2='r1-eth2',
                      params2={ 'ip' : '172.10.64.1/18' } )
        self.addLink( s6, router1, intfName2='r1-eth3',
                      params2={ 'ip' : '172.10.128.1/18' } )
        self.addLink( router, router1, intfName1='r0-eth4',
                      intfName2='r1-eth4',params1={'ip': '10.0.0.1/8'},
                      params2={'ip': '10.0.0.2/8'})
        """self.addLink( s7, router1, intfName2='r1-eth4',
                      params2={'ip' : '10.0.0.1/8' } )
        self.addLink( s7, router, intfName2='r0-eth4',
                      params2={'ip' : '10.0.0.2/8' } )"""
       
topos = { 'custom': ( lambda: NetworkTopo() ) }


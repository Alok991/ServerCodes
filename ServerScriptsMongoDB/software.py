ó
ÿ`TWc           @   s¹   d  d l  m Z m Z d  d l Z d e f d     YZ e d k rµ d  d l Z d  d l m Z d  d l m	 Z	 e j
 e j  e d  Z e e _ e	 j d	 d
 e  e	 j   n  d S(   iÿÿÿÿ(   t   WebSocketClientProtocolt   WebSocketClientFactoryNt   MyClientProtocolc           B   s,   e  Z d    Z d   Z d   Z d   Z RS(   c         C   s   d j  | j  GHd  S(   Ns   Server connected: {0}(   t   formatt   peer(   t   selft   response(    (    s   /home/ron/alive/sofclie.pyt	   onConnect   s    c         C   sP   | r d j  t |   GHn d j  | j d   GH| j d  j d  } d  S(   Ns"   Binary message received: {0} bytess   Text message received: {0}t   utf8t   -(   R   t   lent   decodet   split(   R   t   payloadt   isBinaryt   list(    (    s   /home/ron/alive/sofclie.pyt	   onMessage   s
    $c         C   sÍ  d GHt  d  } | d k rèt  d  } | d k rx t  d  } t  d  } d$ | d
 | } |  j | j d   n  | d k rèt  d  } t  d  } t  d  } d } d } | d k r&t  d  } d }	 xQ |	 t |  k r"t |	  }
 t  d |
 d  } | | d 7} |	 d 7}	 qÕ Wn  | d k rt  d  } d }	 xQ |	 t |  k rt |	  }
 t  d |
 d  } | | d 7} |	 d 7}	 qGWn  d% | d
 | d
 | d
 | d
 | } | d  } |  j | j d   qèn  | d k rÉt  d  } | d k rct  d  } t  d  } t  d  } d& | d
 | d
 | } |  j | j d   n  | d k rÉt  d  } t  d!  } t  d"  } d' | d
 | d
 | } |  j | j d   qÉn  d  S((   Ns   WebSocket connection open.sJ   enter 1 to create/update product doc , enter 2 to create/update home doc 
t   1s=   do you want to enter home_id(a) or create new product doc(b)
t   bs   enter the product_id
s%   enter whether master(m) or slave(s) 
s   C-s   P-R	   R   t   as   enter the home_id
t    i    t   ss   enter the number of switches 
i   s   enter the type of switchs   
t   .t   ms   enter the number of slaves 
s   enter the slave_ids   H-iÿÿÿÿt   2sJ   do you want to create home doc (1) or do you want to update home doc(2) :
s   please enter the home_id
s   please enter the pincode 
s   please enter the address
s   H1-s   please enter the user_id
s$   please enter the hub_I_conc product
s   H2-s   C-P-s   C-H-s   C-H1-s   C-H2-(   t	   raw_inputt   sendMessaget   encodet   intt   str(   R   t   choicet   askt   prod_idt   prod_typR   t   home_idt	   prod_contt
   prod_countt   countt   count1t   tempt
   homechoicet   home_pint   home_addresst   user_idt
   hub_I_conc(    (    s   /home/ron/alive/sofclie.pyt   onOpen3   s`    *
c         C   s   d j  |  GHd  S(   Ns    WebSocket connection closed: {0}(   R   (   R   t   wasCleant   codet   reason(    (    s   /home/ron/alive/sofclie.pyt   onClose|   s    (   t   __name__t
   __module__R   R   R-   R1   (    (    (    s   /home/ron/alive/sofclie.pyR      s   		+	It   __main__(   t   log(   t   reactoru   ws://127.0.0.1:9000s	   127.0.0.1i(#  (   t   autobahn.twisted.websocketR    R   t   sysR   R2   t   twisted.pythonR5   t   twisted.internetR6   t   startLoggingt   stdoutt   factoryt   protocolt
   connectTCPt   run(    (    (    s   /home/ron/alive/sofclie.pyt   <module>   s   {	
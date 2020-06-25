#!/bin/bash

function set_iptable_rule() {
  if [ "$1" == "-h" ]; then
    echo "./iptable_config.sh show"
    echo "./iptable_config.sh port 1080"
    echo "./iptable_config.sh ip 127.0.0.1"
    return
  fi

  if [ "$1" == "show" ]; then
    sudo iptables -L -n -v --line-numbers
    return
  fi

  if [ "$1" == "port" -a "$#" == "2" ]; then
    if [ "$2" == "all" ]; then
      `sudo iptables -A INPUT -p udp --dport 1080 -j DROP`
      `sudo iptables -A INPUT -p udp --dport 8000 -j DROP`
      `sudo iptables -A INPUT -p udp --dport 9700 -j DROP`
      `sudo iptables -A INPUT -p udp --dport 25000 -j DROP`
    else
      `sudo iptables -A INPUT -p udp --dport $2 -j DROP`
    fi
    return
  fi

  if [ "$1" == "ip" -a "$#" == "2" ]; then
    sudo iptables -A INPUT -s $2 -j DROP
    return
  fi
}

set_iptable_rule $1 $2
